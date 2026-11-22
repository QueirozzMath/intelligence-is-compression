const slides=[
 {title:'Intelligence<br><span class="accent">is compression</span>',body:'Podemos medir proximidade entre ideias contando quantos bits elas compartilham?',kind:'hero'},
 {title:'Informação é<br><span class="amber">surpresa</span>',body:'Quanto menos provável um evento, mais perguntas binárias precisamos para identificá-lo.',formula:'I(x) = −log₂ p(x)'},
 {title:'Entropia é o custo médio do melhor código',body:'Símbolos frequentes recebem descrições curtas. A incerteza média estabelece o limite.',formula:'H(P) = −Σ p(x) log₂ p(x)',visual:'tape'},
 {title:'Comprimir é prever',body:'Um compressor economiza bits quando reconhece regularidades e antecipa o que vem depois.',visual:'prediction'},
 {title:'O modelo errado cobra bits extras',body:'Cross-entropy mede o custo real de codificar P usando probabilidades propostas por Q.',formula:'H(P,Q) = H(P) + KL(P‖Q)',visual:'cross'},
 {title:'Complexidade é o tamanho da descrição mais curta',body:'K(x) é incomputável. Compressores reais fornecem aproximações operacionais, nunca a resposta universal.',formula:'K(x) ≲ C(x)'},
 {title:'Quanto A ajuda a descrever B?',body:'A NCD normaliza o ganho obtido quando dois textos são comprimidos juntos.',formula:'NCD(x,y) = [C(xy)−min(Cx,Cy)] / max(Cx,Cy)',visual:'ncd'},
 {title:'Uma escada de evidências',body:'Cada etapa torna mais difícil explicar o resultado por uma coincidência visual.',visual:'evidence'},
 {title:'Dez áreas, uma mesma régua',body:'Resumos reais do arXiv, balanceados por bytes e separados entre treino e teste.',visual:'areas'},
 {title:'Regularidade aparece como menos bits',body:'No corpus rápido, os custos LZMA variam de 2,65 a 2,90 bits por caractere.',visual:'bpc'},
 {title:'A afinidade mais forte',body:'cond-mat e physics compartilham o maior ganho de compressão conjunta observado.',visual:'closest'},
 {title:'Podemos localizar os bits de diferença',body:'A divergência KL se decompõe por palavra e revela o papel do vocabulário especializado.',visual:'words'},
 {title:'A direção muda a pergunta',body:'KL(P‖Q) não é KL(Q‖P). Explicar A com B difere de explicar B com A.',formula:'KL(P‖Q) ≠ KL(Q‖P)'},
 {title:'O teste decisivo acontece fora da amostra',body:'Cada resumo não visto precisa escolher uma área. Uma árvore bonita não basta.',visual:'classification'},
 {title:'<span class="result-number">67,1%</span>',body:'Acurácia do modelo de n-gramas. TF-IDF: 60,5%. NCD k=5: 38,2%.',visual:'result'},
 {title:'Toda estimativa traz incerteza',body:'Bootstrap mostra que o corpus rápido ainda produz intervalos largos. Diferenças pequenas não devem ser superinterpretadas.',visual:'uncertainty'},
 {title:'O compressor também tem um ponto de vista',body:'Janela, ordem de concatenação, vocabulário, taxonomia e tamanho da amostra condicionam a geometria observada.'},
 {title:'Uma descrição curta só importa se ainda generaliza',body:'Os dados sustentam a existência de assinaturas estatísticas entre áreas — não uma taxonomia definitiva do conhecimento.',kind:'closing'}
];
const stage=document.querySelector('#slide-stage');
const bpc=[['hep-th',2.65],['stat',2.74],['cond-mat',2.76],['math',2.76],['astro-ph',2.90]];
function visual(type){
 if(type==='tape')return `<div class="tape"><span>A</span><span>B</span><span>A</span><span>C</span><span>A</span><span class="bit">0</span><span class="bit">10</span><span class="bit">0</span><span class="bit">110</span></div>`;
 if(type==='prediction')return `<div class="tape"><span>teor</span><span class="accent">i</span><span class="accent">a</span><span>→</span><span class="bit">0,62</span><span>−log₂</span><span class="amber">0,69 bit</span></div>`;
 if(type==='cross')return `<div class="tape"><span>P</span><span>→</span><span>Q</span><span>→</span><span class="bit">bits inevitáveis</span><span class="waste">bits desperdiçados</span></div>`;
 if(type==='ncd')return `<div class="metric-pair"><div class="metric"><strong>0</strong>idênticos</div><div class="metric"><strong>0,859</strong>cond-mat ↔ physics</div><div class="metric"><strong>1</strong>sem padrões comuns</div></div>`;
 if(type==='evidence')return `<div class="evidence">${['sanidade','descrição','explicação','predição','incerteza'].map((x,i)=>`<div style="--level:${i}"><strong>${x}</strong><span>${['línguas','mapas','palavras','teste','bootstrap'][i]}</span></div>`).join('')}</div>`;
 if(type==='areas')return `<div class="tape">${['math','astro','cond','hep','cs','bio','stat','econ','phys','quant'].map(x=>`<span>${x}</span>`).join('')}</div>`;
 if(type==='bpc')return `<div class="bars">${bpc.map(([a,v])=>`<div class="bar-row"><span>${a}</span><div class="bar-track"><div class="bar-fill" style="width:${(v-2.5)/.5*100}%"></div></div><strong>${v.toFixed(2)}</strong></div>`).join('')}</div>`;
 if(type==='closest')return `<div class="metric-pair"><div class="metric"><strong>0,859</strong>cond-mat ↔ physics</div><div class="metric"><strong>0,898</strong>math ↔ astro-ph</div></div>`;
 if(type==='words')return `<div class="tape">${['quantum','galaxies','algorithm','theorem','protein'].map((x,i)=>`<span style="font-size:${2.2-i*.2}rem">${x}</span>`).join('')}</div>`;
 if(type==='classification')return `<div class="tape"><span>resumo</span><span>→</span><span>10 modelos</span><span>→</span><span class="green">menor custo</span><span>→</span><span>área</span></div>`;
 if(type==='result')return `<a class="thesis" href="simulations.html#classification">Abrir a classificação interativa →</a>`;
 if(type==='uncertainty')return `<div class="tape"><span>57,2%</span><span class="green">67,1%</span><span>76,3%</span></div>`;
 return '';
}
slides.forEach((s,i)=>{const el=document.createElement('article');el.className='slide';el.id=`slide-${i+1}`;el.innerHTML=`<div class="${s.visual?'slide-grid':''}"><div><h${i===0?1:2}>${s.title}</h${i===0?1:2}><p>${s.body}</p>${s.formula?`<div class="formula">${s.formula}</div>`:''}</div>${s.visual?`<div>${visual(s.visual)}</div>`:''}</div>${i===0?'<span class="citation">Teoria da Informação · apresentação de 20 minutos</span>':''}`;stage.append(el)});
let current=0;function show(n){current=(n+slides.length)%slides.length;document.querySelectorAll('.slide').forEach((s,i)=>s.classList.toggle('active',i===current));document.querySelector('#counter').value=`${current+1} / ${slides.length}`;document.querySelector('#progress-bar').style.width=`${(current+1)/slides.length*100}%`;history.replaceState(null,'',`#${current+1}`);document.title=`${current+1}/${slides.length} — Intelligence is Compression`}
document.querySelector('#prev').onclick=()=>show(current-1);document.querySelector('#next').onclick=()=>show(current+1);document.querySelector('#fullscreen').onclick=()=>document.documentElement.requestFullscreen?.();addEventListener('keydown',e=>{if(['ArrowRight',' ','PageDown'].includes(e.key)){e.preventDefault();show(current+1)}if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();show(current-1)}if(e.key==='Home')show(0);if(e.key==='End')show(slides.length-1)});show(Math.max(0,(+location.hash.slice(1)||1)-1));
