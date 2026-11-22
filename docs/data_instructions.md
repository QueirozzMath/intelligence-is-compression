# Como obter os dados do arXiv

O pipeline procura primeiro por `data/raw/arxiv-metadata*.json` ou `*.jsonl`.

1. Baixe o arquivo `arxiv-metadata-oai-snapshot.json` do conjunto **Cornell-University/arxiv** no Kaggle.
2. Coloque-o em `data/raw/arxiv-metadata-oai-snapshot.json`.
3. Execute `python -m src.cli data` (ou `make data`).

Cada linha deve ser um objeto JSON com, no mínimo, `id`, `abstract` e `categories`; `title`, `update_date` e `authors` são opcionais. O primeiro código em `categories` é tratado como categoria primária. O arquivo bruto não é versionado.

Se não houver dump, `python -m src.cli data --download` tenta a API oficial do arXiv com cache, retomada e intervalo mínimo de três segundos.
