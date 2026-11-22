from diagram_helpers import *
SLIDES={}; CODES={}
def S(n,title,left,right,recall):
 SLIDES[n]=dict(title=title,section='VIII · STABILITÀ E INTERPRETAZIONE' if n<104 else 'IX · UN’ANALISI COMPLETA',left=left,right=right,recall=recall)
def C(n,name,src,title):
 key=f'{n:03}_{name}.R';CODES[key]=src.strip()+'\n';return rf'\PCode{{R · {title}}}{{{key}}}'
def stability_plot():
 rr=table('stability.csv');out,X,Y=axes(0,31,100,410,xlabel='Avvio singolo',ylabel='WSS',xticks=[1,10,20,30],yticks=[130,250,370],h=4.6)
 line(out,X,Y,[(0,129.4978),(31,129.4978)],'Classical','dashed')
 for r in rr:
  x=float(r['ripetizione']);y=float(r['WSS']);c='GeoB' if y>200 else 'GeoA'
  out.append(rf'\fill[{c}]({X(x):.4f},{Y(y):.4f}) circle(2pt);')
 out.append(r'\end{tikzpicture}');return '\n'.join(out)
def perturbation_plot():
 rr=table('perturbations_mean.csv');out,X,Y=axes(0,.85,.9,1.005,xlabel=r'Ampiezza $\sigma$ nelle unità di $Z$',ylabel='Accordo fra coppie',xticks=[0,.2,.4,.6,.8],yticks=[.9,.95,1],h=4.65)
 out[-1]=r'\node[pNote,rotate=90] at(-.2,2.45){Accordo fra coppie};'
 line(out,X,Y,[(float(r['sd']),float(r['accordo'])) for r in rr])
 for r in rr:out.append(rf'\fill[GeoA]({X(r["sd"]):.4f},{Y(r["accordo"]):.4f}) circle(2.5pt);')
 out.append(r'\end{tikzpicture}');return '\n'.join(out)
def heat_co():
 rr=table('co_membership.csv');idx=[0,5,11,30,35,41,60,65,71];body=''
 for a,i in enumerate(idx):
  for b,j in enumerate(idx):
   val=float(rr[i][f'X{j+1}']);x=2.65+b*.42;y=4.3-a*.42
   body+=rf'\fill[GeoA!{int(100*val)}!white]({x},{y}) rectangle({x+.39},{y+.39});'
 body+=r'\node[pNote,text width=8.2cm] at(4.6,.25){Estratto di 9 campioni: bianco = 0, petrolio = 1.\ I valori sono frequenze condizionate alla presenza della coppia.};'
 return tk(body,h=4.9)
def profiles():
 rr=table('profiles_original.csv');heads=[('SiO2',r'SiO$_2$ (\%)',1),('densita',r'Densità (g/cm$^3$)',2),('grana_mm','Grana (mm)',2)];body=''
 for j,(_,lab,_) in enumerate(heads):body+=rf'\node[pNote,text width=2.1cm] at({3.0+j*2.35},4.1){{{lab}}};'
 for i,r in enumerate(rr):
  y=3.05-i*.9;c=COLORS[i]
  body+=rf'\node[pLabel,text={c}] at(.85,{y}){{Gruppo {r["cluster"]}}};'
  for j,(v,lab,dec) in enumerate(heads):body+=rf'\fill[{c}!12]({2.05+j*2.35},{y-.3}) rectangle({3.95+j*2.35},{y+.3});\node[pLabel] at({3+j*2.35},{y}){{$ {it(r[v],dec)} $}};'
 body+=r'\node[pNote] at(4.7,.35){Medie nelle unità originali; trenta campioni per gruppo};'
 return tk(body,h=4.65)
def dist_plot():
 rr=table('assignments.csv');vals=sorted(float(r['distanza2']) for r in rr)
 def quantile(xs,q):
  a=(len(xs)-1)*q;i=int(a);return xs[i]+(a-i)*(xs[min(i+1,len(xs)-1)]-xs[i])
 threshold=quantile(vals,.95)
 out,X,Y=axes(0,91,0,math.ceil(max(vals)),xlabel='Campioni ordinati per distanza',ylabel=r'$\|\mathbf z_i-\boldsymbol\mu_{g(i)}\|^2$',xticks=[1,30,60,90],yticks=[0,2,4,6],h=4.7)
 line(out,X,Y,[(0,threshold),(91,threshold)],'GeoB','dashed')
 for i,v in enumerate(vals):out.append(rf'\fill[{"GeoB" if v>threshold else "GeoA"}]({X(i+1):.4f},{Y(v):.4f}) circle(1.6pt);')
 out.append(r'\end{tikzpicture}');return '\n'.join(out)
