from diagram_helpers import *
SLIDES={};CODES={}
def S(n,title,left,right,recall):
    section='I · TEMPO E CALENDARIO' if n<=14 else 'II · AGGREGAZIONE E RISOLUZIONE'
    SLIDES[n]=dict(title=title,section=section,left=left,right=right,recall=recall)
def C(n,name,src,title):
    key=f'{n:03}_{name}.R';CODES[key]=src.strip()+'\n'
    return rf'\PCode{{R · {title}}}{{{key}}}'
def sampling_intervals():
    body=r'\node[pLabel,anchor=west] at(.3,4){Misura istantanea};\draw[pAxis](.5,3.1)--(9,3.1);\fill[GeoA](4.5,3.1)circle(4pt);\node[pNote] at(4.5,2.55){ore 12:00};'
    body+=r'\node[pLabel,anchor=west] at(.3,1.9){Media su un intervallo};\draw[pAxis](.5,.8)--(9,.8);\fill[GeoB!18](2,.8)rectangle(7,1.4);\draw[GeoB,line width=1.5pt](2,1.4)--(7,1.4);\node[pNote] at(2,.4){00:00};\node[pNote] at(7,.4){24:00};'
    return tk(body,h=4.6)
def duplicate_dates():
    body=r'\node[pFlow,text width=3.5cm] (a) at(2.3,3.5){12 giugno, ore 10\\sensore A: 8,1};\node[pFlow,text width=3.5cm] (b) at(7,3.5){12 giugno, ore 10\\sensore B: 8,4};'
    body+=r'\node[pFlow,text width=7.2cm] (c) at(4.65,1.25){La stessa data può identificare sensori diversi\\La chiave diventa: data e sensore};\draw[pEdge](a.south)--(2.3,2)--(2.3,1.85);\draw[pEdge](b.south)--(7,2)--(7,1.85);'
    return tk(body,h=4.5)
def frequency_grid():
    body=''
    for row in range(2):
        for j in range(12):
            x=.42+j*.74;y=3.1-row*1.4
            body+=rf'\filldraw[fill={"GeoA" if row==0 else "GeoC"}!12,draw=Rule]({x-.31},{y-.3})rectangle({x+.31},{y+.3});\node[pNote] at({x},{y}){{{j+1}}};'
        body+=rf'\node[pNote] at(4.6,{y+.58}){{{1985+row}}};'
    body+=r'\node[pLabel] at(4.6,.5){12 posizioni mensili per anno};'
    return tk(body,h=4.2)
def aggregate_choices():
    body=''
    labs=[('Precipitazione','somma',r'mm nel mese'),('Temperatura','media',r'$^\circ$C nel mese'),('Piena fluviale','massimo',r'picco di portata')]
    for i,(a,b,c) in enumerate(labs):
        y=3.7-i*1.32
        body+=rf'\node[pFlow,text width=3.5cm,minimum height=.9cm] at(2.25,{y}){{{a}}};\draw[pEdge](4.3,{y})--(5.0,{y});\node[pLabel,anchor=west] at(5.3,{y+.2}){{{b}}};\node[pNote,anchor=west] at(5.3,{y-.22}){{{c}}};'
    return tk(body,h=4.5)

S(2,'Che cosa perdiamo senza l’ordine temporale?',
  r'\PLabel{Una stessa distribuzione, due successioni}'+order_pair(),
  r'''\PBody{Rimescolare i valori lascia invariati media, quantili e istogramma. Cambia la relazione fra un’osservazione e quelle che la precedono.}
\vspace{4mm}
\[\mathcal D=\{(t_i,x_i)\}_{i=1}^{n}.\]
\PInfo{La domanda della lezione: quali caratteristiche della serie dipendono dal calendario e dalla successione dei valori?}
\vspace{3mm}
\PBody{Seguiremo una serie storica di CO$_2$ e due archivi simulati, in cui alcune proprietà sono note.}''',
'Il tempo è una coordinata del dato. La distribuzione dei valori, da sola, non descrive una serie.')

