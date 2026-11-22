# Intelligence is Compression

## Aula completa para preparação da apresentação

Este material foi escrito para que qualquer integrante do grupo consiga compreender, explicar e defender o projeto. Ele não é apenas um roteiro dos slides: é uma aula sobre as ideias matemáticas, as decisões experimentais, os resultados e os limites da interpretação.

## 1. A pergunta científica

O projeto investiga uma hipótese operacional: se dois textos compartilham regularidades, então conhecer um deles deve ajudar a descrever o outro usando menos bits. “Regularidade” pode significar padrões de caracteres, morfologia, construções recorrentes, vocabulário técnico ou estilo. A compressão transforma todas essas formas de repetição em uma grandeza mensurável: comprimento de código.

Isso não equivale a afirmar que inteligência seja literalmente compressão. A formulação prudente é: descobrir boas representações e prever dados novos exige explorar regularidades; compressores e modelos probabilísticos permitem medir parte dessas regularidades. O título é uma provocação científica, não uma identidade metafísica.

As perguntas de pesquisa são: áreas científicas próximas compartilham padrões comprimíveis? A distância obtida por compressores recupera alguma organização reconhecível? Modelos treinados em uma área codificam melhor textos da própria área? A estrutura observada generaliza para resumos não vistos? Quais palavras explicam as diferenças?

## 2. Informação como surpresa

Na teoria de Shannon, a informação associada a um evento depende de sua probabilidade. Se um evento é quase certo, observá-lo ensina pouco. Se é raro, sua ocorrência elimina muitas possibilidades e fornece mais informação. A medida que satisfaz as propriedades desejadas é

I(x) = -log2 p(x).

O logaritmo transforma probabilidades multiplicativas em custos aditivos. Dois eventos independentes com probabilidades p e q têm probabilidade conjunta pq, e -log2(pq) = -log2 p - log2 q. A base 2 mede o resultado em bits.

Um evento com probabilidade 1/2 custa 1 bit; com 1/4, custa 2 bits; com 1/8, custa 3 bits. Dizer “custa” significa que um código ideal precisaria aproximadamente desse número de decisões binárias para identificar o evento.

Durante a apresentação, não introduza a fórmula isoladamente. Comece com uma previsão: “qual símbolo vem agora?”. Mostre que símbolos esperados recebem códigos curtos e símbolos improváveis recebem códigos longos. Só então revele o logaritmo.

## 3. Entropia

A entropia de uma distribuição P é a surpresa média:

H(P) = - soma_x p(x) log2 p(x).

Ela mede a incerteza antes de observar o resultado e, ao mesmo tempo, o comprimento médio mínimo alcançável por códigos sem perda sob condições ideais. Uma fonte determinística tem entropia zero. Uma moeda justa tem 1 bit por lançamento. Entre distribuições com o mesmo número de resultados, a uniforme possui entropia máxima.

É importante distinguir entropia de tamanho do arquivo. Entropia é uma propriedade do modelo probabilístico da fonte. O tamanho comprimido é uma estimativa prática afetada por cabeçalhos, algoritmo, tamanho da amostra e capacidade do compressor.

No projeto, bits por caractere, ou bpc, permitem comparar textos de tamanhos diferentes. Se um arquivo de N caracteres é comprimido para B bytes, o custo aproximado é 8B/N bits por caractere. Valores menores indicam maior previsibilidade para aquele compressor.

## 4. Compressão é previsão

Um compressor sem perda precisa permitir a reconstrução exata do texto. Para encurtar a descrição, ele identifica padrões recorrentes. Algoritmos de dicionário referenciam sequências vistas anteriormente; modelos estatísticos atribuem códigos curtos a símbolos prováveis. Em ambos os casos, compressão e previsão estão ligadas.

Gzip combina LZ77 e codificação de Huffman e possui uma janela histórica limitada, tipicamente 32 KB. Bz2 usa transformação de Burrows-Wheeler, move-to-front e Huffman. LZMA usa dicionários maiores e codificação por intervalos, capturando dependências mais longas. Como cada algoritmo enxerga padrões diferentes, nenhuma distância baseada em compressor é independente do compressor.

Os modelos de n-gramas do projeto estimam a probabilidade do próximo caractere a partir dos n-1 caracteres anteriores. A ordem controla o contexto: ordem 1 ignora o passado; ordens maiores capturam combinações locais mais específicas. Contexto demais pode causar esparsidade, por isso é necessária suavização.