def cluster_split():
 a=table('assignments.csv');b=table('assignments_k4.csv');body='';counts={}
 for x,y in zip(a,b):counts[(int(x['kmeans']),int(y['cluster']))]=counts.get((int(x['kmeans']),int(y['cluster'])),0)+1
 y3={1:3.8,2:2.35,3:.9};y4={4:3.8,1:2.8,2:1.8,3:.75}
 for (g,h),n in counts.items():
  body+=rf'\draw[{COLORS[g-1]},opacity=.45,line width={.8+n*.075}pt](2.3,{y3[g]})--(6.9,{y4[h]});\node[pNote,fill=Paper,inner sep=1pt] at(4.6,{(y3[g]+y4[h])/2}){{{n}}};'
 for g,y in y3.items():body+=rf'\node[pFlow,draw={COLORS[g-1]},text width=1.4cm,minimum height=.55cm] at(1.55,{y}){{$k=3$: {g}}};'
 for g,y in y4.items():body+=rf'\node[pFlow,text width=1.4cm,minimum height=.55cm] at(7.65,{y}){{$k=4$: {g}}};'
 return tk(body,h=4.8)

S(94,'Quale stabilità vogliamo verificare?',tk(r'''
\node[pFlow,text width=3.7cm] at(2.25,3.6){Inizializzazione\\stessi dati, altri avvii};
\node[pFlow,text width=3.7cm] at(7.05,3.6){Misurazione\\valori perturbati};
\node[pFlow,text width=3.7cm] at(2.25,1.35){Campionamento\\altre righe disponibili};
\node[pFlow,text width=3.7cm] at(7.05,1.35){Specificazione\\altre variabili o scale};
''',h=4.7)+r'\PBody{Ripetere l’algoritmo sugli stessi dati esamina una fonte di variabilità. Modificare dati o definizione della distanza ne esamina altre.}',r'''
\PLabel{Dichiarare che cosa cambia}
\PBody{Ogni confronto mantiene fisse alcune scelte e ne modifica altre. Il resoconto deve rendere riconoscibile questa distinzione.}
\vspace{4mm}
\PInfo{Una partizione stabile rispetto agli avvii può essere sensibile alla scelta delle variabili o ai nuovi campioni.}
\vspace{3mm}
\PBody{Stabilità numerica, ripetibilità delle misure e plausibilità geologica richiedono verifiche differenti.}
''','La stabilità ha significato rispetto a una perturbazione specificata.')

S(95,'Alcuni avvii si fermano a partizioni peggiori',stability_plot()+r'\PBody{Trenta avvii singoli sulle stesse rocce producono anche soluzioni con WSS molto più alta. La linea tratteggiata indica la soluzione di riferimento.}',C(95,'avvii','''
set.seed(818)
W_avvii <- replicate(30, {
  m <- kmeans(Z, 3, nstart = 1,
              iter.max = 100)
  m$tot.withinss
})
range(W_avvii)
''','ripetere avvii singoli')+r'\PInfo{Gli avvii multipli riducono il rischio di una soluzione sfavorevole. Il minimo trovato rimane un risultato dell’algoritmo.}','Ripetere la ricerca aiuta a distinguere la struttura dei dati da una inizializzazione sfavorevole.')

S(96,'Perturbare i valori misura una sensibilità',perturbation_plot()+r'\PSmall{Per ogni ampiezza: 20 perturbazioni gaussiane, $k=3$, 50 avvii. Il grafico riporta l’accordo medio fra coppie con la partizione di riferimento.}',r'\[Z^*=Z+E,\qquad E_{ij}\sim N(0,\sigma^2).\]'+C(96,'perturbazione','''
# Una perturbazione nelle unità di Z.
set.seed(819)
Zp <- Z + matrix(rnorm(length(Z),
  sd = 0.4), nrow(Z))
kp <- kmeans(Zp, 3, nstart = 50,
             iter.max = 100)
accordo_coppie(km$cluster, kp$cluster)
''','costruire una prova')+r'\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m08-robustezza}{Esperimento · sensibilità}'+r'\PSmall{È una prova convenzionale; il rumore non è stimato da errori strumentali reali.}','Il risultato dipende dall’ampiezza e dal modello della perturbazione adottata.')

