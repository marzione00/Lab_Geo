from diagram_helpers import *
SLIDES={}; CODES={}
def S(n,title,left,right,recall):
 sec='I · CAMPIONI, SCALE E DISTANZE' if n<=14 else 'II · RIDONDANZA E COMPOSIZIONI'
 SLIDES[n]=dict(title=title,section=sec,left=left,right=right,recall=recall)
def C(n,name,src,title):
 key=f'{n:03}_{name}.R';CODES[key]=src.strip()+'\n';return rf'\PCode{{R · {title}}}{{{key}}}'
def matrix_view(z=False):
 rows=table('standardized.csv') if z else DATA
 vars=['SiO2','CaO','densita','grana_mm'];heads=[r'SiO$_2$',r'CaO',r'Densità',r'Grana']
 body=r'\node[pNote,anchor=west] at(.3,4.3){Estratto: 4 colonne delle 8 selezionate};'
 for j,name in enumerate(heads):body+=rf'\node[pLabel] at({2.7+1.7*j},3.7){{{name}}};'
 for i,idx in enumerate([0,1,30,60]):
  y=3.0-i*.68;row=rows[idx]
  body+=rf'\node[pNote,anchor=west] at(.3,{y}){{{row["id"]}}};'
  for j,vv in enumerate(vars):
   val=float(row[vv]);col=('GeoA' if val>=0 else 'GeoB') if z else 'Classical'
   body+=rf'\fill[{col}!12]({1.95+1.7*j},{y-.25}) rectangle({3.45+1.7*j},{y+.25});\node[pNote,text=Ink] at({2.7+1.7*j},{y}){{$ {it(val,2)} $}};'
 body+=r'\node[pNote] at(4.8,.12){Ogni riga conserva l’identificativo del campione};'
 return tk(body,h=4.6)
def distance_geom(weighted=False):
 body=r'\draw[pAxis](.7,.5)--(8.7,.5);\draw[pAxis](.7,.5)--(.7,4.6);'
 body+=r'\fill[GeoA](2,1.2) circle(3pt);\fill[GeoB](6.5,3.6) circle(3pt);\node[pLabel,above left] at(2,1.2){$i$};\node[pLabel,above] at(6.5,3.6){$h$};'
 body+=r'\draw[Muted,dashed](2,1.2)--(6.5,1.2)--(6.5,3.6);\draw[Classical,line width=1.6pt](2,1.2)--(6.5,3.6);\node[pLabel,fill=Paper] at(4.25,2.7){$d(i,h)$};'
 body+=r'\node[pNote] at(4.2,.82){$x_{h1}-x_{i1}$};\node[pNote,anchor=west] at(6.7,2.25){$x_{h2}-x_{i2}$};\node[pNote] at(4.7,.08){Schema con due coordinate numeriche};'
 if weighted:
  body=body.replace('$d(i,h)$','$d_w(i,h)$').replace('$x_{h1}-x_{i1}$',r'$\sqrt{w_1}(z_{h1}-z_{i1})$').replace('$x_{h2}-x_{i2}$',r'$\sqrt{w_2}(z_{h2}-z_{i2})$')
 return tk(body,h=4.8)
def scales_diagram():
 body=''
 for k,sy in enumerate([.13,1.]):
  dx=.4+4.7*k
  body+=rf'\draw[pAxis]({dx+.3},.6)--({dx+4},.6);\draw[pAxis]({dx+.3},.6)--({dx+.3},3.7);'
  for j in range(25):
   u=math.sin(j*2.31);v=math.cos(j*1.73)
   body+=rf'\fill[GeoA]({dx+2+1.5*u:.3f},{2.1+1.25*v*sy:.3f}) circle(1.4pt);'
  body+=rf'\node[pLabel] at({dx+2},4.1){{'+('Scala iniziale' if k==0 else 'Scala ampliata')+'};'
 body+=r'\node[pNote] at(4.8,.1){Schema: cambiare le scale cambia la geometria};'
 return tk(body,h=4.5)
