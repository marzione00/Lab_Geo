from diagram_helpers import *
SLIDES={}; CODES={}
def S(n,title,left,right,recall):
 sec='III · GEOMETRIA DELLA PCA' if n<=44 else 'IV · INTERPRETARE LE COMPONENTI'
 SLIDES[n]=dict(title=title,section=sec,left=left,right=right,recall=recall)
def C(n,name,src,title):
 key=f'{n:03}_{name}.R';CODES[key]=src.strip()+'\n';return rf'\PCode{{R · {title}}}{{{key}}}'
def toy():
 rows=[(-3+.3*i,.65*(-3+.3*i)+.45*math.sin((i+1)*2.1)) for i in range(21)]
 mx=sum(x for x,y in rows)/21;my=sum(y for x,y in rows)/21
 return [(x-mx,y-my) for x,y in rows]
def cloud(angle=None,residuals=False):
 out,X,Y=axes(-3.8,3.8,-2.8,2.8,xlabel='$z_1$',ylabel='$z_2$',xticks=[-3,0,3],yticks=[-2,0,2],equal=True,h=4.65)
 if angle is not None:
  a=angle*math.pi/180;v=(math.cos(a),math.sin(a))
  line(out,X,Y,[(-3.6*v[0],-3.6*v[1]),(3.6*v[0],3.6*v[1])],'Classical','line width=1.4pt')
 for x,y in toy():
  if angle is not None:
   t=x*v[0]+y*v[1];pr=(t*v[0],t*v[1])
   if residuals:line(out,X,Y,[(x,y),pr],'GeoB!65','line width=.55pt')
   out.append(rf'\fill[Classical]({X(pr[0]):.4f},{Y(pr[1]):.4f}) circle(.9pt);')
  out.append(rf'\fill[GeoA]({X(x):.4f},{Y(y):.4f}) circle(1.6pt);')
 out.append(r'\end{tikzpicture}');return '\n'.join(out)
def vector_projection(reconstruct=False):
 out,X,Y=axes(-.4,3,-.4,2.2,xlabel='$z_1$',ylabel='$z_2$',xticks=[0,1,2,3],yticks=[0,1,2],equal=True,h=4.65)
 line(out,X,Y,[(-.4,-.3),(2.7,2.025)],'Classical','line width=1pt')
 line(out,X,Y,[(0,0),(2,1)],'GeoA','-{Latex},line width=1.2pt')
 line(out,X,Y,[(0,0),(1.76,1.32)],'Classical','-{Latex},line width=1.4pt')
 line(out,X,Y,[(1.76,1.32),(2,1)],'GeoB','dashed,line width=1.2pt')
 out+= [rf'\fill[GeoA]({X(2):.3f},{Y(1):.3f}) circle(2.8pt);\node[pLabel,anchor=north west] at({X(2)+.1:.3f},{Y(1)-.08:.3f}){{$\mathbf z=(2,1)$}};',rf'\node[pNote,anchor=south east] at({X(1.76)-.1:.3f},{Y(1.32)+.1:.3f}){{$\widehat{{\mathbf z}}=(1{{,}}76;1{{,}}32)$}};']
 out.append(r'\end{tikzpicture}');return '\n'.join(out)
def rotating_variance():
 rows=toy();xx=sum(x*x for x,y in rows)/20;yy=sum(y*y for x,y in rows)/20;xy=sum(x*y for x,y in rows)/20
 pts=[]
 for deg in range(0,181,2):
  a=math.radians(deg);pts.append((deg,xx*math.cos(a)**2+2*xy*math.cos(a)*math.sin(a)+yy*math.sin(a)**2))
 out,X,Y=axes(0,180,0,5,xlabel=r'Angolo $\theta$ (gradi)',ylabel='Varianza proiettata',xticks=[0,45,90,135,180],yticks=[0,2,4],h=4.6)
 line(out,X,Y,pts)
 theta=.5*math.degrees(math.atan2(2*xy,xx-yy));val=(xx+yy+math.sqrt((xx-yy)**2+4*xy**2))/2
 line(out,X,Y,[(theta,0),(theta,val)],'GeoB','dashed')
 out.append(rf'\fill[GeoB]({X(theta):.4f},{Y(val):.4f}) circle(2.7pt);\node[pNote,anchor=west] at({X(theta)+.2:.4f},{Y(val)-.2:.4f}){{$\theta_1\simeq {it(theta,1)}^\circ$}};')
 out.append(r'\end{tikzpicture}');return '\n'.join(out)
def matrix_factor(labels,dimensions,caption='',operators=None):
 body=''
 n=len(labels);width=(8.8-.35*(n-1))/n
 for i,(l,d) in enumerate(zip(labels,dimensions)):
  x=.3+i*(width+.35)
  body+=rf'\filldraw[fill={COLORS[i%3]}!12,draw={COLORS[i%3]}]({x},1.35) rectangle({x+width},3.45);\node[pLabel] at({x+width/2},2.6){{$ {l} $}};\node[pNote] at({x+width/2},1.85){{$ {d} $}};'
  if i<n-1:body+=rf'\node[pLabel] at({x+width+.175},2.4){{'+('$'+operators[i]+'$' if operators else ('$=$' if i==0 else r'$\times$'))+'};'
 if caption:body+=rf'\node[pNote,text width=8.5cm] at(4.7,.45){{{caption}}};'
 return tk(body,h=4.0)
