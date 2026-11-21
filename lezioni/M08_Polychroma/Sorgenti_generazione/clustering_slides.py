"""Polychroma M08: slide 58–93, partizioni e gerarchie."""
import math
from diagram_helpers import DATA, VARIABLES, LABELS, COLORS, table, metrics, it, tk, axes, line, pca_plot

SLIDES={}
CODES={}

def S(n,title,left,right,recall):
 section=('VI · K-MEANS' if n<=72 else 'VII · NUMERO DEI GRUPPI' if n<=82 else 'VIII · GERARCHIE DI WARD')
 SLIDES[n]=dict(title=title,section=section,left=left.strip(),right=right.strip(),recall=recall)

def code(n,name,text):
 filename=f'{n:03}_{name}.R';CODES[filename]=text.strip()+'\n';return filename

TOY=[(1,1),(1.2,2.1),(2.2,1.35),(5.3,2.4),(6.7,2.9),(6,1.6)]

def cloud(centers=None,segments=False,labels=False,one=False):
 centers=centers or [(sum(x for x,y in TOY[:3])/3,sum(y for x,y in TOY[:3])/3),(sum(x for x,y in TOY[3:])/3,sum(y for x,y in TOY[3:])/3)]
 out=[r'\draw[pAxis](.4,.4)--(8.9,.4);\draw[pAxis](.4,.4)--(.4,3.8);',r'\node[pNote,anchor=west] at(.6,4.05){Schema bidimensionale · stessa unità sui due assi};']
 for i,(x,y) in enumerate(TOY):
  g=0 if one else i//3;c=COLORS[g]
  if segments:out.append(rf'\draw[{c}!55]({x+.5},{y+.3})--({centers[g][0]+.5},{centers[g][1]+.3});')
  out.append(rf'\fill[{c}]({x+.5},{y+.3}) circle(2.8pt);')
  if labels:out.append(rf'\node[pNote,above] at({x+.5},{y+.36}){{$i={i+1}$}};')
 for g,(x,y) in enumerate(centers):
  out.append(rf'\draw[{COLORS[g]},line width=1.6pt]({x+.4},{y+.2})--({x+.6},{y+.4}) ({x+.4},{y+.4})--({x+.6},{y+.2});')
  anchor='north' if g==0 else 'south'
  ly=y+.05 if g==0 else y+.55
  out.append(rf'\node[pNote,text={COLORS[g]},anchor={anchor}] at({x+.5},{ly}){{$\mu_{g+1}$}};')
 return tk('\n'.join(out),w=9.4,h=4.3)

def metric_plot(field,label):
 rows=table('cluster_choices.csv');values=[float(r[field]) for r in rows]
 maxv=400 if field=='WSS' else .7
 out,X,Y=axes(1.8,7.2,0,maxv,xlabel='Numero di gruppi $k$',ylabel=label,w=9,h=4.5,xticks=list(range(2,8)),yticks=[0,200,400] if field=='WSS' else [0,.3,.6])
 pts=[(int(r['k']),float(r[field])) for r in rows]
 line(out,X,Y,pts,'GeoA')
 for k,val in pts:out.append(rf'\fill[GeoA]({X(k):.4f},{Y(val):.4f}) circle(2.5pt);')
 k=3;v=next(v for kk,v in pts if kk==3)
 out.append(rf'\draw[GeoB,line width=1pt]({X(k):.4f},{Y(v):.4f}) circle(4.2pt);')
 out.append(rf'\node[pNote,anchor=west,text=GeoB] at({X(k)+.18:.4f},{Y(v)+.22:.4f}){{$k=3$}};')
 out.append(r'\end{tikzpicture}');return '\n'.join(out)

def pca_groups():
 picture=pca_plot(color='kmeans',h=4.4)
 legend=[]
 for g in range(3):
  x=1.65+2.5*g
  legend.append(rf'\fill[{COLORS[g]}]({x},4.3) circle(2pt);\node[pNote,anchor=west] at({x+.15},4.3){{Gruppo {g+1}}};')
 return picture.replace(r'\end{tikzpicture}', '\n'.join(legend)+'\n'+r'\end{tikzpicture}')

def profiles():
 rows=table('profiles_z.csv');out,X,Y=axes(-1.5,1.5,-.6,7.6,xlabel='Media del gruppo in deviazioni standard',ylabel='',w=9.2,h=4.9,xticks=[-1,0,1],yticks=[])
 # Horizontal profiles: each variable is one row.
 out,X,Y=axes(-1.5,1.5,-.6,7.6,xlabel='Media standardizzata',ylabel='',w=9.2,h=4.9,xticks=[-1,0,1],yticks=[])
 line(out,X,Y,[(0,-.3),(0,7.3)],'Rule','dashed')
 for j,v in enumerate(VARIABLES):out.append(rf'\node[pNote,anchor=east] at({X(-1.5)-.15:.4f},{Y(7-j):.4f}){{{LABELS[v]}}};')
 for r in rows:
  c=COLORS[int(r['cluster'])-1]
  pts=[(float(r[v]),7-j) for j,v in enumerate(VARIABLES)]
  line(out,X,Y,pts,c,'line width=.8pt')
  for xx,yy in pts:out.append(rf'\fill[{c}]({X(xx):.4f},{Y(yy):.4f}) circle(1.8pt);')
 out.append(r'\end{tikzpicture}');return '\n'.join(out)

def dendrogram(cut=False):
 merges=table('ward_merges.csv');order=table('ward_order.csv')
 hmax=float(merges[-1]['height']);pos={int(r['row']):int(r['position']) for r in order}
 out,X,Y=axes(0,91,0,hmax*1.06,xlabel='Posizione della foglia nell’albero',ylabel='Altezza Ward.D2',w=9.3,h=4.8,xticks=[1,30,60,90],yticks=[0,10,20])
 nodes={-i:(pos[i],0) for i in pos}
 for r in merges:
  a=nodes[int(r['left'])];b=nodes[int(r['right'])];h=float(r['height']);k=int(r['step'])
  line(out,X,Y,[a,(a[0],h),(b[0],h),b],'Navy','line width=.5pt')
  nodes[k]=((a[0]+b[0])/2,h)
 if cut:
  height=(float(merges[-3]['height'])+float(merges[-2]['height']))/2
  line(out,X,Y,[(0,height),(91,height)],'GeoB','dashed,line width=1.2pt')
  out.append(rf'\node[pNote,text=GeoB,fill=Paper,anchor=east] at({X(88):.4f},{Y(height)+.22:.4f}){{Taglio in tre gruppi}};')
 out.append(r'\end{tikzpicture}');return '\n'.join(out)

S(58,'Una partizione dei campioni',r'''
\PLabel{Campioni assegnati a gruppi}
'''+cloud(labels=True)+r'''
\PBody{Una partizione assegna ogni campione a un solo gruppo. Le proprietà scelte e la distanza definiscono quali osservazioni vengono considerate vicine.}
''',r'''
\[
\mathcal C=\{C_1,\ldots,C_k\},\qquad
\bigcup_g C_g=\{1,\ldots,n\}
\]
\[
C_g\cap C_h=\varnothing\quad(g\ne h)
\]
\PBody{In K-means si fissa $k$ e si cercano gruppi compatti rispetto alla distanza euclidea al quadrato.}
\PInfo{Il caso delle rocce usa 90 righe e otto variabili standardizzate. L’etichetta litologica generatrice resta esclusa.}
''','Una partizione dipende dalla rappresentazione dei campioni e dal criterio di somiglianza adottato.')