def three_boxes(labels,caption='',colors=None):
 body='';colors=colors or ['Classical','GeoB','GeoC']
 for i,label in enumerate(labels):
  x=1.55+3.15*i
  body+=rf'\node[pFlow,draw={colors[i]}!70,text width=2.45cm,minimum height=1.55cm] at({x},2.7){{{label}}};'
 if caption:body+=rf'\node[pLabel,text width=8.6cm] at(4.7,.9){{{caption}}};'
 return tk(body,h=4.2)
def composition_triangle():
 h=4.05;body=rf'\filldraw[fill=GeoA!7,draw=Muted,line width=.8pt](2,.35)--(7,.35)--(4.5,{.35+h})--cycle;'
 body+=r'\node[pLabel] at(1.65,.2){$A$};\node[pLabel] at(7.35,.2){$B$};\node[pLabel] at(4.5,4.7){$C$};'
 vals=[(.6,.2,.2),(.2,.6,.2),(.2,.2,.6)]
 for i,(a,b,c) in enumerate(vals):
  x=2*a+7*b+4.5*c;y=.35+h*c
  anchor=['east','west','south'][i];dx=[-.15,.15,0][i];dy=[-.12,-.12,.18][i]
  body+=rf'\fill[{COLORS[i]}]({x},{y}) circle(3pt);\node[pNote,anchor={anchor}] at({x+dx},{y+dy}){{$({it(a,1)};{it(b,1)};{it(c,1)})$}};'
 body+=r'\node[pNote] at(4.5,-.12){Tre parti illustrative: $A+B+C=1$};'
 return tk(body,h=4.9)

S(2,'Quali campioni si somigliano?',r'\PLabel{Una stessa matrice, più proprietà}'+pca_plot()+r'\PSmall{I punti rappresentano le 90 rocce sintetiche proiettate sulle prime due componenti. I colori dei gruppi non sono ancora assegnati.}',r'''
\PBody{Ogni roccia è descritta da otto misure. La somiglianza dipende da quali proprietà confrontiamo e da come misuriamo le loro differenze.}
\vspace{4mm}
\[\mathbf x_i=(x_{i1},\ldots,x_{i8}).\]
\PInfo{La domanda della lezione: quali strutture persistono quando cambiamo rappresentazione, variabili o criterio di raggruppamento?}
\vspace{3mm}
\PBody{PCA e clustering richiedono scelte esplicite. L’interpretazione geologica viene discussa attraverso queste scelte.}
''','Una struttura multivariata si interpreta insieme alle misure e alla geometria che l’hanno prodotta.')

S(3,'Novanta rocce, otto proprietà',three_boxes([r'Ossidi\\SiO$_2$, CaO\\MgO, FeO',r'Proprietà fisiche\\densità\\granulometria',r'Indici simulati\\colore\\fossili'],'Dati sintetici del corso: ogni campione mantiene il proprio ID')+r'\PBody{Il dataset comprende 90 campioni. Le etichette generatrici sono Basalto, Arenaria e Calcare: trenta casi per gruppo.}',C(3,'dati','''
# Aprire il progetto Polychroma_M08.
source("setup.R", encoding = "UTF-8")
dim(d)
head(d[, c("id", "SiO2", "densita")])
# Un identificativo per campione.
stopifnot(!anyDuplicated(d$id))
''','leggere i campioni')+r'\PInfo{Colore e fossili sono indici convenzionali del simulatore. I valori non descrivono misure di un affioramento reale.}','Il significato di ogni colonna e la provenienza sintetica dei dati devono accompagnare l’analisi.')