def variance_plot(cumulative=False,loss=False):
 rr=table('variance.csv')
 out,X,Y=axes(.4,8.7,0,100 if cumulative else 60,xlabel='Componente',ylabel=r'Varianza (\%)',xticks=range(1,9),yticks=[0,20,40,60] if not cumulative else [0,50,100],h=4.6)
 for r in rr:
  j=int(r['PC']);val=100*float(r['quota']);c='GeoA' if j<=2 else 'GeoB'
  out.append(rf'\fill[{c}!65]({X(j-.32):.3f},{Y(0):.3f}) rectangle({X(j+.32):.3f},{Y(val):.3f});')
 if cumulative:line(out,X,Y,[(int(r['PC']),100*float(r['cumulata'])) for r in rr],'GeoC')
 out.append(r'\end{tikzpicture}');return '\n'.join(out)
def rotations_chart():
 rr=table('pca_rotation.csv');out=[]
 for i,r in enumerate(rr):
  y=4.4-.48*i;val=float(r['PC1']);x=6.1+4.4*val
  out.append(rf'\node[pNote,anchor=east] at(2.8,{y}){{{LABELS[r["variabile"]]}}};\draw[Rule](3.6,{y})--(8.6,{y});\fill[GeoA!65]({min(6.1,x):.3f},{y-.12}) rectangle({max(6.1,x):.3f},{y+.12});')
 out+= [r'\draw[Muted](6.1,.7)--(6.1,4.75);\node[pNote] at(6.1,.35){0};\draw[Muted](3.9,.7)--(3.9,.6);\draw[Muted](8.3,.7)--(8.3,.6);\node[pNote] at(3.9,.35){$-0{,}5$};\node[pNote] at(8.3,.35){$0{,}5$};\node[pNote] at(6.1,-.05){Coefficiente della rotazione, PC1};']
 return tk('\n'.join(out),h=4.9)
def correlations_circle():
 rr=table('pca_correlations.csv');cx=4.65;cy=2.4;sc=1.75
 body=rf'\draw[Rule]({cx-sc-.15},{cy})--({cx+sc+.15},{cy});\draw[Rule]({cx},{cy-sc-.15})--({cx},{cy+sc+.15});\draw[Muted]({cx},{cy}) circle({sc});'
 labels={'SiO2':(2.8,.8,'east'),'CaO':(6.75,3.8,'west'),'MgO':(2.5,3.75,'east'),'FeO':(2.4,3.1,'east'),'densita':(4.0,4.55,'south'),'grana_mm':(5.2,.45,'west'),'colore':(2.4,2.4,'east'),'fossili':(6.75,2.95,'west')}
 for i,r in enumerate(rr):
  x=cx+sc*float(r['PC1']);y=cy+sc*float(r['PC2']);lx,ly,anchor=labels[r['variabile']]
  body+=rf'\draw[pEdge,draw={COLORS[i%3]}]({cx},{cy})--({x:.4f},{y:.4f});\draw[Muted,line width=.35pt]({x:.4f},{y:.4f})--({lx},{ly});\node[pNote,anchor={anchor},fill=Paper,inner sep=1pt,text={COLORS[i%3]}] at({lx},{ly}){{{LABELS[r["variabile"]]}}};'
 body+=rf'\node[pNote] at({cx},-.08){{Correlazione con PC1}};\node[pNote,rotate=90] at(.55,{cy}){{Correlazione con PC2}};'
 return tk(body,h=4.85)
def reconstruction_plot():
 orig=table('standardized.csv');rec=table('reconstruction_Z2.csv')
 values=[float(r[v]) for rows in [orig,rec] for r in rows for v in VARIABLES]
 low=math.floor(min(values));high=math.ceil(max(values))
 out,X,Y=axes(low,high,low,high,xlabel='Valori standardizzati',ylabel='Ricostruzione con 2 PC',xticks=range(low,high+1,2),yticks=range(low,high+1,2),equal=True,h=4.7)
 line(out,X,Y,[(low,low),(high,high)],'Muted','dashed')
 for a,b in zip(orig,rec):
  for v in VARIABLES:
   x=float(a[v]);y=float(b[v]);out.append(rf'\fill[GeoA,opacity=.4]({X(x):.4f},{Y(y):.4f}) circle(.8pt);')
 out.append(r'\end{tikzpicture}');return '\n'.join(out)
def curved_dependence():
 out,X,Y=axes(-2.2,2.2,-.2,4.4,xlabel='$x$',ylabel='$y=x^2$',xticks=[-2,0,2],yticks=[0,2,4],h=4.65,equal=True)
 for i in range(41):
  x=-2+i*.1;y=x*x
  out.append(rf'\fill[GeoA]({X(x):.4f},{Y(y):.4f}) circle(1.7pt);')
 out.append(r'\end{tikzpicture}');return '\n'.join(out)

