# Intelligence is Compression

Projeto de Teoria da Informação que testa uma ideia simples: se dois conjuntos de resumos científicos compartilham regularidades, um compressor ou modelo probabilístico treinado em um deles deve descrever o outro com menos bits. O pipeline compara áreas do arXiv usando NCD, entropia, entropia cruzada e divergência KL — sem redes neurais, embeddings ou modelos pré-treinados.

## O que o projeto produz

- uma réplica de sanidade com línguas da Declaração Universal dos Direitos Humanos;
- compressibilidade, NCD, dendrogramas e MDS entre áreas;
- experimento sobre a janela de 32 KB do gzip;
- modelos de caracteres de ordem 1–6 com Witten–Bell;
- palavras que mais contribuem para KL;
- classificação individual por NCD, n-gramas e TF-IDF;
- análise de textos interdisciplinares e robustez por bootstrap;
- figuras em PNG 300 dpi e SVG;
- 13 cenas ManimGL, incluindo três visualizações 3D.
- uma apresentação de 20 minutos em PPTX editável/importável no Canva;
- um relatório de apoio em PDF com quatro páginas.

Nenhum resultado é inventado: `results/summary.md` só é escrito depois que os CSVs correspondentes existem.

## Instalação

Requer Python 3.10+. No Python 3.13/3.14, `audioop-lts` fornece a compatibilidade de áudio removida da biblioteca padrão.

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt
```

Alternativa recomendada, sem alterar o Python do sistema:

```bash
uv python install 3.12
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Para as animações, Pango e uma implementação OpenGL funcional são necessários; LaTeX é opcional. O pacote `imageio-ffmpeg` fornece um ffmpeg isolado quando não existe uma instalação do sistema.

## Dados

O caminho mais reprodutível é baixar `arxiv-metadata-oai-snapshot.json` do dataset **Cornell-University/arxiv** no Kaggle e colocá-lo em `data/raw/`. Consulte [`docs/data_instructions.md`](docs/data_instructions.md). Alternativamente:

```bash
python -m src.cli data --download
```

Essa opção usa a API oficial, cache incremental e espera pelo menos três segundos entre chamadas.

## Execução

```bash
# teste rápido, percorrendo a mesma lógica com amostras menores
python -m src.cli all --quick

# execução completa
python -m src.cli all

# testes unitários
python -m pytest
```

Em sistemas com GNU Make: `make quick`, `make all` e `make test`. Todos os parâmetros científicos ficam em `config.yaml`, com seed fixa 42.

## Animações

Este projeto usa o **ManimGL de 3Blue1Brown** (`pip install manimgl`), não a Community Edition.

```bash
# uma cena interativa/preview
manimgl animations/scenes_data.py B2GrowingDendrogram

# grava todas em preview 480p15 e salva último frame
make animations

# versão final 1080p60
make animations-final
```

As cenas leem exclusivamente `results/tables/`; rode o pipeline antes. Em Windows sem Bash, execute os comandos individuais listados em [`docs/animations_notes.md`](docs/animations_notes.md).

## Apresentação e relatório

### Downloads rápidos

- **[Abrir a apresentação web interativa](https://queirozzmath.github.io/intelligence-is-compression/web/)**
- **[Abrir diretamente o laboratório de simulações e animações](https://queirozzmath.github.io/intelligence-is-compression/web/simulations.html)**
- **[Apresentação web interativa — prévia desta versão](https://raw.githack.com/QueirozzMath/intelligence-is-compression/feat/interactive-web-presentation/web/index.html)**
- **[Laboratório de simulações — prévia desta versão](https://raw.githack.com/QueirozzMath/intelligence-is-compression/feat/interactive-web-presentation/web/simulations.html)**
- **[Baixar a apresentação editável em PPTX](deliverables/intelligence_is_compression_20min.pptx)**
- **[Baixar a aula completa em PDF](deliverables/relatorio_intelligence_is_compression.pdf)**
- **[Acessar todas as figuras, gráficos, dados e simulações](docs/visual_gallery.md)**
- [Ler a aula completa em Markdown](docs/aula_completa.md)

Links diretos para experiências: [surpresa em bits](web/simulations.html#surprise), [construtor de códigos](web/simulations.html#codes), [cross-entropy](web/simulations.html#cross-entropy), [NCD entre textos](web/simulations.html#ncd), [janela do gzip](web/simulations.html#gzip-window), [mapa das áreas](web/simulations.html#areas), [classificação](web/simulations.html#classification) e [superfície 3D](web/simulations.html#surface).

Os entregáveis são gerados diretamente dos CSVs versionados, preservando a rastreabilidade dos números:

```bash
npm install
make deliverables
```

Os arquivos finais aparecem em `deliverables/`. O PPTX usa formas vetoriais, textos editáveis e notas do apresentador; pode ser aberto no PowerPoint, Google Slides ou importado no Canva. O relatório é uma aula extensa e autônoma para preparação do grupo.

A versão web não depende de internet nem de bibliotecas externas. Para evitar restrições de alguns navegadores ao abrir arquivos locais, rode `make web` e acesse `http://localhost:8000/web/`.

Neste ambiente, as 13 classes foram importadas com sucesso no ManimGL 1.7.2. A API do arXiv bloqueou o IP, mas o fallback público do Hugging Face produziu um corpus rápido real e balanceado; os resultados versionados vêm desse corpus. Os MP4 não foram renderizados porque ffmpeg não estava instalado. Nenhum vídeo ou resultado foi simulado.

## Interpretação e limitações

NCD aproxima uma distância baseada em complexidade de Kolmogorov, mas o resultado depende do compressor, ordem de concatenação, janela e tamanho do texto. Vocabulário compartilhado pode dominar sem representar proximidade conceitual. A taxonomia do arXiv, a limpeza e o balanceamento também introduzem escolhas. A KL estimada compara modelos suavizados finitos, não distribuições verdadeiras. TF-IDF é incluído como baseline lexical, não como parte da proposta de compressão.

Os resultados concretos e eventuais desvios das hipóteses esperadas são documentados automaticamente em `results/summary.md` após uma execução. Se os agrupamentos forem surpreendentes, devem ser tratados como achado ou limitação, não corrigidos manualmente.

## Estrutura

- `src/data.py`: aquisição, limpeza, balanceamento e partições;
- `src/compress.py`: gzip/bz2/lzma e NCD;
- `src/ngram.py`: entropia e modelos Witten–Bell;
- `src/experiments/`: experimentos 0–8 e exportação para Manim;
- `animations/`: cenas A1–A4, B1–B6 e C1–C3;
- `tests/`: invariantes matemáticos e ausência de vazamento;
- `docs/`: plano, decisões e roteiros.

## Referências

- Benedetto et al. (2002), *Language Trees and Zipping*.
- 3Blue1Brown, *But what is cross-entropy?*
- Shannon (1948), *A Mathematical Theory of Communication*.

