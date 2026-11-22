#!/usr/bin/env node
/* Gera uma apresentação PPTX editável e um relatório PDF a partir dos CSVs reais. */
const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');
const PDFDocument = require('pdfkit');

const ROOT = path.resolve(__dirname, '..');
const TABLES = path.join(ROOT, 'results', 'tables');
const OUT = path.join(ROOT, 'deliverables');
fs.mkdirSync(OUT, { recursive: true });

const C = {
  bg: '101820', panel: '16232C', grid: '31414A', white: 'F2EDE3',
  muted: 'A9B0AE', blue: '67B7C7', yellow: 'E8C56A', red: 'D97564',
  green: '72B69A', purple: 'A995C8', orange: 'D99559',
};
const AREA = { math:'58C4DD', 'astro-ph':'F6C85F', 'cond-mat':'6EE7B7',
  'hep-th':'D58BF0', cs:'71A7FF', 'q-bio':'FF8A65', stat:'FDE68A', econ:'C49A6C',
  physics:'B7C0D1', 'quant-ph':'A78BFA' };

function csv(name) {
  const lines = fs.readFileSync(path.join(TABLES, name), 'utf8').trim().split(/\r?\n/);
  const rows = lines.map(line => {
    const out=[]; let cur=''; let quoted=false;
    for (let i=0;i<line.length;i++) { const ch=line[i];
      if(ch==='"') quoted=!quoted; else if(ch===','&&!quoted){out.push(cur);cur='';} else cur+=ch;
    } out.push(cur); return out;
  });
  return { header: rows[0], rows: rows.slice(1) };
}
function records(name) { const t=csv(name); return t.rows.map(r=>Object.fromEntries(t.header.map((h,i)=>[h,r[i]]))); }

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'Intelligence is Compression';
pptx.subject = 'Teoria da Informação: compressão, entropia cruzada e estrutura do conhecimento';
pptx.title = 'Intelligence is Compression';
pptx.company = 'Trabalho de graduação';
pptx.lang = 'pt-BR';
pptx.theme = { headFontFace:'Georgia', bodyFontFace:'Arial', lang:'pt-BR' };
pptx.defineSlideMaster({
  title:'MASTER', background:{color:C.bg},
  objects:[
    { line:{x:0.55,y:7.13,w:12.2,h:0,line:{color:C.grid,width:0.45}} },
    { line:{x:0.58,y:0.34,w:0.42,h:0,line:{color:C.yellow,width:2.4}} },
    { text:{text:'INTELLIGENCE IS COMPRESSION',options:{x:0.58,y:7.18,w:3.2,h:0.16,fontFace:'Arial',fontSize:6.5,color:C.muted,charSpacing:1.8,margin:0}}},
    { text:{text:'TEORIA DA INFORMAÇÃO',options:{x:10.2,y:7.18,w:2.5,h:0.16,fontFace:'Arial',fontSize:6.5,color:C.muted,charSpacing:1.8,align:'right',margin:0}}},
  ], slideNumber:{x:12.75,y:7.15,color:C.muted,fontSize:7}
});

const ST = pptx.ShapeType;
function slide(title, kicker='') {
  const s=pptx.addSlide('MASTER');
  if(kicker) s.addText(kicker.toUpperCase(),{x:0.62,y:0.38,w:5.5,h:0.22,fontFace:'Arial',fontSize:8.5,bold:true,color:C.blue,charSpacing:2.2,margin:0});
  if(title) s.addText(title,{x:0.58,y:0.68,w:12.1,h:0.62,fontFace:'Georgia',fontSize:25.5,bold:false,color:C.white,margin:0,breakLine:false,fit:'shrink'});
  return s;
}
function txt(s,text,x,y,w,h,size=18,color=C.white,opts={}) { s.addText(text,{x,y,w,h,fontFace:'Arial',fontSize:size,color,margin:0,breakLine:false,fit:'shrink',valign:'mid',...opts}); }
function box(s,x,y,w,h,fill=C.panel,line=C.grid,r=0.04) { s.addShape(r?ST.roundRect:ST.rect,{x,y,w,h,rectRadius:r,fill:{color:fill,transparency:14},line:{color:line,width:0.65},radius:r}); }
function circle(s,x,y,d,fill,line=fill) { s.addShape(ST.ellipse,{x,y,w:d,h:d,fill:{color:fill},line:{color:line,width:1}}); }
function line(s,x,y,w,h,color=C.grid,width=1,dash='solid') { s.addShape(ST.line,{x,y,w,h,line:{color,width,dashType:dash,beginArrowType:'none',endArrowType:'none'}}); }
function note(s, text) { s.addNotes(`Tempo sugerido: ${text}`); }
function formula(s,parts,x,y,w,h,size=23) { s.addText(parts,{x,y,w,h,fontFace:'Arial',fontSize:size,margin:0,align:'center',valign:'mid',fit:'shrink'}); }
function pill(s,text,x,y,w,color=C.blue) { s.addShape(ST.roundRect,{x,y,w,h:0.32,rectRadius:0.16,fill:{color,transparency:82},line:{color,width:0.7}}); txt(s,text,x,y,w,0.32,9,color,{bold:true,align:'center'}); }
function axis(s,x,y,w,h,xlabel='',ylabel='') { line(s,x,y+h,w,0,C.muted,1.2); line(s,x,y,0,h,C.muted,1.2); if(xlabel)txt(s,xlabel,x+w-1.4,y+h+0.18,1.4,0.25,9,C.muted,{align:'right'}); if(ylabel)txt(s,ylabel,x-0.2,y-0.34,1.8,0.25,9,C.muted); }