S(27,'La nuvola dei campioni ha direzioni privilegiate',cloud()+r'\PBody{Esempio didattico con due variabili centrate: i punti occupano una fascia inclinata. Una direzione lungo la fascia ne conserva gran parte della variabilità.}',r'''
\PLabel{Rappresentare con meno coordinate}
\PBody{La PCA cerca assi nuovi attraverso il centro della nuvola. La prima direzione massimizza la varianza delle coordinate proiettate.}
\vspace{4mm}
\PInfo{La PCA considera congiuntamente le variabili selezionate. Non richiede una risposta da prevedere.}
\vspace{3mm}
\[\mathbf z_i\in\mathbb R^p\quad\longmapsto\quad t_i\in\mathbb R.\]
''','Una componente principale è una coordinata costruita dalle variabili della matrice centrata.')

S(28,'Il prodotto scalare dà una coordinata',vector_projection()+r'\PBody{Il vettore unitario $\mathbf v=(0{,}8;0{,}6)$ fissa una direzione. Il prodotto scalare misura la coordinata di $\mathbf z$ lungo quella direzione.}',r'''
\[t=\mathbf z^\top\mathbf v.\]
\[t=2(0{,}8)+1(0{,}6)=2{,}2.\]
'''+C(28,'prodotto_scalare','''
z_es <- c(2, 1)
v_es <- c(0.8, 0.6)
sum(v_es^2)  # norma unitaria
t_es <- sum(z_es * v_es)
t_es
''','calcolare uno score')+r'\PSmall{Il simbolo $t$ indica una coordinata scalare, non un vettore nel piano.}','Lo score è il prodotto scalare fra la riga centrata e una direzione unitaria.')

S(29,'La proiezione torna nello spazio delle misure',vector_projection(True)+r'\PBody{Moltiplicando lo score per la direzione si ricostruisce la proiezione. Lo scarto residuo è ortogonale all’asse.}',r'\[\widehat{\mathbf z}=t\mathbf v,\qquad \mathbf r=\mathbf z-t\mathbf v.\]'+C(29,'proiezione','''
z_hat <- t_es * v_es
res_es <- z_es - z_hat
z_hat
# Proiezione e residuo sono ortogonali.
sum(res_es * v_es)
''','controllare l’ortogonalità')+r'\PInfo{Nel diagramma: $\widehat{\mathbf z}=(1{,}76;1{,}32)$ e $\mathbf r=(0{,}24;-0{,}32)$.}','La proiezione è un vettore; lo score ne è la coordinata sull’asse scelto.')

S(30,'Ruotare l’asse cambia la varianza',rotating_variance()+r'\PBody{La stessa nuvola didattica viene proiettata su assi con angoli diversi. La direzione del massimo conserva la maggiore varianza in una coordinata.}',r'''
\[\mathbf v(\theta)=(\cos\theta,\sin\theta).\]
\[t_i(\theta)=\mathbf z_i^\top\mathbf v(\theta).\]
\PBody{Invertire l’asse di $180^\circ$ cambia il segno degli scores, ma conserva la loro varianza.}
\vspace{4mm}
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m08-pca-geometria}{Esperimento · ruotare un asse}
\PInfo{Il diagramma descrive l’esempio bidimensionale; la PCA delle rocce sarà calcolata sulle otto colonne.}
''','La prima componente massimizza la varianza proiettata nella scala scelta.')

S(31,'La covarianza descrive la varianza proiettata',matrix_factor(['(n-1)S',r'Z^\top','Z'],[r'p\times p',r'p\times n',r'n\times p'],r'Il prodotto è diviso per $n-1$; le colonne di $Z$ sono centrate')+r'\[S=\frac{Z^\top Z}{n-1}.\]',r'\[\operatorname{Var}(Z\mathbf v)=\mathbf v^\top S\mathbf v.\]'+C(31,'covarianza','''
S <- crossprod(Z) / (nrow(Z) - 1)
max(abs(S - cov(Z)))
# Su colonne standardizzate, S è
# anche la matrice di correlazione.
max(abs(S - cor(X)))
''','costruire la forma quadratica')+r'\PSmall{Il divisore $n-1$ è quello della covarianza campionaria usata in questa lezione.}','La forma quadratica combina varianze e covarianze nella direzione scelta.')

