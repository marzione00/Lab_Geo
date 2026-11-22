from diagram_helpers import *
SLIDES={};CODES={}
def S(n,title,left,right,recall):
    SLIDES[n]=dict(title=title,section='III · TREND, STAGIONE E SMOOTHING',left=left,right=right,recall=recall)
def C(n,name,src,title):
    key=f'{n:03}_{name}.R';CODES[key]=src.strip()+'\n';return rf'\PCode{{R · {title}}}{{{key}}}'
def tempplot(columns,labels='',h=4.3,first=None):
    a=[dict(r, tempo0=i) for i,r in enumerate(rows('temperatura_componenti.csv',True))]
    if first:a=a[:first]
    return plot_series(a,columns,xcol='tempo0',xlabel='Mese da gennaio 2000',ylabel=r'Temperatura ($^\circ$C)',h=h)+rf'\PSmall{{{labels}}}'
def leakage():
    body=r'\fill[GeoA!9](.3,1.2)rectangle(5.5,3.25);\fill[GeoB!11](5.5,1.2)rectangle(9,3.25);\node[pLabel] at(2.8,3.85){Periodo disponibile};\node[pLabel] at(7.3,3.85){Periodo futuro};\draw[GeoB,dashed,line width=1pt](5.5,.7)--(5.5,3.5);'
    for j in range(9):
        x=.6+j
        body+=rf'\fill[{"GeoA" if j<=4 else "GeoB"}]({x},2.25)circle(3pt);'
    body+=r'\draw[GeoC,line width=1.4pt,rounded corners=1mm](2.2,1.65)rectangle(7,2.85);\node[pNote,text width=8.4cm] at(4.7,.55){Una finestra centrata vicino al confine entra nel periodo futuro};'
    return tk(body,h=4.4)
def reference_months():
    body=''
    for y in range(5):
        for m in range(12):
            x=.55+.72*m;yy=3.8-.58*y
            body+=rf'\filldraw[fill={"GeoB!55" if m==0 else "GeoA!10"},draw=Rule]({x-.24},{yy-.18})rectangle({x+.24},{yy+.18});'
        body+=rf'\node[pNote,anchor=east] at(.16,{3.8-.58*y}){{{2000+y}}};'
    body+=r'\node[pNote] at(4.6,.65){I cinque mesi di gennaio definiscono il riferimento di gennaio};'
    return tk(body,h=4.3)

S(26,'Una serie può essere descritta per componenti',
  component_chart()+r'\[X_t=T_t+S_t+R_t.\]',
  r'''\PBody{Un andamento graduale $T_t$ e una stagione $S_t$ descrivono due scale di variazione. Il resto $R_t$ raccoglie ciò che rimane dopo questa rappresentazione.}
\vspace{3mm}
\PInfo{Nella temperatura simulata conosciamo le componenti del generatore. Nei dati osservati dobbiamo stimarle attraverso un modello.}
\vspace{3mm}
\PBody{La scomposizione additiva è una scelta. Componenti con ampiezza proporzionale al livello possono richiedere una trasformazione, se compatibile con il significato e il dominio dei dati.}''',
'Le componenti dipendono dalla rappresentazione adottata. Il resto può conservare struttura.')

S(27,'Nel simulatore conosciamo le componenti',
  plot_series(TEMP[:60],['trend_simulato','stagione_simulata'],xcol='tempo0',xlabel='Mese da gennaio 2000',ylabel=r'$^\circ$C',h=4.1)+r'\PSmall{Trend in blu, stagione in rame. Le due curve hanno la stessa unità.}',
  r'''\[T_t=12+0{,}012t,\qquad S_t=-8\cos\!\left(\frac{2\pi t}{12}\right).\]
\PSmall{$t=0$ corrisponde a gennaio 2000. Il file comprende 240 mesi.}'''+
  C(27,'componenti',r'''
ricostruita_T <- with(temp,
  trend_simulato + stagione_simulata +
    residuo_simulato)
err_T <- max(abs(temp$temperatura_C -
                 ricostruita_T))
stopifnot(err_T < 2e-8)
''','verificare l’identità')+r'\PBody{L’identità consente di confrontare una stima delle componenti con la verità del simulatore.}',
'Conoscere il generatore permette di distinguere una ricostruzione esatta da una stima statistica.')

S(28,'La stagione ricorre entro l’anno',
  seasonal_overlay(),
  C(28,'stagione',r'''
# Una linea per ogni anno del segmento.
yr <- as.integer(format(d$data, "%Y"))
mo <- as.integer(format(d$data, "%m"))
matplot(1:12, sapply(c(1985, 1992, 2001),
  function(a) d$co2_ppm[yr == a]),
  type = "l", lty = 1, xlab = "Mese",
  ylab = "CO2 (ppm)")
''','confrontare gli anni')+r'\PBody{La forma entro l’anno può ripetersi mentre il livello cresce. Un ciclo di calendario si distingue da oscillazioni con durata variabile.}',
'Il confronto fra gli stessi mesi di anni diversi aiuta a riconoscere la stagionalità.')

