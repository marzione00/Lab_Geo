SLIDES={}
CODES={}
def S(n,title,left,right,recall):
    SLIDES[n]=dict(title=title,section='LABORATORIO E CONCLUSIONI',left=left,right=right,recall=recall)
def table(rows):
    out=[r'\begin{tikzpicture}[x=1cm,y=1cm]',r'\fill[Navy](0,0) rectangle(17.7,.65);']
    for x,t in [(2.2,'Esperimento'),(7.85,'Quantità da confrontare'),(14.3,'Controllo necessario')]:
        out.append(rf'\node[pLabel,text=white,font=\bfseries\fontsize{{10}}{{12}}\selectfont] at({x},.325){{{t}}};')
    for j,(slug,lab,calc,check) in enumerate(rows):
        y=-(j+1)*1.08
        out.append(rf'\fill[{"white" if j%2==0 else "GeoTint"}](0,{y}) rectangle(17.7,{y+1.08});')
        for x,w,t in [(2.2,4.0,rf'\href{{https://marzione00.github.io/Lab_Geo/\#laboratorio/m05-{slug}}}{{{lab}}}'),(7.85,6.2,calc),(14.3,5.4,check)]:
            out.append(rf'\node[pLabel,text width={w}cm] at({x},{y+.54}){{{t}}};')
    out.append(r'\end{tikzpicture}')
    return '\n'.join(out)

SLIDES[103]=dict(title='I laboratori sul campionamento e sugli intervalli',section='LABORATORIO E CONCLUSIONI',wide=r'''
\PLabel{Esperimenti 1–5 · titoli collegati al sito}
'''+table([
('estimandi','Misure o stazioni','Media delle righe e media delle medie di stazione','Quali pesi definiscono il parametro?'),
('selezione','Precisione e selezione','Centro, SE e MSE delle stime','Il sito simula direttamente stime normali.'),
('distribuzioni','Distribuzione delle medie',r'SD delle medie e $1/\sqrt n$','Distinguere numerosità $n$ e repliche $B$.'),
('dipendenza','Covarianze e precisione','SE corretto e SE sotto indipendenza','La correlazione è comune a tutte le coppie.'),
('intervalli','Copertura degli intervalli','Frazione di intervalli che contengono 10','La copertura usa tutte le $B$ repliche.')])+r'''
\PBody{Per ciascun esperimento: formulare una previsione, cambiare un parametro, registrare il risultato e spiegare lo scarto dalla previsione.}
''',recall='Il confronto fra scenari richiede una domanda esplicita e il controllo delle altre condizioni della simulazione.')

SLIDES[104]=dict(title='I laboratori sul ricampionamento',section='LABORATORIO E CONCLUSIONI',wide=r'''
\PLabel{Esperimenti 6–9 · titoli collegati al sito}
'''+table([
('bootstrap','Bootstrap elementare','SE delle medie bootstrap e intervallo percentile','Il campione osservato resta fisso.'),
('ricampionamento','Stazioni intere','Bootstrap delle righe e delle colonne','12 stazioni indipendenti, 6 misure ciascuna.'),
('blocchi','Blocchi circolari','SE per righe e per sequenze contigue','Serie AR(1), 120 valori, lunghezza $L$.'),
('precisione','Stabilità del quantile','SD di 30 limiti superiori calcolati','Stesso campione di 30 valori, nuovo calcolo.')])+r'''
\PBody{Il quaderno propone due configurazioni per esperimento. Conservare parametri e seme con la conclusione.}
\PSmall{I casi browser di stazioni e blocchi sono distinti dai CSV del corso. Dimensioni e generatori sono documentati nel progetto.}
''',recall='Il ricampionamento deve conservare le relazioni fra osservazioni rilevanti per il disegno e per il parametro.')

SLIDES[105]=dict(title='La scelta dell’unità da ricampionare',section='LABORATORIO E CONCLUSIONI',wide=r'''
\PLabel{Una decisione motivata dal disegno}
\begin{tikzpicture}[x=1cm,y=1cm]
\fill[Navy](0,0) rectangle(17.7,.65);
\node[pLabel,text=white] at(3,.325){Struttura dei dati};
\node[pLabel,text=white] at(8.95,.325){Operazione};
\node[pLabel,text=white] at(14.8,.325){Condizione da discutere};
\foreach \yy/\a/\b/\c in {
-1/{Osservazioni indipendenti con distribuzione comune}/{Singole osservazioni con reinserimento}/{Distribuzione empirica adeguata al parametro},
-2/{Strati con quote fissate}/{Ricampionamento separato negli strati}/{Pesi della popolazione dichiarati},
-3/{Misure appaiate}/{Coppie complete, stessi indici}/{Indipendenza fra coppie},
-4/{Misure in stazioni}/{Stazioni intere}/{Indipendenza fra stazioni e pesi corretti},
-5/{Serie temporale dipendente}/{Blocchi contigui}/{Stazionarietà e dipendenza a corto raggio}}{
\fill[white](0,\yy-.5) rectangle(17.7,\yy+.5);
\draw[Rule](0,\yy-.5)--(17.7,\yy-.5);
\node[pLabel,text width=5.5cm] at(3,\yy){\a};
\node[pLabel,text width=5.5cm] at(8.95,\yy){\b};
\node[pLabel,text width=5.3cm] at(14.8,\yy){\c};
}
\end{tikzpicture}
\PSmall{Questa tabella riguarda i casi studiati. Disegni complessi, forti dipendenze e pesi di inclusione richiedono metodi coerenti con l'indagine.}
''',recall='La struttura osservata orienta il ricampionamento. La sua validità dipende dalle ipotesi sul processo che ha generato i dati.')