// 1 — capa
{
 const s=pptx.addSlide(); s.background={color:C.bg};
 for(let i=0;i<70;i++){const x=(i*2.91)%13.1,y=(i*1.73)%7.3,d=0.018+(i%4)*0.008; circle(s,x,y,d,i%7===0?C.yellow:C.grid);}
 txt(s,'Intelligence',0.7,1.08,11.9,0.9,46,C.white,{fontFace:'Georgia',italic:true,charSpacing:0.4});
 txt(s,'is compression',0.7,1.98,11.9,0.9,46,C.blue,{fontFace:'Georgia',charSpacing:0.4});
 txt(s,'Podemos medir proximidade entre ideias\ncontando quantos bits elas compartilham?',0.75,3.28,8.2,1.1,23,C.muted);
 const bits='01101001 01100100 01100101 01101001 01100001';
 txt(s,bits,0.77,5.18,7.5,0.3,11,C.yellow,{charSpacing:1.4});
 txt(s,'TEORIA DA INFORMAÇÃO  /  ESTUDO EMPÍRICO',0.77,6.35,8.5,0.3,9,C.white,{charSpacing:1.6,bold:true});
 note(s,'0:45 — Abra com a pergunta, não com a resposta. Diga que o projeto usa apenas texto, probabilidades e compressores; nenhum embedding ou rede neural.');
}

// 2 — roteiro visual
{
 const s=slide('Uma pergunta, quatro movimentos','mapa da história');
 const items=[['1','SURPRESA','Quanto custa observar um símbolo?'],['2','CÓDIGO','Prever bem é descrever com poucos bits.'],['3','DISTÂNCIA','Textos parecidos reutilizam padrões.'],['4','TESTE','A estrutura encontrada generaliza?']];
 items.forEach((it,i)=>{const x=0.7+i*3.12; box(s,x,1.72,2.72,3.55); circle(s,x+0.18,1.95,0.52,[C.blue,C.yellow,C.green,C.purple][i]); txt(s,it[0],x+0.18,1.95,0.52,0.52,14,C.bg,{bold:true,align:'center'}); txt(s,it[1],x+0.18,2.72,2.25,0.35,15,C.white,{bold:true,charSpacing:1}); txt(s,it[2],x+0.18,3.28,2.25,1.0,16,C.muted); if(i<3){line(s,x+2.74,3.45,0.36,0,C.muted,1.5);}});
 txt(s,'Shannon  →  cross-entropy  →  NCD  →  classificação',0.72,5.9,11.7,0.42,20,C.white,{align:'center'});
 note(s,'0:45 — Antecipe a jornada. Essa tela funciona como contrato com a audiência e evita um sumário textual.');
}