S(97,'Confrontare appartenenze, non numeri di gruppo',tk(r'''
\node[pLabel] at(1.1,4.1){Campione};\node[pLabel] at(4.4,4.1){Partizione A};\node[pLabel] at(7.3,4.1){Partizione B};
\foreach \i/\a/\b in {1/1/3,2/1/3,3/2/1,4/2/1,5/3/2,6/3/2}{\node[pNote] at(1.1,3.9-.48*\i){\i};\node[pNote] at(4.4,3.9-.48*\i){\a};\node[pNote] at(7.3,3.9-.48*\i){\b};}
\node[pNote,text width=8.5cm] at(4.6,.25){Stesse coppie unite e separate, etichette numeriche diverse};
''',h=4.6)+r'\[A_{ih}=\mathbf 1\{g(i)=g(h)\}.\]',C(97,'coappartenenza','''
a <- c(1, 1, 2, 2, 3, 3)
b <- c(3, 3, 1, 1, 2, 2)
# I numeri dei gruppi sono arbitrari.
mean(a == b)
accordo_coppie(a, b)  # vale 1
indice_rand_corretto(a, b)
''','ignorare i nomi dei gruppi')+r'\PInfo{L’accordo fra coppie conta unioni e separazioni concordi. L’indice di Rand corretto considera anche l’accordo atteso date le dimensioni dei gruppi.}','Una permutazione delle etichette conserva la partizione.')

S(98,'I sottocampioni cambiano le righe osservate',heat_co()+r'\PSmall{Quaranta estrazioni di 72 righe su 90, senza reinserimento. Le scale di $Z$ restano fisse: si esamina la variazione delle righe, non la ristima delle scale.}',r'\[\widehat P_{ih}=\frac{\#\{\text{presenti e uniti}\}}{\#\{\text{entrambi presenti}\}}.\]'+C(98,'sottocampione','''
# Una delle quaranta estrazioni.
set.seed(820)
idx <- sort(sample(1:nrow(Z), 72))
ks <- kmeans(Z[idx, ], 3, nstart = 30,
             iter.max = 100)
outer(ks$cluster, ks$cluster, "==")[1:4, 1:4]
''','estrarre le righe')+r'\PSmall{Una coppia mai osservata avrebbe frequenza non definita. Questa frequenza non è una probabilità di verità geologica.}','La frequenza di coappartenenza va riferita alle occasioni in cui entrambi i campioni erano presenti.')

S(99,'Cambiare le variabili cambia la domanda',tk(r'''
\node[pFlow,text width=3.6cm] at(2.25,3.2){Otto proprietà\\chimica, fisica, indici};
\node[pFlow,text width=3.6cm] at(7.05,3.2){Quattro ossidi\\concentrazioni standardizzate};
\draw[pEdge](2.25,2.45)--(4.65,1.35);\draw[pEdge](7.05,2.45)--(4.65,1.35);
\node[pLabel,text width=8cm] at(4.65,.6){In questo dataset: accordo fra coppie = 1};
''',h=4.6)+r'\PBody{Su questi dati artificiali, i due insiemi di variabili producono la stessa partizione. È un risultato da registrare, senza supporlo valido per altri campioni.}',C(99,'variabili','''
chim <- c("SiO2", "CaO", "MgO", "FeO")
set.seed(819)
kc <- kmeans(scale(d[chim]), 3,
              nstart = 50)
accordo_coppie(km$cluster, kc$cluster)
''','confrontare due selezioni')+r'\PInfo{Qui si confrontano concentrazioni standardizzate. La geometria dei log-rapporti costituisce un’altra scelta di analisi.}','Una verifica di sensibilità deve riportare anche quando il risultato rimane invariato.')

S(100,'Un campione distante richiede un controllo',dist_plot()+r'\PBody{Le distanze dal centro del proprio gruppo ordinano i campioni per scostamento interno. La linea segna il 95° percentile osservato, scelto come soglia esplorativa.}',C(100,'campioni_distanti','''
delta <- Z - km$centers[km$cluster, ]
d2_centro <- rowSums(delta^2)
soglia <- quantile(d2_centro, .95)
segnala <- d2_centro > soglia
d[segnala, c("id", v)]
''','identificare righe da esaminare')+r'\PInfo{La soglia non è un test probabilistico e non giustifica una cancellazione automatica. Occorre controllare misure, provenienza e sensibilità della partizione.}','La distanza segnala uno scostamento; la spiegazione richiede il contesto del campione.')

