"""Aquisição, limpeza, mapeamento e balanceamento dos resumos do arXiv."""
from __future__ import annotations

import hashlib
import json
import re
import time
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import requests

from src.config import ROOT, ensure_directories

LATEX_MATH = re.compile(r"\$.*?\$|\\\[.*?\\\]|\\\(.*?\\\)", re.DOTALL)
LATEX_COMMAND = re.compile(r"\\[A-Za-z]+\*?(?:\[[^]]*\])?(?:\{[^{}]*\})?")
URL = re.compile(r"https?://\S+|www\.\S+")
ISOLATED_NUMBER = re.compile(r"(?<!\w)[+-]?(?:\d+[.,]?)+(?!(?:\w))")
SPACE = re.compile(r"\s+")
WORD = re.compile(r"[a-z]+(?:'[a-z]+)?")
ENGLISH_MARKERS = {"the", "of", "and", "to", "in", "we", "a", "is", "for", "that", "with", "on", "are"}


def clean_abstract(text: str) -> str:
    """Remove marcação e ruído preservando prosa científica em inglês."""
    text = URL.sub(" ", text)
    text = LATEX_MATH.sub(" ", text)
    text = LATEX_COMMAND.sub(" ", text)
    text = text.replace("{", " ").replace("}", " ").replace("~", " ")
    text = ISOLATED_NUMBER.sub(" ", text.lower())
    return SPACE.sub(" ", text).strip()


def looks_english(text: str) -> bool:
    words = WORD.findall(text)
    return len(words) >= 40 and sum(word in ENGLISH_MARKERS for word in words) / len(words) >= 0.025


def root_area(category: str, allowed: list[str]) -> str | None:
    """Mapeia a categoria primária para a raiz configurada."""
    if category.startswith("astro-ph"):
        candidate = "astro-ph"
    elif category.startswith("cond-mat"):
        candidate = "cond-mat"
    elif category.startswith("hep-th"):
        candidate = "hep-th"
    elif category.startswith("quant-ph"):
        candidate = "quant-ph"
    else:
        candidate = category.split(".", 1)[0]
    return candidate if candidate in allowed else None


def iter_dump(path: Path) -> Iterator[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"JSON inválido em {path.name}:{line_number}") from exc


def download_arxiv(areas: list[str], target_per_area: int, cache_path: Path) -> None:
    """Baixa lotes da API oficial com cache incremental e pausa de 3 s."""
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    existing = cache_path.read_text(encoding="utf-8").count("\n") if cache_path.exists() else 0
    namespace = {"a": "http://www.w3.org/2005/Atom"}
    mode = "a" if existing else "w"
    with cache_path.open(mode, encoding="utf-8") as output:
        for area in areas:
            collected = 0
            start = 0
            query_area = area if area in {"hep-th", "quant-ph"} else f"{area}.*"
            while collected < target_per_area:
                response = None
                for attempt in range(2):
                    if attempt or start or collected:
                        time.sleep(min(30.0, max(3.1, 8.0 * (2 ** attempt))))
                    response = requests.get(
                        "https://export.arxiv.org/api/query",
                        params={"search_query": f"cat:{query_area}", "start": start, "max_results": 100, "sortBy": "submittedDate"},
                        timeout=15,
                        headers={"User-Agent": "intelligence-is-compression/0.1 (contato acadêmico; uso moderado)"},
                    )
                    if response.status_code not in {429, 503}:
                        break
                    retry_after = response.headers.get("Retry-After")
                    if retry_after and retry_after.isdigit():
                        time.sleep(min(30.0, float(retry_after)))
                assert response is not None
                response.raise_for_status()
                entries = ET.fromstring(response.text).findall("a:entry", namespace)
                if not entries:
                    break
                for entry in entries:
                    categories = [node.attrib["term"] for node in entry.findall("a:category", namespace)]
                    record = {
                        "id": (entry.findtext("a:id", default="", namespaces=namespace).rsplit("/", 1)[-1]),
                        "title": entry.findtext("a:title", default="", namespaces=namespace),
                        "abstract": entry.findtext("a:summary", default="", namespaces=namespace),
                        "categories": " ".join(categories),
                    }
                    output.write(json.dumps(record, ensure_ascii=False) + "\n")
                    collected += 1
                output.flush()
                start += len(entries)