code(59,'obiettivo',r'''
# Sei punti illustrativi, due gruppi.
u59 <- rbind(c(1,1), c(1.2,2.1),
 c(2.2,1.35), c(5.3,2.4),
 c(6.7,2.9), c(6,1.6))
g59 <- rep(1:2, each = 3)
cent59 <- rowsum(u59, g59) / 3
# Somma dei quadrati delle distanze.
sum((u59 - cent59[g59, ])^2)
''')
S(59,'La dispersione entro i gruppi',r'''
\[
W(\mathcal C)=\sum_{g=1}^{k}\sum_{i\in C_g}
\|\mathbf z_i-\boldsymbol\mu_g\|^2
\]
'''+cloud(segments=True)+r'''
\PSmall{Ogni segmento contribuisce con il quadrato della propria lunghezza. $\mathbf z_i$ è il vettore delle misure; $\boldsymbol\mu_g$ è il centroide.}
''',r'''
\PCode{R · calcolare la WSS}{059_obiettivo.R}
\PSmall{\texttt{rowsum()} somma le righe di ciascun gruppo. Qui ogni gruppo ha tre osservazioni, quindi dividiamo per tre.}
\PSmall{WSS indica la somma quadratica entro i gruppi. Il suo valore dipende dalla scala delle variabili.}
''','K-means cerca una partizione con piccola dispersione quadratica rispetto ai centroidi.')

code(60,'centroide',r'''
# Tre osservazioni di un gruppo.
A60 <- rbind(c(0,0), c(2,0),
             c(1,3))
mu60 <- colMeans(A60)
mu60  # Il centroide e' (1, 1).
w60 <- function(candidato) {
 sum(sweep(A60, 2, candidato)^2)
}
c(centroide = w60(mu60),
  alternativa = w60(c(1,2)))
''')
S(60,'Perché il centroide è una media',r'''
\[
\boldsymbol\mu_g=\frac{1}{n_g}
\sum_{i\in C_g}\mathbf z_i
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,0) rectangle(9.3,3.7);
\draw[pAxis](1.5,.6)--(4.4,.6);\draw[pAxis](2,.25)--(2,3.75);\node[pNote] at(2,.15){0};\node[pNote] at(4,.15){2};\node[pNote,anchor=east] at(1.9,3.6){3};
\foreach \x/\y in {2/.6,4/.6,3/3.6}{\fill[GeoA](\x,\y) circle(3pt);\draw[GeoA!55](\x,\y)--(3,1.6);}
\draw[Classical,line width=1.5pt](2.9,1.5)--(3.1,1.7)(2.9,1.7)--(3.1,1.5);
\node[pLabel,anchor=west] at(4.6,1.65){Media $(1,1)$};
\node[pNote,anchor=west] at(4.6,2.5){Tre punti: $(0,0),(2,0),(1,3)$};
\end{tikzpicture}
\[
\begin{aligned}
\sum_{i\in C_g}\|\mathbf z_i-\mathbf c\|^2
&=\sum_{i\in C_g}\|\mathbf z_i-\boldsymbol\mu_g\|^2\\
&\quad+n_g\|\mathbf c-\boldsymbol\mu_g\|^2
\end{aligned}
\]
''',r'''
\PCode{R · confrontare due centri}{060_centroide.R}
\PSmall{L’ultimo termine della scomposizione è non negativo e si annulla nel centroide. La media minimizza quindi la somma quadratica per un gruppo fissato.}
''','A parità di appartenenze, il centro che minimizza la WSS è la media delle coordinate del gruppo.')

code(61,'assegnazione',r'''
# Centri provvisori dello schema.
cent61 <- rbind(c(1,1), c(6,3))
dist261 <- sapply(1:2, function(g) {
 rowSums(sweep(u59, 2,
               cent61[g, ])^2)
})
# Righe: punti. Colonne: centri.
round(dist261, 2)
max.col(-dist261,
        ties.method = "first")
''')
S(61,'L’assegnazione al centro più vicino',r'''
\[
g_i\leftarrow\arg\min_g
\|\mathbf z_i-\boldsymbol\mu_g\|^2
\]
'''+cloud(centers=[(1,1),(6,3)],segments=True)+r'''
\PSmall{Con centri fissati, ogni osservazione sceglie il contributo minore alla WSS. I confini fra due centri sono i luoghi dei punti equidistanti.}
''',r'''
\PCode{R · confrontare le distanze}{061_assegnazione.R}
\PSmall{\texttt{max.col(-dist261)} seleziona la colonna con distanza minima. La regola per le parità viene dichiarata esplicitamente.}
''','L’appartenenza dipende dalla posizione del campione rispetto a tutti i centroidi.')

code(62,'aggiornamento',r'''
# Manteniamo i gruppi appena trovati.
g62 <- max.col(-dist261,
              ties.method = "first")
cent62 <- rowsum(u59, g62) /
 as.vector(table(g62))
cent62
# Controllo prima e dopo le medie.
c(prima = sum((u59-
               cent61[g62, ])^2),
  dopo = sum((u59-
              cent62[g62, ])^2))
''')
S(62,'L’aggiornamento dei centroidi',r'''
\PLabel{Le appartenenze sono momentaneamente fissate}
'''+cloud(segments=True)+r'''
\PBody{Dopo l’assegnazione, ogni centro viene spostato nella media del proprio gruppo. Questo passaggio riduce o conserva la WSS per le appartenenze correnti.}
''',r'''
\PCode{R · ricalcolare i centri}{062_aggiornamento.R}
\PSmall{Lo schema ha due gruppi non vuoti. Un’implementazione generale deve anche specificare come gestire un gruppo rimasto senza osservazioni.}
''','Assegnazione e aggiornamento risolvono due problemi condizionati l’uno al risultato dell’altro.')

code(63,'iterazioni',r'''
# Lloyd: una dimostrazione esplicita.
cent63 <- cent61
W63 <- numeric(5)
for (passo in 1:5) {
 dd <- sapply(1:2, function(g)
  rowSums(sweep(u59,2,cent63[g,])^2))
 lab <- max.col(-dd,
                ties.method="first")
 cent63 <- rowsum(u59,lab) /
   as.vector(table(lab))
 scarti63 <- u59-cent63[lab,]
 W63[passo] <- sum(scarti63^2)
}
W63
''')
S(63,'Le iterazioni di Lloyd',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,0) rectangle(9.4,4.3);
\node[pFlow,text width=3.25cm] (a) at(2.2,3.2){Assegna ai centri più vicini};
\node[pFlow,text width=3.25cm] (b) at(7,3.2){Ricalcola le medie dei gruppi};
\draw[pEdge](a.east)--(b.west);
\draw[pEdge](b.south)--(7,1.4)--(2.2,1.4)--(a.south);
\node[pNote,fill=Paper] at(4.6,1.4){Ripeti fino alla stabilizzazione};
\node[pLabel] at(4.6,.45){La WSS non aumenta a ogni passaggio esatto};
\end{tikzpicture}
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m08-kmeans}{Esperimento · iterazioni di K-means}
\PBody{La procedura alternata rende visibile la ricerca. R usa per impostazione predefinita Hartigan--Wong; \texttt{algorithm="Lloyd"} richiede invece questa variante.}
''',r'''
\PCode{R · cinque passi sullo schema}{063_iterazioni.R}
''','L’algoritmo illustrato e l’implementazione utilizzata devono essere identificati separatamente.')

code(64,'avvii',r'''
# Stessa matrice, singoli avvii.
set.seed(818)
W64 <- replicate(20,
 kmeans(Z, centers=3, nstart=1,
        iter.max=100)$tot.withinss)
range(W64)
# Ora molte inizializzazioni.
set.seed(816)
km <- kmeans(Z, 3, nstart=50,
             iter.max=100)