S(32,'La norma unitaria rende definito il massimo',tk(r'''
\draw[Muted](4.5,2.5) circle(1.7);
\draw[pAxis](2.4,2.5)--(6.65,2.5);\draw[pAxis](4.5,.35)--(4.5,4.65);
\draw[pEdge](4.5,2.5)--(5.86,3.52);\fill[GeoA](5.86,3.52) circle(2.8pt);
\node[pLabel,anchor=west] at(6.1,3.75){$\|\mathbf v\|=1$};
\node[pNote] at(4.5,.02){Nel piano, le direzioni unitarie giacciono su una circonferenza};
''',h=4.9)+r'\PBody{Senza un vincolo sulla lunghezza, moltiplicare $\mathbf v$ per una costante farebbe crescere arbitrariamente la varianza degli scores.}',r'''
\[\max_{\mathbf v^\top\mathbf v=1}\mathbf v^\top S\mathbf v.\]
\PBody{Con il moltiplicatore $\lambda$ si considera}
\[L(\mathbf v,\lambda)=\mathbf v^\top S\mathbf v-\lambda(\mathbf v^\top\mathbf v-1).\]
\PInfo{Il vincolo permette di confrontare orientamenti, mantenendo la stessa lunghezza del vettore.}
''','Il problema di massimo confronta direzioni unitarie, non vettori di lunghezza arbitraria.')

S(33,'Autovettore e autovalore emergono dal massimo',cloud(33,True)+r'\PBody{Nella direzione ottimale, la matrice di covarianza moltiplica il vettore per un fattore scalare. Quel fattore è la varianza della componente.}',r'''
\[\nabla_{\mathbf v}L=2S\mathbf v-2\lambda\mathbf v=0.\]
\[S\mathbf v=\lambda\mathbf v.\]
\[\mathbf v^\top S\mathbf v=\lambda\quad(\|\mathbf v\|=1).\]
\PBody{La prima componente usa l’autovettore associato al maggiore autovalore. Gli altri autovalori descrivono la varianza lungo gli assi successivi.}
\PInfo{Il disegno illustra una proiezione su un asse vicino alla direzione principale dell’esempio.}
''','L’autovalore misura la varianza dello score; l’autovettore definisce la direzione.')

S(34,'La seconda direzione è ortogonale alla prima',tk(r'''
\draw[pAxis](1,2.4)--(8,2.4);\draw[pAxis](4.5,.25)--(4.5,4.55);
\draw[pEdge,draw=Classical,line width=1.5pt](4.5,2.4)--(6.5,3.9);
\draw[pEdge,draw=GeoB,line width=1.5pt](4.5,2.4)--(3.0,4.4);
\node[pLabel,anchor=west] at(6.7,4.0){$\mathbf v_1$};\node[pLabel,anchor=east] at(2.85,4.45){$\mathbf v_2$};
\node[pNote] at(4.5,.05){Direzioni illustrative: $(0{,}8;0{,}6)$ e $(-0{,}6;0{,}8)$};
''',h=4.75)+r'\PBody{La seconda componente massimizza la varianza rimasta fra le direzioni ortogonali alla prima. La scala grafica conserva gli angoli retti.}',r'\[\mathbf v_1^\top\mathbf v_2=0,\qquad\|\mathbf v_2\|=1.\]'+C(34,'ortogonali','''
v2_es <- c(-0.6, 0.8)
sum(v_es * v2_es)
sum(v2_es^2)
# Due direzioni per descrivere il piano.
''','verificare due assi'),'Le componenti successive massimizzano la varianza imponendo l’ortogonalità alle precedenti.')

S(35,'Otto variabili producono otto coordinate principali',matrix_factor(['T','Z','V'],[r'90\times8',r'90\times8',r'8\times8'],'Ogni colonna di V è una direzione; ogni riga di T è un campione')+r'\PBody{Con tutti gli assi, la rotazione cambia le coordinate e conserva distanze e informazione. La riduzione di dimensione avviene quando si omettono componenti.}',r'''
\[T=ZV,\qquad V^\top V=I.\]
\[\|\mathbf z_i-\mathbf z_h\|^2=\|\mathbf t_i-\mathbf t_h\|^2.\]
\PInfo{In questo caso $n=90>p=8$. Un rango ridotto o un numero minore di campioni può limitare le componenti non nulle.}
''','Ruotare tutti gli assi e conservare soltanto pochi assi sono operazioni diverse.')

S(36,'La SVD calcola la stessa geometria',matrix_factor(['Z','U','D',r'V^\top'],[r'90\times8',r'90\times8',r'8\times8',r'8\times8'],r'SVD ridotta: $U$ ha colonne ortonormali e $D$ è diagonale')+r'\[Z=UDV^\top,\qquad\lambda_k=\frac{d_k^2}{n-1}.\]',C(36,'svd','''
# d contiene i valori singolari.
sv <- svd(Z)
lambda_svd <- sv$d^2 / (nrow(Z) - 1)
lambda_svd
max(abs(crossprod(sv$v) - diag(8)))
''','calcolare i valori singolari')+r'\PInfo{La funzione \texttt{prcomp} usa la SVD della matrice centrata e, se richiesto, ridimensionata.}','I quadrati dei valori singolari, divisi per n−1, sono le varianze delle componenti.')