## 5. Entropia cruzada

Suponha que os dados sejam gerados por P, mas o código tenha sido construído usando Q. O custo médio é a entropia cruzada:

H(P,Q) = - soma_x p(x) log2 q(x).

Se Q atribui alta probabilidade aos eventos que realmente ocorrem, o custo é baixo. Se Q está errado, pagamos bits extras. A identidade central é

H(P,Q) = H(P) + KL(P || Q).

H(P) é a incerteza inevitável da fonte. KL(P||Q) é o desperdício causado pelo modelo errado. A divergência KL é não negativa e vale zero quando as distribuições coincidem nos eventos relevantes.

KL não é uma distância métrica: em geral KL(P||Q) difere de KL(Q||P), não há simetria e não vale a desigualdade triangular. A direção tem interpretação. “Quanto custa explicar matemática com um modelo de astronomia?” é uma pergunta diferente de “quanto custa explicar astronomia com matemática?”.

No corpus, matemática codificada pelo modelo de astro-ph custa aproximadamente 3,08 bpc, contra 2,54 bpc no modelo próprio, um excesso de cerca de 0,54 bpc. Este número vem dos CSVs produzidos pelo pipeline.

## 6. Suavização Witten-Bell

Um modelo de n-gramas ingênuo atribuiria probabilidade zero a sequências nunca observadas. Isso produziria custo infinito quando uma sequência nova aparecesse. A suavização Witten-Bell reserva massa de probabilidade para eventos não vistos com base no número de tipos distintos já encontrados.

A intuição é simples: se um contexto gerou muitos símbolos diferentes, ainda há chance razoável de aparecer algo novo; se sempre gerou o mesmo símbolo, a massa reservada pode ser menor. Esse mecanismo permite avaliar texto fora da amostra sem inventar contagens artificiais grandes.

## 7. Complexidade de Kolmogorov

A complexidade de Kolmogorov K(x) é o tamanho do programa mais curto que produz x em uma máquina universal prefix-free. Ela formaliza a ideia de descrição mínima. Uma sequência altamente regular, como mil repetições de “01”, possui descrição curta; uma sequência verdadeiramente aleatória não oferece atalho substancial.

K(x) é incomputável. Não existe algoritmo geral que encontre sempre o menor programa. Compressores reais fornecem limites superiores: se um compressor produz C(x) bytes, então existe ao menos uma descrição de x com esse tamanho mais o decodificador.

Essa distinção deve ser dita explicitamente. O projeto não mede a complexidade de Kolmogorov verdadeira; usa compressores práticos como aproximações operacionais.

## 8. NCD

A distância de compressão normalizada é

NCD(x,y) = [C(xy) - min(C(x),C(y))] / max(C(x),C(y)).

C(xy) é o tamanho da concatenação comprimida. Se x e y compartilham padrões, comprimir juntos permite reutilização e C(xy) cresce menos. O numerador estima informação adicional; o denominador normaliza pela complexidade do objeto maior.

Idealmente, valores próximos de zero indicam objetos muito parecidos e valores próximos de um indicam pouca estrutura compartilhada. Na prática, podem ocorrer desvios por cabeçalhos, ordem de concatenação, janelas e imperfeições do compressor.

Benedetto et al. aplicaram essa ideia a textos em diferentes línguas. O projeto reproduz uma verificação qualitativa com traduções da Declaração Universal dos Direitos Humanos antes de aplicar o método ao arXiv. Esse controle positivo testa se a implementação recupera estrutura conhecida.

## 9. Dados e desenho experimental

O corpus reúne resumos reais do arXiv em dez macroáreas: math, astro-ph, cond-mat, hep-th, cs, q-bio, stat, econ, physics e quant-ph. O pipeline normaliza espaços, filtra textos muito curtos, balanceia as áreas por bytes e separa treino e teste.

Balancear por bytes é importante porque compressores se beneficiam de mais dados. Sem balanceamento, uma área maior poderia parecer mais previsível apenas por oferecer mais oportunidades de aprender padrões. A seed 42 torna amostragem e partições reproduzíveis.