CODES['106_fossili.R']='''# Diametri in micrometri, dati del corso
x106 <- fossili$diametro_tot_um
g106 <- split(x106,fossili$morfotipo)
set.seed(17)
b106 <- replicate(2000,
  mean(sample(x106,replace=TRUE)))
s106 <- replicate(2000,mean(vapply(
  g106,function(z)
    mean(sample(z,replace=TRUE)),0.0)))
c(pooled=sd(b106),strati=sd(s106))
'''
S(106,'Due disegni per la media dei fossili',r'''
\PLabel{160 osservazioni sintetiche: 80 per morfotipo}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.6cm,fill=GeoA!7] (r) at(2.2,4){Rounded\\80 diametri};
\node[pFlow,text width=3.6cm,fill=GeoB!7] (s) at(7,4){Spiky\\80 diametri};
\node[pFlow,text width=7cm,minimum height=.7cm] (u) at(4.6,2.45){160 diametri, con morfotipo registrato};
\node[pFlow,text width=3.6cm] (p) at(2.2,.8){Pooled\\quote casuali nelle repliche};
\node[pFlow,text width=3.6cm] (t) at(7,.8){Stratificato\\80 estrazioni per gruppo};
\draw[pEdge](r.south)--(u.north west);
\draw[pEdge](s.south)--(u.north east);
\draw[pEdge](u.south west)--(p.north);
\draw[pEdge](u.south east)--(t.north);
\end{tikzpicture}
\[
\bar x=\tfrac12\bar x_{\mathrm R}+\tfrac12\bar x_{\mathrm S}.
\]
\PSmall{Con 80 osservazioni per gruppo, la stima puntuale coincide. I due ricampionamenti rappresentano disegni diversi.}
''',r'''
\PCode{R · confronto fra ricampionamenti}{106_fossili.R}
\PSmall{Confrontare i SE e i quantili 2,5 e 97,5. Motivare quale disegno corrisponde alla domanda formulata.}
''','Una stima puntuale uguale può avere distribuzioni di ricampionamento diverse quando cambiano le quote di gruppo.')

CODES['107_relazione.R']='''# Registrare risultato e ambiente
r107 <- lab_ricampionamento(
  tau=2,B=1000,seed=17)
dir.create("Risultati",
           showWarnings=FALSE)
saveRDS(r107,"Risultati/stazioni.rds")
writeLines(capture.output(sessionInfo()),
  "Risultati/sessionInfo.txt")
'''
S(107,'La relazione accompagna il risultato numerico',r'''
\PLabel{Una consegna breve, con elementi verificabili}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \yy/\n/\tit/\desc in {
4.25/1/{Domanda}/{Popolazione, parametro e unità di misura.},
3.05/2/{Disegno}/{Unità selezionate, gruppi e dipendenze.},
1.85/3/{Stima}/{Valore, SE, intervallo e metodo usato.},
.65/4/{Limiti}/{Selezione, poche unità, precisione del calcolo.}}{
\node[circle,fill=Classical!10,draw=Classical,minimum size=.7cm] at(.65,\yy){\n};
\node[pLabel,anchor=west] at(1.35,\yy+.17){\textbf{\tit}};
\node[pNote,anchor=west,text width=7.4cm,align=left] at(1.35,\yy-.28){\desc};
}
\end{tikzpicture}
\PSmall{Allegare lo script e una figura che renda visibile il confronto fra le procedure.}
''',r'''
\PCode{R · conservare parametri e ambiente}{107_relazione.R}
\PSmall{\texttt{saveRDS()} conserva oggetti e parametri. \texttt{sessionInfo()} registra versione di R e ambiente.}
\PInfo{La conclusione specifica popolazione, ipotesi e metodo dell'intervallo.}
''','Un risultato è interpretabile quando la relazione rende espliciti bersaglio, disegno, metodo e limiti.')