S(37,'Scores e direzioni hanno ruoli diversi',matrix_factor(['T','Z','V'],[r'n\times p',r'n\times p',r'p\times p'],r'$T$ descrive i campioni; $V$ descrive la costruzione degli assi')+r'\[t_{ik}=\sum_{j=1}^{p}z_{ij}v_{jk}.\]',r'''
\PBody{Lo score del campione $i$ sulla componente $k$ è una combinazione lineare delle sue otto misure standardizzate.}
\vspace{3mm}
\PInfo{Una riga di $T$ identifica una roccia. Una riga di $V$ riguarda una variabile originaria. Confondere le due matrici cambia il significato del grafico.}
\vspace{3mm}
\[T=UD\qquad\text{dalla SVD di }Z.\]
''','Gli scores localizzano i campioni; i coefficienti della rotazione definiscono le componenti.')

S(38,'L’oggetto PCA conserva la trasformazione',pca_plot()+r'\PBody{Questa è la PCA delle otto proprietà delle rocce. Centratura e standardizzazione sono richieste esplicitamente nella chiamata.}',C(38,'prcomp','''
pc <- prcomp(X, center = TRUE,
             scale. = TRUE)
head(pc$x[, 1:2])  # scores
pc$rotation[, 1:2] # direzioni
pc$center          # medie
pc$scale           # deviazioni standard
''','stimare la PCA')+r'\PInfo{Il campo \texttt{sdev} contiene le deviazioni standard delle componenti. Le varianze si ottengono elevandole al quadrato.}','L’oggetto stimato conserva i parametri necessari a trasformare altri campioni.')

S(39,'Autovalori, SVD e risultato di R',variance_plot()+r'\PBody{I primi due autovalori sono circa $4{,}406$ e $2{,}521$. La loro somma descrive gran parte della varianza totale, pari a otto.}',C(39,'autovalori','''
lam <- pc$sdev^2
lam
sum(lam) # otto colonne di varianza 1
max(abs(lam - lambda_svd))
# Il confronto controlla la convenzione n-1.
''','confrontare le varianze')+r'\[\operatorname{tr}(S)=\sum_k\lambda_k=p=8.\]','Le varianze delle componenti si sommano alla varianza totale della matrice analizzata.')

S(40,'Gli scores sono incorrelati nel campione di stima',tk(r'''
\node[pLabel] at(4.6,4.35){$\operatorname{Cov}(T)$};
\foreach \i in {0,...,4}{\foreach \j in {0,...,4}{\pgfmathtruncatemacro{\d}{\i==\j}\ifnum\d=1\fill[GeoA!65](2.9+.62*\j,3.55-.62*\i) rectangle(3.48+.62*\j,4.13-.62*\i);\else\fill[white](2.9+.62*\j,3.55-.62*\i) rectangle(3.48+.62*\j,4.13-.62*\i);\fi}}
\node[pNote,text width=8.4cm] at(4.6,.65){Schema della diagonale: varianze positive; covarianze fuori diagonale nulle};
''',h=4.75)+r'\[\operatorname{Cov}(T)=V^\top S V=\operatorname{diag}(\lambda_1,\ldots,\lambda_p).\]',C(40,'scores_covarianza','''
T <- pc$x
cov_T <- cov(T)
max(abs(cov_T - diag(lam)))
# Le piccole differenze sono numeriche.
''','verificare la covarianza')+r'\PBody{La proprietà riguarda la matrice usata per stimare gli assi. Un nuovo insieme può mostrare covarianze differenti.}','La rotazione principale diagonalizza la covarianza del campione di stima.')

S(41,'Incorrelazione e indipendenza',curved_dependence()+r'\PInfo{Gli stessi punti del codice R mostrano una dipendenza curva con correlazione campionaria nulla.}',r'\[Y=X^2,\qquad X\text{ simmetrico attorno a }0.\]'+C(41,'dipendenza_curva','''
# Relazione deterministica non lineare.
u <- seq(-2, 2, length.out = 41)
y_curva <- u^2
cor(u, y_curva)
plot(u, y_curva, pch = 19,
  xlab = "x", ylab = "x^2")
''','riconoscere una dipendenza')+r'\PBody{Conoscere $X$ determina $Y$, anche se la covarianza è zero. L’indipendenza richiede condizioni ulteriori.}','La covarianza diagonale degli scores non dimostra indipendenza probabilistica.')

S(42,'Il segno di una componente è arbitrario',tk(r'''
\draw[pEdge,draw=GeoA,line width=1.7pt](1.7,1.1)--(7.5,4.0);
\draw[pEdge,draw=GeoB,line width=1.7pt](7.35,3.65)--(1.55,.75);
\node[pLabel] at(7.75,4.2){$\mathbf v_k$};\node[pLabel] at(1.15,.45){$-\mathbf v_k$};
\node[pLabel,fill=Paper] at(4.7,2.4){$\mathbf t_k\mathbf v_k^\top=(-\mathbf t_k)(-\mathbf v_k)^\top$};
''',h=4.7)+r'\PBody{L’inversione congiunta di direzione e scores lascia invariata la ricostruzione. Un grafico specchiato può rappresentare la stessa PCA.}',C(42,'segno','''
# Ricostruzione della sola PC1.
R1 <- pc$x[, 1] %o% pc$rotation[, 1]
R1_opposta <- (-pc$x[, 1]) %o%
              (-pc$rotation[, 1])
max(abs(R1 - R1_opposta))
''','invertire asse e coordinate')+r'\PInfo{Il segno dei coefficienti descrive contrasti fra variabili all’interno della stessa convenzione.}','Cambiare il segno di un asse non cambia varianze, distanze o ricostruzione.')