S(4,'La matrice conserva le righe dei campioni',matrix_view()+r'\[X=(x_{ij})\in\mathbb R^{90\times8}.\]',r'''
\PBody{L’indice $i$ identifica il campione; $j$ identifica la variabile. Una riga confronta più proprietà della stessa roccia.}
\vspace{4mm}
\PInfo{Una colonna contiene misure omogenee per definizione e unità. L’identificativo rimane esterno alla matrice numerica.}
\vspace{3mm}
\PBody{Conservare l’ordine delle righe consente di ricongiungere coordinate principali, gruppi e osservazioni originali.}
''','Il punto nello spazio multivariato corrisponde a una riga identificabile della tabella.')

S(5,'Le unità definiscono le coordinate',three_boxes([r'Ossidi\\percentuale in massa',r'Densità\\g/cm$^3$',r'Granulometria\\mm'],'Otto colonne numeriche possono avere scale e significati diversi')+r'\PBody{Una differenza di dieci punti percentuali e una differenza di un grammo per centimetro cubo non hanno un peso naturale comune.}',r'''
\[\mathbf x_i=(\text{SiO}_2,\ldots,\rho,g,c,f)_i.\]
\PBody{La somma dei quadrati combina valori numerici. Le conversioni di unità possono modificare il contributo di una proprietà alla distanza.}
\vspace{3mm}
\PInfo{Prima della standardizzazione, occorre stabilire quali differenze scientifiche debbano contare nella somiglianza.}
''','Una distanza fra variabili eterogenee incorpora una scelta di scala e di rilevanza.')

S(6,'Misure, identificativi ed etichette',three_boxes([r'ID\\ricollegare i risultati',r'Otto misure\\costruire $X$',r'Litologia generatrice\\confrontare a posteriori'],'Soltanto il blocco centrale entra nella matrice di analisi')+r'\PBody{L’etichetta del simulatore è tenuta separata. Usarla come una coordinata introdurrebbe la risposta attesa nel criterio di somiglianza.}',C(6,'etichette','''
# Colonne con ruoli diversi.
id <- d$id
etichette <- d$litologia_generatrice
X <- as.matrix(d[v])
stopifnot(!"id" %in% colnames(X),
  !"litologia_generatrice" %in%
    colnames(X))
''','separare i ruoli')+r'\PSmall{Le etichette potranno colorare un grafico già calcolato o alimentare una tabella di confronto.}','Una variabile usata per interpretare il risultato può restare esclusa dal calcolo dei gruppi.')

S(7,'Selezionare le variabili per nome',matrix_view()+r'\PBody{La selezione esplicita rende leggibile la scelta delle proprietà. L’ordine delle colonne è conservato nelle trasformazioni successive.}',C(7,'matrice','''
# Evitare selezioni per posizione.
v <- c("SiO2", "CaO", "MgO", "FeO",
       "densita", "grana_mm",
       "colore", "fossili")
X <- as.matrix(d[v])
stopifnot(all(is.finite(X)),
  all(apply(X, 2, sd) > 0))
dim(X)
''','costruire la matrice')+r'\PInfo{I controlli numerici verificano completezza e variabilità. La scelta scientifica delle colonne richiede comunque una motivazione.}','Un dataset leggibile da R può ancora contenere colonne inappropriate per la domanda.')

S(8,'La scala cambia la geometria',scales_diagram()+r'\PBody{Moltiplicare una coordinata per mille allunga la nuvola lungo quell’asse. Le distanze grezze cambiano anche se la proprietà fisica è la stessa.}',C(8,'unita','''
# Stessa granulometria: mm oppure um.
a <- X[, c("SiO2", "grana_mm")]
b <- a
b[, "grana_mm"] <- 1000 * b[, "grana_mm"]
c(mm = as.numeric(dist(a))[1],
  um = as.numeric(dist(b))[1])
''','convertire una sola unità')+r'\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m08-standardizzazione}{Esperimento · scale e distanze}','Una conversione differente fra colonne cambia la distanza euclidea grezza.')