S(3,'Ogni valore ha un tempo e una durata',
  time_pairs()+r'\[\Delta t_i=t_i-t_{i-1}.\]',
  r'''\PBody{L’indice $i$ conta le righe. Il tempo $t_i$ indica quando avviene la misura. Passare dalla riga 2 alla riga 3 può significare un giorno, un mese o un intervallo irregolare.}
\vspace{3mm}
\PInfo{Coordinate lungo una carota o una traversa sono spaziali. Si possono studiare dipendenze rispetto alla distanza, dichiarando unità e spaziatura.}
\vspace{3mm}
\PBody{Un ritardo ha significato soltanto quando sappiamo quale intervallo separa le osservazioni.}''',
'La distanza fra due tempi osservati deve restare distinguibile dal numero di righe che li separa.')

S(4,'Le date diventano oggetti di R',
  calendar(missing=False)+r'\PBody{Una data civile comprende anno, mese e giorno. Il formato anno-mese-giorno evita l’ambiguità fra notazioni italiane e anglosassoni.}',
  C(4,'date',r'''
# ISO 8601: anno-mese-giorno.
date_es <- as.Date(c("2001-01-01",
                    "2001-02-01",
                    "2001-03-01"))
class(date_es)
diff(date_es)
# Febbraio e gennaio hanno durate diverse.
''','leggere le date')+r'\PInfo{Una griglia mensile è regolare nel calendario, anche se gli intervalli in giorni hanno durata diversa.}',
'La classe Date conserva il calendario. Una successione di mesi non è una successione di 30 giorni.')

S(5,'Istanti e intervalli descrivono misure diverse',
  sampling_intervals(),
  r'''\PBody{Una temperatura alle ore 12 e una media giornaliera riassumono quantità diverse. Alla data occorre associare il significato della misura.}
\vspace{3mm}
\[\bar x_{[a,b]}=\frac{1}{b-a}\int_a^b x(t)\,dt.\]
\PSmall{La formula definisce una media temporale continua ideale. I dati discreti richiedono una regola di approssimazione.}
\vspace{3mm}
\PInfo{Per serie orarie servono anche fuso, ora legale e convenzione dell’istante: inizio, centro o fine dell’intervallo.}''',
'Data, durata e procedura di misura stabiliscono quale quantità stiamo confrontando.')

S(6,'La provenienza della CO₂ storica',
  provenance()+r'\PSmall{Fonte: archivio distribuito con statsmodels, attribuito a Keeling e Whorf e al CDIAC.}',
  r'''\PBody{Il file settimanale del corso contiene le concentrazioni storiche dell’osservatorio di Mauna Loa. Il periodo va da marzo 1958 a dicembre 2001.}
\vspace{3mm}
\PInfo{La versione mensile del corso media i valori settimanali disponibili, assegnandoli al mese della data. È un’aggregazione locale documentata.}
\vspace{3mm}
\PBody{Questi dati servono a studiare tendenza, stagione e dipendenza temporale. La data finale dell’archivio resta esplicita in ogni analisi.}
\vspace{2mm}
\PSmall{\href{https://www.statsmodels.org/stable/datasets/generated/co2.html}{Fonte e descrizione dell’archivio storico}}''',
'La media mensile derivata ha una definizione propria. Non va confusa con una serie mensile ufficiale aggiornata.')

hist=[dict(r,anno=int(r['data'][:4])+(int(r['data'][5:7])-1)/12) for r in MON]
S(7,'Una crescita attraversata da oscillazioni',
  plot_series(hist,['co2_ppm'],'anno','Anno',r'CO$_2$ (ppm)',xticks=[1960,1970,1980,1990,2000])+r'\PSmall{Medie mensili derivate. Gli intervalli privi di valori restano interruzioni della linea.}',
  C(7,'archivio',r'''
source("setup.R", encoding = "UTF-8")
range(wk$data)
nrow(wk)
sum(is.na(wk$co2))
# 2284 date, di cui 59 prive di valore.
c(osservati = sum(!is.na(wk$co2)),
  mancanti = sum(is.na(wk$co2)))
''','contare le osservazioni')+r'\PInfo{La crescita di lungo periodo e le oscillazioni annuali pongono domande diverse. Le esamineremo separatamente.}',
'Un grafico della serie deve mostrare periodo, unità e assenze prima di qualsiasi trasformazione.')