S(43,'Autovalori vicini e direzioni poco stabili',tk(r'''
\draw[Muted,fill=GeoA!8](4.6,2.45) ellipse(2.3 and 1.9);
\draw[pEdge,draw=GeoA](4.6,2.45)--(6.8,2.45);\draw[pEdge,draw=GeoA](4.6,2.45)--(4.6,4.25);
\draw[pEdge,draw=GeoB,dashed](4.6,2.45)--(6.5,3.55);\draw[pEdge,draw=GeoB,dashed](4.6,2.45)--(3.7,4.0);
\node[pNote,text width=8.5cm] at(4.6,.08){Schema: una nuvola quasi circolare distingue debolmente i due orientamenti};
''',h=4.7)+r'\PBody{Quando due autovalori sono uguali, più basi ortonormali descrivono lo stesso sottospazio. Se sono vicini, piccole perturbazioni possono ruotare gli assi.}',r'''
\[\lambda_k\simeq\lambda_{k+1}.\]
\PBody{La stabilità del piano può essere maggiore della stabilità dei suoi singoli vettori. Il confronto fra PCA richiede attenzione ai sottospazi e ai segni.}
\vspace{3mm}
\PInfo{Un nome geologico attribuito a una singola componente va sostenuto dai coefficienti e dalla loro stabilità.}
''','La stabilità di una rappresentazione non si valuta soltanto confrontando il segno dei coefficienti.')

S(44,'PCA e regressione minimizzano scarti diversi',tk(r'''
\draw[pAxis](.6,.6)--(8.7,.6);\draw[pAxis](.6,.6)--(.6,4.4);
\draw[Classical,line width=1.3pt](1.2,1)--(7.8,3.8);
\fill[GeoA](4.8,3.85) circle(3pt);
\draw[GeoB,line width=1.25pt](4.8,3.85)--(4.8,2.5273);
\draw[GeoC,line width=1.25pt](4.8,3.85)--(5.2756,2.7290);
\node[pNote,anchor=east] at(4.6,3.2){Scarto verticale};
\node[pNote,anchor=west] at(5.65,3.65){Scarto ortogonale};
\node[pNote] at(4.7,.1){Schema sullo stesso sistema di coordinate};
''',h=4.7)+r'\PBody{La regressione ordinaria distingue risposta e predittore. La PCA cerca una rappresentazione della nuvola nella metrica dichiarata.}',r'''
\PLabel{Regressione lineare semplice}
\[\min_{a,b}\sum_i(y_i-a-bx_i)^2.\]
\PLabel{PCA con una componente}
\[\min_{\|\mathbf v\|=1}\sum_i\|\mathbf z_i-(\mathbf z_i^\top\mathbf v)\mathbf v\|^2.\]
\PInfo{Le due rette possono differire. Scambiando le coordinate, cambia il problema della regressione ordinaria.}
''','La PCA rappresenta la variabilità congiunta; la regressione ordinaria modella una risposta condizionata.')

S(45,'Quanta varianza conserva ogni componente?',variance_plot()+r'\PBody{Nel caso delle rocce, PC1 conserva il $55{,}1\%$ e PC2 il $31{,}5\%$ della varianza standardizzata. Le altre sei componenti conservano la parte restante.}',r'\[q_k=\frac{\lambda_k}{\sum_\ell\lambda_\ell}.\]'+C(45,'quote','''
quota <- pc$sdev^2 / sum(pc$sdev^2)
data.frame(PC = 1:8,
  quota = quota, cumulata = cumsum(quota))
''','calcolare le quote')+r'\PInfo{La percentuale riguarda la matrice trasformata. Una diversa scala delle colonne può cambiare le quote.}','La varianza spiegata va riferita alla matrice e alla scala effettivamente analizzate.')

S(46,'La cumulata orienta la scelta delle dimensioni',variance_plot(True)+r'\PBody{Le prime due componenti conservano l’$86{,}6\%$; tre arrivano al $92{,}0\%$. Aggiungere componenti riduce la perdita di ricostruzione.}',r'\[Q_q=\sum_{k=1}^{q}q_k.\]'+C(46,'cumulata','''
barplot(100 * quota, names.arg = 1:8,
  xlab = "Componente",
  ylab = "Varianza (%)")
cumsum(quota)
''','leggere lo spettro')+r'\PInfo{Una soglia percentuale è un criterio di sintesi. La scelta dipende anche dalle proprietà che occorre rappresentare.}','Il numero di componenti si motiva con perdita, leggibilità e scopo dell’analisi.')

