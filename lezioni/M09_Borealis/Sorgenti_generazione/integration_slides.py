from diagram_helpers import *
SLIDES={};CODES={}
def S(n,title,left,right,recall):
    SLIDES[n]=dict(title=title,section='VIII · ANALISI DELLA CO₂',left=left,right=right,recall=recall)
def C(n,name,src,title):
    key=f'{n:03}_{name}.R';CODES[key]=src.strip()+'\n';return rf'\PCode{{R · {title}}}{{{key}}}'
TR=rows('co2_trasformazioni.csv',True)
def co2plot(col,caption,h=4.3):
    a=[dict(r,anno=int(r['data'][:4])+(int(r['data'][5:7])-1)/12) for r in TR if math.isfinite(val(r.get(col)))]
    return plot_series(a,[col],'anno','Anno','ppm',h=h,xticks=[1986,1990,1995,2000])+rf'\PSmall{{{caption}}}'
def test_table():
    tests=rows('test_stazionarieta.csv',True)
    selected=['co2_livello','co2_diff1','co2_diff12','co2_combinata']
    labs=['Livello',r'$\Delta_1$',r'$\Delta_{12}$',r'$\Delta_1\Delta_{12}$']
    body=r'\node[pNote,anchor=west] at(.15,4.05){Serie};\node[pNote] at(3.8,4.05){ADF};\node[pNote] at(6.0,4.05){KPSS Level};\node[pNote] at(8.1,4.05){KPSS Trend};'
    for i,(ss,lab) in enumerate(zip(selected,labs)):
        y=3.35-i*.73
        body+=rf'\fill[GeoA!{6 if i%2 else 12}](.05,{y-.3})rectangle(9.2,{y+.3});\node[pLabel,anchor=west] at(.15,{y}){{{lab}}};'
        a=[r for r in tests if r['serie']==ss]
        for j,r in enumerate(a):
            rel=r['relazione_p'];symbol=r'\approx' if rel=='circa' else rel
            digs=3 if rel=='circa' else 2
            text='$'+symbol+r'\,'+it(r["p_stampato"],digs)+'$'
            body+=rf'\node[pNote,text=Ink] at({3.8+j*2.15},{y}){{{text}}};'
    body+=r'\node[pNote] at(4.65,.25){ADF: costante + trend, $k=4$. KPSS: lshort = TRUE.};'
    return tk(body,h=4.5)
def contrast_lags():
    out,X,Y=axes(.5,3.5,-1,1,'',r'$\widehat\rho$',h=4.4,xticks=[],yticks=[-1,0,1])
    line(out,X,Y,[(.55,0),(3.45,0)],'Rule')
    for i,(col,lab) in enumerate([('diff1',r'$\Delta_1$'),('diff12',r'$\Delta_{12}$'),('diff1_12',r'$\Delta_1\Delta_{12}$')],1):
        a=[val(r[col]) for r in TR if math.isfinite(val(r[col]))];v=acf_values(a)
        for dx,k,c in [(-.13,1,'GeoA'),(.13,12,'GeoB')]:
            x=X(i+dx)
            out.append(rf'\fill[{c}!70]({x-.19},{Y(0):.4f})rectangle({x+.19},{Y(v[k]):.4f});')
        out.append(rf'\node[pLabel] at({X(i)},.27){{{lab}}};')
    out.append(r'\node[pNote,fill=Paper] at(5.1,4.1){Blu: ritardo 1. Rame: ritardo 12.};')
    return finish(out)
def final_diagram():
    body=r'\node[pFlow,text width=3.4cm] (a) at(2.2,3.5){Calendario esplicito\\date, assenze e copertura};\node[pFlow,text width=3.4cm] (b) at(7.0,3.5){Modello dichiarato\\trend, stagione e dipendenza};'
    body+=r'\node[pFlow,text width=7.2cm,minimum height=1.25cm] (c) at(4.6,1.3){Risultato interpretabile\\dato originario, trasformazione, evidenza e limiti};\draw[pEdge](a.south)--(2.2,2.1)--(2.2,1.95);\draw[pEdge](b.south)--(7.0,2.1)--(7.0,1.95);'
    return tk(body,h=4.5)

S(97,'Quale trasformazione serve alla CO₂?',
  co2plot('livello','Archivio mensile derivato: gennaio 1985–dicembre 2001.'),
  r'''\PBody{La serie cresce e mostra una forte oscillazione entro l’anno. La scelta della trasformazione dipende da ciò che vogliamo studiare.}
\vspace{3mm}
\PInfo{Confronteremo livello, cambiamento mensile, cambiamento rispetto allo stesso mese dell’anno precedente e differenza combinata.}
\vspace{3mm}
\PBody{Ogni trasformazione modifica significato, numerosità e dipendenza. Il confronto deve conservarne la traccia e non può basarsi soltanto su un p-value.}''',
'La domanda scientifica viene prima della trasformazione. Ogni alternativa deve avere un significato leggibile.')