km$tot.withinss
''')
S(64,'Inizializzazione e minimi locali',r'''
\PLabel{Schema della funzione obiettivo}
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,0) rectangle(9.4,4.2);
\draw[pAxis](.6,.5)--(9,.5);\draw[pAxis](.6,.5)--(.6,4.0);
\draw[GeoA,line width=1.3pt] plot[smooth] coordinates{(.9,3.5)(1.6,2)(2.5,1.7)(3.2,2.6)(4.1,3.2)(5.1,1.3)(6.2,.9)(7.3,2.1)(8.6,3.4)};
\node[pLabel] at(2.3,1.2){Minimo locale};\node[pLabel] at(6.1,.25){WSS minore};
\draw[pEdge,GeoB](1.25,3.6)--(2.15,2.1);\draw[pEdge,GeoB](7.9,3.3)--(6.55,1.35);
\node[pNote] at(4.8,3.9){Percorsi schematici da inizializzazioni differenti};
\end{tikzpicture}
\PBody{La discesa della WSS non garantisce il minimo globale. Più avvii aumentano le possibilità di trovare una soluzione migliore, senza costituire una dimostrazione di ottimalità.}
''',r'''
\PCode{R · confrontare gli avvii}{064_avvii.R}
\PSmall{\texttt{set.seed()} rende ripetibile la sequenza casuale. \texttt{nstart} cambia il numero di inizializzazioni tentate.}
''','Riproducibilità dell’esecuzione e ottimalità della partizione sono proprietà differenti.')

code(65,'kmeans',r'''
# Otto colonne standardizzate in Z.
set.seed(816)
km <- kmeans(Z, centers = 3,
             nstart = 50,
             iter.max = 100)
km$size
round(km$centers, 2)
c(WSS = km$tot.withinss,
  totale = km$totss)
''')
S(65,'K-means sulle 90 rocce',r'''
\PLabel{La partizione viene stimata in otto dimensioni}
'''+pca_groups()+r'''
\PBody{Il grafico mostra le prime due componenti; il calcolo usa tutte le otto variabili standardizzate. I tre colori indicano le etichette numeriche di K-means.}
''',r'''
\PCode{R · il modello di riferimento}{065_kmeans.R}
\[
n_1=n_2=n_3=30,\qquad W=129{,}50
\]
\PSmall{Qui studiamo la soluzione con $k=3$. Le slide successive confrontano diversi valori di $k$.}
''','La figura è bidimensionale; la funzione obiettivo considera tutte le coordinate della matrice Z.')

code(66,'controllo_wss',r'''
# Un centroide per ciascuna riga.
centri66 <- km$centers[
 km$cluster, , drop = FALSE]
dist266 <- rowSums((Z-centri66)^2)
c(manuale = sum(dist266),
  kmeans = km$tot.withinss)
stopifnot(abs(sum(dist266)-
 km$tot.withinss) < 1e-8)
''')
S(66,'Controllare la funzione obiettivo',r'''
\[
d_i^2=\sum_{j=1}^{8}(z_{ij}-\mu_{g_i j})^2,
\qquad W=\sum_{i=1}^{90}d_i^2
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,0) rectangle(9.4,3.6);
\foreach \x/\lab/\col in {1.5/1/GeoA,4.7/2/GeoB,7.9/3/GeoC}{
\node[pFlow,text width=2.1cm] (a\lab) at(\x,2.6){Scarti al centroide \lab};
\draw[pEdge](\x,1.95)--(\x,1.25);}
\draw[Classical](1.5,1.25)--(7.9,1.25);\draw[pEdge](4.7,1.25)--(4.7,.65);
\node[pLabel] at(4.7,.3){Somma: WSS $=129{,}50$};
\end{tikzpicture}
\PBody{La verifica riproduce la quantità restituita da R usando le assegnazioni e i centroidi effettivi. Non dipende dalla proiezione mostrata in figura.}
''',r'''
\PCode{R · ricostruire la WSS}{066_controllo_wss.R}
\PSmall{L’indicizzazione \texttt{km\$centers[km\$cluster, ]} associa a ogni campione il centroide del suo gruppo.}
''','Una quantità calcolata automaticamente diventa leggibile quando se ne ricostruisce la definizione.')

code(67,'scomposizione',r'''
# Variabilita' totale, entro e fra.
T67 <- sum(scale(Z,scale=FALSE)^2)
W67 <- km$tot.withinss
B67 <- sum(km$size *
             rowSums(km$centers^2))
c(T = T67, W = W67, B = B67)
stopifnot(abs(T67-W67-B67)<1e-8)
''')
S(67,'Dispersione totale, entro e fra gruppi',r'''
\[
T=\sum_i\|\mathbf z_i-\bar{\mathbf z}\|^2=W+B
\]
\[
B=\sum_g n_g\|\boldsymbol\mu_g-\bar{\mathbf z}\|^2
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,0) rectangle(9.4,3.05);
\fill[GeoA](.7,1.25) rectangle(2.155,2.05);
\fill[GeoB](2.155,1.25) rectangle(8.7,2.05);
\node[pLabel,above] at(4.7,2.2){Totale $T=(90-1)\times8=712$};
\node[pNote] at(1.43,.75){$W=129{,}50$};
\node[pNote] at(5.45,.75){$B=582{,}50$};
\end{tikzpicture}
\PBody{La matrice standardizzata ha media zero e otto varianze campionarie unitarie. La decomposizione confronta punti, centroidi e media generale.}
''',r'''
\PCode{R · verificare T = W + B}{067_scomposizione.R}
\PInfo{Una grande quota fra gruppi descrive la partizione costruita. Non è una prova esterna dell’esistenza di tre litologie naturali.}
''','La separazione fra i centroidi e la dispersione entro i gruppi compongono la variabilità totale.')

code(68,'profili',r'''
# Le medie nelle unita' originali.
prof68 <- aggregate(d[v],
 list(cluster=km$cluster), mean)
prof68
# Oppure si inverte la scala di Z.
mu68 <- sweep(km$centers, 2,
 attr(Z,"scaled:scale"), "*")
mu68 <- sweep(mu68, 2,
 attr(Z,"scaled:center"), "+")
round(mu68[,c("SiO2","densita")],2)
''')
S(68,'I centroidi nelle unità originali',r'''
\[
\bar x_{gj}=\bar x_j+s_j\,\mu_{gj}
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,0) rectangle(9.4,3.9);
\node[pLabel] at(1.3,3.45){Gruppo};\node[pLabel] at(4,3.45){SiO$_2$ (\%)};\node[pLabel] at(7.2,3.45){Densità (g/cm$^3$)};
\draw[Rule](.5,3.0)--(9,3.0);
\foreach \y/\g/\si/\de/\col in {2.5/1/8{,}02/2{,}65/GeoA,1.6/2/69{,}68/2{,}58/GeoB,.7/3/50{,}43/2{,}95/GeoC}{
\node[pLabel,text=\col] at(1.3,\y){\g};\node[pLabel] at(4,\y){\si};\node[pLabel] at(7.2,\y){\de};}
\end{tikzpicture}
\PBody{Un centroide standardizzato misura uno scarto relativo. Tornare alle unità originali permette di descrivere quantitativamente i campioni del gruppo.}
''',r'''
\PCode{R · recuperare la scala}{068_profili.R}
\PSmall{I numeri sono medie dei dati sintetici. Non rappresentano criteri universali di classificazione petrografica.}
''','L’interpretazione scientifica richiede le unità, le definizioni delle variabili e le distribuzioni entro i gruppi.')

code(69,'piano_pca',r'''
# La PCA serve qui alla figura.
pc <- prcomp(Z, center=FALSE,
             scale.=FALSE)
q69 <- pc$sdev^2 / sum(pc$sdev^2)
plot(pc$x[,1:2], pch=19,asp=1,
     col=km$cluster,
     xlab="PC1", ylab="PC2")