S(47,'Il piano principale è una proiezione',pca_plot()+r'\PBody{Due punti vicini in figura possono differire su componenti escluse. La distanza proiettata non può superare quella nello spazio completo.}',r'\[\sum_{k=1}^{2}(t_{ik}-t_{hk})^2\leq\sum_{k=1}^{8}(t_{ik}-t_{hk})^2.\]'+C(47,'distanze_proiezione','''
DT <- as.matrix(dist(pc$x))
D2 <- as.matrix(dist(pc$x[, 1:2]))
max(D2 - DT)
# Differenza non positiva, salvo
# arrotondamenti numerici.
''','confrontare le distanze')+r'\PSmall{Gli assi riportano le quote di varianza. Nel disegno, un’unità su PC1 ha la stessa lunghezza di un’unità su PC2.}','La vicinanza nella proiezione non esclude differenze lungo le componenti omesse.')

S(48,'I coefficienti costruiscono una componente',rotations_chart()+r'\PBody{La figura mostra i coefficienti della prima direzione. Segni concordi contribuiscono nello stesso verso; segni opposti definiscono un contrasto.}',r'\[t_{i1}=\sum_j z_{ij}v_{j1},\qquad\sum_jv_{j1}^2=1.\]'+C(48,'loadings','''
pc$rotation[, 1]
# Contributi della prima riga allo score.
a48 <- pc$rotation[, 1]
contributi_riga <- Z[1, ] * a48
sum(contributi_riga)
pc$x[1, 1]
''','ricostruire uno score'),'I coefficienti si leggono insieme ai valori standardizzati e alla convenzione di segno.')

S(49,'Coefficienti e correlazioni sono quantità diverse',matrix_factor(['C_{ZT}','V',r'\Lambda^{1/2}'],[r'8\times8',r'8\times8',r'8\times8'],r'Con variabili standardizzate e componenti di varianza positiva')+r'\[\operatorname{Cor}(Z_j,T_k)=\sqrt{\lambda_k}\,v_{jk}.\]',C(49,'correlazioni_pc','''
cor_PC <- sweep(pc$rotation, 2,
                pc$sdev, "*")
round(cor_PC[, 1:2], 3)
max(abs(cor_PC - cor(Z, pc$x)))
''','ottenere le correlazioni')+r'\PInfo{Il campo \texttt{rotation} contiene autovettori unitari. Per il cerchio delle correlazioni occorre includere la scala della componente.}','La lunghezza di una freccia dipende dalla quantità rappresentata e dalla scala adottata.')

S(50,'Il cerchio delle correlazioni descrive le variabili',correlations_circle()+r'\PBody{Le coordinate delle frecce sono le correlazioni con PC1 e PC2. Una freccia corta può indicare informazione presente soprattutto nelle altre componenti.}',r'''
\[R^2_{j,2}=\operatorname{Cor}(Z_j,T_1)^2+\operatorname{Cor}(Z_j,T_2)^2.\]
\PBody{Il valore misura quanta varianza della variabile $j$ è rappresentata nel piano. È compreso fra zero e uno.}
\vspace{3mm}
\PInfo{Gli angoli approssimano le associazioni fra variabili soltanto nella misura in cui il piano le rappresenta bene.}
''','Il cerchio riporta correlazioni: non è il grafico dei coefficienti grezzi della rotazione.')

S(51,'Contributo all’asse e qualità di rappresentazione',tk(r'''
\node[pFlow,text width=3.65cm] at(2.25,3.2){$v_{jk}^{\,2}$\\peso della variabile\\nella direzione $k$};
\node[pFlow,text width=3.65cm] at(7,3.2){$\sum_{k\leq q}\lambda_kv_{jk}^{\,2}$\\varianza di $Z_j$\\rappresentata in $q$ PC};
\node[pNote,text width=8.5cm] at(4.65,1.15){La prima somma è sulle variabili di un asse; la seconda sulle componenti di una variabile.};
''',h=4.6)+r'\PBody{I due indicatori rispondono a domande diverse. Un coefficiente elevato su un asse non riassume da solo la rappresentazione totale di una proprietà.}',C(51,'qualita','''
peso_PC1 <- pc$rotation[, 1]^2
qualita2 <- rowSums(cor_PC[, 1:2]^2)
data.frame(variabile = v,
  peso_PC1 = peso_PC1,
  rappresentata_2PC = qualita2)
''','confrontare due indicatori')+r'\[\sum_jv_{jk}^2=1,\qquad 0\leq R^2_{j,q}\leq1.\]','Ogni indicatore deve dichiarare che cosa somma e rispetto a quale totale è normalizzato.')

S(52,'Un biplot richiede una convenzione di scala',matrix_factor([r'\widehat Z_2','T_2',r'V_2^\top'],[r'90\times8',r'90\times2',r'2\times8'],r'Biplot con marcatori delle righe $T_2$ e delle colonne $V_2$')+r'\[\widehat z_{ij}^{(2)}=\mathbf t_{i,1:2}^\top\mathbf v_{j,1:2}.\]',r'''
\PBody{Il prodotto scalare fra un punto e il vettore di una variabile ricostruisce un valore standardizzato approssimato.}
\vspace{3mm}
\PInfo{Questa convenzione usa gli scores e i coefficienti. Le frecce del cerchio delle correlazioni hanno una scala diversa.}
\vspace{3mm}
\PBody{Moltiplicare i marcatori delle righe per una costante e dividere quelli delle colonne per la stessa costante conserva i prodotti, ma cambia il disegno.}
''','Punti e frecce nello stesso grafico si interpretano soltanto dopo avere dichiarato la scala del biplot.')

