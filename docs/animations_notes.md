# Notas das animações ManimGL

As 13 cenas são independentes, usam fundo escuro e leem valores de `results/tables/`. As 13 classes foram importadas com sucesso no ManimGL 1.7.2. Tempos abaixo são alvos de roteiro; confirme a duração exata dos MP4 após renderizar, pois o ambiente não possuía ffmpeg nem os CSVs reais (a API do arXiv respondeu HTTP 429).

| Cena | Arquivo | Duração alvo | Slide | Ideia e fala curta |
|---|---|---:|---:|---|
| A1 | `scenes_basics.py` | 35 s | 2 | Probabilidades reais viram comprimentos `−log2 p`; símbolos prováveis custam menos bits. |
| A2 | `scenes_basics.py` | 30 s | 3 | O bloco KL é exatamente o custo extra entre entropia própria e cruzada. |
| A3 | `scenes_basics.py` | 45 s | 5 | Textos próximos permitem maior reaproveitamento ao comprimir a concatenação. |
| A4 | `scenes_basics.py` | 35 s | 10 | A janela de 32 KB explica por que gzip perde relações longas. |
| B1 | `scenes_data.py` | 35 s | 6 | A matriz nasce célula a célula; cor e número são a mesma NCD real. |
| B2 | `scenes_data.py` | 45 s | 6 | As fusões do linkage aparecem na ordem e altura exportadas pelo SciPy. |
| B3 | `scenes_data.py` | 50 s | 8 | Três pares mostram as palavras que carregam mais KL. |
| B4 | `scenes_data.py` | 30 s | 3 | Um ponto percorre a curva real de loss conforme cresce o treino. |
| B5 | `scenes_data.py` | 50 s | 9 | Um acerto e um erro reais competem por menor bpc. |
| B6 | `scenes_data.py` | 30 s | 10 | Setas desiguais tornam visível a assimetria da KL. |
| C1 | `scenes_3d.py` | 35 s | 7 | MDS 3D converte a matriz NCD em um mapa orbital das áreas. |
| C2 | `scenes_3d.py` | 50 s | 9 | PCA via NumPy reduz os vetores de bpc; `DotCloud` mantém 1.500 pontos eficientes. |
| C3 | `scenes_3d.py` | 45 s | 3 | A bolinha desce na superfície de entropia cruzada até `Q=P`. |

## Comandos

```bash
manimgl animations/scenes_basics.py A2CrossEntropyWaste -w
manimgl animations/scenes_data.py B2GrowingDendrogram -w
manimgl animations/scenes_3d.py C2ArticlesCloud3D -w
bash animations/render_all.sh preview
bash animations/render_all.sh final
```

O script também chama `-so` para salvar o último frame. Se OpenGL não abrir, execute numa sessão gráfica local com drivers atualizados; a versão do ManimGL deve ser conferida com `manimgl --help`. Dependências do sistema: ffmpeg, Pango/Cairo e OpenGL; LaTeX é opcional porque o projeto usa `Text`.

## Ordem para a apresentação

A1 → A2 → B4 → A3 → B1 → B2 → C1 → B3 → B5 → C2 → A4 → B6 → C3. Para uma aula curta, priorize A2, B2, B3, C1 e C2.