sum(q69[1:2])
''')
S(69,'Il piano PCA e lo spazio del clustering',r'''
\PLabel{La figura conserva l’86,59\% della varianza}
'''+pca_groups()+r'''
\[
\sum_{r=1}^{2}(t_{ir}-t_{hr})^2
\leq\sum_{r=1}^{8}(t_{ir}-t_{hr})^2
\]
''',r'''
\PCode{R · mostrare i gruppi}{069_piano_pca.R}
\PBody{Due punti vicini nel piano possono differire nelle componenti omesse. Il colore deriva dal modello calcolato sulle otto variabili.}
\PInfo{La quota di varianza sul grafico riguarda la PCA, non l’accuratezza della classificazione.}
''','Una proiezione visualizza la partizione senza riprodurre necessariamente tutte le distanze usate per stimarla.')

code(70,'distanze_pc',r'''
# Tutte le PC: rotazione ortogonale.
D70 <- as.matrix(dist(Z))
T70 <- as.matrix(dist(pc$x))
max(abs(D70-T70))
# Due PC: le distanze si contraggono.
Q70 <- as.matrix(dist(pc$x[,1:2]))
stopifnot(max(Q70-D70)<1e-8)
''')
S(70,'Tutte le componenti conservano le distanze',r'''
\[
\|\mathbf z_i-\mathbf z_h\|^2
=\|\mathbf t_i-\mathbf t_h\|^2
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,0) rectangle(9.4,3.8);
\draw[pAxis](1,.7)--(4,.7);\draw[pAxis](1,.4)--(1,3.6);
\fill[GeoA](1.5,1.2) circle(3pt);\fill[GeoB](3.5,2.2) circle(3pt);\draw[Classical,line width=1.5pt](1.5,1.2)--(3.5,2.2);
\draw[pAxis](5.7,.7)--(8.8,.7);\draw[pAxis](6,.4)--(6,3.6);
\fill[GeoA](6.183013,1.383013) circle(3pt);\fill[GeoB](7.415064,3.249038) circle(3pt);\draw[Classical,line width=1.5pt](6.183013,1.383013)--(7.415064,3.249038);
\node[pNote] at(2.4,.15){Prima};\node[pNote] at(7.05,.15){Dopo una rotazione};
\draw[pEdge](4.1,2)--(4.9,2);
\end{tikzpicture}
\PSmall{La rotazione ortogonale conserva lunghezze e WSS per una data partizione. Troncamento e riscalatura delle PC cambiano invece la geometria.}
''',r'''
\PCode{R · verificare le distanze}{070_distanze_pc.R}
\PInfo{Le due figure sono uno schema di isometria. Differenze di minimi locali o inizializzazione possono comunque dare esiti diversi in una ricerca numerica.}
''','Ruotare tutte le coordinate conserva la distanza euclidea; eliminarne o ridimensionarne alcune la modifica.')

code(71,'variabili',r'''
# Una diversa domanda di somiglianza.
chim71 <- c("SiO2","CaO","MgO","FeO")
Z71 <- scale(d[chim71])
set.seed(819)
km71 <- kmeans(Z71,3,nstart=50)
# Tabella, senza confrontare i nomi.
table(tutte=km$cluster,
      chimica=km71$cluster)
''')
S(71,'La selezione delle variabili pesa sul risultato',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,0) rectangle(9.4,4.1);
\node[pFlow,text width=3.35cm] (a) at(2.35,3.0){Otto misure chimiche e fisiche};
\node[pFlow,text width=3.35cm] (b) at(7.0,3.0){Quattro concentrazioni};
\node[pFlow,text width=3.35cm] (c) at(2.35,.85){Distanza in $\mathbb R^8$};
\node[pFlow,text width=3.35cm] (d) at(7.0,.85){Distanza in $\mathbb R^4$};
\draw[pEdge](a)--(c);\draw[pEdge](b)--(d);
\end{tikzpicture}
\PBody{Una selezione diversa definisce una diversa nozione di somiglianza. Anche duplicare una colonna ne aumenta il peso implicito nella distanza.}
''',r'''
\PCode{R · un’analisi di sensibilità}{071_variabili.R}
\PSmall{Nel dataset sintetico il confronto conserva le appartenenze per queste impostazioni. Il risultato va controllato, non assunto in generale.}
''','La stabilità rispetto alle variabili utilizzate è una proprietà da valutare sul problema concreto.')

S(72,'La forma dei gruppi e i campioni estremi',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,0) rectangle(9.4,4.2);
\draw[GeoA!50,fill=GeoA!5](2.6,2.35) ellipse(2.0cm and .45cm);
\draw[GeoB!50,fill=GeoB!5](6.2,1.6) ellipse(1.9cm and .45cm);
\foreach \x/\y in {.9/2.3,1.4/2.45,2/2.15,2.6/2.4,3.2/2.2,3.9/2.45,4.3/2.3}{\fill[GeoA](\x,\y) circle(2.2pt);}
\foreach \x/\y in {4.7/1.6,5.1/1.45,5.6/1.75,6.2/1.5,6.8/1.8,7.4/1.5,7.8/1.7}{\fill[GeoB](\x,\y) circle(2.2pt);}
\fill[GeoC](8.65,3.65) circle(3pt);\node[pNote,anchor=east] at(8.3,3.6){Punto estremo};
\node[pNote] at(4.7,.55){Schema: gruppi allungati e un’osservazione isolata};
\end{tikzpicture}
\PBody{Il contributo alla WSS cresce con il quadrato della distanza. La funzione obiettivo attribuisce quindi grande peso agli scarti elevati. Gruppi allungati, densità molto diverse e osservazioni estreme possono richiedere una rappresentazione o un criterio differente.}
''',r'''
\[
\|\mathbf z_i-\boldsymbol\mu_g\|^2
\]
\PBody{Prima di interpretare un gruppo piccolo, occorre controllare le sue osservazioni e il processo di misura. Un campione insolito può essere informativo oppure problematico.}
\PInfo{Il disegno illustra condizioni possibili. Non è un risultato ricavato dalle 90 rocce del laboratorio.}
''','Il criterio di compattezza deve essere compatibile con la struttura che si vuole descrivere.')

S(73,'Il numero dei gruppi è una scelta da motivare',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,0) rectangle(9.4,4.1);
\foreach \x/\k in {1.65/2,4.7/3,7.75/4}{
\node[pFlow,text width=2.3cm] at(\x,3.1){$k=\k$};
\draw[pEdge](\x,2.45)--(\x,1.65);}
\node[pLabel,text width=8.5cm] at(4.7,1.2){Confrontare dispersione, separazione, dimensioni dei gruppi e sensibilità};
\end{tikzpicture}
\PBody{Il numero di categorie nel simulatore non deve fissare la risposta dell’analisi esplorativa. La scelta di $k$ va documentata sulla matrice dichiarata.}
''',r'''
\PLabel{Tre elementi del confronto}
\PBody{La WSS misura la dispersione interna. La silhouette confronta coesione e separazione. I profili descrivono il significato delle differenze.}
\PInfo{Nel caso guida verranno confrontati $k=2,\ldots,7$ sulle stesse otto variabili e con la stessa standardizzazione.}
\PSmall{L’etichetta generatrice sarà consultata successivamente, come informazione sulla simulazione.}
''','Il numero dei cluster deve rispondere alla domanda scientifica e a confronti espliciti fra alternative.')