S(8,'La tabella conserva valore e copertura',
  source_table(CO2)+r'\PSmall{Prime cinque righe del segmento 1985–2001. La copertura conta i valori settimanali disponibili.}',
  C(8,'tabella',r'''
head(d, 5)
str(d)
# Tre ruoli: data, concentrazione, copertura.
stopifnot(inherits(d$data, "Date"),
  is.numeric(d$co2_ppm),
  all(d$n_settimane >= 0))
''','riconoscere le colonne')+r'\PBody{La concentrazione e il numero di settimane devono viaggiare insieme. Due medie uguali possono poggiare su quantità diverse di osservazioni.}',
'La copertura è un’informazione sulla misura aggregata e deve rimanere nella tabella.')

S(9,'L’ordinamento segue il calendario',
  time_pairs()+r'\PInfo{Il controllo delle date avviene prima dell’assegnazione di una frequenza alla serie.}',
  C(9,'ordinare',r'''
# L'ordinamento coinvolge l'intera tabella.
wk <- wk[order(wk$data), ]
stopifnot(!anyNA(wk$data))
anyDuplicated(wk$data)
table(as.integer(diff(wk$data)))
# Una differenza in Date restituisce giorni.
''','ordinare tutte le colonne')+r'\PBody{Ordinare soltanto i valori romperebbe l’associazione con date e metadati. Ogni riga deve restare integra.}',
'La serie ordinata conserva le associazioni fra date, valori e informazioni sulla misura.')

S(10,'Un’assenza occupa una posizione',
  calendar()+r'\PBody{Aprile resta nella griglia con valore NA. La distanza fra marzo e maggio continua a essere di due mesi.}',
  C(10,'assenze',r'''
cal_es <- data.frame(
  data = seq(as.Date("2001-01-01"),
             by = "month", length.out = 8),
  valore = c(5, 7, 6, NA, 9, 7, 6, 4))
cal_es[is.na(cal_es$valore), ]
# Il NA mantiene la posizione di aprile.
''','conservare il mese assente')+r'\PInfo{Sostituire NA con zero affermerebbe che il valore osservato è nullo. È un’informazione diversa da un’assenza.}',
'Un valore mancante e un valore nullo esprimono situazioni diverse.')

S(11,'Le date duplicate richiedono una spiegazione',
  duplicate_dates(),
  C(11,'duplicati',r'''
duplicati <- wk[
  duplicated(wk$data) |
    duplicated(wk$data, fromLast = TRUE), ]
nrow(duplicati)
# Qui il risultato e' zero.
# Con piu' sensori, controllare data + sensore.
''','isolare i duplicati')+r'\PBody{Repliche, sensori diversi ed errori di registrazione possono condividere una data. La regola di aggregazione dipende dalla loro origine.}'+r'\vspace{3mm}\PInfo{Eliminare una riga prima di identificarne il ruolo può cancellare una misura valida.}',
'La chiave che identifica un’osservazione può comprendere più campi oltre alla data.')

S(12,'La griglia rende espliciti i mesi attesi',
  calendar()+r'\PBody{Il confronto con una griglia completa distingue una riga assente da una riga presente con misura mancante.}',
  C(12,'griglia',r'''
griglia_es <- data.frame(
  data = seq(min(cal_es$data), max(cal_es$data),
             by = "month"))
osservati_es <- cal_es[-4, ]
completo_es <- merge(griglia_es, osservati_es,
                    by = "data", all.x = TRUE)
completo_es
''','ricostruire il calendario')+r'\PSmall{La chiave data deve essere univoca prima del merge. In caso contrario, una data può generare più righe.}',
'La griglia attesa è una scelta esplicita fondata sul calendario e sul protocollo di osservazione.')