S(29,'Una media mobile combina valori vicini',
  window_diagram()+r'\[M_t^{(q)}=\frac{1}{2q+1}\sum_{j=-q}^{q}X_{t+j}.\]',
  r'''\PBody{La semilarghezza $q$ conta i vicini su ciascun lato. Con $q=2$ la finestra contiene cinque valori, tutti con peso $1/5$.}
\vspace{3mm}
\PInfo{Il risultato viene collocato al tempo centrale $t$. Un’oscillazione può attenuarsi quando la finestra include fasi diverse del ciclo.}
\vspace{3mm}
\PBody{La media mobile modifica la risoluzione con cui leggiamo l’andamento locale. La scelta della finestra va motivata rispetto alla domanda.}''',
'La larghezza della finestra stabilisce quali variazioni contribuiscono a ciascun valore smussato.')

S(30,'Tre e tredici mesi mostrano dettagli diversi',
  tempplot(['osservata','ma3','ma13'],'Blu: osservata. Rame: media a 3 mesi. Viola: media a 13 mesi.',first=72),
  C(30,'media_mobile',r'''
ma3 <- stats::filter(z, rep(1/3, 3),
                     sides = 2)
ma13 <- stats::filter(z, rep(1/13, 13),
                      sides = 2)
plot(z, col = "grey60")
lines(ma3, col = "#C57E42")
lines(ma13, col = "#7363AA", lwd = 2)
''','confrontare due finestre')+r'\PInfo{La finestra di tredici mesi attenua fortemente il ciclo annuale. Non garantisce di eliminarlo esattamente: i pesi e il numero di mesi contano.}',
'Una curva più liscia conserva meno dettaglio. La finestra deve essere sempre dichiarata.')

S(31,'Ai bordi mancano alcuni vicini',
  edge_window()+r'\PBody{Con una finestra centrata di $2q+1$ valori, i primi e gli ultimi $q$ risultati sono NA se non estendiamo la serie.}',
  C(31,'bordi',r'''
c(NA_media3 = sum(is.na(ma3)),
  NA_media13 = sum(is.na(ma13)))
which(is.na(ma13))
# Con 240 dati completi: 2 NA e 12 NA.
stopifnot(sum(is.na(ma3)) == 2L,
          sum(is.na(ma13)) == 12L)
''','riconoscere i bordi incompleti')+r'\PInfo{Una finestra più corta al bordo cambia la definizione della stima. Un’estensione artificiale introduce ipotesi sui dati esterni.}',
'La regola ai bordi è parte del metodo e può influenzare le conclusioni sulle osservazioni più recenti.')

S(32,'Una finestra rivolta al passato è causale',
  window_diagram(past=True)+r'\[M_t^-=\frac{1}{L}\sum_{j=0}^{L-1}X_{t-j}.\]',
  C(32,'filtro_causale',r'''
passato13 <- stats::filter(z,
  rep(1/13, 13), sides = 1)
# Ogni valore usa presente e 12 mesi precedenti.
head(cbind(z, ma13, passato13), 15)
''','usare soltanto dati già disponibili')+r'\PBody{$L$ indica il numero complessivo di valori, incluso il presente. Qui la finestra è causale nel senso temporale del filtro.}'+r'\vspace{3mm}\PInfo{La curva segue più lentamente un cambiamento. Questo ritardo è distinto dalla disponibilità di dati futuri.}',
'Un filtro causale rispetta l’ordine di disponibilità dei dati. Non stabilisce relazioni di causa fra variabili.')

S(33,'Una trasformazione può anticipare il futuro',
  leakage(),
  r'''\PBody{Se calcoliamo una media centrata su tutta la serie, alcuni valori vicini al confine usano osservazioni del periodo successivo.}
\vspace{3mm}
\PInfo{Una valutazione predittiva deve riprodurre ciò che sarebbe stato disponibile in quel momento, compresa la stima delle trasformazioni.}
\vspace{3mm}
\PBody{Per una descrizione retrospettiva possiamo usare vicini futuri, dichiarandolo. Per una previsione dobbiamo rispettare la data in cui il risultato viene prodotto.}''',
'La disponibilità temporale dei dati riguarda anche preprocessing, riferimenti e parametri stimati.')

S(34,'LOESS adatta una regressione locale',
  local_fit()+r'\PSmall{Schema illustrativo: vicino al tempo centrale, i punti evidenziati contribuiscono alla regressione locale.}',
  r'''\PBody{LOESS stima un polinomio in un intorno di ciascun tempo. I punti più vicini ricevono maggiore peso.}
\vspace{3mm}
\[\widehat\beta(t)=\arg\min_\beta\sum_i w_i(t)\,[x_i-p_\beta(t_i-t)]^2.\]
\PSmall{$p_\beta$ è il polinomio locale. I pesi $w_i(t)$ dipendono dalla distanza temporale.}
\vspace{3mm}
\PInfo{Lo span stabilisce la quota di osservazioni coinvolte nell’intorno, per i valori usuali fra 0 e 1. Uno span piccolo segue dettagli più locali.}''',
'Il parametro span governa la scala locale di adattamento. La curva stimata dipende da questa scelta.')