// 3 — surpresa
{
 const s=slide('O que precisa ser verdadeiro para a hipótese sobreviver?','perguntas de pesquisa');
 const qs=[
  ['Q1','ESTRUTURA','Áreas relacionadas devem compartilhar padrões comprimíveis.',C.blue],
  ['Q2','DIREÇÃO','Modelos próprios devem codificar melhor seus textos.',C.yellow],
  ['Q3','GENERALIZAÇÃO','A estrutura deve prever resumos nunca vistos.',C.green]
 ];
 qs.forEach((q,i)=>{const y=1.62+i*1.45;txt(s,q[0],0.78,y,0.72,0.46,18,q[3],{fontFace:'Georgia',bold:true});line(s,1.65,y+0.25,1.0,0,q[3],2.2);txt(s,q[1],2.95,y-0.02,2.2,0.34,11,q[3],{bold:true,charSpacing:1.2});txt(s,q[2],5.05,y-0.05,6.95,0.68,18,C.white,{fontFace:'Georgia'});});
 txt(s,'Uma árvore visualmente plausível não basta.',2.85,6.15,7.8,0.38,15,C.muted,{italic:true,align:'center'});
 note(s,'0:55 — Apresente as três perguntas como critérios de sucesso. Destaque que a classificação fora da amostra é o teste mais forte.');
}

// 4 — surpresa
{
 const s=slide('Informação é surpresa','shannon, 1948');
 const probs=[0.5,0.25,0.125,0.0625];
 probs.forEach((p,i)=>{const x=0.85+i*2.55,h=3.25*p/0.5; box(s,x,5.5-h,1.45,h,[C.blue,C.green,C.yellow,C.red][i],[C.blue,C.green,C.yellow,C.red][i],0.05); txt(s,`${Math.round(p*100)}%`,x,5.58,1.45,0.3,12,C.muted,{align:'center'}); txt(s,`${-Math.log2(p)} bit${i?'s':''}`,x,4.98-h,1.45,0.35,15,C.white,{bold:true,align:'center'});});
 formula(s,[{text:'I(x) = −log₂ p(x)',options:{color:C.white,bold:true}},{text:'   →   raro = caro',options:{color:C.yellow}}],8.7,2.0,3.7,0.8,25);
 txt(s,'dobrar a raridade\nadiciona 1 bit',8.9,3.2,3.25,0.9,21,C.muted,{align:'center'});
 note(s,'1:10 — Explique que um bit resolve uma escolha binária equiprovável. Se a probabilidade cai pela metade, precisamos de uma pergunta binária a mais.');
}

// 4 — entropia
{
 const s=slide('Entropia é o custo médio do melhor código','do símbolo à fonte');
 const ps=[0.5,0.25,0.125,0.125], labels=['A','B','C','D'];
 let x=0.72; ps.forEach((p,i)=>{const w=p*7.5; box(s,x,2.05,w,1.0,[C.blue,C.green,C.yellow,C.purple][i],[C.bg,C.bg,C.bg,C.bg][i],0.02); txt(s,`${labels[i]}  ${Math.round(p*100)}%`,x,2.05,w,1,16,C.bg,{bold:true,align:'center'}); x+=w;});
 formula(s,[{text:'H(P) = ',options:{color:C.white}},{text:'Σ p(x)',options:{color:C.blue,bold:true}},{text:' · [−log₂ p(x)]',options:{color:C.yellow,bold:true}}],8.65,1.95,3.85,0.9,23);
 const tree=[['A','0'],['B','10'],['C','110'],['D','111']];
 tree.forEach((v,i)=>{const yy=3.65+i*0.55; txt(s,v[0],1.0,yy,0.5,0.35,16,[C.blue,C.green,C.yellow,C.purple][i],{bold:true}); txt(s,v[1],1.75,yy,1.2,0.35,16,C.white,{bold:true,charSpacing:4}); const dots=v[1].length; for(let j=0;j<dots;j++)circle(s,3.4+j*0.38,yy+0.08,0.16,v[1][j]==='0'?C.blue:C.yellow);});
 txt(s,'símbolos frequentes recebem códigos curtos',6.1,4.28,5.7,0.55,21,C.white,{align:'center'});
 txt(s,'A compressão aproxima o limite imposto pela entropia.',6.1,5.02,5.7,0.45,15,C.muted,{align:'center'});
 note(s,'1:20 — Faça a ponte central: um bom compressor é um bom preditor. O comprimento médio do código não pode ficar abaixo de H(P) de forma geral.');
}

