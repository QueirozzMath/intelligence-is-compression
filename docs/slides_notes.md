# Notas para os slides

Os nomes abaixo correspondem a PNG e SVG em `results/figures/`. Só use uma figura depois de ela ter sido produzida pelo pipeline.

## Figuras e fala curta

### `exp0_udhr_dendrogram`

- **Ideia:** antes do arXiv, o método recupera qualitativamente famílias linguísticas.
- **Fala (~30 s):** “Demos ao compressor traduções do mesmo texto. Sem dicionário, ele reaproveita padrões de caracteres e aproxima línguas aparentadas. Isso funciona como controle positivo da implementação.”
- **Teoria:** NCD aproxima distância de informação/complexidade de Kolmogorov.

### `exp1_bpc_compressors` e `exp1_entropy_by_order`

- **Ideia:** áreas e compressores diferem em previsibilidade; contexto reduz incerteza.
- **Fala:** “Bits por caractere é o custo da descrição. Barras menores indicam mais regularidade. À direita, aumentar a ordem reduz a entropia porque o passado informa o próximo símbolo.”
- **Teoria:** entropia condicional e códigos ótimos.

### `exp2_ncd_heatmap_lzma`, `exp2_dendrogram_lzma`, `exp2_mds_lzma`

- **Ideia:** três leituras da mesma matriz: pares, hierarquia e mapa.
- **Fala:** “Cada célula mede quanto os textos se ajudam a comprimir. O dendrograma funde os menores custos; o MDS tenta preservar todas as distâncias em duas dimensões.”
- **Teoria:** NCD, linkage médio e MDS clássico.

### `exp3_compressor_window`

- **Ideia:** a memória do algoritmo limita a distância que ele consegue enxergar.
- **Fala:** “Depois de 32 KB, o gzip não pode referenciar qualquer trecho anterior. LZMA e bz2 mantêm estruturas diferentes e por isso a separação varia com o tamanho.”
- **Teoria:** compressor prático versus compressor universal ideal.

### `exp4_cross_entropy`, `exp4_kl`, `exp4_kl_asymmetry`

- **Ideia:** descrever A com o modelo de B custa bits extras, e o custo tem direção.
- **Fala:** “A diagonal é o modelo especializado. Subtrair esse custo próprio deixa o excesso, interpretado como KL estimada. Trocar A e B muda a pergunta.”
- **Teoria:** `H(P,Q) = H(P) + KL(P||Q)`.

### `exp4_loss_vs_data`

- **Ideia:** mais dados melhoram a previsão, com retornos decrescentes.
- **Fala:** “O modelo é só contagem de n-gramas, mas já mostra a forma conceitual do pré-treino: observar mais texto reduz a loss no teste.”
- **Teoria:** entropia cruzada fora da amostra.

### `exp5_word_contributions`

- **Ideia:** palavras individuais mostram onde estão os bits de diferença.
- **Fala:** “Decompomos KL por palavra. O gráfico transforma uma distância abstrata em termos reconhecíveis e mostra por que vocabulário especializado separa áreas.”
- **Teoria:** soma `p(w) log2(p(w)/q(w))`.

### `exp6_confusion_matrices` e `exp6_method_comparison`

- **Ideia:** classificação testa a distância em artigos nunca vistos.
- **Fala:** “Não basta uma árvore bonita. Aqui cada resumo precisa escolher uma área. As confusões revelam fronteiras reais e o TF-IDF calibra quão forte é o sinal lexical.”
- **Teoria:** decisão pelo menor comprimento de código; MDL.

### `exp7_interdisciplinary`

- **Ideia:** textos híbridos tendem a ocupar a fronteira dos dois modelos.
- **Fala:** “Cada eixo é custo sob uma área. Cross-lists reais — ou misturas explicitamente marcadas quando eles faltam — testam se o espaço de bits preserva interdisciplinaridade.”
- **Teoria:** entropia cruzada como coordenada relativa a modelos.

## Roteiro sugerido (11 slides)

1. Pergunta: inteligência é encontrar descrições curtas?
2. Entropia, surpresa e código ótimo (A1).
3. Entropia cruzada e KL (A2).
4. Controle positivo com línguas (Exp0).
5. Do compressor à NCD (A3).
6. Heatmap e dendrograma das áreas (B1/B2).
7. Mapa 2D/3D (C1).
8. Onde estão os bits: palavras (B3).
9. Classificação e nuvem de artigos (B5/C2).
10. Limites: janela, assimetria, taxonomia (A4/B6).
11. Conclusão: compressão como teste operacional de estrutura.