S(9,'La distanza euclidea combina gli scarti',distance_geom()+r'\PBody{Nel piano, il teorema di Pitagora collega gli scarti lungo due assi alla lunghezza del segmento. La stessa somma si estende a otto coordinate.}',r'''
\[d(i,h)^2=\sum_{j=1}^{p}(x_{ij}-x_{hj})^2.\]
\PBody{$i$ e $h$ sono due campioni; $p=8$ è il numero delle variabili. Ogni scarto entra al quadrato.}
'''+C(9,'distanza','''
# Due righe della matrice originale.
scarti <- X[1, ] - X[2, ]
sqrt(sum(scarti^2))
# Stesso valore nella matrice distanze.
as.matrix(dist(X))[1, 2]
''','calcolare una distanza'),'Prima di interpretare una distanza, occorre conoscere coordinate, unità e trasformazioni.')

S(10,'Centrare e dividere per la dispersione',tk(r'''
\draw[pAxis](.8,2.6)--(8.7,2.6);
\foreach \x/\t in {1.5/{-2},3.1/{-1},4.7/{0},6.3/{1},7.9/{2}}{\draw[Muted](\x,2.48)--(\x,2.72);\node[pLabel] at(\x,2.1){$\t$};}
\fill[GeoB](6.3,2.6) circle(3.5pt);
\node[pLabel] at(4.7,3.75){$x=\bar x+s\quad\longrightarrow\quad z=1$};
\node[pNote] at(4.7,1.05){Una deviazione standard diventa l’unità di confronto};
''',h=4.3)+r'\PBody{Sottrarre la media sposta l’origine. Dividere per la deviazione standard modifica la scala della colonna.}',r'''
\[z_{ij}=\frac{x_{ij}-\bar x_j}{s_j},\quad s_j>0.\]
\[\bar z_j=0,\qquad s_{z_j}=1.\]
\PBody{La standardizzazione attribuisce lo stesso peso numerico iniziale a uno scarto di una deviazione standard in ciascuna colonna.}
\PInfo{La scelta resta sensibile agli estremi e alla definizione delle variabili. Non rende uguali le forme delle distribuzioni.}
''','Lo z-score cambia origine e scala; non elimina asimmetria, dipendenza o valori atipici.')

S(11,'Conservare i parametri della standardizzazione',matrix_view(True)+r'\PBody{I numeri standardizzati sono scarti relativi alla variabilità della colonna. Le medie e le scale permettono di ritrovare le unità originali.}',C(11,'standardizzazione','''
Z <- scale(X, center = TRUE,
           scale = TRUE)
medie <- attr(Z, "scaled:center")
devstd <- attr(Z, "scaled:scale")
# Verificare la trasformazione.
round(colMeans(Z), 10)
apply(Z, 2, sd)
''','centrare e ridimensionare')+r'\[x_{ij}=\bar x_j+s_jz_{ij}.\]','Medie, scale e ordine delle colonne fanno parte del risultato dell’analisi.')

S(12,'Collocare un nuovo campione',three_boxes([r'Misure nuove\\stesse unità',r'Medie e scale\\del riferimento',r'Coordinate nuove\\nello stesso spazio'],'La trasformazione resta fissata al campione di riferimento')+r'\PBody{Ricalcolare medie e scale sul nuovo insieme cambierebbe il sistema di coordinate, rendendo incomparabili le posizioni.}',r'\[z_{\mathrm{nuovo},j}=\frac{x_{\mathrm{nuovo},j}-\bar x_j}{s_j}.\]'+C(12,'nuovo_campione','''
# Esempio di applicazione ai primi casi.
# Non sono dati nuovi indipendenti.
nuovi <- X[1:3, , drop = FALSE]
Znuovi <- scale(nuovi,
  center = medie, scale = devstd)
max(abs(Znuovi - Z[1:3, ]))
''','riutilizzare il riferimento'),'Per confrontare campioni vecchi e nuovi si applica la stessa trasformazione.')