// 5 — cross entropy
{
 const s=slide('Cross-entropy mede o preço de acreditar no modelo errado','a ideia do 3blue1brown');
 const vals=[['H(P)','2,54',C.blue],['+ KL(P‖Q)','0,54',C.yellow],['H(P,Q)','3,08',C.white]];
 vals.forEach((v,i)=>{const x=0.8+i*4.1; box(s,x,1.9,3.55,2.15); txt(s,v[0],x+0.2,2.18,3.15,0.35,17,v[2],{bold:true,align:'center'}); txt(s,v[1],x+0.2,2.72,3.15,0.66,34,v[2],{bold:true,align:'center'}); txt(s,'bits / caractere',x+0.2,3.43,3.15,0.3,10,C.muted,{align:'center'}); if(i<2)txt(s,i===0?'+':'=',x+3.62,2.75,0.45,0.5,25,C.muted,{bold:true,align:'center'});});
 formula(s,[{text:'H(P,Q)',options:{color:C.white,bold:true}},{text:' = H(P) + ',options:{color:C.muted}},{text:'KL(P‖Q)',options:{color:C.yellow,bold:true}}],2.55,4.75,8.1,0.62,27);
 txt(s,'exemplo real: texto de matemática codificado pelo modelo de astro-ph',2.2,5.55,8.9,0.4,13,C.muted,{align:'center'});
 note(s,'1:20 — P é a fonte real; Q é nossa crença. A entropia cruzada é o número de bits que de fato pagamos. A diferença para o custo próprio é a divergência KL.');
}

// 6 — método
{
 const s=slide('O experimento transforma texto em comprimento de código','pipeline reproduzível');
 const items=[['arXiv','10 áreas\nresumos'],['limpeza','mesma cota\nde bytes'],['modelos','gzip · bz2 · lzma\nn-gramas'],['medidas','bpc · NCD\ncross-entropy'],['testes','mapas · árvores\nclassificação']];
 items.forEach((v,i)=>{const x=0.55+i*2.55; circle(s,x+0.62,1.72,1.05,[C.blue,C.green,C.yellow,C.purple,C.red][i]); txt(s,String(i+1).padStart(2,'0'),x+0.62,1.72,1.05,1.05,18,C.bg,{bold:true,align:'center'}); txt(s,v[0].toUpperCase(),x,3.02,2.25,0.35,13,C.white,{bold:true,align:'center',charSpacing:1}); txt(s,v[1],x,3.48,2.25,0.8,14,C.muted,{align:'center'}); if(i<4)line(s,x+1.72,2.24,0.82,0,C.grid,2);});
 pill(s,'seed = 42',1.35,5.42,1.7,C.blue); pill(s,'sem embeddings',3.33,5.42,2.1,C.green); pill(s,'treino ≠ teste',5.72,5.42,2.0,C.yellow); pill(s,'CSV antes do gráfico',8.0,5.42,2.75,C.purple);
 note(s,'1:15 — Explique a separação treino/teste, o balanceamento por bytes e que cada figura nasce de um CSV. A análise foi feita sobre corpus rápido real do arXiv.');
}

{
 const s=slide('Uma escada de evidências, não uma única figura','validade científica');
 const levels=[['1','SANIDADE','línguas conhecidas'],['2','DESCRIÇÃO','bpc, matrizes e mapas'],['3','EXPLICAÇÃO','palavras que carregam bits'],['4','PREDIÇÃO','artigos fora da amostra'],['5','INCERTEZA','bootstrap e estabilidade']];
 levels.forEach((v,i)=>{const x=0.72+i*2.48,y=5.55-i*0.78;box(s,x,y,2.05,0.62,C.panel,[C.grid,C.grid,C.grid,C.grid,C.grid][i],0.02);txt(s,v[0],x+0.12,y,0.35,0.62,12,[C.blue,C.yellow,C.purple,C.green,C.red][i],{bold:true,align:'center'});txt(s,v[1],x+0.48,y+0.03,1.42,0.24,9,C.white,{bold:true,charSpacing:0.5});txt(s,v[2],x+0.48,y+0.29,1.42,0.24,8,C.muted);if(i<4)line(s,x+2.05,y+0.31,0.43,-0.78,C.grid,1.2);});
 txt(s,'Quanto mais alto, mais difícil é explicar o resultado por acaso visual.',2.0,1.7,9.2,0.5,19,C.white,{fontFace:'Georgia',italic:true,align:'center'});
 note(s,'0:55 — Explique que o projeto combina controle positivo, descrição, explicabilidade, predição e incerteza. Isso organiza a seção de resultados.');
}