S(98,'La differenza mensile conserva la stagione',
  co2plot('diff1',r'$\Delta_1X_t=X_t-X_{t-1}$, dal febbraio 1985.'),
  C(98,'co2_diff1',r'''
delta1 <- diff(y)
plot(delta1, ylab = "Differenza (ppm)")
acf(as.numeric(delta1), lag.max = 24,
    main = "Differenza mensile")
length(delta1) # 203 valori
''','esaminare il cambiamento mensile')+r'\PBody{Una crescita graduale si trasforma in incrementi. La salita e la discesa entro l’anno continuano però a produrre un andamento periodico.}'+r'\vspace{3mm}\PInfo{Il valore misura una differenza fra medie mensili consecutive, espressa in ppm.}',
'Una differenza ordinaria può ridurre l’andamento di lungo periodo senza rimuovere il ciclo stagionale.')

S(99,'La differenza stagionale confronta due anni',
  co2plot('diff12',r'$\Delta_{12}X_t=X_t-X_{t-12}$, dal gennaio 1986.'),
  C(99,'co2_diff12',r'''
delta12 <- diff(y, lag = 12)
plot(delta12,
     ylab = "Differenza rispetto a 12 mesi (ppm)")
length(delta12) # 192 valori
acf(as.numeric(delta12), lag.max = 24)
''','confrontare lo stesso mese')+r'\PBody{Confrontare lo stesso mese di due anni sottrae una stagione che si ripete identica. Le variazioni del ciclo e della crescita possono rimanere.}'+r'\vspace{2mm}\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m09-differenze}{Esperimento · Differenze}',
'Una differenza a dodici mesi esprime una variazione annuale. Non è una variazione mensile.')

S(100,'La differenza combinata cambia ancora la serie',
  co2plot('diff1_12',r'$\Delta_1\Delta_{12}X_t$, dal febbraio 1986.'),
  C(100,'co2_combinata',r'''
deltaC <- diff(diff(y, lag = 12))
alternativaC <- diff(diff(y), lag = 12)
stopifnot(max(abs(deltaC - alternativaC)) < 1e-10)
length(deltaC) # 191 valori
plot(deltaC, ylab = "Differenza combinata (ppm)")
''','verificare l’ordine delle differenze')+r'\PInfo{Gli operatori lineari commutano sulla stessa serie completa. Il valore confronta due incrementi mensili distanti un anno.}',
'La differenza combinata può attenuare più strutture e introdurne altre. L’ACF va esaminata di nuovo.')

S(101,'Ogni trasformazione ha il proprio calendario',
  transform_four(),
  C(101,'allineare_trasformazioni',r'''
confronto <- data.frame(
  data = d$data,
  livello = as.numeric(y),
  diff1 = c(NA, as.numeric(delta1)),
  diff12 = c(rep(NA, 12), as.numeric(delta12)),
  combinata = c(rep(NA, 13), as.numeric(deltaC)))
head(confronto, 15)
''','riallineare i risultati alle date')+r'\PBody{Le assenze iniziali indicano valori non definibili con l’archivio disponibile. Le date dei risultati restano quelle dell’ultimo termine coinvolto.}',
'La lunghezza della serie trasformata non basta: bisogna sapere a quali mesi corrispondono i suoi valori.')

S(102,'Il risultato cambia con l’ipotesi',
  test_table()+r'\PSmall{P-value realmente calcolati con tseries 0.10-63. Le disuguaglianze conservano gli avvisi sulle tabelle.}',
  r'''\PBody{Sul livello, ADF rifiuta la radice unitaria nel modello con trend. KPSS rifiuta un livello costante, mentre non rifiuta la stazionarietà attorno a un trend.}
\vspace{3mm}
\PInfo{Questi esiti non autorizzano a concludere automaticamente che il livello richieda una differenza. Le ipotesi deterministiche cambiano la lettura.}
\vspace{3mm}
\PBody{La differenza stagionale produce un quadro meno concorde. La combinata è compatibile con i riferimenti stazionari esaminati, ma ciò non dimostra indipendenza.}''',
'La soglia convenzionale del 5\\% va letta insieme a specificazione, grafici e struttura temporale residua.')