S(101,'Descrivere i gruppi nelle unità originali',profiles()+r'\PBody{Le medie standardizzate facilitano il confronto dei profili. Tornare alle unità originali permette di discutere l’entità delle differenze.}',C(101,'profili_originali','''
profili <- aggregate(d[v],
  list(gruppo = km$cluster), mean)
profili[, c("gruppo", "SiO2",
             "densita", "grana_mm")]
# Esaminare anche dispersione e casi.
''','riassumere le proprietà')+r'\PInfo{La media non descrive la dispersione interna. Due gruppi possono avere profili simili e variabilità differente.}','L’interpretazione deve tornare alle proprietà misurate e alla variabilità dentro ciascun gruppo.')

S(102,'Confrontare con informazioni esterne',tk(r'''
\node[pFlow,text width=3.5cm] at(2.2,3.35){Variabili selezionate\\costruiscono i gruppi};
\node[pFlow,text width=3.5cm] at(7,3.35){Informazioni esterne\\mettono alla prova l’interpretazione};
\draw[pEdge](2.2,2.5)--(4.6,1.45);\draw[pEdge](7,2.5)--(4.6,1.45);
\node[pLabel,text width=8cm] at(4.6,.7){Indipendenza del confronto e qualità del campionamento};
''',h=4.6)+r'\PBody{Nel simulatore conosciamo le etichette che hanno generato i dati. Recuperarle verifica il comportamento sul caso costruito.}',C(102,'generatore','''
# L'etichetta non e stata usata nella stima.
generatore <- d$litologia_generatrice
table(gruppo = km$cluster, generatore)
indice_rand_corretto(km$cluster, generatore)
''','confrontare con il simulatore')+r'\PInfo{L’accordo perfetto ottenuto qui non dimostra una classificazione geologica valida su rocce reali. Servono dati indipendenti e un contesto osservativo.}','Recuperare i gruppi costruiti dal simulatore è un controllo del caso didattico.')

S(103,'Il nome geologico viene dopo le evidenze',pca_plot('kmeans')+r'\PSmall{I tre gruppi colorati usano gli otto z-score; la figura ne mostra due componenti. I nomi geologici non sono coordinate dell’algoritmo.}',r'''
\PBody{Una partizione raggruppa somiglianze rispetto alla metrica adottata. Una spiegazione geologica deve collegarle a processi, materiali e osservazioni pertinenti.}
\vspace{3mm}
\PInfo{Nel dataset, colore e fossili sono indici sintetici convenzionali. Una loro differenza numerica non autorizza da sola una diagnosi petrografica.}
\vspace{3mm}
\PBody{Provenienza, unità, variabili escluse e disegno di campionamento delimitano ciò che il risultato può sostenere.}
''','La separazione geometrica sostiene una descrizione; la spiegazione geologica richiede altre evidenze.')

S(104,'Dalla matrice ai risultati',tk(r'''
\node[pFlow,text width=2.1cm] (x) at(1.2,2.4){$X$\\otto proprietà};
\node[pFlow,text width=2.0cm] (z) at(4,2.4){$Z$\\scale salvate};
\node[pFlow,text width=2.5cm] (p) at(7.65,4){PCA\\scores e direzioni};
\node[pFlow,text width=2.5cm] (k) at(7.65,2.35){K-means\\partizione};
\node[pFlow,text width=2.5cm] (h) at(7.65,.7){Ward\\gerarchia};
\draw[pEdge](x)--(z);\draw[pEdge](z)--(p);\draw[pEdge](z)--(k);\draw[pEdge](z)--(h);
''',h=4.85)+r'\PBody{PCA, K-means e Ward analizzano qui la stessa matrice standardizzata. Il piano PCA viene usato per visualizzare i gruppi stimati nello spazio completo.}',r'''
\PLabel{Passaggi conservati}
\PBody{Le colonne sono scelte per nome. Le scale sono stimate una volta. Ogni risultato mantiene l’identificativo della riga originaria.}
\vspace{3mm}
\PInfo{Usare soltanto PC1 e PC2 come dati del clustering definirebbe una diversa analisi. Occorrerebbe dichiararla e confrontarla.}
\vspace{3mm}
\PBody{Il resoconto collega geometria, scelta del numero di gruppi, sensibilità e profili nelle unità originali.}
''','La sequenza delle trasformazioni deve permettere di ricostruire la distanza usata da ciascun metodo.')