// 8 — compressibilidade
{
 const s=slide('Regularidade aparece como menos bits por caractere','resultado 1');
 const data=records('exp1_compressibility.csv').filter(r=>r.kind==='compressor'&&r.method==='lzma').map(r=>({a:r.area,v:+r.value})).sort((a,b)=>a.v-b.v);
 const min=2.55,max=3.0; axis(s,3.5,1.72,8.55,4.35,'bits / caractere');
 data.forEach((d,i)=>{const y=1.88+i*0.4,w=(d.v-min)/(max-min)*7.7; txt(s,d.a,0.75,y,2.35,0.28,12,AREA[d.a],{bold:true,align:'right'}); s.addShape(ST.roundRect,{x:3.5,y:y+0.03,w,h:0.2,rectRadius:0.1,fill:{color:AREA[d.a]},line:{color:AREA[d.a]}}); txt(s,d.v.toFixed(2),3.58+w,y-0.01,0.55,0.3,10,C.white,{bold:true});});
 txt(s,'menor custo = mais padrões reutilizáveis',7.25,6.28,4.8,0.32,13,C.muted,{align:'right'});
 note(s,'1:10 — Não interprete o ranking como “área mais inteligente”. Ele mede regularidade textual no corpus: estilo, fórmulas, vocabulário e repetição.');
}

// 8 — NCD
{
 const s=slide('NCD mede o quanto dois textos se ajudam a comprimir','de benedetto ao arxiv');
 formula(s,[{text:'NCD(x,y) = ',options:{color:C.white}},{text:'C(xy) − min{C(x),C(y)}',options:{color:C.yellow,bold:true}},{text:'\nmax{C(x),C(y)}',options:{color:C.blue,bold:true}}],0.75,1.62,5.45,1.5,22);
 line(s,2.95,2.56,2.9,0,C.muted,1);
 const pairs=[['cond-mat','physics',0.859,C.green,'mais próximo'],['math','astro-ph',0.898,C.red,'mais distante']];
 pairs.forEach((p,i)=>{const y=1.72+i*2.15; box(s,7.05,y,5.35,1.62); circle(s,7.38,y+0.45,0.46,AREA[p[0]]); circle(s,7.68,y+0.45,0.46,AREA[p[1]]); txt(s,`${p[0]}  ↔  ${p[1]}`,8.32,y+0.22,3.65,0.38,16,C.white,{bold:true}); txt(s,`NCD = ${p[2].toFixed(3)}`,8.32,y+0.7,2.0,0.34,15,p[3],{bold:true}); pill(s,p[4],10.35,y+0.72,1.55,p[3]);});
 txt(s,'0 = idênticos',0.9,4.45,2.2,0.35,15,C.green,{bold:true}); line(s,2.9,4.62,5.2,0,C.grid,7); circle(s,2.82,4.51,0.22,C.green); circle(s,7.98,4.51,0.22,C.red); txt(s,'1 = sem estrutura compartilhada',8.25,4.45,3.5,0.35,15,C.red,{bold:true});
 note(s,'1:30 — Mostre numerador e denominador visualmente. NCD aproxima uma distância baseada em complexidade de Kolmogorov usando um compressor real. Cite Benedetto et al. como controle conceitual.');
}

// 9 — mapa de distâncias em rede
{
 const s=slide('A matriz de distâncias vira um mapa de afinidades','resultado 2');
 const t=csv('exp2_ncd_lzma.csv'); const labels=t.header.slice(1); const vals=t.rows.map(r=>r.slice(1).map(Number));
 const pos={math:[1.4,2.1], 'hep-th':[3.4,1.8], 'quant-ph':[5.25,2.35], 'cond-mat':[6.85,3.3], physics:[8.8,3.25], 'astro-ph':[10.85,2.15], cs:[3.3,5.1],stat:[5.1,4.85],econ:[6.75,5.45],'q-bio':[9.15,5.08]};
 const edges=[]; for(let i=0;i<labels.length;i++)for(let j=i+1;j<labels.length;j++)edges.push([labels[i],labels[j],vals[i][j]]); edges.sort((a,b)=>a[2]-b[2]).slice(0,14).forEach(e=>{const a=pos[e[0]],b=pos[e[1]],strength=(0.90-e[2])/0.045; line(s,a[0]+0.21,a[1]+0.21,b[0]-a[0],b[1]-a[1],C.blue,0.7+strength*3);});
 labels.forEach(a=>{const p=pos[a]; circle(s,p[0],p[1],0.52,AREA[a]); txt(s,a,p[0]-0.28,p[1]+0.62,1.08,0.3,11,C.white,{bold:true,align:'center'});});
 txt(s,'arestas = 14 menores NCDs',9.5,6.38,2.75,0.26,10,C.muted,{align:'right'});
 note(s,'1:15 — Este não é um mapa geográfico nem semântico absoluto. As arestas mostram apenas os 14 pares mais próximos; espessura maior significa mais regularidade compartilhada.');
}

