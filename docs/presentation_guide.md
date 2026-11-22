# Guia da apresentação

## Entregáveis

- `deliverables/intelligence_is_compression_20min.pptx`: 16 slides, formato 16:9, elementos vetoriais editáveis e notas do apresentador.
- `deliverables/relatorio_intelligence_is_compression.pdf`: relatório A4 de quatro páginas para preparar a fala.

## Ritmo sugerido

A soma das notas de cada slide é aproximadamente 19min45s. Os slides 3–5 constroem a teoria; 6–11 apresentam método e resultados; 12–14 fazem validação e crítica; 15 fecha a tese. Se o tempo cair para 15 minutos, pule os slides 2, 11 e 13.

## Uso no Canva

1. No Canva, escolha **Criar design → Importar arquivo**.
2. Envie o `.pptx` da pasta `deliverables/`.
3. Confira apenas quebras de linha e fontes; o arquivo usa Aptos, com substituição segura por Arial/Inter.
4. Preserve a proporção 16:9. Os gráficos são formas, não capturas de tela, então cores e rótulos permanecem editáveis.

## Regeneração

Execute `make deliverables` sempre que os CSVs em `results/tables/` mudarem. O gerador não recalcula os experimentos; ele apenas transforma os resultados existentes em narrativa visual.