def download_huggingface(dataset: str, areas: list[str], target_per_area: int, cache_path: Path) -> None:
    """Baixa somente linhas cuja categoria primária pertence à área via Dataset Server."""
    if cache_path.exists() and cache_path.stat().st_size:
        _download_huggingface_random_pages(dataset, areas, target_per_area, cache_path)
        return
    endpoint = "https://datasets-server.huggingface.co/filter"
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    patterns = {area: (area if area in {"hep-th", "quant-ph", "astro-ph", "cond-mat"} else f"{area}.") for area in areas}
    try:
        with cache_path.open("w", encoding="utf-8") as output:
            for area in areas:
                collected = 0
                offset = 0
                while collected < target_per_area:
                    response = requests.get(
                        endpoint,
                        params={
                            "dataset": dataset, "config": "default", "split": "train",
                            "where": f'"categories" LIKE \'{patterns[area]}%\'',
                            "offset": offset, "length": min(100, target_per_area - collected),
                        },
                        timeout=90,
                        headers={"User-Agent": "intelligence-is-compression/0.1 (academic project)"},
                    )
                    response.raise_for_status()
                    rows = response.json().get("rows", [])
                    if not rows:
                        break
                    for wrapped in rows:
                        row = wrapped.get("row", wrapped)
                        output.write(json.dumps({
                            "id": row.get("id"), "title": row.get("title", ""),
                            "abstract": row.get("abstract", ""), "categories": row.get("categories", ""),
                        }, ensure_ascii=False) + "\n")
                        collected += 1
                    output.flush()
                    offset += len(rows)
                if collected < target_per_area:
                    raise RuntimeError(f"Hugging Face retornou apenas {collected} registros para {area}")
    except (requests.RequestException, RuntimeError):
        _download_huggingface_random_pages(dataset, areas, target_per_area, cache_path)


def _download_huggingface_random_pages(dataset: str, areas: list[str], target: int, cache_path: Path) -> None:
    """Fallback determinístico quando o Dataset Server não oferece filtro SQL."""
    headers = {"User-Agent": "intelligence-is-compression/0.1 (academic project)"}
    metadata = requests.get("https://datasets-server.huggingface.co/size", params={"dataset": dataset}, timeout=60, headers=headers)
    metadata.raise_for_status()
    splits = [item for item in metadata.json().get("size", {}).get("splits", []) if item.get("config") == "default" and item.get("split") == "train"]
    if not splits:
        raise RuntimeError("Não foi possível descobrir o tamanho do split do Hugging Face")
    total_rows = int(splits[0]["num_rows"])
    page_size = 100
    rng = np.random.default_rng(42)
    recent_start = int(total_rows * 0.65) // page_size * page_size
    recent_pages = rng.permutation(np.arange(recent_start, total_rows, page_size))
    older_pages = rng.permutation(np.arange(0, recent_start, page_size))
    page_offsets = np.concatenate([recent_pages, older_pages])
    counts = Counter({area: 0 for area in areas})
    seen: set[str] = set()
    if cache_path.exists():
        for line in cache_path.read_text(encoding="utf-8").splitlines():
            if not line:
                continue
            row = json.loads(line)
            categories = str(row.get("categories", "")).split()
            area = root_area(categories[0], areas) if categories else None
            if area:
                counts[area] += 1
                seen.add(str(row.get("id", "")))
    with cache_path.open("a", encoding="utf-8") as output:
        for offset in page_offsets[:5000]:
            response = None
            for attempt in range(3):
                try:
                    response = requests.get(
                        "https://datasets-server.huggingface.co/rows",
                        params={"dataset": dataset, "config": "default", "split": "train", "offset": int(offset), "length": page_size},
                        timeout=60, headers=headers,
                    )
                    response.raise_for_status()
                    break
                except requests.RequestException:
                    response = None
                    time.sleep(2.0 * (attempt + 1))
            if response is None:
                continue
            for wrapped in response.json().get("rows", []):
                row = wrapped.get("row", wrapped)
                record_id = str(row.get("id", ""))
                categories = str(row.get("categories", "")).split()
                area = root_area(categories[0], areas) if categories else None
                if area and counts[area] < target and record_id not in seen:
                    output.write(json.dumps({"id": record_id, "title": row.get("title", ""), "abstract": row.get("abstract", ""), "categories": " ".join(categories)}, ensure_ascii=False) + "\n")
                    counts[area] += 1
                    seen.add(record_id)
            output.flush()
            if all(counts[area] >= target for area in areas):
                return
    missing = {area: target - counts[area] for area in areas if counts[area] < target}
    raise RuntimeError(f"Amostragem do Hugging Face insuficiente: {missing}")