code(74,'suddivisione',r'''
# Una suddivisione di un gruppo.
g74a <- rep(1, nrow(u59))
g74b <- rep(1:2, each=3)
w74 <- function(lab) {
 cent <- rowsum(u59,lab) /
   as.vector(table(lab))
 sum((u59-cent[lab,,drop=FALSE])^2)
}
c(un_gruppo=w74(g74a),
  due_gruppi=w74(g74b))
''')
S(74,'La WSS e il numero dei gruppi',r'''
\[
W^*_{k+1}\leq W^*_k,\qquad W^*_n=0
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,0) rectangle(9.4,3.5);
\draw[Classical,rounded corners=2mm,fill=Classical!5](.5,.7) rectangle(3.7,2.9);
\foreach \x/\y in {1/1.3,1.2/2.3,2.0/1.8,2.7/1.1,3.2/2.2}{\fill[Classical](\x,\y) circle(2.5pt);}
\draw[pEdge](4,1.8)--(4.8,1.8);
\draw[GeoA,rounded corners=2mm,fill=GeoA!5](5.1,.7) rectangle(6.7,2.9);
\draw[GeoB,rounded corners=2mm,fill=GeoB!5](7,.7) rectangle(8.9,2.9);
\foreach \x/\y in {5.6/1.3,5.8/2.3,6.3/1.8}{\fill[GeoA](\x,\y) circle(2.5pt);}
\foreach \x/\y in {7.5/1.1,8.4/2.2}{\fill[GeoB](\x,\y) circle(2.5pt);}
\node[pNote] at(4.7,.2){Schema: una partizione può essere ulteriormente suddivisa};
\end{tikzpicture}
\PBody{La proprietà riguarda l’ottimo globale $W^*_k$. La WSS trovata da un algoritmo con pochi avvii può non rispettare la monotonia a causa di minimi locali.}
''',r'''
\PCode{R · un esempio di suddivisione}{074_suddivisione.R}
\PSmall{Con un gruppo per osservazione ogni campione coincide con il proprio centroide e la WSS è nulla. Questo estremo non offre una sintesi utile.}
''','Ridurre la WSS aumentando k è atteso: il guadagno va confrontato con la maggiore complessità.')

code(75,'confronto_k',r'''
# Stessa geometria per tutti i k.
set.seed(817)
ks <- 2:7
fits <- lapply(ks, function(k)
 kmeans(Z, k, nstart=50,
        iter.max=100))
W75 <- vapply(fits, function(m)
 m$tot.withinss, numeric(1))
data.frame(k=ks, WSS=W75)
plot(ks,W75,type="b",pch=19,
     xlab="k",ylab="WSS")
''')
S(75,'La curva della WSS nelle rocce sintetiche',r'''
\PLabel{Confronto effettivo da k = 2 a k = 7}
'''+metric_plot('WSS','WSS')+r'''
\PBody{Il passaggio da due a tre gruppi riduce fortemente la WSS. Le riduzioni successive sono più piccole. La forma della curva suggerisce un’alternativa da approfondire.}
''',r'''
\PCode{R · confrontare le soluzioni}{075_confronto_k.R}
\PSmall{Il cosiddetto gomito può essere ambiguo o assente. Non costituisce una regola universale per scegliere $k$.}
''','La curva della WSS mostra il guadagno di compattezza ottenuto aggiungendo gruppi.')

code(76,'coesione_separazione',r'''
# Un campione e il proprio gruppo.
D <- dist(Z)
DD76 <- as.matrix(D)
i76 <- 1
g76 <- km$cluster
stessi76 <- which(g76==g76[i76] &
          seq_along(g76)!=i76)
a76 <- mean(DD76[i76,stessi76])
altri76 <- setdiff(unique(g76),
                   g76[i76])
b76 <- min(sapply(altri76,function(g)
 mean(DD76[i76,g76==g])))
c(a=a76,b=b76)
''')
S(76,'Coesione e separazione di un campione',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,0) rectangle(9.4,4.4);
\filldraw[GeoA!8,draw=GeoA!50](2.1,2.4) circle(1.3cm);
\filldraw[GeoB!8,draw=GeoB!50](6.55,2.4) circle(1.45cm);
\fill[Classical](2,2.35) circle(3.6pt);
\foreach \x/\y in {1.1/2.7,1.6/1.55,2.7/2.8,2.85/1.9}{\draw[GeoA!60](2,2.35)--(\x,\y);\fill[GeoA](\x,\y) circle(2.6pt);}
\foreach \x/\y in {5.6/2.2,6.2/3.1,7.2/2.6,6.8/1.55}{\draw[GeoB!45](2,2.35)--(\x,\y);\fill[GeoB](\x,\y) circle(2.6pt);}
\node[pLabel,text=GeoA,text width=3.8cm] at(2.1,.55){$a_i$: media interna};
\node[pLabel,text=GeoB,text width=3.8cm] at(6.75,.55){$b_i$: media esterna};
\end{tikzpicture}
\PSmall{$b_i$ è la minima fra le distanze medie verso ciascun altro gruppo. Non è la distanza dal singolo punto esterno più vicino. Schema con due gruppi.}
''',r'''
\PCode{R · a e b per il campione R001}{076_coesione_separazione.R}
''','La silhouette confronta distanze medie tra osservazioni; non utilizza la sola distanza dai centroidi.')

code(77,'silhouette',r'''
# Formula per il campione R001.
s77 <- (b76-a76)/max(a76,b76)
s77
# Funzione fornita nel file
# R/funzioni_analisi.R.
sil <- silhouette_base(km$cluster,D)
stopifnot(abs(s77-sil[i76])<1e-8)
summary(sil)
''')
S(77,'La larghezza silhouette',r'''
\[
s_i=\frac{b_i-a_i}{\max(a_i,b_i)},\qquad -1\leq s_i\leq1
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,0) rectangle(9.4,3.2);
\draw[pAxis](.8,1.6)--(8.9,1.6);
\foreach \x/\lab in {1/-1,4.7/0,8.4/1}{\draw[Muted](\x,1.5)--(\x,1.7);\node[pLabel] at(\x,1.1){$\lab$};}
\node[pNote,text width=2.7cm] at(1.6,2.55){Più vicino, in media, a un altro gruppo};
\node[pNote,text width=2.4cm] at(4.7,2.55){Distanze medie simili};
\node[pNote,text width=2.6cm] at(7.9,2.55){Buona separazione relativa};
\end{tikzpicture}
\PBody{Una silhouette negativa segnala un’assegnazione poco convincente rispetto alla distanza scelta. Per un gruppo con un solo membro si adotta la convenzione $s_i=0$.}
''',r'''
\PCode{R · dalla definizione al vettore}{077_silhouette.R}
\PSmall{La funzione del progetto gestisce anche il caso $a_i=b_i=0$, restituendo zero. Il risultato resta un indice geometrico.}
''','Una silhouette misura quanto un’assegnazione sia coerente con le distanze, non la verità geologica del gruppo.')

code(78,'silhouette_grafico',r'''
# Distribuzione delle 90 silhouette.
ord78 <- order(km$cluster,sil)
barplot(sil[ord78], space=0,
 col=km$cluster[ord78], border=NA,
 ylab="Silhouette",xlab="Campioni")
abline(h=0,lty=2)
c(media=mean(sil),minimo=min(sil),
  massimo=max(sil))
''')
def silhouette_bars():
 rows=sorted(table('assignments.csv'),key=lambda r:(int(r['kmeans']),float(r['silhouette'])))
 out,X,Y=axes(0,90,0,.85,xlabel='Campioni ordinati entro ciascun gruppo',ylabel='Silhouette',w=9.2,h=4.5,xticks=[1,30,60,90],yticks=[0,.4,.8])
 for i,r in enumerate(rows):
  col=COLORS[int(r['kmeans'])-1];out.append(rf'\fill[{col}]({X(i):.4f},{Y(0):.4f}) rectangle({X(i+.9):.4f},{Y(r["silhouette"]):.4f});')
 for g in range(3):out.append(rf'\node[pNote,text={COLORS[g]}] at({X(g*30+15):.4f},{Y(.81):.4f}){{Gruppo {g+1}}};')
 out.append(r'\end{tikzpicture}');return '\n'.join(out)
S(78,'Le silhouette dei singoli campioni',r'''
\PLabel{Partizione K-means con k = 3}
'''+silhouette_bars()+r'''
\PBody{Tutte le silhouette sono positive; la più piccola è circa 0,345. La figura permette di distinguere osservazioni meno separate anche quando la media è elevata.}
''',r'''
\PCode{R · guardare anche la distribuzione}{078_silhouette_grafico.R}
\[
\bar s=0{,}626,\qquad \min s_i=0{,}345
\]
\PSmall{La posizione orizzontale ordina i campioni per gruppo e silhouette. Non rappresenta una coordinata geografica.}
''','La silhouette media riassume la partizione; i valori individuali mostrano dove l’assegnazione è meno netta.')

code(79,'silhouette_k',r'''
# Le soluzioni di k = 2,...,7.
S79 <- vapply(fits, function(m)
 mean(silhouette_base(m$cluster,D)),
 numeric(1))