// 10 — palavras
{
 const s=slide('Podemos localizar onde estão os bits de diferença','explicabilidade');
 const data=records('exp5_word_contributions.csv').filter(r=>r.pair_type==='distante').sort((a,b)=>+a.rank-+b.rank).slice(0,10);
 const max=Math.max(...data.map(d=>+d.contribution));
 data.forEach((d,i)=>{const col=i<5?0:1,idx=i%5,x=0.8+col*6.25,y=1.63+idx*0.91,w=(+d.contribution/max)*3.55; txt(s,d.word,x,y,1.75,0.3,13,C.white,{bold:true,align:'right'}); s.addShape(ST.roundRect,{x:x+1.95,y:y+0.03,w,h:0.24,rectRadius:0.12,fill:{color:col?C.purple:C.blue},line:{color:col?C.purple:C.blue}}); txt(s,(+d.contribution).toFixed(3),x+2.05+w,y,0.75,0.3,10,C.muted);});
 txt(s,'contribuição  p(w) · log₂[p(w)/q(w)]',0.82,6.35,5.0,0.28,11,C.yellow,{bold:true});
 note(s,'1:05 — A divergência não é uma caixa-preta: ela se decompõe por palavra. Vocabulário especializado explica parte importante da separação entre áreas.');
}

// 11 — assimetria
{
 const s=slide('Proximidade depende da direção da pergunta','kl não é uma distância métrica');
 const asym=records('exp4_asymmetry.csv').slice(0,4);
 asym.forEach((d,i)=>{const y=1.65+i*1.08; txt(s,d.area_a,0.75,y+0.15,1.45,0.35,14,AREA[d.area_a],{bold:true,align:'right'}); txt(s,d.area_b,11.15,y+0.15,1.45,0.35,14,AREA[d.area_b],{bold:true}); const ab=+d.kl_a_b,ba=+d.kl_b_a; line(s,2.55,y+0.14,8.25,0,C.orange,1+ab*9); txt(s,ab.toFixed(2),5.55,y-0.14,1,0.28,10,C.orange,{align:'center',bold:true}); line(s,10.8,y+0.58,-8.25,0,C.blue,1+ba*9); txt(s,ba.toFixed(2),6.65,y+0.48,1,0.28,10,C.blue,{align:'center',bold:true});});
 pill(s,'A → B',4.28,6.15,1.55,C.orange); pill(s,'B → A',7.5,6.15,1.55,C.blue);
 note(s,'1:00 — KL(P||Q) e KL(Q||P) respondem perguntas diferentes. Um vocabulário amplo pode explicar um estreito melhor do que o contrário.');
}

// 12 — classificação
{
 const s=slide('A árvore é bonita. Mas ela prevê textos novos?','teste fora da amostra');
 const data=records('exp6_metrics.csv').sort((a,b)=>+a.accuracy-+b.accuracy); const max=.75;
 data.forEach((d,i)=>{const y=1.6+i*1.05,w=+d.accuracy/max*8.4,color=d.method==='n-grama'?C.green:d.method==='TF-IDF'?C.blue:C.purple; txt(s,d.method,0.75,y,1.95,0.34,14,C.white,{bold:true,align:'right'}); s.addShape(ST.roundRect,{x:3.0,y:y+0.02,w,h:0.34,rectRadius:0.17,fill:{color},line:{color}}); txt(s,`${(+d.accuracy*100).toFixed(1)}%`,3.18+w,y-0.01,0.8,0.38,13,color,{bold:true});});
 box(s,8.65,5.55,3.55,0.65,C.panel,C.green); txt(s,'n-grama vence: 67,1%',8.65,5.55,3.55,0.65,16,C.green,{bold:true,align:'center'});
 txt(s,'Resultado honesto: compressão encontra estrutura,\nmas o compressor escolhido limita o sinal.',0.85,5.62,7.25,0.8,18,C.muted);
 note(s,'1:25 — Este é o teste decisivo. O n-grama supera TF-IDF; NCD k=5 fica em 38,2%. Não venda NCD como vencedor: ele é uma lente estrutural, não o melhor classificador neste corpus.');
}