S(35,'Lo span modifica l’andamento stimato',
  tempplot(['osservata','loess20','loess60'],'Blu: osservata. Rame: span 0,20. Viola: span 0,60.'),
  C(35,'loess',r'''
tempo_T <- seq_along(z)
lo20 <- loess(as.numeric(z) ~ tempo_T,
              span = 0.20)
lo60 <- loess(as.numeric(z) ~ tempo_T,
              span = 0.60)
head(cbind(predict(lo20), predict(lo60)))
# Stesse osservazioni, diverso intorno.
''','confrontare gli span')+r'\PBody{La curva più regolare non è automaticamente più corretta. Confrontiamo le scelte e cerchiamo quali conclusioni rimangono stabili.}',
'Una scelta di smoothing va valutata rispetto alla scala del fenomeno e ai cambiamenti che interessa descrivere.')

S(36,'La mediana mobile risponde meno a un picco',
  median_outlier()+r'\PSmall{Esempio illustrativo. Ai bordi la mediana conserva il dato originale.}',
  C(36,'mediana',r'''
v_es <- c(0, .2, -.1, .1, 6, -.1, .2, 0, .1)
med_es <- runmed(v_es, k = 3, endrule = "keep")
avg_es <- stats::filter(v_es, rep(1/3, 3))
cbind(v_es, med_es, avg_es)
# Una finestra di tre valori.
''','confrontare media e mediana')+r'\PInfo{La mediana limita l’effetto di un valore isolato. Prima di attenuarlo, occorre capire se rappresenta un errore o un evento reale.}',
'Una procedura robusta può proteggere da errori isolati e, allo stesso tempo, attenuare eventi importanti.')

S(37,'Un’anomalia dipende dal riferimento',
  reference_months()+r'\[A_t=X_t-C_{m(t)},\qquad C_m=\operatorname{media}_{\rm base}(X_t\mid m(t)=m).\]',
  C(37,'anomalia',r'''
mese_T <- as.integer(format(temp$data, "%m"))
base_T <- temp$data >= as.Date("2000-01-01") &
          temp$data <= as.Date("2004-12-01")
clima_T <- tapply(temp$temperatura_C[base_T],
                 mese_T[base_T], mean)
riferimento_T <- unname(clima_T[mese_T])
anomalia_T <- temp$temperatura_C - riferimento_T
''','usare la base 2000–2004')+r'\PInfo{Base didattica di cinque anni (2000–2004), distinta da una normale climatologica trentennale.}',
'Ogni anomalia deve dichiarare la base, la variabile e il periodo cui si riferisce.')

S(38,'STL separa trend, stagione e resto',
  tempplot(['stl_trend','stl_stagione','stl_residuo'],'Blu: trend stimato. Rame: stagione stimata. Viola: resto.',first=72),
  C(38,'stl',r'''
stl_T <- stl(z, s.window = "periodic",
             robust = TRUE)
componenti_T <- stl_T$time.series
err_stl <- max(abs(rowSums(componenti_T) -
                   as.numeric(z)))
stopifnot(err_stl < 1e-10)
plot(stl_T)
''','ricostruire la serie da STL')+r'\PInfo{s.window = "periodic" impone una stagione che si ripete. robust = TRUE riduce l’influenza dei valori anomali nella stima.}',
'Una ricostruzione esatta verifica l’identità additiva. Non dimostra che le singole componenti stimate siano vere.')

S(39,'Il resto merita una nuova analisi',
  anomaly_plot()+r'\PSmall{Temperatura simulata: anomalie rispetto alla base 2000–2004. Il trend successivo resta visibile.}',
  C(39,'registro_componenti',r'''
tab_T <- data.frame(
  data = temp$data,
  osservata = temp$temperatura_C,
  riferimento = riferimento_T,
  anomalia = anomalia_T,
  resto_STL = componenti_T[, "remainder"])
head(tab_T, 3)
''','conservare osservazioni e derivati')+r'\PBody{Togliere una stagione o una curva graduale non garantisce che il resto sia indipendente. Il prossimo controllo riguarda le relazioni fra tempi diversi.}'+r'\vspace{2mm}\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m09-smoothing}{Esperimento · Smoothing}',
'Anomalie e resti rispondono a definizioni diverse. Entrambi possono mantenere autocorrelazione.')


# Le note che spiegano la figura restano nella stessa colonna.
for n,p in [(27,r"\PBody{L’identità consente di confrontare una stima delle componenti con la verità del simulatore.}"),(37,r'\PInfo{Base didattica di cinque anni (2000–2004), distinta da una normale climatologica trentennale.}')]:
    assert p in SLIDES[n]['right']
    SLIDES[n]['right']=SLIDES[n]['right'].replace(p,'')
    SLIDES[n]['left']+=p