indici <- data.frame(k=ks,WSS=W75,
                      silhouette=S79)
indici
plot(ks,S79,type="b",pch=19,
 xlab="k",ylab="Silhouette media")
''')
S(79,'Confrontare la silhouette media',r'''
\PLabel{Le stesse distanze per le sei partizioni}
'''+metric_plot('silhouette','Silhouette media')+r'''
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m08-silhouette}{Esperimento · numero dei gruppi e silhouette}
''',r'''
\PCode{R · confronto fra k}{079_silhouette_k.R}
\PBody{Tra le alternative esplorate, $k=3$ ha la silhouette media più elevata. Qui WSS e silhouette indicano la stessa soluzione.}
\PSmall{La preferenza vale per queste variabili, questa scala e queste soluzioni numeriche.}
''','Un massimo della silhouette individua una soluzione preferibile rispetto alle alternative effettivamente confrontate.')

code(80,'quattro_gruppi',r'''
# Un'alternativa esplicita: k = 4.
set.seed(1601)
km4 <- kmeans(Z,4,nstart=50,
              iter.max=100)
km4$size
table(k3=km$cluster,k4=km4$cluster)
aggregate(d[v],
 list(cluster=km4$cluster),mean)
''')
S(80,'Che cosa aggiunge un quarto gruppo',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,0) rectangle(9.4,3.65);
\foreach \x/\c/\lab in {1.5/GeoA/1,4.7/GeoB/2,7.9/GeoC/3}{\node[pFlow,draw=\c,text=\c,text width=1.8cm] at(\x,2.9){Gruppo \lab};}
\draw[pEdge](1.5,2.35)--(1.5,1.2);\draw[pEdge](7.9,2.35)--(7.9,1.2);
\draw[pEdge](4.7,2.35)--(3.9,1.2);\draw[pEdge](4.7,2.35)--(5.5,1.2);
\foreach \x/\lab in {1.5/A,3.9/B,5.5/C,7.9/D}{\node[pFlow,minimum width=1.05cm,minimum height=.7cm] at(\x,.75){\lab};}
\node[pNote] at(4.7,.05){Schema di confronto; K-means non impone partizioni annidate};
\end{tikzpicture}
\PBody{Si controllano dimensioni, profili e corrispondenze dei gruppi. Una nuova classe può descrivere una differenza interna oppure riflettere pochi campioni particolari.}
''',r'''
\PCode{R · esaminare k = 4}{080_quattro_gruppi.R}
\PSmall{La tabella di contingenza mostra come cambiano le appartenenze. K-means con $k+1$ può anche riassegnare campioni fra più gruppi.}
''','Aumentare k richiede di spiegare quali differenze aggiuntive vengano rappresentate.')

code(81,'riepilogo',r'''
# Indici per le stesse soluzioni.
data.frame(k=ks,
 WSS=round(W75,2),
 silhouette=round(S79,3),
 minimo_gruppo=vapply(fits,
  function(m)min(m$size),numeric(1)))
# La scelta non legge la litologia.
ks[which.max(S79)]
''')
S(81,'Una scelta sostenuta da più controlli',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,0) rectangle(9.4,4.0);
\node[pFlow,text width=3.4cm] (a) at(2.3,3.15){Dispersione interna};
\node[pFlow,text width=3.4cm] (b) at(7.05,3.15){Separazione relativa};
\node[pFlow,text width=3.4cm] (c) at(2.3,1.05){Dimensioni dei gruppi};
\node[pFlow,text width=3.4cm] (d) at(7.05,1.05){Profili e sensibilità};
\draw[pEdge](a.south)--(c.north);\draw[pEdge](b.south)--(d.north);
\end{tikzpicture}
\PBody{Nessun indicatore esaurisce la decisione. Una separazione numerica deve restare leggibile nelle misure e sufficientemente stabile alle scelte dell’analisi.}
''',r'''
\PCode{R · una tabella di confronto}{081_riepilogo.R}
\PSmall{Il massimo della silhouette è un criterio esplicito. Il confronto con WSS, numerosità e profili ne rende visibili le conseguenze.}
''','La scelta di k va motivata mostrando alternative e conseguenze, non soltanto un valore ottimo.')

S(82,'La scelta nel caso sintetico',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,0) rectangle(9.4,3.65);
\node[pLabel] at(4.7,3.15){Soluzione studiata: $k=3$};
\node[pFlow,text width=2.1cm] at(1.65,1.75){WSS $129{,}50$};
\node[pFlow,text width=2.1cm] at(4.7,1.75){Silhouette media $0{,}626$};
\node[pFlow,text width=2.1cm] at(7.75,1.75){Numerosità $30,30,30$};
\node[pNote,text width=8.5cm] at(4.7,.45){Dati, otto variabili, standardizzazione e avvii restano dichiarati};
\end{tikzpicture}
\PBody{La riduzione della WSS e il confronto delle silhouette sostengono la scelta di tre gruppi nel caso guida. Occorre ancora descrivere i profili e valutare la sensibilità.}
''',r'''
\PLabel{Una conclusione circoscritta}
\PBody{Le tre classi rappresentano una sintesi delle 90 rocce simulate nella geometria scelta. L’etichetta del simulatore resta un confronto successivo.}
\PInfo{Un dato reale può presentare transizioni continue, gruppi sovrapposti o più scale di organizzazione. Una partizione discreta è una scelta di rappresentazione.}
''','Le evidenze interne sostengono una soluzione esplorativa sul campione; la validazione geologica richiede altro contesto.')

S(83,'Una gerarchia di fusioni',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,0) rectangle(9.4,4.6);
\foreach \x/\lab in {1/A,2.4/B,4.1/C,6.2/D,8/E}{\node[pLabel] at(\x,.35){\lab};}
\draw[Navy,line width=1.1pt](1,.65)--(1,1.6)--(2.4,1.6)--(2.4,.65);
\draw[Navy,line width=1.1pt](1.7,1.6)--(1.7,2.6)--(4.1,2.6)--(4.1,.65);
\draw[Navy,line width=1.1pt](6.2,.65)--(6.2,1.9)--(8,1.9)--(8,.65);
\draw[Navy,line width=1.1pt](2.9,2.6)--(2.9,4)--(7.1,4)--(7.1,1.9);
\node[pNote,anchor=west] at(4.6,3.2){Schema di cinque campioni};
\end{tikzpicture}
\PBody{Il metodo agglomerativo parte da un gruppo per campione e fonde due gruppi alla volta. Ogni fusione resta incorporata nelle successive.}
''',r'''
\[
n\ \longrightarrow\ n-1\ \longrightarrow\cdots\longrightarrow\ 1
\]
\PBody{Il criterio di collegamento stabilisce quale fusione eseguire. Il dendrogramma conserva l’ordine e l’altezza delle fusioni.}
\PInfo{L’albero viene costruito prima di scegliere un taglio. Le foglie sono campioni; i nodi interni rappresentano gruppi fusi.}
''','Il clustering gerarchico costruisce partizioni annidate attraverso fusioni successive e irreversibili.')

S(84,'Il criterio di Ward',r'''
\[
\Delta W(A,B)=\frac{n_A n_B}{n_A+n_B}
\|\bar{\mathbf z}_A-\bar{\mathbf z}_B\|^2
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,0) rectangle(9.4,3.65);
\draw[GeoA,fill=GeoA!7](2.0,2.0) circle(.95cm);\draw[GeoB,fill=GeoB!7](6.7,2.0) circle(1.25cm);
\node[pLabel] at(2,2.0){$\bar{\mathbf z}_A$};\node[pLabel] at(6.7,2.0){$\bar{\mathbf z}_B$};
\draw[<->,Classical,line width=1.1pt](3.15,2.0)--(5.25,2.0);
\node[pNote] at(2,.6){$n_A$ campioni};\node[pNote] at(6.7,.4){$n_B$ campioni};
\end{tikzpicture}
\PBody{Ward sceglie la fusione che aumenta meno la WSS. Il costo combina distanza fra centroidi e numerosità dei due gruppi.}
''',r'''
\[
W_{A\cup B}=W_A+W_B+\Delta W(A,B)
\]
\PSmall{Il centroide del gruppo unito è la media ponderata dei due centroidi. La formula vale per la dispersione euclidea quadratica.}
\PInfo{Due coppie con la stessa distanza fra centroidi possono avere costi di fusione diversi se cambiano le numerosità.}
''','Ward minimizza l’incremento della dispersione interna a ogni singola fusione.')

code(85,'costo_fusione',r'''
# Due gruppi, una sola coordinata.
A85 <- c(0,2)
B85 <- c(5,7)
w85 <- function(x) sum((x-mean(x))^2)
delta85 <- w85(c(A85,B85))-
           w85(A85)-w85(B85)
