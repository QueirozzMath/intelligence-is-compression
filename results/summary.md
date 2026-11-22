# Resumo dos resultados

Todos os valores abaixo são lidos dos CSVs gerados pelo pipeline.

## Bits por caractere (LZMA)

| area     |     bpc |
|:---------|--------:|
| hep-th   | 2.6496  |
| stat     | 2.74133 |
| cond-mat | 2.7584  |
| math     | 2.7648  |
| quant-ph | 2.78827 |
| cs       | 2.8064  |
| econ     | 2.83307 |
| q-bio    | 2.83413 |
| physics  | 2.84587 |
| astro-ph | 2.90027 |

## Pares NCD

- Mais próximo: **cond-mat ↔ physics** (0.859)
- Mais distante: **math ↔ astro-ph** (0.898)

## Classificação

| method   |   accuracy |   f1_macro |
|:---------|-----------:|-----------:|
| NCD k=1  |   0.276316 |   0.289354 |
| NCD k=5  |   0.381579 |   0.386603 |
| n-grama  |   0.671053 |   0.682816 |
| TF-IDF   |   0.605263 |   0.590247 |