O repositório contém uma execução rápida real e balanceada. Ela percorre o mesmo pipeline da configuração completa, mas usa menos dados, exemplos de teste e reamostragens. Portanto, demonstra o método sem sustentar a mesma precisão estatística de uma execução completa.

Não há embeddings, redes neurais ou modelos pré-treinados. Isso isola a pergunta: quanta estrutura emerge apenas de contagem, probabilidade e compressão?

## 10. Experimentos

O experimento 0 é o controle com línguas. O experimento 1 compara compressibilidade e entropia por ordem. O experimento 2 constrói matrizes NCD, dendrogramas e mapas MDS. O experimento 3 testa como o tamanho e a janela do compressor afetam a separação. O experimento 4 mede entropia cruzada, KL, assimetria e curva de aprendizado. O experimento 5 decompõe divergência por palavra. O experimento 6 classifica artigos não vistos. O experimento 7 examina textos interdisciplinares. O experimento 8 estima robustez por bootstrap.

Os CSVs são produzidos antes das figuras. As animações e a apresentação consomem esses CSVs, evitando números digitados manualmente. Isso é parte do rigor: uma mudança nos dados pode regenerar todos os artefatos.

## 11. Dendrogramas, MDS e interpretação

Uma matriz NCD contém uma distância para cada par de áreas. O dendrograma aplica agrupamento hierárquico e funde primeiro os grupos mais próximos. A altura da fusão representa a distância do linkage, não causalidade nem uma taxonomia definitiva.

MDS procura coordenadas em poucas dimensões que preservem as distâncias tanto quanto possível. É uma projeção: distorções são inevitáveis. Proximidade visual só deve ser interpretada em conjunto com a matriz original e métricas de ajuste.

No resultado LZMA, cond-mat e physics formam o par mais próximo, com NCD aproximadamente 0,859. Math e astro-ph formam o par mais distante, com aproximadamente 0,898. O intervalo total é estreito; portanto, o resultado indica ordenação relativa, não clusters perfeitamente separados.

## 12. Explicabilidade por palavras

A KL discreta pode ser decomposta:

KL(P||Q) = soma_w p(w) log2[p(w)/q(w)].

Cada palavra contribui positiva ou negativamente. Termos frequentes em P e raros em Q elevam o custo. O gráfico de contribuições transforma uma diferença abstrata em vocabulário reconhecível e mostra quanto da separação é lexical.

Essa explicabilidade também revela uma limitação: se palavras especializadas dominam, a distância pode medir jargão mais do que proximidade conceitual profunda. O achado continua válido, mas sua interpretação precisa ser específica.

## 13. Classificação como teste de generalização

Mapas atraentes não bastam. Para testar se a estrutura possui poder preditivo, cada resumo de teste deve escolher uma área sem ter sido usado no ajuste. O projeto compara NCD k=1, NCD k=5, modelo de n-gramas e TF-IDF.

Na execução versionada, n-gramas alcançam 67,1% de acurácia e 68,3% de F1 macro. TF-IDF alcança 60,5%. NCD k=5 alcança 38,2% e NCD k=1, 27,6%. O n-grama é o melhor método do experimento; NCD encontra estrutura, mas não é o melhor classificador.

F1 macro calcula F1 separadamente para cada classe e tira a média, dando o mesmo peso a todas as áreas. Isso é útil mesmo com balanceamento, porque expõe desempenho desigual entre classes.

Uma ótima apresentação não esconde o resultado desfavorável. Pelo contrário: ele separa duas teses. “Existe estrutura comprimível” recebe suporte. “Qualquer compressor é um classificador competitivo” não recebe.

## 14. Bootstrap e incerteza

Bootstrap reamostra observações com reposição para aproximar a variabilidade de uma estatística. Repetimos o cálculo em várias amostras e usamos percentis como intervalo empírico.

Os intervalos de acurácia são relativamente largos porque o modo rápido possui poucos exemplos. Isso impede superinterpretação de diferenças pequenas. Para o trabalho final, uma execução completa aumentaria o número de artigos e reamostragens.

Bootstrap não corrige vieses sistemáticos do corpus ou do modelo. Ele mede variação sob a amostra observada.

## 15. Interdisciplinaridade

Um artigo interdisciplinar pode ser representado por seus custos sob dois modelos. Um texto típico de A deve custar menos sob A; um texto típico de B, menos sob B; textos híbridos tendem a ocupar regiões intermediárias.