f85 <- length(A85)*length(B85) /
 (length(A85)+length(B85)) *
 (mean(A85)-mean(B85))^2
c(incremento=delta85,formula=f85)
''')
S(85,'Un costo di fusione calcolato a mano',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,0) rectangle(9.4,3.3);
\draw[pAxis](.6,1.5)--(8.8,1.5);
\foreach \x/\lab in {1/0,3/2,6/5,8/7}{\draw[Muted](\x,1.4)--(\x,1.6);\node[pNote] at(\x,1.05){\lab};}
\fill[GeoA](1,1.5) circle(3pt);\fill[GeoA](3,1.5) circle(3pt);
\fill[GeoB](6,1.5) circle(3pt);\fill[GeoB](8,1.5) circle(3pt);
\node[pLabel,text=GeoA] at(2,2.45){$\bar z_A=1$};\node[pLabel,text=GeoB] at(7,2.45){$\bar z_B=6$};
\draw[<->,Classical](2,.45)--(7,.45);\node[pNote,fill=Paper] at(4.5,.45){Distanza fra medie: 5};
\end{tikzpicture}
\[
\Delta W=\frac{2\cdot2}{2+2}(1-6)^2=25
\]
\PSmall{Ogni gruppo ha WSS pari a 2. Il gruppo unito ha WSS pari a 29: l’aumento è 25.}
''',r'''
\PCode{R · le due espressioni coincidono}{085_costo_fusione.R}
\PSmall{Questo piccolo esempio usa una sola coordinata. Nelle rocce si sommano gli scarti quadratici sulle otto coordinate.}
''','Il costo di Ward è una differenza di WSS, calcolabile anche direttamente sulle osservazioni.')

code(86,'ward',r'''
# Distanze euclidee ordinarie.
D <- dist(Z, method="euclidean")
h <- hclust(D, method="ward.D2")
plot(h,labels=FALSE,
     xlab="Campioni",sub="Ward.D2",
     ylab="Altezza")
tail(h$height,3)
''')
S(86,'Il dendrogramma delle 90 rocce',r'''
\PLabel{Gerarchia effettiva sulle otto variabili}
'''+dendrogram()+r'''
\PSmall{Le foglie sono ordinate per disegnare l’albero senza incroci. L’asse orizzontale non rappresenta una distanza metrica tra campioni.}
''',r'''
\PCode{R · costruire la gerarchia}{086_ward.R}
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m08-ward}{Esperimento · gerarchie e Ward}
\PSmall{\texttt{ward.D2} richiede distanze euclidee ordinarie e le eleva al quadrato durante gli aggiornamenti. \texttt{h\$merge} conserva le fusioni. Gli indici negativi indicano foglie; quelli positivi rinviano a fusioni precedenti.}
''','Il dendrogramma va letto attraverso i nodi e le loro altezze, non attraverso la distanza orizzontale delle foglie.')

code(87,'altezza',r'''
# Prima fusione: due campioni.
f87 <- -h$merge[1, ]
delta87 <- sum((Z[f87[1], ]-
                Z[f87[2], ])^2)/2
c(deltaW=delta87,
  altezza2_su_2=h$height[1]^2/2)
stopifnot(abs(delta87-
             h$height[1]^2/2)<1e-8)
''')
S(87,'La convenzione delle altezze Ward.D2',r'''
\[
h_r=\sqrt{2\,\Delta W_r},\qquad
\Delta W_r=\frac{h_r^2}{2}
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,0) rectangle(9.4,3.75);
\draw[Navy,line width=1.2pt](2,.5)--(2,2.75)--(7,2.75)--(7,.5);
\draw[pAxis](.8,.5)--(.8,3.4);
\draw[Muted,dashed](.8,2.75)--(2,2.75);
\node[pNote,anchor=east] at(.65,2.75){$h_r$};
\node[pLabel] at(4.5,1.65){Fusione al livello $r$};
\node[pNote] at(4.7,.15){Schema della scala verticale};
\end{tikzpicture}
\PBody{La relazione vale per \texttt{hclust(dist(Z), method="ward.D2")}. L’altezza restituita da R non coincide direttamente con l’incremento della WSS.}
''',r'''
\PCode{R · controllare la prima fusione}{087_altezza.R}
\PSmall{Per due singoli campioni, $n_A=n_B=1$: il costo è metà della distanza euclidea al quadrato. Il progetto verifica la relazione anche sulle fusioni successive.}
''','Le altezze di un dendrogramma dipendono dal metodo e dalla convenzione dell’implementazione.')

code(88,'taglio',r'''
# Taglio della stessa gerarchia.
ward <- cutree(h, k=3)
table(ward)
plot(h,labels=FALSE,sub="Ward.D2")
rect.hclust(h,k=3,border=1:3)
# L'albero resta lo stesso.
ward4 <- cutree(h,k=4)
table(tre=ward,quattro=ward4)
''')
S(88,'Tagliare la gerarchia in tre gruppi',r'''
\PLabel{Una partizione ottenuta dall’albero}
'''+dendrogram(cut=True)+r'''
\PBody{Un taglio orizzontale identifica i rami che rimangono separati. \texttt{cutree()} restituisce l’appartenenza di ogni osservazione nell’ordine originale dei dati.}
''',r'''
\PCode{R · ottenere le appartenenze}{088_taglio.R}
\PSmall{Passare da tre a quattro gruppi taglia un ramo della stessa gerarchia. Le partizioni sono annidate, a differenza di fit K-means indipendenti.}
''','Il taglio sceglie una risoluzione dell’albero già costruito, senza ricalcolare tutte le fusioni.')