S(103,'Compatibilità con un test non basta',
  contrast_lags(),
  C(103,'diagnosi_residua',r'''
varianti <- list(diff1 = delta1,
                 diff12 = delta12,
                 combinata = deltaC)
sapply(varianti, function(v) {
  a <- as.numeric(acf(as.numeric(v),
    lag.max = 12, plot = FALSE)$acf)
  c(lag1 = a[2], lag12 = a[13])
})
''','confrontare la memoria residua')+r'\PInfo{Anche una serie compatibile con la stazionarietà può restare autocorrelata. Una correlazione negativa dopo differenziazione va interpretata nel contesto del processo.}',
'Stazionarietà, assenza di correlazione e indipendenza sono proprietà distinte.')

S(104,'La trasformazione rimane riproducibile',
  tk(r'\node[pFlow,text width=3.4cm] (a) at(2.3,3.4){Archivio originario\\date e concentrazioni};\node[pFlow,text width=3.4cm] (b) at(7,3.4){Regola applicata\\ritardi, ordine, parametri};\node[pFlow,text width=6.9cm] (c) at(4.6,1.3){Tabella dei risultati e registro delle scelte};\draw[pEdge](a.south)--(2.3,2.1)--(2.3,1.87);\draw[pEdge](b.south)--(7,2.1)--(7,1.87);',h=4.4),
  C(104,'esportare',r'''
dir.create("Risultati", showWarnings = FALSE)
write.csv(confronto,
  "Risultati/CO2_trasformazioni.csv",
  row.names = FALSE)
scelte <- list(periodo = range(d$data),
  frequenza = 12, ritardi = c(1, 12),
  ADF_k = 4, KPSS_lshort = TRUE)
saveRDS(scelte, "Risultati/scelte.rds")
''','salvare dati e scelte')+r'\PBody{Il resoconto accompagna il risultato con definizione, provenienza, unità, periodo e controlli effettuati.}',
'Salvare soltanto la serie finale perderebbe le informazioni necessarie per spiegarla e riprodurla.')

S(105,'Una conclusione circoscritta ai dati',
  co2plot('livello','La conclusione riguarda il segmento storico e la sua definizione di media mensile.'),
  r'''\PBody{Nel segmento 1985–2001, la media mensile derivata passa da 344,925 a 371,020 ppm fra il primo e l’ultimo mese. Il grafico mostra crescita e oscillazione stagionale.}
\vspace{3mm}
\PInfo{Le trasformazioni esaminate modificano entrambe le strutture. I test dipendono dai termini deterministici e non stabiliscono da soli quale rappresentazione usare.}
\vspace{3mm}
\PBody{Per un uso predittivo occorrerà confrontare le alternative rispettando l’ordine temporale. La valutazione su dati successivi sarà il tema del modulo seguente.}''',
'Una conclusione scientifica distingue ciò che il campione mostra dalle proprietà che il modello assume.')

S(106,'Quale informazione conserva la tua serie?',
  final_diagram(),
  r'''\PBody{Prima di interpretare una curva trasformata, dobbiamo poter rispondere: quali osservazioni usa, a quali date si riferisce e quale parte del fenomeno rappresenta?}
\vspace{3mm}
\[Z_t=g_t(X_1,\ldots,X_n).\]
\PSmall{$g_t$ indica la regola applicata alla data $t$.}
\PInfo{Una buona analisi permette di risalire dal risultato alle scelte che lo hanno prodotto. Le formule, il codice e i diagrammi devono descrivere lo stesso calcolo.}
\vspace{3mm}
\PSmall{Dati e attività: \href{https://marzione00.github.io/Lab_Geo/}{GeoStat Lab, M09}. Documentazione: \href{https://stat.ethz.ch/R-manual/R-devel/library/stats/html/00Index.html}{R, stats} e \href{https://cran.r-project.org/web/packages/tseries/tseries.pdf}{tseries}. Fonti e specificazioni complete accompagnano i sorgenti.}''',
'Il risultato acquista significato quando conserva un legame verificabile con osservazioni, calendario e ipotesi.')


# I valori osservati accompagnano la curva; le fonti accompagnano lo schema finale.
for n,p in [(105,r'\PBody{Nel segmento 1985–2001, la media mensile derivata passa da 344,925 a 371,020 ppm fra il primo e l’ultimo mese. Il grafico mostra crescita e oscillazione stagionale.}'),(106,r'\PSmall{Dati e attività: \href{https://marzione00.github.io/Lab_Geo/}{GeoStat Lab, M09}. Documentazione: \href{https://stat.ethz.ch/R-manual/R-devel/library/stats/html/00Index.html}{R, stats} e \href{https://cran.r-project.org/web/packages/tseries/tseries.pdf}{tseries}. Fonti e specificazioni complete accompagnano i sorgenti.}')]:
    assert p in SLIDES[n]['right']
    SLIDES[n]['right']=SLIDES[n]['right'].replace(p,'')
    SLIDES[n]['left']+=p