S(13,'Valori mancanti e variabili costanti',three_boxes([r'Valori mancanti\\procedura dichiarata',r'Dispersione nulla\\divisione impossibile',r'Indice qualitativo\\distanza da motivare'],'La preparazione dipende dal processo di misura')+r'\PBody{Nel dataset didattico le otto colonne sono complete e variabili. In un rilievo reale, mancanze e limiti analitici richiedono scelte documentate.}',C(13,'controlli','''
data.frame(variabile = colnames(X),
  mancanti = colSums(is.na(X)),
  deviazione = apply(X, 2, sd))
# Un valore NA non significa zero.
# Una colonna costante non ammette z-score.
''','controllare le colonne')+r'\PInfo{Cancellare righe o imputare valori può cambiare distanze e gruppi. La modifica va valutata rispetto alla domanda e alle cause delle mancanze.}','La validità numerica della matrice precede il calcolo; la validità scientifica precede entrambe.')

S(14,'La standardizzazione conserva la correlazione',tk(r'''
\node[pFlow,text width=3.7cm] (a) at(2.2,3.05){$X_j,X_\ell$\\unità originali};
\node[pFlow,text width=3.7cm] (b) at(7.0,3.05){$Z_j,Z_\ell$\\scarti standardizzati};
\draw[pEdge](a)--(b);
\node[pLabel] at(4.6,1.65){$\operatorname{Cor}(X_j,X_\ell)=\operatorname{Cor}(Z_j,Z_\ell)$};
\node[pNote,text width=8.3cm] at(4.6,.65){Centratura e divisione per scale positive conservano le correlazioni di Pearson.};
''',h=4.3)+r'\PBody{Una forte associazione fra due colonne rimane visibile dopo lo z-score. Il problema della ridondanza richiede un esame separato.}',C(14,'correlazioni','''
# Stesse relazioni, nuove unità.
max(abs(cor(X) - cor(Z)))
round(cor(Z)[1:4, 1:4], 2)
# Zero è atteso entro l'errore numerico.
''','confrontare le correlazioni')+r'\PInfo{Media zero e varianza uno non implicano indipendenza. Due colonne standardizzate possono essere quasi identiche.}','Standardizzazione e rimozione della dipendenza rispondono a problemi diversi.')

S(15,'Una colonna duplicata pesa due volte',tk(r'''
\node[pLabel] at(4.6,3.8){Esempio: scarti standardizzati $(2,1)$};
\fill[GeoA!65](.8,2.5) rectangle(4,3.1);\fill[GeoB!65](4,2.5) rectangle(4.8,3.1);
\node[pNote,anchor=west] at(5.1,2.8){$d^2=4+1=5$};
\fill[GeoA!65](.8,1.2) rectangle(4,1.8);\fill[GeoB!65](4,1.2) rectangle(4.8,1.8);\fill[GeoA!35](4.8,1.2) rectangle(8,1.8);
\node[pNote] at(4.65,.6){Prima coordinata duplicata: $d_{\rm nuovo}^2=4+1+4=9$};
''',h=4.4)+r'\PBody{La duplicazione non aggiunge una misura indipendente. Aumenta il peso di una proprietà nella distanza complessiva.}',r'\[d_{\rm nuovo}^2=d^2+(z_{ij}-z_{hj})^2.\]'+C(15,'duplicazione','''
# Ripetere SiO2 cambia la distanza.
Zd <- cbind(Z, SiO2_copia = Z[, "SiO2"])
c(prima = as.matrix(dist(Z))[1, 2],
  dopo = as.matrix(dist(Zd))[1, 2])
''','duplicare una coordinata'),'La selezione delle colonne assegna anche pesi impliciti alle proprietà.')