S(13,'ts assegna una frequenza alla successione',
  frequency_grid()+r'\[t_i=1985+\frac{i-1}{12},\qquad i=1,\ldots,204.\]',
  C(13,'ts',r'''
y <- ts(d$co2_ppm,
        start = c(1985, 1), frequency = 12)
start(y)
end(y)
frequency(y)
head(time(y))
# Il tempo interno e' espresso in anni.
''','costruire la serie mensile')+r'\PInfo{ts memorizza inizio e frequenza. La tabella con le date civili resta necessaria per ricondurre ogni risultato al calendario.}',
'frequency = 12 dichiara dodici passi per anno. Non verifica da sola la regolarità del file.')

S(14,'Il segmento completo comprende 204 mesi',
  source_table([CO2[i] for i in [0,1,2,202,203]])+r'\PSmall{Gennaio 1985–dicembre 2001: 17 anni, 204 mesi, nessun valore mancante.}',
  C(14,'controllo_ts',r'''
griglia <- seq(as.Date("1985-01-01"),
               as.Date("2001-12-01"), by = "month")
stopifnot(identical(d$data, griglia),
          nrow(d) == 204L,
          !anyNA(d$co2_ppm),
          !anyDuplicated(d$data))
# Solo ora la frequenza descrive il file.
''','verificare prima del calcolo')+r'\PBody{Useremo questo segmento per confrontare trasformazioni. Il calendario sarà mantenuto anche quando le differenze accorciano la serie.}',
'Un controllo esplicito del calendario rende verificabili le trasformazioni successive.')

S(15,'Ogni media porta con sé la copertura',
  coverage()+r'\PSmall{Archivio mensile completo: numero di mesi per quantità di valori settimanali disponibili.}',
  r'''\[\bar x_m=\frac{1}{n_m}\sum_{\substack{i\in m\\x_i\ \mathrm{osservato}}}x_i.\]
\PBody{$n_m$ conta le osservazioni disponibili nel mese. Quando $n_m=0$, la media rimane assente.}
\vspace{3mm}
\PInfo{Un conteggio alto non garantisce una copertura uniforme: anche la posizione delle assenze nel mese può influenzare il risultato.}
\vspace{3mm}
\PBody{Nel segmento 1985–2001 ogni mese ha almeno tre osservazioni settimanali. L’archivio completo ha copertura più variabile.}''',
'Una media senza informazioni sulla copertura può nascondere periodi osservati in modo disomogeneo.')

S(16,'Dal valore settimanale alla media mensile',
  r'\PLabel{Una regola riproducibile}'+source_table(MON[10:15])+r'\PBody{Il raggruppamento usa il mese della data. Una settimana che attraversa due mesi non viene suddivisa fra loro.}',
  C(16,'aggregare',r'''
mese_w <- format(wk$data, "%Y-%m")
gruppi_w <- split(wk$co2, mese_w)
media_m <- vapply(gruppi_w, function(v) {
  if (all(is.na(v))) NA_real_
  else mean(v, na.rm = TRUE)
}, numeric(1))
n_m <- vapply(gruppi_w, function(v)
  sum(!is.na(v)), integer(1))
head(cbind(media_m, n_m))
''','aggregare con una regola esplicita')+r'\PSmall{La condizione all(is.na(v)) evita di restituire NaN per un mese completamente privo di valori.}',
'La convenzione di assegnazione al mese appartiene alla definizione del dato derivato.')

