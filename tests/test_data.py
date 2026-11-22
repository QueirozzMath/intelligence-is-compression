import json

from src.data import clean_abstract, prepare_data


def test_limpeza_remove_latex_url_e_numeros():
    cleaned = clean_abstract(r"The value $x=42$ uses \alpha at https://example.com in 2024.")
    assert "http" not in cleaned
    assert "42" not in cleaned
    assert "alpha" not in cleaned


def test_particoes_nao_vazam(monkeypatch, tmp_path):
    import src.data as data_module

    (tmp_path / "data/raw").mkdir(parents=True)
    (tmp_path / "data/processed").mkdir(parents=True)
    (tmp_path / "results/tables").mkdir(parents=True)
    filler = "the study of the system and the model is important for the analysis and we show that " * 8
    records = []
    for area in ("math", "cs"):
        for index in range(8):
            records.append({"id": f"{area}-{index}", "abstract": filler + area + chr(97 + index), "categories": area})
    dump = tmp_path / "data/raw/arxiv-metadata-test.json"
    dump.write_text("\n".join(json.dumps(record) for record in records), encoding="utf-8")
    monkeypatch.setattr(data_module, "ROOT", tmp_path)
    config = {"areas": ["math", "cs"], "seed": 42, "min_abstract_chars": 300, "train_bytes_per_area": 900, "test_bytes_per_area": 900, "quick": True}
    prepare_data(config)
    frame = data_module.load_abstracts()
    assert set(frame.query("split == 'train'").id).isdisjoint(frame.query("split == 'test'").id)