SLIDES[108]=dict(title='Domande per verificare il ragionamento',section='LABORATORIO E CONCLUSIONI',wide=r'''
\PLabel{Risposte motivate, con una formula o un esempio}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \xx/\yy/\n/\q in {
4.25/4.4/1/{Due stazioni hanno 2 e 8 misure. Quali pesi servono per descrivere la stazione media?},
13.35/4.4/2/{Perché 60 osservazioni correlate possono contenere poca informazione sulla media?},
4.25/2.4/3/{Quale quantità resta fissa e quale cambia nello studio della copertura?},
13.35/2.4/4/{Quali unità entrano insieme in una replica bootstrap di dati appaiati?},
4.25/.4/5/{Perché aumentare B può stabilizzare un limite senza correggere la selezione?},
13.35/.4/6/{Che cosa bisogna conservare quando si ricampiona una serie temporale?}}{
\node[pFlow,text width=7.9cm,minimum height=1.55cm] at(\xx,\yy){\textbf{\n.}\ \q};
}
\end{tikzpicture}
\PSmall{Le risposte devono distinguere le proprietà teoriche del metodo dai risultati di una singola simulazione. Indicazioni per il docente nel progetto.}
''',recall='La scelta del metodo deve poter essere spiegata a partire dalla domanda e dal disegno, prima di eseguire il codice.')

S(109,'Riferimenti per formule e procedure',r'''
\PLabel{Campionamento e ricampionamento}
\PBody{\textbf{Cochran, W. G. (1977).}\\\emph{Sampling Techniques}, 3a edizione, Wiley. Disegni campionari, pesi e popolazioni finite.}
\vspace{3mm}
\PBody{\textbf{Efron, B. (1979).}\\\href{https://doi.org/10.1214/aos/1176344552}{Bootstrap Methods: Another Look at the Jackknife}. \emph{Annals of Statistics}, 7, 1--26.}
\vspace{3mm}
\PBody{\textbf{Künsch, H. R. (1989).}\\\href{https://doi.org/10.1214/aos/1176347265}{The Jackknife and the Bootstrap for General Stationary Observations}. \emph{Annals of Statistics}, 17, 1217--1241.}
\vspace{3mm}
\PSmall{I casi didattici esplicitano ipotesi più semplici rispetto ai disegni affrontati nella letteratura specialistica.}
''',r'''
\PLabel{Documentazione ufficiale di R}
\PBody{\href{https://stat.ethz.ch/R-manual/R-devel/library/base/html/sample.html}{\texttt{sample()}}\\Selezione casuale, reinserimento, pesi.}
\vspace{3mm}
\PBody{\href{https://stat.ethz.ch/R-manual/R-devel/library/stats/html/sd.html}{\texttt{sd()}} e \href{https://stat.ethz.ch/R-manual/R-devel/library/stats/html/quantile.html}{\texttt{quantile()}}\\Deviazione standard e quantili campionari.}
\vspace{3mm}
\PBody{\href{https://stat.ethz.ch/R-manual/R-devel/library/stats/html/t.test.html}{\texttt{t.test()}}\\Intervalli per medie e differenze.}
\vspace{3mm}
\PBody{\href{https://stat.ethz.ch/R-manual/R-devel/library/base/html/Random.html}{Generazione casuale in R}\\Seme, algoritmi e riproducibilità.}
\PInfo{La guida inclusa distingue i risultati del modello, le stime su un campione e la precisione numerica dei ricampionamenti.}
''','Le formule richiedono ipotesi esplicite. La documentazione del software chiarisce gli argomenti e le convenzioni del calcolo.')

S(110,'Da Pelago ai confronti fra gruppi',r'''
\PLabel{Fonti del corso e materiali operativi}
\PBody{\href{https://marzione00.github.io/Lab_Geo/}{Laboratorio di analisi dei dati per le Scienze della Terra}.}
\vspace{3mm}
\PBody{\href{https://github.com/marzione00/Lab_Geo/tree/main/moduli/M05}{Modulo M05 originale}: 105 slide e 20 laboratori R6. Questa presentazione riorganizza il percorso in 110 slide.}
\vspace{3mm}
\PBody{I nove esperimenti browser hanno funzioni R locali con gli stessi parametri e meccanismi di generazione. I dati dei fossili e dei provini sono sintetici.}
\vspace{3mm}
\PSmall{Consultazione: 18 novembre 2026. Il progetto contiene sorgenti TikZ, frammenti R, dati, quaderno, soluzioni e corrispondenza con i 20 laboratori originali.}
''',r'''
\PLabel{Gemina · modulo M06}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=6.1cm] (a) at(3.4,3.4){\textbf{Pelago}\\stima di un parametro\\e incertezza campionaria};
\node[pFlow,text width=6.1cm,fill=GeoTint] (b) at(3.4,1.05){\textbf{Gemina}\\contrasti fra gruppi\\e valutazione delle ipotesi};
\draw[pEdge](a)--(b);
\end{tikzpicture}
\PBody{Il passo successivo parte da una differenza con segno e unità di misura, poi ne valuta l'incertezza e il rapporto con un'ipotesi dichiarata.}
''','Prima di confrontare gruppi occorre riconoscere le unità indipendenti, definire il contrasto e stimarne l’incertezza.')