// 13 — incerteza
{
 const s=slide('Toda acurácia vem com incerteza','robustez por bootstrap');
 const data=records('exp8_accuracy_ci.csv'); const x0=3.15,scale=10.2;
 [0,.25,.5,.75,1].forEach(v=>{const x=x0+v*scale;line(s,x,1.55,0,4.35,C.grid,0.7,'dash');txt(s,`${v*100}%`,x-0.3,6.03,0.6,0.25,9,C.muted,{align:'center'});});
 data.forEach((d,i)=>{const y=2.0+i*0.93,lo=+d.ci_low,hi=+d.ci_high,v=+d.accuracy,color=d.method==='n-grama'?C.green:d.method==='TF-IDF'?C.blue:C.purple;txt(s,d.method,0.68,y-0.11,2.0,0.32,13,C.white,{bold:true,align:'right'});line(s,x0+lo*scale,y,(hi-lo)*scale,0,color,5);circle(s,x0+v*scale-0.11,y-0.11,0.22,C.white,color);});
 txt(s,'intervalos largos = corpus de teste ainda pequeno',7.4,6.37,4.9,0.26,11,C.muted,{align:'right'});
 note(s,'1:00 — Os intervalos lembram que diferenças pequenas não devem ser superinterpretadas. Robustez é parte do resultado, não um apêndice.');
}

// 14 — limites
{
 const s=slide('O compressor também impõe sua própria visão de mundo','limitações');
 const items=[['JANELA','gzip esquece padrões\nalém de 32 KB',C.yellow],['ORDEM','C(xy) pode diferir\nde C(yx)',C.red],['VOCABULÁRIO','proximidade lexical\n≠ proximidade conceitual',C.blue],['TAXONOMIA','rótulos do arXiv\nnão são verdade absoluta',C.purple]];
 items.forEach((it,i)=>{const x=0.72+(i%2)*6.2,y=1.62+Math.floor(i/2)*2.3;box(s,x,y,5.72,1.75);circle(s,x+0.32,y+0.34,0.62,it[2]);txt(s,String(i+1),x+0.32,y+0.34,0.62,0.62,15,C.bg,{bold:true,align:'center'});txt(s,it[0],x+1.18,y+0.27,3.9,0.35,14,it[2],{bold:true,charSpacing:1});txt(s,it[1],x+1.18,y+0.78,4.05,0.68,16,C.white);});
 txt(s,'Um compressor prático não é o compressor universal ideal.',1.65,6.34,10.0,0.35,17,C.muted,{italic:true,align:'center'});
 note(s,'1:20 — Conecte cada limitação a uma decisão experimental. O mapa é uma propriedade conjunta dos textos, do pré-processamento e do compressor.');
}

// 15 — conclusão
{
 const s=slide('O que os bits nos permitiram enxergar?','síntese');
 const claims=[['01','PREVER','compressão operacionaliza\na noção de regularidade'],['02','COMPARAR','NCD e cross-entropy\ncriam geometrias semânticas'],['03','TESTAR','classificação separa\nvisual atraente de evidência']];
 claims.forEach((c,i)=>{const x=0.72+i*4.16;box(s,x,1.7,3.72,3.38);txt(s,c[0],x+0.25,1.95,0.7,0.55,25,[C.blue,C.yellow,C.green][i],{bold:true});txt(s,c[1],x+0.25,2.8,3.1,0.35,15,C.white,{bold:true,charSpacing:1});txt(s,c[2],x+0.25,3.4,3.15,0.95,17,C.muted);});
 txt(s,'Inteligência, aqui, não é “comprimir tudo”.',1.0,5.73,11.3,0.4,21,C.white,{bold:true,align:'center'});
 txt(s,'É descobrir uma descrição curta que ainda generaliza.',1.0,6.18,11.3,0.4,21,C.blue,{bold:true,align:'center'});
 note(s,'1:10 — Retome a pergunta inicial. A contribuição é metodológica: usar custo de descrição como instrumento mensurável e validar se a estrutura encontrada generaliza.');
}

// 16 — referências
{
 const s=slide('Referências essenciais','para continuar');
 const refs=[['SHANNON · 1948','A Mathematical Theory of Communication','fundação de entropia, canal e codificação'],['BENEDETTO ET AL. · 2002','Language Trees and Zipping','distâncias entre textos via compressores'],['3BLUE1BROWN','But what is cross-entropy?','intuição visual para surpresa e modelo errado']];
 refs.forEach((r,i)=>{const y=1.55+i*1.48;box(s,0.78,y,11.78,1.08);txt(s,r[0],1.06,y+0.17,2.65,0.28,11,[C.blue,C.yellow,C.green][i],{bold:true,charSpacing:0.7});txt(s,r[1],3.65,y+0.12,5.3,0.36,17,C.white,{bold:true});txt(s,r[2],3.65,y+0.56,6.9,0.28,11,C.muted);});
 txt(s,'Perguntas?',0.8,6.25,11.8,0.42,26,C.white,{bold:true,align:'center'});
 note(s,'0:25 — Encerre e abra para perguntas. Tempo total planejado: aproximadamente 19min45s.');
}