S(17,'La ricostruzione si confronta con il file',
  tk(r'\node[pFlow,text width=3.4cm] (a) at(2.3,3.3){Medie ricostruite\\dal file settimanale};\node[pFlow,text width=3.4cm] (b) at(7,3.3){Medie mensili\\distribuite con il corso};\draw[pEdge](a.south)--(2.3,1.55)--(3.5,1.55);\draw[pEdge](b.south)--(7,1.55)--(5.8,1.55);\node[pFlow,text width=1.7cm] at(4.65,1.55){Confronto\\per data};',h=4.2)+r'\PBody{La corrispondenza è verificata dopo l’allineamento delle date. La tolleranza riflette gli arrotondamenti del CSV.}',
  C(17,'confronto',r'''
pos <- match(format(mon$data, "%Y-%m"),
             names(media_m))
ricostruita <- unname(media_m[pos])
stopifnot(identical(is.na(ricostruita),
                    is.na(mon$co2_ppm)))
scarto <- max(abs(ricostruita - mon$co2_ppm),
              na.rm = TRUE)
stopifnot(scarto < 1e-6)
scarto
''','verificare la ricostruzione'),
'Il confronto numerico richiede le stesse date, la stessa regola e una tolleranza dichiarata.')

S(18,'La media delle medie cambia i pesi',
  month_weights(),
  r'''\PBody{Due periodi hanno medie 10 e 20. Il primo contiene due misure, il secondo otto.}
\vspace{3mm}
\[\bar x_{\rm periodi}=\frac{10+20}{2}=15.\]
\[\bar x_{\rm misure}=\frac{2\cdot10+8\cdot20}{10}=18.\]
\PInfo{La prima quantità pesa allo stesso modo i periodi. La seconda pesa allo stesso modo le dieci misure disponibili.}''',
'La media dei periodi e la media delle misure rispondono a domande diverse quando le numerosità cambiano.')

S(19,'I pesi dichiarano la quantità stimata',
  r'''\[\bar x_{\rm misure}=\frac{\sum_{m=1}^{M}n_m\bar x_m}{\sum_{m=1}^{M}n_m}.\]
\[\bar x_{\rm periodi}=\frac{1}{M}\sum_{m=1}^{M}\bar x_m.\]'''+columns_bars([15,18],['Periodi','Misure'],['GeoA','GeoB'],h=3.4),
  C(19,'pesi',r'''
medie_es <- c(10, 20)
conteggi_es <- c(2, 8)
mean(medie_es)
weighted.mean(medie_es, conteggi_es)
mean(rep(medie_es, conteggi_es))
# Gli ultimi due risultati coincidono.
''','calcolare le due medie')+r'\PBody{Numerosità uguali fanno coincidere le due formule. Possono coincidere anche in casi particolari, per esempio se tutte le medie dei periodi sono uguali.}',
'Prima di calcolare una media complessiva bisogna scegliere cosa riceve uguale peso.')

S(20,'Intervalli diversi possono richiedere durate',
  interval_weights()+r'\[\bar x_{\rm tempo}=\frac{1\cdot10+3\cdot20}{1+3}=17{,}5.\]',
  C(20,'durate',r'''
valori_es <- c(10, 20)
durate_es <- c(1, 3) # ore
weighted.mean(valori_es, durate_es)
# Ipotesi: ogni valore rappresenta
# l'intero intervallo indicato.
''','pesare per il tempo rappresentato')+r'\PInfo{I pesi di durata sono appropriati se il valore rappresenta l’intero intervallo. Misure puntuali irregolari richiedono un modello di interpolazione o integrazione.}',
'Un peso temporale ha senso soltanto insieme all’ipotesi su ciò che accade fra due misure.')

S(21,'Somma, media e massimo cambiano la domanda',
  aggregate_choices(),
  C(21,'operatori',r'''
pioggia_es <- c(0, 5, 12, NA, 3)
c(totale_osservato = sum(pioggia_es, na.rm = TRUE),
  media_osservata = mean(pioggia_es, na.rm = TRUE),
  massimo_osservato = max(pioggia_es, na.rm = TRUE),
  giorni_osservati = sum(!is.na(pioggia_es)))
''','specificare l’aggregato')+r'\PBody{Una somma con un giorno assente è il totale dei soli giorni osservati. Un massimo su un periodo incompleto può perdere proprio il picco.}',
'La gestione delle assenze deve essere coerente con la quantità che l’aggregato intende descrivere.')