S(89,'Ruotare i rami non cambia la gerarchia',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,0) rectangle(9.4,4.05);
\draw[Navy,line width=1pt](.7,.6)--(.7,1.6)--(1.8,1.6)--(1.8,.6);
\draw[Navy,line width=1pt](3,.6)--(3,2.1)--(4.1,2.1)--(4.1,.6);
\draw[Navy,line width=1pt](1.25,1.6)--(1.25,3.25)--(3.55,3.25)--(3.55,2.1);
\foreach \x/\lab in {.7/A,1.8/B,3/C,4.1/D}{\node[pNote] at(\x,.25){\lab};}
\draw[Navy,line width=1pt](5.4,.6)--(5.4,2.1)--(6.5,2.1)--(6.5,.6);
\draw[Navy,line width=1pt](7.7,.6)--(7.7,1.6)--(8.8,1.6)--(8.8,.6);
\draw[Navy,line width=1pt](5.95,2.1)--(5.95,3.25)--(8.25,3.25)--(8.25,1.6);
\foreach \x/\lab in {5.4/D,6.5/C,7.7/B,8.8/A}{\node[pNote] at(\x,.25){\lab};}
\node[pLabel] at(4.7,3.8){Stesse fusioni, diverso ordine delle foglie};
\end{tikzpicture}
\PBody{Scambiare i due figli di un nodo modifica l’ordine grafico senza cambiare i gruppi rappresentati. La vicinanza delle etichette sulla pagina non è una distanza geologica.}
''',r'''
\PLabel{Che cosa resta invariato}
\PBody{Rimangono gli insiemi di campioni riuniti da ogni nodo e le altezze delle fusioni. Cambia soltanto il loro ordine di disegno.}
\PInfo{Il diagramma è uno schema di quattro campioni. L’asse orizzontale serve a disporre le foglie e non ha unità fisiche.}
''','Una gerarchia è definita dalle relazioni di inclusione dei gruppi, non dall’ordine sinistra-destra delle etichette.')

code(90,'confronto_ward',r'''
# Stessi campioni, stessa scala, k=3.
tab90 <- table(Kmeans=km$cluster,
               Ward=ward)
tab90
# I numeri dei gruppi non sono nomi
# geologici ne' ordini di grandezza.
''')
S(90,'Confrontare Ward e K-means',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,0) rectangle(9.4,4.2);
\node[pLabel] at(5.45,3.8){Gruppo Ward};
\foreach \x/\lab in {3.7/1,5.4/2,7.1/3}{\node[pLabel] at(\x,3.2){\lab};}
\node[pNote,rotate=90] at(.6,1.9){Gruppo K-means};
\foreach \y/\lab in {2.5/1,1.6/2,.7/3}{\node[pLabel] at(1.8,\y){\lab};}
\foreach \x/\y/\val in {3.7/2.5/0,5.4/2.5/0,7.1/2.5/30,3.7/1.6/0,5.4/1.6/30,7.1/1.6/0,3.7/.7/30,5.4/.7/0,7.1/.7/0}{
\node[pLabel,minimum width=1.2cm,minimum height=.65cm,fill=GeoTint] at(\x,\y){\val};}
\draw[Rule](2.6,2.95)--(8,2.95);
\end{tikzpicture}
\PBody{Nel caso sintetico le appartenenze coincidono, pur con una permutazione dei numeri. Il gruppo 1 di K-means corrisponde al gruppo 3 di Ward.}
''',r'''
\PCode{R · la tabella di contingenza}{090_confronto_ward.R}
\PSmall{L’accordo tra due algoritmi usa gli stessi dati. È un controllo di coerenza interna, non un’evidenza geologica indipendente.}
''','Le etichette dei cluster sono arbitrarie: il confronto riguarda quali campioni vengono raggruppati insieme.')

code(91,'coappartenenza',r'''
# Confronto senza nomi dei gruppi.
A91 <- outer(km$cluster,
              km$cluster,"==")
B91 <- outer(ward,ward,"==")
sopra91 <- upper.tri(A91)
mean(A91[sopra91]==B91[sopra91])
# Confronto non sensibile ai nomi.
all(A91==B91)
''')
S(91,'Confrontare le coappartenenze',r'''
\[
A_{ih}=\mathbf 1\{g_i=g_h\},\qquad i<h
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,0) rectangle(9.4,3.8);
\foreach \x/\lab in {1.5/A,3.4/B,5.7/C,7.6/D}{\node[pFlow,minimum width=.85cm,minimum height=.7cm] at(\x,2.5){\lab};}
\draw[GeoA,line width=1.8pt](1.95,2.5)--(2.95,2.5);
\draw[GeoB,line width=1.8pt](6.15,2.5)--(7.15,2.5);
\node[pNote] at(2.45,1.6){Stesso gruppo};\node[pNote] at(6.65,1.6){Stesso gruppo};
\node[pLabel] at(4.7,.55){I legami restano uguali se rinominiamo i gruppi};
\end{tikzpicture}
\PBody{Per ogni coppia si registra se i due campioni appartengono allo stesso gruppo. Questa descrizione elimina la dipendenza dai nomi numerici dei cluster.}
''',r'''
\PCode{R · accordo delle coppie}{091_coappartenenza.R}
\PSmall{Si usa il triangolo superiore per escludere la diagonale e non contare due volte ogni coppia. Il semplice accordo non corregge per il caso.}
''','Un confronto fra partizioni deve restare invariato quando si permutano le etichette dei gruppi.')

code(92,'wss_ward',r'''
# WSS della partizione di Ward.
mu92 <- rowsum(Z,ward) /
         as.vector(table(ward))
W92 <- sum((Z-mu92[ward,])^2)
c(Kmeans=km$tot.withinss,Ward=W92)
# Nello stesso spazio, confrontiamo
# la stessa quantita' geometrica.
''')
S(92,'Due strategie di ricerca differenti',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,0) rectangle(9.4,4.1);
\node[pFlow,text width=3.4cm] (k) at(2.35,3.05){K-means: numero $k$ fissato};
\node[pFlow,text width=3.4cm] (w) at(7,3.05){Ward: fusioni successive};
\node[pLabel,text width=3.6cm] at(2.35,1.4){Riassegnazioni possibili durante la ricerca};
\node[pLabel,text width=3.6cm] at(7,1.4){Fusioni conservate nella gerarchia};
\draw[pEdge](k.south)--(2.35,2.05);\draw[pEdge](w.south)--(7,2.05);
\end{tikzpicture}
\PBody{Entrambi coinvolgono dispersioni quadratiche, ma esplorano le partizioni in modi diversi. L’accordo osservato sulle rocce sintetiche non è garantito su altri dati.}
''',r'''
\PCode{R · confrontare la WSS}{092_wss_ward.R}
\PSmall{La partizione di Ward può avere WSS maggiore di una soluzione K-means con lo stesso $k$. Ogni fusione è scelta localmente nel percorso gerarchico.}
''','Un criterio locale di fusione e una ricerca a k fissato possono produrre partizioni differenti.')

S(93,'Dalla concordanza alla robustezza',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,0) rectangle(9.4,4.0);
\node[pFlow,text width=3.1cm] (a) at(2.3,3.0){Stessi dati, algoritmi differenti};
\node[pFlow,text width=3.1cm] (b) at(7.0,3.0){Dati o variabili leggermente modificati};
\node[pFlow,text width=3.1cm] (c) at(2.3,1.0){Concordanza fra le partizioni};
\node[pFlow,text width=3.1cm] (d) at(7.0,1.0){Stabilità delle appartenenze};
\draw[pEdge](a)--(c);\draw[pEdge](b)--(d);
\end{tikzpicture}
\PBody{L’accordo fra Ward e K-means è una prima informazione. Per valutare la robustezza occorre anche modificare aspetti dichiarati dell’analisi e controllare quali campioni cambiano gruppo.}
''',r'''
\PLabel{Che cosa resta da esaminare}
\PBody{L’inizializzazione riguarda la ricerca numerica. Una perturbazione delle misure riguarda la sensibilità ai dati. Una diversa selezione di colonne riguarda il significato della somiglianza.}
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m08-robustezza}{Esperimento · sensibilità di una partizione}
\PInfo{Le diverse fonti di variazione vanno esaminate separatamente, mantenendo un riferimento riconoscibile.}
''','Concordanza fra metodi e stabilità rispetto ai dati rispondono a domande complementari.')