S(53,'Ricostruire le otto variabili con due componenti',reconstruction_plot()+r'\PBody{Ogni punto confronta un valore standardizzato con la sua ricostruzione. La diagonale corrisponde a una ricostruzione esatta.}',r'\[\widehat Z_2=T_2V_2^\top.\]'+C(53,'ricostruzione','''
Z2 <- pc$x[, 1:2, drop = FALSE] %*%
  t(pc$rotation[, 1:2, drop = FALSE])
sqrt(mean((Z - Z2)^2))
# RMSE nelle unità standardizzate.
''','ricostruire la matrice')+r'\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m08-pca-ricostruzione}{Esperimento · ricostruzione}','La riduzione a due componenti approssima tutte le colonne e conserva un errore misurabile.')

S(54,'Gli autovalori omessi misurano la perdita',variance_plot()+r'\PBody{Le sei componenti escluse conservano il $13{,}4\%$ della varianza. L’errore quadratico totale della ricostruzione è circa $95{,}51$.}',r'\[\|Z-\widehat Z_q\|_F^2=(n-1)\sum_{k>q}\lambda_k.\]'+C(54,'errore_ricostruzione','''
errore <- sum((Z - Z2)^2)
teoria <- (nrow(Z)-1) * sum(lam[3:8])
c(calcolato = errore, teoria = teoria)
errore / sum(Z^2)
''','verificare la perdita')+r'\PSmall{La norma di Frobenius al quadrato somma i quadrati di tutti gli elementi della matrice.}','La perdita di ricostruzione e la varianza esclusa sono due letture della stessa quantità.')

S(55,'Ritornare alle unità originali',matrix_factor([r'\widehat X',r'\widehat Z D_s',r'\mathbf 1\bar{\mathbf x}^{\top}'],[r'90\times8',r'90\times8',r'90\times8'],r'$D_s=\operatorname{diag}(s)$; si sommano le medie dopo la riscalatura',operators=['=','+'])+r'\PBody{L’errore torna nelle unità della proprietà. Una buona ricostruzione standardizzata può avere rilevanza diversa per densità e concentrazione.}',C(55,'unita_originali','''
X2 <- sweep(Z2, 2, pc$scale, "*")
X2 <- sweep(X2, 2, pc$center, "+")
head(cbind(originale = X[, "densita"],
  ricostruita = X2[, "densita"]))
''','invertire la trasformazione')+r'\PInfo{La ricostruzione lineare non impone vincoli fisici come positività o limiti di concentrazione.}','Una ricostruzione va controllata nelle unità e nel dominio fisico delle variabili.')

S(56,'Il numero di componenti dipende dallo scopo',tk(r'''
\node[pFlow,text width=3.6cm] at(2.3,3.3){Visualizzazione\\un piano leggibile};
\node[pFlow,text width=3.6cm] at(7.0,3.3){Ricostruzione\\errore accettabile};
\node[pFlow,text width=3.6cm] at(2.3,1.3){Analisi successiva\\distanza da preservare};
\node[pFlow,text width=3.6cm] at(7.0,1.3){Interpretazione\\proprietà rilevanti};
''',h=4.4)+r'\PBody{Una componente di varianza ridotta può contenere un contrasto scientificamente utile. La percentuale totale non ne misura automaticamente l’importanza.}',C(56,'dimensioni','''
# Perdita relativa per q = 1,...,8.
data.frame(q = 1:8,
  conservata = cumsum(quota),
  persa = 1 - cumsum(quota))
''','confrontare più dimensioni')+r'\PInfo{Se si costruiscono i cluster su poche PC, si modifica la distanza eliminando le direzioni omesse. La scelta deve essere esplicita.}','Due componenti possono bastare per una figura e non bastare per ogni analisi successiva.')

S(57,'Proiettare nuovi dati con gli assi già stimati',pca_plot()+r'\PBody{Le nuove righe usano medie, scale e rotazione dell’oggetto PCA. Le colonne devono corrispondere alle variabili della stima.}',C(57,'predict_pca','''
# Esempio su righe già presenti:
# verifica della trasformazione.
scores_nuovi <- predict(pc, X[1:3, ])
max(abs(scores_nuovi - pc$x[1:3, ]))
# Per veri nuovi campioni mantenere
# nomi, unità e ordine delle variabili.
''','applicare la trasformazione')+r'\[T_{\rm nuovo}=Z_{\rm nuovo}V.\]'+r'\PInfo{Ristimare la PCA sull’insieme ampliato cambia il riferimento. Proiettare e ristimare sono operazioni distinte.}','La rappresentazione dei nuovi campioni usa i parametri dell’oggetto stimato.')
