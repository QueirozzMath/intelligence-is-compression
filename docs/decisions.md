# Registro de decisões

- **Nome do repositório:** `intelligence-is-compression`, pois o GitHub não aceita espaços. O título humano permanece “Intelligence is Compression”.
- **Isolamento:** o projeto foi criado em subdiretório próprio porque o workspace já continha um repositório não relacionado.
- **Visibilidade:** privada por padrão, por ser um trabalho acadêmico ainda em desenvolvimento.
- **Dados:** nenhum corpus sintético é usado para produzir resultados científicos. Sem dump local ou rede, a etapa de dados falha com instruções acionáveis.
- **Suavização:** interpolação recursiva de Witten–Bell em caracteres. Ela reserva massa para símbolos inéditos e permite ordens 1–6 sem dependências de modelos prontos.
- **Concatenação da NCD:** calculamos as duas ordens, `C(xy)` e `C(yx)`, e usamos a média para reduzir o efeito de ordem.
- **MDS/PCA:** implementados com autodecomposição/SVD do NumPy, sem scikit-learn.
- **Manim:** cenas usam `Text` por padrão para não exigir LaTeX. Fórmulas são strings Unicode; isso mantém a importação portátil.
- **GitHub:** o usuário criou `QueirozzMath/intelligence-is-compression`; o diretório isolado foi inicializado como repositório independente e conectado a esse remoto.
- **Execução de dados em 22/11/2026:** a API oficial respondeu HTTP 429/timeout. O fallback `UniverseTBD/arxiv-abstracts-large` do Hugging Face produziu o corpus rápido real; páginas recentes foram priorizadas porque a categoria `econ` só existe desde 2017. Nenhum resultado científico foi criado a partir de dados simulados.