S(16,'I pesi rendono esplicita la scelta',distance_geom(True)+r'\PBody{Moltiplicare una coordinata per la radice di un peso equivale a pesare il suo scarto quadratico nella distanza.}',r'''
\[d_w^2(i,h)=\sum_j w_j(z_{ij}-z_{hj})^2.\]
\PBody{Pesi positivi conservano una distanza euclidea dopo il ridimensionamento. Un peso nullo esclude una direzione dal confronto.}
'''+C(16,'pesi','''
# Esempio: dimezzare il peso di SiO2.
pesi <- rep(1, ncol(Z))
pesi[1] <- 0.5
Zw <- sweep(Z, 2, sqrt(pesi), "*")
as.matrix(dist(Zw))[1:3, 1:3]
''','applicare pesi dichiarati'),'Un peso va motivato: il calcolo rende la scelta riproducibile, non la giustifica da solo.')

S(17,'Correlazione e ridondanza delle proprietà',tk(''.join(rf'\node[pFlow,text width=3.2cm] at({2.3+4.7*(i%2)},{3.4-1.8*(i//2)}){{{t}}};' for i,t in enumerate(['Proprietà condivisa','Misure correlate','Colonna derivata','Scelta della distanza'])),h=4.4)+r'\PBody{Una correlazione elevata può riflettere un legame fisico, il processo di simulazione, una definizione comune o un vincolo di composizione.}',C(17,'ridondanza','''
# Esaminare la struttura, non una soglia sola.
R <- cor(Z)
round(R, 2)
# Gli ossidi sono una parte di una
# composizione: la chiusura conta.
''','esaminare la matrice')+r'\PInfo{L’esclusione di una misura correlata è una decisione scientifica. Va confrontata con il risultato ottenuto usando entrambe le colonne.}','La ridondanza si interpreta attraverso la definizione delle misure e l’effetto sul risultato.')

S(18,'Una relazione esatta riduce la dimensione',tk(r'''
\draw[Muted,fill=GeoA!12](1,1)--(6.9,.7)--(8.4,3.4)--(2.5,3.7)--cycle;
\foreach \x/\y in {2/1.6,3/2.1,4/1.4,5/2.6,6/2.2,7/2.9}{\fill[GeoA](\x,\y) circle(2pt);}
\node[pLabel,fill=Paper] at(4.7,4.35){$D_{\rm tot}-D_{\rm int}-2s=0$};
\node[pNote,text width=8.3cm] at(4.8,.1){Schema: tre misure vincolate giacciono su un piano};
''',h=4.7)+r'\PBody{Nel caso dei fossili di Annula, tre colonne derivano da una relazione geometrica. Il terzo asse contiene soltanto l’arrotondamento numerico.}',C(18,'fossili','''
f <- read.csv("Dati/fossili_simulati.csv")
M <- as.matrix(f[c("diametro_tot_um",
  "diametro_int_um", "spessore_um")])
max(abs(M[, 1] - M[, 2] - 2*M[, 3]))
prcomp(M, scale. = TRUE)$sdev
''','ritrovare un vincolo noto')+r'\PSmall{Lo scarto massimo è circa $10^{-8}$, coerente con l’arrotondamento delle cifre del CSV.}','La dimensione effettiva può essere inferiore al numero delle colonne.')

S(19,'Il rango distingue colonne e informazione',three_boxes([r'Tre colonne\\misure disponibili',r'Un vincolo lineare\\dipendenza esatta',r'Due direzioni\\variabilità libera'],'Una colonna derivata non crea una nuova direzione indipendente')+r'\PBody{Il rango conta le direzioni linearmente indipendenti. Nei calcoli numerici occorre distinguere uno zero esatto da un valore molto piccolo.}',r'''
\[\operatorname{rank}(Z)\leq\min(n-1,p).\]
\PBody{La centratura limita il rango a $n-1$. Ulteriori vincoli fra colonne possono ridurlo ancora.}
'''+C(19,'rango','''
sv_f <- svd(scale(M))$d
sv_f / max(sv_f)
# La terza direzione è trascurabile
# alla precisione dei dati forniti.
sum(sv_f > max(sv_f) * 1e-7)
''','valutare la dimensione numerica'),'Il numero di variabili registrate non coincide necessariamente con la dimensione effettiva.')

