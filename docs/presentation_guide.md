# Guia da apresentação

## Entregáveis

- `deliverables/intelligence_is_compression_20min.pptx`: 18 slides, formato 16:9, elementos vetoriais editáveis e notas do apresentador.
- `deliverables/relatorio_intelligence_is_compression.pdf`: aula completa em PDF, com 20 capítulos e paginação automática.
- `docs/aula_completa.md`: fonte editável da aula.
- `docs/visual_gallery.md`: índice de figuras, gráficos, dados e simulações.

## Ritmo sugerido

A soma das notas é aproximadamente 19min45s. Os slides 3–7 constroem pergunta e teoria; 8–13 apresentam método e resultados; 14–16 fazem validação e crítica; 17 fecha a tese. Se o tempo cair para 15 minutos, pule os slides de mapa da história, assimetria e bootstrap.

## Uso no Canva

1. No Canva, escolha **Criar design → Importar arquivo**.
2. Envie o `.pptx` da pasta `deliverables/`.
3. Confira apenas quebras de linha e fontes; o arquivo combina Georgia e Arial, com substituição segura por Source Serif/Inter.
4. Preserve a proporção 16:9. Os gráficos são formas, não capturas de tela, então cores e rótulos permanecem editáveis.

## Regeneração

Execute `make deliverables` sempre que os CSVs em `results/tables/` mudarem. O gerador não recalcula os experimentos; ele apenas transforma os resultados existentes em narrativa visual.