def _stable_id(record: dict[str, Any]) -> str:
    return str(record.get("id") or hashlib.sha256(str(record.get("abstract", "")).encode()).hexdigest()[:16])


def prepare_data(config: dict[str, Any], download: bool = False) -> pd.DataFrame:
    """Prepara partições sem sobreposição e corpora com bytes iguais por área."""
    ensure_directories()
    candidates = sorted((ROOT / "data/raw").glob("arxiv-metadata*.json*"))
    if not candidates and download:
        cache = ROOT / "data/raw/arxiv-api-cache.jsonl"
        target = 50 if config["quick"] else 1200
        try:
            download_arxiv(config["areas"], target, cache)
            candidates = [cache]
        except requests.RequestException:
            hf_cache = ROOT / "data/raw/arxiv-metadata-huggingface.jsonl"
            download_huggingface(config["huggingface_dataset"], config["areas"], target, hf_cache)
            candidates = [hf_cache]
    if not candidates:
        raise FileNotFoundError("Dump do arXiv ausente. Consulte docs/data_instructions.md ou use data --download.")

    by_area: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in iter_dump(candidates[0]):
        categories = str(record.get("categories", "")).split()
        if not categories:
            continue
        area = root_area(categories[0], config["areas"])
        cleaned = clean_abstract(str(record.get("abstract", "")))
        if area and len(cleaned) >= config["min_abstract_chars"] and looks_english(cleaned):
            secondary = sorted({value for category in categories[1:] if (value := root_area(category, config["areas"])) and value != area})
            by_area[area].append({"id": _stable_id(record), "area": area, "text": cleaned, "cross_areas": secondary})

    missing = [area for area in config["areas"] if not by_area[area]]
    if missing:
        raise RuntimeError(f"Áreas sem resumos válidos: {', '.join(missing)}")
    rng = np.random.default_rng(config["seed"])
    rows: list[dict[str, Any]] = []
    targets = {"train": int(config["train_bytes_per_area"]), "test": int(config["test_bytes_per_area"])}
    corpus_rows: list[dict[str, Any]] = []
    for area in config["areas"]:
        records = by_area[area]
        rng.shuffle(records)
        cursor = 0
        for split, byte_target in targets.items():
            chosen: list[dict[str, Any]] = []
            byte_count = 0
            while cursor < len(records) and byte_count < byte_target:
                record = records[cursor]
                cursor += 1
                chosen.append(record)
                byte_count += len(record["text"].encode("utf-8")) + 1
            if byte_count < byte_target:
                raise RuntimeError(f"Dados insuficientes para {area}/{split}: {byte_count:,} de {byte_target:,} bytes")
            rows.extend({**record, "split": split} for record in chosen)
            joined = "\n".join(record["text"] for record in chosen)
            while len(joined.encode("utf-8")) > byte_target:
                joined = joined[:-1]
            corpus_rows.append({"area": area, "split": split, "text": joined, "bytes": len(joined.encode("utf-8"))})

    frame = pd.DataFrame(rows)
    frame.to_json(ROOT / "data/processed/abstracts.jsonl", orient="records", lines=True, force_ascii=False)
    pd.DataFrame(corpus_rows).to_json(ROOT / "data/processed/corpora.jsonl", orient="records", lines=True, force_ascii=False)
    stats = []
    for (area, split), group in frame.groupby(["area", "split"], sort=False):
        stats.append({"area": area, "split": split, "abstracts": len(group), "bytes": sum(len(text.encode("utf-8")) for text in group.text), "vocabulary": len(set(WORD.findall(" ".join(group.text))))})
    result = pd.DataFrame(stats)
    result.to_csv(ROOT / "results/tables/corpus_stats.csv", index=False)
    return result


def load_abstracts() -> pd.DataFrame:
    return pd.read_json(ROOT / "data/processed/abstracts.jsonl", lines=True)


def load_corpora() -> pd.DataFrame:
    return pd.read_json(ROOT / "data/processed/corpora.jsonl", lines=True)