S(20,'Le parti di una composizione sono vincolate',composition_triangle()+r'\PBody{Il triangolo rappresenta tre parti che sommano a uno. Nel dataset, quattro ossidi e il resto completano invece il cento per cento.}',r'\[\sum_{j=1}^{D}x_{ij}=100.\]'+C(20,'chiusura','''
parti <- c("SiO2", "CaO", "MgO",
           "FeO", "resto_wt")
comp <- as.matrix(d[parti])
range(rowSums(comp))
max(abs(rowSums(comp) - 100))
''','verificare la composizione')+r'\PInfo{La densità e la granulometria non sono parti della composizione chimica. Non entrano nella chiusura.}','La composizione richiede parti dichiarate e un totale comune; non comprende tutte le colonne numeriche.')

S(21,'La chiusura può indurre associazioni',three_boxes([r'Quantità positive\\$A,B,C$',r'Dividere per\\$A+B+C$',r'Frazioni\\$a+b+c=1$'],'Il denominatore comune collega anche componenti generate indipendentemente')+r'\PBody{La correlazione delle frazioni può differire dalla correlazione delle quantità assolute. Il segno non è fissato universalmente dalla sola chiusura.}',C(21,'correlazione_chiusura','''
set.seed(17)
assolute <- matrix(rlnorm(450), ncol = 3)
frazioni <- assolute / rowSums(assolute)
c(prima = cor(assolute)[1, 2],
  dopo = cor(frazioni)[1, 2])
''','confrontare quantità e frazioni')+r'\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m08-composizioni}{Esperimento · composizioni}','Il vincolo sul totale contribuisce alla struttura delle correlazioni osservate.')

S(22,'Un rapporto conserva la scala relativa',tk(r'''
\node[pFlow,text width=3.4cm] at(2.2,3.1){$(A,B)=(2,5)$\\$A/B=0{,}4$};
\node[pFlow,text width=3.4cm] at(7,3.1){$(cA,cB)=(6,15)$\\$cA/cB=0{,}4$};
\draw[pEdge](4.1,3.1)--node[pNote,above]{$c=3$}(5.1,3.1);
\node[pLabel] at(4.7,1.5){$\log(A/B)=\log A-\log B$};
\node[pNote] at(4.7,.55){Sono necessarie due parti strettamente positive};
''',h=4.5)+r'\PBody{Moltiplicare tutte le parti per lo stesso fattore non modifica i rapporti. Il logaritmo esprime i rapporti come differenze.}',C(22,'rapporti','''
# Il totale si semplifica nel rapporto.
lr_prima <- log(assolute[, 1] /
                assolute[, 2])
lr_dopo <- log(frazioni[, 1] /
               frazioni[, 2])
max(abs(lr_prima - lr_dopo))
''','verificare l’invarianza')+r'\PInfo{Il log-rapporto rappresenta una relazione fra parti: occorre sapere quali parti vengono confrontate.}','I rapporti restano invariati alla moltiplicazione comune delle quantità positive.')

S(23,'La trasformazione centrata dei log-rapporti',three_boxes([r'Parti positive\\$x_1,\ldots,x_D$',r'Media geometrica\\$g(\mathbf x)$',r'Coordinate CLR\\$\log[x_j/g(\mathbf x)]$'],'Ogni parte è confrontata con il riferimento geometrico della stessa riga')+r'\[g(\mathbf x)=\exp\!\left(\frac1D\sum_j\log x_j\right).\]',r'\[\operatorname{clr}(\mathbf x)_j=\log x_j-\frac1D\sum_\ell\log x_\ell.\]'+C(23,'clr','''
# Solo le cinque parti chimiche.
stopifnot(all(comp > 0))
log_comp <- log(comp)
clr <- log_comp - rowMeans(log_comp)
head(clr, 3)
max(abs(rowSums(clr)))
''','calcolare le coordinate CLR'),'La CLR descrive ogni parte rispetto alla media geometrica; non standardizza le otto proprietà miste.')