function buildReport() {
 const out=path.join(OUT,'relatorio_intelligence_is_compression.pdf');
 const doc=new PDFDocument({size:'A4',bufferPages:true,margins:{top:58,bottom:58,left:58,right:58},info:{Title:'Aula completa — Intelligence is Compression',Author:'Projeto de Teoria da Informação'}});
 doc.pipe(fs.createWriteStream(out));
 const source=fs.readFileSync(path.join(ROOT,'docs','aula_completa.md'),'utf8');
 const blocks=source.split(/\n\s*\n/).map(x=>x.trim()).filter(Boolean);

 doc.rect(0,0,595,842).fill('#101820');
 doc.fillColor('#E8C56A').font('Helvetica-Bold').fontSize(9).text('TEORIA DA INFORMAÇÃO',{characterSpacing:2});
 doc.fillColor('#F2EDE3').font('Times-Italic').fontSize(38).text('Intelligence',{continued:false});
 doc.fillColor('#67B7C7').font('Times-Roman').fontSize(38).text('is compression');
 doc.moveDown(1.2).fillColor('#A9B0AE').font('Helvetica').fontSize(14).text('Aula completa para compreender, apresentar e defender o projeto',{width:430});
 doc.fillColor('#F2EDE3').font('Helvetica').fontSize(9).text('MATERIAL DE PREPARAÇÃO  /  EDIÇÃO GERADA A PARTIR DO REPOSITÓRIO',58,742,{characterSpacing:1.1});
 doc.addPage();

 for(const block of blocks.slice(2)) {
  if(block.startsWith('## ')) {
   if(doc.y>690) doc.addPage();
   doc.moveDown(.7).fillColor('#67B7C7').font('Helvetica-Bold').fontSize(8).text('CAPÍTULO',{characterSpacing:1.8});
   doc.moveDown(.25).fillColor('#101820').font('Times-Roman').fontSize(21).text(block.slice(3),{lineGap:1});
   doc.moveDown(.45).strokeColor('#D8D2C7').lineWidth(.7).moveTo(58,doc.y).lineTo(537,doc.y).stroke();doc.moveDown(.65);
  } else if(block.startsWith('# ')) {
   continue;
  } else {
   const isFormula=/^(?:I\(|H\(|KL\(|NCD\()/.test(block);
   if(isFormula) {
    doc.moveDown(.2).fillColor('#101820').font('Times-Italic').fontSize(13.5).text(block,{align:'center',lineGap:4});doc.moveDown(.55);
   } else {
    doc.fillColor('#26343A').font('Helvetica').fontSize(10.2).text(block,{align:'justify',lineGap:3.2});doc.moveDown(.62);
   }
  }
 }
 const range=doc.bufferedPageRange();
 for(let i=0;i<range.count;i++) {
  doc.switchToPage(i);
  if(i>0) {
   doc.strokeColor('#D8D2C7').lineWidth(.45).moveTo(58,805).lineTo(537,805).stroke();
   doc.fillColor('#7A8585').font('Helvetica').fontSize(7.5).text('INTELLIGENCE IS COMPRESSION',58,812,{width:250,lineBreak:false});
   doc.text(`${i+1} / ${range.count}`,437,812,{width:100,align:'right',lineBreak:false});
  }
 }
 doc.end(); return out;
}

(async()=>{
 const pptxPath=path.join(OUT,'intelligence_is_compression_20min.pptx');
 function auditColors(value, where='pptx', seen=new WeakSet()) {
  if (!value || typeof value !== 'object' || seen.has(value)) return;
  seen.add(value);
  for (const [key, child] of Object.entries(value)) {
   if (key === 'color' && child != null && typeof child !== 'string') console.error('Cor inválida:', where, child);
   if (child && typeof child === 'object') auditColors(child, `${where}.${key}`, seen);
  }
 }
 auditColors(pptx);
 await pptx.writeFile({fileName:pptxPath});
 const report=buildReport();
 console.log(`PPTX: ${pptxPath}`);
 console.log(`PDF:  ${report}`);
})();