S(105,'Che cosa cambia passando da tre a quattro gruppi?',cluster_split()+r'\PBody{Nel calcolo mostrato, il gruppo 2 con trenta casi si divide in due gruppi di 18 e 12. Le altre due appartenenze rimangono unite.}',C(105,'quattro_gruppi','''
set.seed(1601)
km4 <- kmeans(Z, 4, nstart = 50)
table(k3 = km$cluster, k4 = km4$cluster)
mean(silhouette_base(km4$cluster, dist(Z)))
aggregate(d[v], list(gruppo = km4$cluster), mean)
''','confrontare una suddivisione')+r'\PInfo{La WSS diminuisce, ma la silhouette media peggiora nel confronto del caso. Le differenze nei profili aiutano a capire che cosa separa il nuovo taglio.}','Un gruppo aggiuntivo deve essere motivato dalle differenze introdotte e dallo scopo dell’analisi.')

S(106,'Due chiamate PCA equivalenti',tk(r'''
\node[pFlow,text width=3.7cm] at(2.25,3.35){$X$\\centratura e scala dentro \texttt{prcomp}};
\node[pFlow,text width=3.7cm] at(7.05,3.35){\texttt{scale(X)}\\trasformazione già applicata};
\draw[pEdge](2.25,2.45)--(4.65,1.45);\draw[pEdge](7.05,2.45)--(4.65,1.45);
\node[pLabel,text width=8.5cm] at(4.65,.7){Stessa matrice analizzata, stesse varianze e ricostruzione};
''',h=4.75)+r'\PBody{La seconda chiamata evita di applicare di nuovo centratura e scala. Nel calcolo del corso gli scores coincidono numericamente.}',C(106,'equivalenza','''
pa <- prcomp(X, center = TRUE,
             scale. = TRUE)
pb <- prcomp(scale(X), center = FALSE,
             scale. = FALSE)
max(abs(pa$sdev - pb$sdev))
max(abs(pa$x - pb$x))
''','verificare le convenzioni')+r'\PSmall{Fra implementazioni diverse possono cambiare segni o basi di sottospazi degeneri. La rappresentazione va confrontata tenendo conto di queste equivalenze.}','Le impostazioni di centratura e scala fanno parte della definizione dell’analisi.')

S(107,'Ogni risultato deve tornare al proprio campione',tk(r'''
\node[pFlow,text width=2.25cm] at(1.45,3.0){ID originale\\\texttt{d\$id}};
\node[pFlow,text width=2.55cm] at(4.65,3.0){Coordinate\\PC1, PC2};
\node[pFlow,text width=2.55cm] at(7.9,3.0){Gruppi e qualità\\K-means, Ward, silhouette};
\draw[Rule,line width=1.2pt](.3,1.7)--(9.1,1.7);
\node[pLabel,text width=8.5cm] at(4.65,.8){Una riga per campione; nessun ricongiungimento basato sulla posizione in un grafico};
''',h=4.6)+r'\PBody{La tabella finale permette di riesaminare i casi, collegarli alle misure e documentare quali trasformazioni hanno prodotto i risultati.}',C(107,'tabella_finale','''
sil <- silhouette_base(km$cluster, dist(Z))
risultati <- data.frame(id = d$id,
  pc$x[, 1:2], kmeans = km$cluster,
  ward = cutree(h, k = 3), silhouette = sil)
write.csv(risultati, "Risultati/campioni.csv",
          row.names = FALSE)
''','salvare risultati identificabili')+r'\PSmall{Le scale, la selezione delle colonne e i semi casuali restano nel codice che accompagna la tabella.}','L’identificativo consente di ricondurre scores, appartenenze e controlli alle osservazioni originarie.')

S(108,'Quali somiglianze sostengono questi dati?',pca_plot('kmeans')+r'\PBody{In questa simulazione, tre gruppi sono ben separati nella geometria standardizzata. K-means e Ward recuperano le stesse appartenenze.}',r'''
\PLabel{Risultato del caso studiato}
\PBody{Due componenti conservano l’$86{,}6\%$ della varianza. Il piano riassume la struttura principale e lascia un errore di ricostruzione misurabile.}
\vspace{3mm}
\PInfo{Il risultato si sostiene con scale dichiarate, confronto dei gruppi, verifica degli avvii e perturbazioni. La sua estensione a rocce reali richiede un’altra evidenza.}
\vspace{3mm}
\PBody{La domanda da portare a un nuovo dataset: quali scelte producono la somiglianza osservata e quali osservazioni potrebbero metterla in discussione?}
''','Una conclusione multivariata collega risultati numerici, scelte di analisi e significato delle misure.')