S(24,'Le coordinate CLR sommano a zero',tk(r'''
\node[pLabel] at(4.6,4){$\operatorname{clr}_1+\cdots+\operatorname{clr}_D=0$};
\draw[Muted,fill=GeoC!12](1.2,1.2)--(6.8,.6)--(8.4,3)--(2.8,3.6)--cycle;
\draw[pEdge](2.2,1.65)--(4.9,1.35);\draw[pEdge](2.2,1.65)--(3.1,2.9);
\node[pNote,text width=8.5cm] at(4.6,.1){Schema: per $D=3$ le coordinate occupano un piano in $\mathbb R^3$};
''',h=4.5)+r'\PBody{Cinque coordinate CLR appartengono a uno spazio di dimensione al più quattro. La covarianza è singolare per costruzione.}',r'\[\operatorname{rank}\{\operatorname{Cov}(\mathrm{CLR})\}\leq D-1.\]'+C(24,'pca_clr','''
# PCA nella geometria CLR dichiarata.
pc_clr <- prcomp(clr, center = TRUE,
                 scale. = FALSE)
pc_clr$sdev
# Ultima SD circa zero: vincolo noto.
''','riconoscere la singolarità')+r'\PSmall{Qui la scala CLR viene mantenuta. Ridimensionare separatamente le sue colonne cambierebbe la geometria.}','Una covarianza singolare può derivare da un vincolo scientifico noto, non da un errore del software.')

S(25,'Gli zeri richiedono una spiegazione',three_boxes([r'Zero strutturale\\parte assente',r'Sotto soglia\\misura censurata',r'Cifra arrotondata\\precisione limitata'],'La stessa cifra registrata può nascere da processi diversi')+r'\PBody{Il logaritmo di zero non è definito. Aggiungere una costante cambia soprattutto i rapporti che coinvolgono parti poco abbondanti.}',r'''
\[\log\frac{x_j+\delta}{x_\ell+\delta}\not\equiv\log\frac{x_j}{x_\ell}.\]
\PBody{Il parametro $\delta$ introduce una scelta aggiuntiva. Deve essere collegato al processo di misura e valutato con un’analisi di sensibilità.}
\PInfo{Le cinque parti chimiche del dataset sono positive. Gli zeri presenti in altri indici non autorizzano a includerli nella composizione.}
''','Prima di sostituire uno zero, occorre distinguere assenza reale, censura e arrotondamento.')

S(26,'Due geometrie per due domande',tk(r'''
\node[pFlow,text width=3.4cm] at(2.25,3.3){Otto proprietà miste\\$X\to Z$};
\node[pFlow,text width=3.4cm] at(7.0,3.3){Cinque parti chimiche\\$C\to\mathrm{CLR}(C)$};
\draw[pEdge](2.25,2.65)--(2.25,1.8);\draw[pEdge](7,2.65)--(7,1.8);
\node[pLabel,text width=3.7cm] at(2.25,1.2){Somiglianza rispetto alla dispersione delle proprietà};
\node[pLabel,text width=3.7cm] at(7,1.2){Somiglianza rispetto ai rapporti fra parti};
''',h=4.5)+r'\PBody{Il percorso principale usa le otto proprietà standardizzate del laboratorio. L’approfondimento CLR risponde a una domanda composizionale distinta.}',r'''
\PLabel{Scelte da documentare}
\PBody{Variabili incluse, trasformazione, unità, eventuali pesi e trattamento delle misure mancanti.}
\vspace{4mm}
\PInfo{Le due rappresentazioni non si confrontano soltanto contando quanti gruppi producono. Cambiano le proprietà considerate e il significato della distanza.}
\vspace{3mm}
\PBody{La PCA viene ora costruita sulla matrice $Z$ delle otto variabili.}
''','La geometria dell’analisi deve corrispondere alla domanda sulle somiglianze dei campioni.')