Essa visualização não prova interdisciplinaridade conceitual. Ela testa compatibilidade linguística com os modelos das áreas. Cross-lists reais são preferíveis; misturas artificiais, quando usadas, precisam ser marcadas explicitamente.

## 16. Principais limitações

Primeiro, o compressor define o que conta como padrão. Segundo, gzip possui memória limitada. Terceiro, C(xy) pode diferir de C(yx). Quarto, textos maiores reduzem overhead relativo. Quinto, a taxonomia do arXiv é administrativa e artigos podem pertencer a mais de uma área. Sexto, limpeza e idioma alteram estatísticas. Sétimo, proximidade lexical não é sinônimo de proximidade conceitual. Oitavo, MDS e dendrogramas simplificam a matriz.

Essas limitações não invalidam o projeto. Elas delimitam a afirmação: medimos regularidades textuais acessíveis a modelos específicos em um corpus específico.

## 17. Como apresentar em vinte minutos

Nos primeiros quatro minutos, construa surpresa e entropia. Do quarto ao sétimo, explique cross-entropy, KL e compressão como previsão. Do sétimo ao décimo, apresente NCD e o desenho experimental. Do décimo ao décimo quinto, mostre resultados e palavras explicativas. Do décimo quinto ao décimo oitavo, mostre classificação e bootstrap. Use os dois minutos finais para limitações e conclusão.

Não leia equações termo por termo. Explique a pergunta respondida por cada uma. Não descreva todos os elementos de um gráfico; direcione o olhar para a comparação relevante. Faça pausas depois dos resultados principais.

## 18. Perguntas prováveis e respostas

“Por que não usar embeddings?” Porque o objetivo é isolar teoria da informação e testar quanto emerge de comprimento de código sem representações pré-treinadas.

“NCD é realmente uma métrica?” A versão ideal baseada em complexidade normalizada possui propriedades métricas aproximadamente; a implementação com compressores reais pode violá-las.

“Por que LZMA?” Porque possui dicionário maior e costuma explorar dependências mais longas. O projeto também compara gzip e bz2 para mostrar dependência do compressor.

“Acurácia de 67% é boa?” Com dez classes, está muito acima do acaso de 10%, mas a relevância depende do corpus e dos intervalos. TF-IDF é um baseline importante.

“Isso mede inteligência?” Mede regularidade, custo de descrição e capacidade de generalização em texto. O título conecta essas ideias a uma visão de inteligência, mas os dados não demonstram uma teoria geral da mente.

“Por que KL é assimétrica?” Porque a expectativa é tomada sob P. Eventos comuns em P e raros em Q têm efeito diferente dos eventos comuns em Q e raros em P.

## 19. Checklist antes da apresentação

Confirme a proporção 16:9, as fontes substituídas pelo Canva, a legibilidade a distância, os vídeos offline e as notas. Abra o PPTX no computador da sala. Leve uma cópia em PDF e outra em pendrive. Teste o tempo com cronômetro. Cada integrante deve saber explicar a pergunta, a identidade H(P,Q)=H(P)+KL, a NCD, o protocolo de treino/teste, o resultado de classificação e pelo menos três limitações.

## 20. Conclusão

O projeto mostra que comprimento de descrição é uma lente concreta para estudar estrutura textual. Entropia conecta probabilidade a bits; entropia cruzada mede o custo de usar o modelo errado; KL localiza o excesso; NCD transforma compressão conjunta em afinidade; classificação testa generalização.

A conclusão mais forte sustentada pelos dados é: áreas científicas deixam assinaturas estatísticas detectáveis, e modelos simples de caracteres conseguem explorá-las para prever textos novos. A conclusão que deve ser evitada é: a geometria obtida representa de forma definitiva a organização do conhecimento.

## Referências

SHANNON, C. E. A Mathematical Theory of Communication. Bell System Technical Journal, 1948.

BENEDETTO, D.; CAGLIOTI, E.; LORETO, V. Language Trees and Zipping. Physical Review Letters, 2002.

LI, M.; CHEN, X.; LI, X.; MA, B.; VITÁNYI, P. The Similarity Metric. IEEE Transactions on Information Theory, 2004.

3BLUE1BROWN. But what is cross-entropy? Material audiovisual educacional.