S(22,'Aggregare attenua le variazioni rapide',
  aggregate_signal()+r'\PSmall{Segnale illustrativo con periodicità di 12 e 3 mesi. Le medie sono calcolate su blocchi disgiunti.}',
  C(22,'risoluzione',r'''
mese_es <- 1:48
segnale_es <- sin(2*pi*mese_es/12) +
              0.35*sin(2*pi*mese_es/3)
blocco3 <- (mese_es - 1) %/% 3
blocco12 <- (mese_es - 1) %/% 12
tapply(segnale_es, blocco3, mean)
tapply(segnale_es, blocco12, mean)
''','cambiare la risoluzione')+r'\PInfo{Una media annuale può cancellare il ciclo entro l’anno. Dal dato aggregato non si ricostruiscono in generale i valori originali.}',
'La risoluzione temporale limita le oscillazioni e gli eventi che possiamo riconoscere.')

S(23,'Un campionamento rado può nascondere un ciclo',
  aliasing(),
  r'''\PBody{Nel disegno, il segnale oscilla fra $-1$ e $1$. I campioni cadono sempre nella stessa fase e sono tutti uguali a 1.}
\vspace{3mm}
\[f_s>2f_{\max}.\]
\PSmall{Condizione del modello ideale: segnale limitato in frequenza e campionamento uniforme. $f_s$ è la frequenza di campionamento.}
\vspace{3mm}
\PInfo{L’aliasing rende indistinguibili frequenze diverse alla risoluzione osservata. Irregolarità e assenze richiedono analisi ulteriori.}''',
'Una serie osservata quasi costante può derivare da un segnale variabile campionato sempre alla stessa fase.')

S(24,'Risoluzione e copertura si esaminano insieme',
  r'\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m09-aggregazione}{Esperimento · Aggregazione}'+aggregate_signal(),
  r'''\PBody{Nell’esperimento, allargare l’intervallo di aggregazione modifica la forma e la variabilità della serie.}
\vspace{3mm}
\PInfo{Confrontare finestre da 1, 3 e 12 mesi. Descrivere quale oscillazione si attenua e quali picchi non restano riconoscibili.}
\vspace{3mm}
\PBody{Il confronto è interpretabile se teniamo ferma anche la regola sulle assenze. Un cambiamento di copertura può alterare la media quanto un cambiamento del segnale.}
\vspace{3mm}
\PSmall{\href{https://marzione00.github.io/Lab_Geo/\#laboratorio/m09-calendario}{Esperimento complementare: calendario e mesi mancanti}}''',
'L’aggregazione modifica insieme il dettaglio visibile e il significato delle osservazioni.')

S(25,'Il dato analizzabile conserva la sua storia',
  tk(r'\node[pFlow,text width=2.4cm] (a) at(1.55,3.1){Valore\\unità e definizione};\node[pFlow,text width=2.4cm] (b) at(4.7,3.1){Tempo\\data e durata};\node[pFlow,text width=2.4cm] (c) at(7.85,3.1){Copertura\\valori disponibili};\node[pLabel,text width=8.5cm] at(4.7,1.25){Le trasformazioni si aggiungono al dato originario\\con regola, parametri e calendario di validità.};',h=4.2),
  C(25,'registro',r'''
registro <- data.frame(
  data = d$data,
  co2_ppm = d$co2_ppm,
  n_settimane = d$n_settimane)
attr(registro, "definizione") <-
  "Media delle settimane assegnate al mese"
head(registro, 3)
# Le colonne derivate verranno aggiunte dopo.
''','preparare il registro')+r'\PBody{Passiamo ora alla forma della serie: andamento graduale, oscillazione periodica e variazioni che restano dopo averle rappresentate.}',
'Un’analisi riproducibile mantiene collegati osservazione originaria, calendario e trasformazioni.')


# Il significato delle repliche accompagna il diagramma.
p = r"\PBody{Repliche, sensori diversi ed errori di registrazione possono condividere una data. La regola di aggregazione dipende dalla loro origine.}"
assert p in SLIDES[11]['right']
SLIDES[11]['right']=SLIDES[11]['right'].replace(p,'')
SLIDES[11]['left']+=p
