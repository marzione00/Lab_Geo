"""Futura: 109 pagine di contenuto, oltre alla copertina vettoriale/3D.
Testo originale in italiano; riferimenti numerici letti dai calcoli R.
"""
from componenti import *

slide(2, 'Un percorso dalla domanda alla previsione',
 lab('Nove passaggi collegati')+table(['Sezione', 'p.'],[
 [internal_link(3,'Definire il compito e l’informazione'),'3'],
 [internal_link(11,'Costruire riferimenti confrontabili'),'11'],
 [internal_link(23,'Capire memoria e innovazioni'),'23'],
 [internal_link(40,'Specificare ARIMA e stagionalità'),'40'],
 [internal_link(58,'Diagnosticare le innovazioni stimate'),'58'],
 [internal_link(70,'Validare rispettando il tempo'),'70'],
 [internal_link(83,'Leggere errori e intervalli'),'83'],
 [internal_link(94,'Estendere a due variabili'),'94'],
 [internal_link(102,'Consegnare un progetto riproducibile'),'102']], [8.3,.7]),
 p('Borealis ha introdotto calendario, dipendenza e trasformazioni. Futura usa queste conoscenze per formulare e valutare una previsione.')+
 info('Tre archivi locali: CO$_2$ storica, fossili simulati e processi temporali simulati. Ogni risultato conserva unità, periodo e origine.')+
 p('Le 20 attività mantengono gli identificativi M10\\_N01--M10\\_N20 del sito. I notebook aggiungono risultati eseguiti, spiegazioni e verifiche.'),
 'Una buona previsione nasce da una domanda verificabile e da un protocollo dichiarato.')

slide(3, 'Dal descrivere una serie al prevederne il seguito',
 boxes([('a',2.2,3.5,'M09: descrivere\\\\tendenza e dipendenza',3.9,'GeoA'),
        ('b',7.4,3.5,'M10: prevedere\\\\a un’origine dichiarata',3.9,'GeoB'),
        ('c',2.2,1.1,'Trasformazioni\\\\e ipotesi sulla serie',3.9,'GeoA'),
        ('d',7.4,1.1,'Errori futuri\\\\e limiti del modello',3.9,'GeoB')],
       [('a','b',''),('a','c',''),('b','d',''),('c','d','')])+
 eq(r'\{y_1,\ldots,y_T\}\quad\longrightarrow\quad\widehat y_{T+h\mid T}'),
 p('La descrizione riguarda ciò che osserviamo. La previsione aggiunge un criterio: il modello deve funzionare su valori che non ha usato per stimarsi.')+
 info('Riconoscere una stagione non garantisce che la previsione migliori un semplice ciclo ripetuto.')+
 p('Il caso guida è una verifica storica: ci collochiamo a dicembre 1998 e valutiamo i mesi successivi.'),
 'L’adeguatezza descrittiva e l’utilità previsionale rispondono a domande diverse.')

slide(4, 'Origine, orizzonte e variabile da prevedere',
 timeline('origin')+eq(r'\widehat y_{T+h\mid T}=g_h(\mathcal F_T)'),
 p('L’origine $T$ è l’ultimo istante con dati disponibili. L’orizzonte $h$ misura la distanza fino al valore futuro. La variabile deve avere unità e risoluzione esplicite.')+
 info('Qui: concentrazione media mensile derivata di CO$_2$, in ppm. Origine dicembre 1998; orizzonti da 1 a 36 mesi.'),
 'Ogni previsione deve indicare che cosa prevede, quando viene emessa e quanto lontano guarda.',
 code('T0 <- end(train)\nh <- length(test)\nc(anno=T0[1], mese=T0[2], h=h)\nstopifnot(h == 36L)', 'R · fissare origine e orizzonte'), notebook=1, source=[3])

slide(5, 'Quali informazioni esistono davvero all’origine?',
 boxes([('a',2.0,3.65,'Misure osservate\\\\fino a $T$',3.2,'GeoA'),
        ('b',2.0,1.2,'Calendario futuro\\\\già noto a $T$',3.2,'GeoC'),
        ('c',7.2,2.4,'Previsione\\\\$\\widehat y_{T+h\\mid T}$',3.8,'GeoB')],
       [('a','c',''),('b','c','')])+
 sm('La misura futura entra soltanto quando si valuta l’errore.'),
 p('Il mese dell’anno è noto in anticipo. Una temperatura futura misurata sul campo non lo è. Un regressore utilizzabile in stima può quindi non essere disponibile in previsione.')+
 info('Per covariate future ignote occorre prevederle, definire scenari o rinunciare al loro impiego. La scelta va dichiarata nel compito.')+
 p('Anche correzioni, medie mobili e normalizzazioni devono usare soltanto l’informazione accessibile all’origine.'),
 'La disponibilità dell’informazione è una proprietà del compito, non della colonna nel file.', source=[3])

slide(6, 'Un protocollo storico con date precise',
 timeline()+table(['Parte','Uso'],[['1985--1998','Stima, diagnostica, validazione interna'],['1999--2001','Verifica finale del protocollo fissato']],[3,6.1]),
 p('La separazione viene fissata prima di confrontare i risultati sul test. I 168 mesi iniziali contengono tutte le informazioni usate per stimare il modello.')+
 info('Le tre origini interne sono dicembre 1994, 1995 e 1996; ciascuna prevede i 12 mesi successivi, sempre dentro il periodo di addestramento.'),
 'Il test finale valuta una procedura già definita; non serve a scegliere la variante più favorevole.',
 code('train <- window(y, end=c(1998,12))\ntest <- window(y, start=c(1999,1))\nstopifnot(length(train)==168,\n          length(test)==36)', 'R · separare per calendario'), notebook=1, source=[4])

slide(7, 'La CO2 è un archivio storico documentato',
 fig('01_CO2_finestra','204 medie mensili derivate; separazione a dicembre 1998. I dati terminano nel 2001.'),
 p('Il file locale riprende la serie di M09. Le medie mensili derivano dall’aggregazione dei valori settimanali del vecchio archivio distribuito con statsmodels.')+
 info('La data associata al mese e il numero di settimane disponibili restano nel CSV. Questa aggregazione non coincide necessariamente con una serie mensile ufficiale.')+
 sm('La provenienza e l’impronta SHA-256 sono conservate con i dati. Il notebook non scarica nuovi valori durante l’esecuzione.'),
 'Una serie storica chiusa permette un esperimento riproducibile; la sua provenienza resta parte del risultato.', source=[4,33])

slide(8, 'Prevedere una distribuzione futura',
 distribution()+eq(r'Y_{T+h}\mid\mathcal F_T\ \sim\ F_{T,h}'),
 p('La previsione puntuale riassume la distribuzione futura. L’intervallo descrive parte della sua dispersione, condizionatamente alle ipotesi adottate.')+
 info('Due modelli possono avere lo stesso centro e attribuire probabilità molto diverse ai valori estremi.')+
 p('Un intervallo predittivo riguarda una nuova osservazione. Un intervallo per la media descrive l’incertezza di una quantità media e risponde a un’altra domanda.'),
 'Centro, dispersione e probabilità degli eventi devono essere interpretati separatamente.', source=[5,22])

slide(9, 'La perdita stabilisce quale centro è ottimale',
 loss()+eq(r'\arg\min_a\,\mathbb E[(Y-a)^2\mid\mathcal F_T]=\mathbb E[Y\mid\mathcal F_T]'),
 p('La perdita quadratica penalizza fortemente gli errori grandi e porta alla media condizionata. Con perdita assoluta, una mediana condizionata minimizza il rischio.')+
 info('Perdite asimmetriche possono favorire un quantile: sottostimare e sovrastimare non hanno sempre lo stesso costo.')+
 sm('Nel modulo useremo MAE e RMSE, dichiarando anche il segno dell’errore. Un’unica graduatoria non rappresenta ogni possibile decisione.'),
 'La previsione “migliore” dipende anche dalla perdita con cui la si valuta.', source=[5,24])

slide(10, 'Il quaderno del compito previsionale',
 table(['Voce','Scelta del laboratorio'],[
 ['Obiettivo','CO$_2$ media mensile derivata, ppm'],['Origine','Dicembre 1998'],['Orizzonte','36 mesi, gennaio 1999--dicembre 2001'],
 ['Riferimenti','Ultimo valore, stagione, deriva'],['Modello','SARIMA $(0,1,1)(0,1,1)_{12}$'],['Valutazione','MAE, RMSE, bias e copertura descrittiva']], [2.6,6.5]),
 p('Prima del modello si scrive una scheda del compito. Dati, esclusioni e convenzioni diventano controlli automatici quando è possibile.')+
 info('La specifica centrale riprende quella del sito. Gli approfondimenti aggiunti nelle slide sono riconoscibili e non modificano il test finale.')+
 sm('Il notebook M10\\_N01 verifica calendario e lunghezze; M10\\_N18 prepara la consegna.'),
 'Una scelta registrata può essere verificata; una scelta implicita può cambiare durante l’analisi.', notebook=1, source=[3,4,31])

slide(11, 'Il riferimento fissa il confronto',
 table(['Metodo','Che cosa conserva'],[['Media','Livello medio dell’addestramento'],['Ultimo valore','Livello più recente'],['Stagionale','Ultimo ciclo annuale osservato'],['Deriva','Variazione media fra inizio e fine']],[3.0,6.0]),
 p('Un modello articolato acquista interesse quando migliora un riferimento adeguato al compito. Tutti i metodi devono usare la stessa origine, le stesse date e la stessa scala.')+
 info('La media del passato è utile come contrasto didattico. Su una serie con crescita persistente può essere un riferimento troppo debole.')+
 p('I riferimenti del laboratorio non richiedono la stima di una struttura ARMA.'),
 'La complessità del modello non è una misura del suo vantaggio previsionale.', notebook=2, source=[6])

slide(12, 'La media del passato presume un livello stabile',
 eq(r'\bar y_T=\frac{1}{T}\sum_{t=1}^T y_t')+eq(r'\widehat y_{T+h\mid T}^{\,\mathrm{media}}=\bar y_T')+
 info('La stessa previsione viene ripetuta per tutti gli orizzonti. Se la serie cresce, la media storica può restare lontana dall’ultimo livello.'),
 p('Questo riferimento usa tutte le osservazioni con lo stesso peso. Non conserva il mese dell’anno e non prolunga una tendenza.')+
 p('Può essere sensato per una serie che oscilla attorno a un livello costante; la scelta deve dipendere dalla struttura del problema.'),
 'Una media storica è un modello implicito di stabilità del livello.',
 code('p_media <- rep(mean(train), 36)\nhead(p_media)\nstopifnot(length(unique(p_media))==1)', 'R · riferimento al livello medio'), source=[6])

slide(13, 'L’ultimo valore prolunga il livello più recente',
 eq(r'\widehat y_{T+h\mid T}^{\,\mathrm{ultimo}}=y_T')+
 boxes([('a',2.0,2.6,r'Ultima misura\\$y_T$',3,'GeoA'),('b',7.2,2.6,r'36 copie\\$y_T,\ldots,y_T$',4,'GeoB')],[('a','b','')],4.1),
 p('La previsione resta orizzontale. È il centro naturale di un random walk senza deriva, con innovazioni future a media nulla.')+
 info('La previsione puntuale costante non implica incertezza costante: in un random walk la varianza dell’errore cresce con l’orizzonte.'),
 'Il riferimento all’ultimo valore conserva il livello, ma non aggiunge una stagione o una deriva.',
 code('p_ultimo <- rep(tail(train,1), 36)\nhead(p_ultimo)\nstopifnot(length(p_ultimo)==36)', 'R · ultimo valore'), notebook=2, source=[6])

slide(14, 'Il riferimento stagionale ripete un ciclo già noto',
 seasons()+eq(r'\widehat y_{T+h\mid T}=y_{T+h-12\lceil h/12\rceil}'),
 p('Per i primi 12 mesi si riusa l’ultimo anno osservato. A origine fissa, lo stesso ciclo si ripete anche nel secondo e nel terzo anno di previsione.')+
 info('Gennaio 2000 usa gennaio 1998, perché gennaio 1999 non era disponibile a dicembre 1998.'),
 'A origine fissa il riferimento stagionale non può incorporare osservazioni future.',
 code('p_stag <- rep(tail(train,12),\n              length.out=36)\nstopifnot(identical(\n  as.numeric(p_stag[1:12]),\n  as.numeric(p_stag[13:24])))', 'R · ripetere l’ultima stagione'), notebook=20, source=[7])

slide(15, 'L’indice stagionale va verificato sui mesi',
 table(['Previsione','Valore storico utilizzato'],[['Gennaio 1999','Gennaio 1998'],['Dicembre 1999','Dicembre 1998'],['Gennaio 2000','Gennaio 1998'],['Dicembre 2001','Dicembre 1998']],[4.1,5.0]),
 p('Una sequenza lunga il numero corretto di righe può avere una fase sbagliata. Il calendario permette di riconoscere una rotazione accidentale del ciclo.')+
 info('I test del notebook confrontano la corrispondenza tra mese previsto e mese riutilizzato, oltre alla lunghezza del vettore.'),
 'L’allineamento temporale è parte della correttezza della previsione.',
 code('mese_futuro <- rep(1:12,3)\nmese_fonte <- rep(cycle(tail(\n  train,12)),3)\nstopifnot(all(mese_futuro==\n              mese_fonte))', 'R · controllare la fase'), notebook=20, source=[7])

slide(16, 'La deriva prolunga una variazione media',
 eq(r'\widehat\delta=\frac{y_T-y_1}{T-1}')+eq(r'\widehat y_{T+h\mid T}^{\,\mathrm{deriva}}=y_T+h\widehat\delta')+
 info('La pendenza è una variazione per mese. Non è la pendenza di una regressione stimata su tutti i punti.'),
 p('Il metodo unisce il primo e l’ultimo livello e prolunga quella pendenza. Gli estremi possono influenzarlo molto, specialmente in presenza di stagione o anomalie.')+
 p('La deriva è un riferimento esplicito per la crescita: evita che il modello stagionale venga confrontato soltanto con metodi privi di tendenza.'),
 'Una deriva semplice può essere competitiva, ma la sua pendenza dipende dagli estremi osservati.',
 code('yy <- as.numeric(train)\ndelta <- (tail(yy,1)-yy[1])/\n         (length(yy)-1)\np_deriva <- tail(yy,1)+(1:36)*delta', 'R · stimare la deriva'), notebook=2, source=[6])

slide(17, 'Ogni riferimento porta ipotesi riconoscibili',
 table(['Metodo','Rischio da discutere'],[['Media','Livello storico lontano da quello attuale'],['Ultimo','Mancata crescita e mancata stagione'],['Stagionale','Ciclo stabile senza crescita fra anni'],['Deriva','Pendenza costante e stagione assente']],[2.9,6.1]),
 p('I riferimenti rappresentano ipotesi diverse. Osservare come sbagliano aiuta a capire quale informazione aggiunge il modello.')+
 info('Una previsione stagionale che ripete il 1998 può riconoscere i mesi alti e bassi e sottostimare il livello degli anni successivi.')+
 p('Le ipotesi si discutono prima della graduatoria. La prestazione si misura poi sugli stessi valori futuri.'),
 'Un riferimento va giudicato per la struttura che conserva e per quella che trascura.', source=[6,7])

slide(18, 'Le traiettorie rendono visibili le differenze',
 fig('02_baseline_CO2','Previsioni emesse alla stessa origine. Il grafico mostra le ipotesi dei riferimenti prima delle metriche.'),
 p('L’ultimo valore produce una linea orizzontale. La deriva cresce in modo lineare. Il riferimento stagionale ripete la stessa forma annuale.')+
 info('La differenza tra metodi riguarda l’informazione mantenuta dal passato. Il test finale quantificherà quanto queste scelte siano utili.')+
 sm('Per confronti numerici usare le tabelle eseguite, non misure ricavate a occhio dal grafico.'),
 'Disegnare le previsioni permette di controllare subito livello, stagione e orientamento della tendenza.', notebook=2, source=[6])

slide(19, 'Un buon adattamento non basta a prevedere bene',
 boxes([('a',2.1,3.5,'Dati usati\\\\per la stima',3.5,'GeoA'),('b',7.3,3.5,'Adattamento\\\\entro il campione',3.5,'GeoA'),
        ('c',2.1,1.1,'Dati tenuti\\\\fuori dalla stima',3.5,'GeoB'),('d',7.3,1.1,'Errore\\\\di previsione',3.5,'GeoB')], [('a','b',''),('c','d','')]),
 p('Aggiungere parametri può ridurre l’errore sul campione usato per stimarli. Questa riduzione non garantisce un miglioramento sui valori successivi.')+
 info('Il residuo del modello e l’errore di previsione fuori campione hanno ruoli distinti. La diagnostica dei residui non sostituisce la validazione.')+
 p('La verifica deve ricostruire il momento in cui la previsione sarebbe stata emessa.'),
 'La capacità di spiegare il passato deve essere accompagnata da una prova sul futuro disponibile in seguito.', source=[8,9])

slide(20, 'Due origini diverse definiscono due esperimenti',
 table(['Origine fissa','Origini aggiornate'],[['Una stima a dicembre 1998','Nuove stime quando arrivano dati'],['36 orizzonti dalla stessa origine','Più previsioni emesse nel tempo'],['Il ciclo 1998 viene ripetuto','Il ciclo può incorporare nuovi mesi'],['Una traiettoria storica riservata','Più coppie origine--orizzonte']],[4.5,4.5]),
 p('Aggiornare il modello ogni mese è possibile, ma cambia il compito. Non si può attribuire alla previsione emessa nel 1998 l’informazione arrivata nel 1999.')+
 info('Il laboratorio centrale conserva un’origine fissa per il test finale. La validazione interna usa origini successive, tutte precedenti al test.'),
 'L’origine della previsione deve restare associata a ogni errore misurato.', source=[7,8])

slide(21, 'Le origini interne fanno una prova prima del test',
 origins()+eq(r'T_o\in\{120,132,144\},\qquad h=1,\ldots,12'),
 p('A ciascuna origine si ricostruisce il passato disponibile e si stima di nuovo. I 12 mesi successivi diventano la verifica di quella previsione.')+
 info('Le tre finestre di verifica coprono 1995, 1996 e 1997. Il 1998 rimane disponibile per la stima finale sui 168 mesi.')+
 sm('Approfondiremo finestre, metriche e dipendenza fra errori nella sezione sulla validazione.'),
 'La validazione temporale ripete il compito previsionale senza aprire il test finale.', notebook=5, source=[8,9])

slide(22, 'Laboratorio: quattro riferimenti confrontabili',
 lab('Controlli richiesti')+table(['Controllo','Criterio'],[['Origine','Identica per ogni metodo'],['Date','36 mesi nello stesso ordine'],['Scala','ppm per osservazioni e previsioni'],['Stagione','Ultimi 12 mesi ripetuti'],['Futuro','Nessuna lettura del test nella stima']],[2.6,6.4]),
 p('M10\\_N02 costruisce i riferimenti; M10\\_N20 verifica la stagione. La funzione comune restituisce vettori confrontabili.')+
 info('Verificare la forma delle previsioni prima di calcolare gli errori. Un errore di allineamento può sembrare una cattiva prestazione del metodo.'),
 'La comparabilità è una condizione del confronto, non un dettaglio da controllare dopo.',
 code('b <- baseline(train, h=36)\nstopifnot(all(lengths(b)==36))\nstopifnot(all(is.finite(\n  unlist(b))))\nnames(b)', 'R · contratto dei riferimenti'), notebook=2, source=[6,7])

slide(23, 'Un AR(1) separa memoria e innovazione',
 memory('AR')+eq(r'X_t=\phi X_{t-1}+\varepsilon_t'),
 p('Nel processo centrato, una parte del valore corrente dipende dal passato. L’innovazione aggiunge ciò che il modello non poteva prevedere al passo precedente.')+
 info('Assumiamo innovazioni a media nulla, varianza $\\sigma^2$ e indipendenti dal passato. La normalità è un’ipotesi ulteriore, utile per intervalli gaussiani.')+
 sm('Se $X_t$ è centrato rispetto a $\\mu$, la serie originale è $Y_t=\\mu+X_t$.'),
 'La memoria trasmette informazione passata; l’innovazione rappresenta la parte nuova.', source=[10])

slide(24, 'Media e intercetta non sono lo stesso parametro',
 eq(r'Y_t=c+\phi Y_{t-1}+\varepsilon_t')+eq(r'\mu=c+\phi\mu\quad\Longrightarrow\quad\mu=\frac{c}{1-\phi}')+
 eq(r'Y_t-\mu=\phi(Y_{t-1}-\mu)+\varepsilon_t'),
 p('La relazione vale per un AR(1) stazionario con $|\\phi|<1$. Scrivere il modello attorno alla media rende trasparente la previsione di lungo periodo.')+
 info('Nella convenzione di stats::arima, per un ARMA non differenziato il termine chiamato intercept rappresenta la media del processo, non il $c$ della ricorrenza.'),
 'Prima di interpretare un coefficiente bisogna conoscere la parametrizzazione usata dal software.',
 code('mu <- 10\nphi <- 0.65\nc0 <- mu*(1-phi)\nstopifnot(all.equal(\n  c0/(1-phi), mu))', 'R · dalla media alla ricorrenza'), source=[10,33])

slide(25, 'La previsione a un passo elimina lo shock futuro',
 eq(r'\mathbb E[\varepsilon_{T+1}\mid\mathcal F_T]=0')+
 eq(r'\widehat Y_{T+1\mid T}=\mu+\phi(Y_T-\mu)')+
 info('Con $\\mu=0$, $\\phi=0{,}65$ e $Y_T=2$, il centro previsto è $1{,}30$.'),
 p('Il valore osservato all’origine è noto. L’innovazione futura non lo è: nella media condizionata il suo contributo scompare.')+
 p('Questo non afferma che l’innovazione reale sarà zero. Il valore futuro può trovarsi sopra o sotto il centro previsto.'),
 'La media condizionata annulla il contributo medio dell’innovazione, non la sua variabilità.',
 code('phi <- 0.65; xT <- 2\np1 <- phi*xT\nc(previsione=p1, varianza=1)', 'R · previsione AR(1) a un passo'), source=[10,11])

slide(26, 'La ricorsione porta la previsione verso la media',
 fig('16_AR1_previsione','Esempio teorico: $\\phi=0{,}65$, $\\mu=0$, $X_T=2$, $\\sigma=1$. Parametri noti.')+
 eq(r'\widehat Y_{T+h\mid T}=\mu+\phi^h(Y_T-\mu)'),
 p('Ogni nuovo passo moltiplica per $\\phi$ lo scostamento residuo dalla media. Quando $|\\phi|<1$, il contributo dell’ultima osservazione si attenua.')+
 info('Se $\\phi<0$, il centro previsto alterna il segno dello scostamento. Se $\\phi$ è vicino a 1, il ritorno è più lento.'),
 'La previsione AR(1) stazionaria ricorda sempre meno il valore iniziale al crescere di $h$.',
 code('h_ar <- 1:30\np_ar <- 0.65^h_ar*2\nhead(p_ar)', 'R · ricorsione in forma chiusa'), source=[10])

slide(27, 'L’errore raccoglie gli shock non ancora osservati',
 eq(r'e_{T+h\mid T}=\sum_{j=0}^{h-1}\phi^j\varepsilon_{T+h-j}')+
 table(['Orizzonte','Innovazioni che entrano'],[['1',r'$\varepsilon_{T+1}$'],['2',r'$\varepsilon_{T+2}+\phi\varepsilon_{T+1}$'],['3',r'$\varepsilon_{T+3}+\phi\varepsilon_{T+2}+\phi^2\varepsilon_{T+1}$']],[2,7.1]),
 p('Allungare l’orizzonte aggiunge nuove innovazioni. Gli shock più vicini all’origine vengono trasmessi attraverso potenze di $\\phi$.')+
 info('La somma riguarda soltanto innovazioni successive a $T$. Con parametri noti, la storia osservata è già incorporata nel centro previsto.')+
 sm('Il segno dell’errore adottato qui è sempre osservato meno previsto.'),
 'L’orizzonte aumenta il numero di innovazioni che la previsione non può conoscere.', source=[11])

slide(28, 'La varianza AR(1) cresce verso un limite',
 fig('17_AR1_varianza','Parametri noti. Il limite coincide con la varianza stazionaria del processo.')+
 eq(r'\operatorname{Var}(e_{T+h\mid T})=\sigma^2\frac{1-\phi^{2h}}{1-\phi^2}'),
 p('Con innovazioni incorrelate, la varianza della somma è la somma delle varianze pesate. Per $|\\phi|<1$, la serie geometrica converge.')+
 info('A un passo la varianza è $\\sigma^2$. Per orizzonti lunghi tende a $\\sigma^2/(1-\\phi^2)$: non cresce senza limite come nel random walk.'),
 'In un AR(1) stazionario, l’incertezza condizionata tende alla variabilità marginale del processo.',
 code('v_ar <- (1-0.65^(2*h_ar))/\n        (1-0.65^2)\nc(primo=v_ar[1],\n  limite=1/(1-0.65^2))', 'R · varianza previsionale'), source=[11])

slide(29, 'Il coefficiente cambia persistenza e oscillazione',
 fig('14_AR1_traiettorie','Quattro simulazioni con innovazioni di varianza unitaria; i percorsi servono a confrontare forme di dipendenza.'),
 p('Un coefficiente positivo alto tende a produrre sequenze persistenti. Un coefficiente negativo favorisce alternanza fra scostamenti di segno opposto.')+
 info('Non basta osservare una lunga sequenza sopra la media per diagnosticare una tendenza: anche un processo stazionario molto persistente può produrla.')+
 sm('Le simulazioni usano semi registrati. Le traiettorie non rappresentano misure ambientali.'),
 'Persistenza elevata e non stazionarietà possono apparire simili in campioni brevi.', source=[10,12])

slide(30, 'L’autocorrelazione teorica segue le potenze di phi',
 fig('15_AR1_ACF_teorica','ACF esatte dei processi illustrati; non sono stime ottenute da un singolo campione.')+
 eq(r'\rho(k)=\phi^{|k|}'),
 p('Per $\\phi>0$ la correlazione decresce mantenendo il segno. Per $\\phi<0$ il segno alterna. Il modulo determina la velocità di attenuazione.')+
 info('L’ACF campionaria oscilla attorno alla forma teorica. Un grafico campionario non deve coincidere punto per punto con questa curva.'),
 'La struttura teorica orienta l’interpretazione; l’incertezza campionaria resta visibile.',
 code('lag_ar <- 0:20\nrho <- 0.65^lag_ar\ncbind(lag=lag_ar, rho=rho)[1:6,]', 'R · ACF teorica'), source=[10,12])

slide(31, 'Un AR(p) usa più ritardi della stessa serie',
 eq(r'X_t=\phi_1X_{t-1}+\cdots+\phi_pX_{t-p}+\varepsilon_t')+
 eq(r'\phi(B)X_t=\varepsilon_t,\qquad\phi(z)=1-\sum_{j=1}^p\phi_jz^j')+
 info('L’operatore di ritardo soddisfa $BX_t=X_{t-1}$. Le radici del polinomio descrivono la stabilità della ricorrenza.'),
 p('I coefficienti pesano ritardi diversi. La somma dei coefficienti, da sola, non è un controllo generale della stazionarietà per ogni ordine.')+
 p('Per un AR causale stazionario tutte le radici di $\\phi(z)=0$ devono stare fuori dal cerchio unitario.'),
 'Negli AR di ordine superiore la condizione corretta riguarda tutte le radici del polinomio.', source=[12])

slide(32, 'Le radici AR devono stare fuori dal cerchio unitario',
 roots('AR')+eq(r'1-0{,}6z=0\quad\Longrightarrow\quad z=1/0{,}6'),
 p('Il disegno mostra un AR(1) con $\\phi=0{,}6$. La radice è circa $1{,}67$ e ha modulo maggiore di uno.')+
 info('Per un AR(2), polyroot riceve i coefficienti in ordine di potenza crescente: costante, termine in $z$, termine in $z^2$.'),
 'Radici AR fuori dal cerchio unitario corrispondono a una dinamica causale stazionaria.',
 code('phi2 <- c(0.6,-0.2)\nradici <- polyroot(c(1,-phi2))\nMod(radici)\nstopifnot(all(Mod(radici)>1))', 'R · controllo per un AR(2)'), source=[12])

slide(33, 'Un MA(1) combina innovazioni, non osservazioni',
 memory('MA')+eq(r'X_t=\varepsilon_t+\theta\varepsilon_{t-1}'),
 p('Il termine moving average indica una combinazione di innovazioni presenti e passate. Non è una media mobile usata per lisciare i dati.')+
 info('Adottiamo il segno positivo della convenzione R. Le innovazioni hanno media nulla, varianza $\\sigma^2$ e sono incorrelate nel tempo.'),
 'Nel modello MA si mediano shock latenti; una media mobile descrittiva combina dati osservati.',
 code('set.seed(101033)\nx_ma <- arima.sim(list(ma=0.6),\n                  n=240)\nhead(x_ma)', 'R · simulare un MA(1)'), source=[13])

slide(34, 'L’ACF di un MA(1) si annulla oltre il primo ritardo',
 fig('18_MA1_ACF','ACF teorica per $\\theta=0{,}6$.')+
 eq(r'\rho(1)=\frac{\theta}{1+\theta^2},\qquad\rho(k)=0\ \ (|k|>1)'),
 p('Due valori consecutivi condividono un’innovazione. Valori separati da più di un passo non condividono innovazioni in questo modello.')+
 info('La proprietà di taglio vale per l’ACF teorica. Le correlazioni campionarie ai ritardi successivi non sono esattamente zero.'),
 'Il taglio teorico dell’ACF non elimina le fluttuazioni della sua stima campionaria.',
 code('theta <- 0.6\nc(rho1=theta/(1+theta^2),\n  rho2=0)\nARMAacf(ma=theta, lag.max=5)', 'R · ACF MA(1)'), source=[13])

slide(35, 'Invertire un MA permette di ricostruire gli shock',
 roots('MA')+eq(r'\theta(z)=1+\theta z,\qquad |z_{\mathrm{radice}}|>1'),
 p('L’invertibilità consente di esprimere le innovazioni mediante una combinazione stabile della storia osservata. Per MA(1) richiede $|\\theta|<1$.')+
 info('Stazionarietà e invertibilità sono proprietà diverse: un MA finito è stazionario sotto le ipotesi sulle innovazioni, anche quando non è invertibile.'),
 'La condizione sulle radici MA sceglie una rappresentazione degli shock recuperabile dal passato.',
 code('theta <- 0.6\nradice_ma <- polyroot(c(1,theta))\nMod(radice_ma)\nstopifnot(Mod(radice_ma)>1)', 'R · invertibilità MA(1)'), source=[14])

slide(36, 'Nel MA(1) la memoria predittiva diretta è breve',
 eq(r'\widehat X_{T+1\mid T}=\theta\varepsilon_T')+
 eq(r'\widehat X_{T+h\mid T}=0\quad (h\geq2)')+
 info('Queste formule assumono innovazioni ricostruite dalla storia e parametri noti. Con un campione finito, l’inizializzazione introduce una differenza pratica.'),
 p('A un passo rimane lo shock noto all’origine. A due o più passi entrano soltanto innovazioni future, la cui media condizionata è zero.')+
 p('L’incertezza rimane: la varianza passa da $\\sigma^2$ a $\\sigma^2(1+\\theta^2)$. Una previsione media nulla non significa processo costante.'),
 'Una memoria predittiva finita può convivere con una variabilità futura non nulla.', source=[13,14])

slide(37, 'ARMA combina propagazione e shock ritardati',
 eq(r'\phi(B)X_t=\theta(B)\varepsilon_t')+
 eq(r'X_t=\phi X_{t-1}+\varepsilon_t+\theta\varepsilon_{t-1}')+
 table(['Componente','Informazione rappresentata'],[['AR','Valori passati e propagazione'],['MA','Innovazioni passate e correzioni']],[2.5,6.6]),
 p('Un ARMA(1,1) unisce le due strutture. Le condizioni per una rappresentazione causale e invertibile si applicano ai rispettivi polinomi.')+
 info('AR e MA possono produrre ACF simili su campioni brevi. L’identificazione richiede confronto, parsimonia e verifica.'),
 'La struttura ARMA descrive la dipendenza dopo che il livello e la stagione sono stati trattati.',
 code('set.seed(101037)\nx_arma <- arima.sim(\n  list(ar=0.65,ma=0.4), n=240)\nacf(x_arma, plot=FALSE)$acf[1:6]', 'R · processo ARMA(1,1)'), source=[14,15])

slide(38, 'La risposta a un impulso rende visibile la memoria',
 fig('19_risposta_impulso','Risposte teoriche a un’innovazione unitaria: AR(1), MA(1) e ARMA(1,1).',height=4.75)+
 eq(r'X_t=\sum_{j=0}^{\infty}\psi_j\varepsilon_{t-j}'),
 p('I coefficienti $\\psi_j$ descrivono quanto resta di uno shock dopo $j$ passi. Nel MA finito la risposta termina; nell’AR causale si attenua nel tempo.')+
 info('La rappresentazione è lineare e riferita al modello. Non attribuisce automaticamente allo shock un significato fisico causale.'),
 'La durata dell’effetto di un’innovazione spiega la forma della memoria previsionale.',
 code('psi <- c(1,ARMAtoMA(\n  ar=0.65, ma=0.4, lag.max=20))\nhead(psi)', 'R · pesi della risposta'), source=[10,13,14])

slide(39, 'ACF e PACF suggeriscono ipotesi da verificare',
 fig('20_ARMA_ACF_PACF','Esempio simulato ARMA(1,1): entrambe le funzioni possono attenuarsi gradualmente.'),
 p('Per un AR puro la PACF teorica si interrompe dopo l’ordine; per un MA puro si interrompe l’ACF. In una combinazione ARMA entrambe possono avere una coda.')+
 info('Su dati reali, tendenza, stagione, campione breve e rumore alterano la leggibilità di questi indizi.')+
 p('I grafici orientano una piccola famiglia di candidati. Non sono un algoritmo infallibile per scegliere un modello.'),
 'L’identificazione propone una struttura; diagnostica e validazione ne valutano l’utilità.', source=[12,13,14])

slide(40, 'ARIMA modella la dipendenza dopo le differenze',
 boxes([('a',2.1,3.7,r'Serie in livelli\\$Y_t$',3.4,'GeoA'),
        ('b',7.3,3.7,r'Differenze\\$W_t=(1-B)^dY_t$',3.7,'GeoB'),
        ('c',7.3,1.1,r'Modello ARMA\\per $W_t$',3.7,'GeoC')], [('a','b',''),('b','c','')])+
 eq(r'\phi(B)(1-B)^dY_t=\theta(B)\varepsilon_t'),
 p('La sigla ARIMA$(p,d,q)$ distingue ordine autoregressivo, numero di differenze e ordine della parte MA.')+
 info('Differenziare cambia la variabile modellata. Il software deve poi ricostruire la previsione nella scala dei livelli.')+
 p('Le differenze si scelgono per affrontare una struttura persistente; non si aggiungono soltanto per ridurre un indice numerico.'),
 'ARIMA applica una struttura ARMA alla serie trasformata dalle differenze.', source=[15])

slide(41, 'La prima differenza misura un cambiamento',
 eq(r'\Delta Y_t=Y_t-Y_{t-1}=(1-B)Y_t')+
 table(['Serie','Interpretazione'],[['$Y_t$','Concentrazione nel mese $t$, ppm'],['$\\Delta Y_t$','Variazione fra due mesi, ppm'],['$\\Delta^2Y_t$','Variazione della variazione, ppm']],[3,6.0]),
 p('La differenza conserva l’unità fisica ma cambia la domanda. Un valore vicino a zero indica un cambiamento piccolo, non una concentrazione piccola.')+
 info('Per una griglia mensile, un incremento è riferito a un passo di calendario. Non è automaticamente un tasso istantaneo per giorno.'),
 'Trasformare la serie richiede di riscrivere il significato della quantità analizzata.',
 code('d1 <- diff(train)\nc(livelli=length(train),\n  differenze=length(d1))\nhead(d1)', 'R · differenza ordinaria'), source=[15])

slide(42, 'La differenza stagionale confronta lo stesso mese',
 eq(r'\Delta_{12}Y_t=Y_t-Y_{t-12}=(1-B^{12})Y_t')+
 seasons()+sm('La differenza confronta mesi omologhi; il riferimento stagionale usa lo stesso collegamento per prevedere.'),
 p('La differenza a 12 mesi rimuove una componente che si ripete identica ogni anno. Se il livello cresce, la differenza stagionale può conservare una media positiva.')+
 info('Una stagione deterministica stabile e una radice unitaria stagionale sono ipotesi diverse. La scelta delle differenze deve essere motivata.'),
 'La frequenza della serie dà significato al ritardo stagionale.',
 code('d12 <- diff(train, lag=12)\nstopifnot(length(d12)==156)\nfrequency(train)', 'R · differenza a dodici mesi'), source=[16])

slide(43, 'Le due differenze combinano quattro osservazioni',
 eq(r'(1-B)(1-B^{12})Y_t')+eq(r'=Y_t-Y_{t-1}-Y_{t-12}+Y_{t-13}')+
 table(['Termine','Peso'],[['$Y_t$','$+1$'],['$Y_{t-1}$','$-1$'],['$Y_{t-12}$','$-1$'],['$Y_{t-13}$','$+1$']],[6.0,3.0]),
 p('Le differenze ordinaria e stagionale commutano. Nel campione mensile iniziale si perdono 13 valori per calcolare direttamente la trasformazione combinata.')+
 info('Il modello in spazio di stato può trattare l’inizializzazione internamente. Questo non autorizza a interpretare senza cautela i primi residui.'),
 'Espandere gli operatori permette di controllare segni, ritardi e perdita di osservazioni.',
 code('w <- diff(diff(train, lag=12))\nw2 <- diff(diff(train), lag=12)\nstopifnot(isTRUE(all.equal(w,w2)))\nlength(w)', 'R · combinare le differenze'), source=[16,18])

slide(44, 'Il confronto delle trasformazioni resta nel train',
 fig('21_differenze_CO2','Tre trasformazioni calcolate sui soli 168 mesi di addestramento.'),
 p('Confrontiamo andamento, dispersione e dipendenza dopo ogni trasformazione. L’obiettivo è una struttura sufficientemente stabile per il modello scelto.')+
 info('Il grafico suggerisce ipotesi, ma non dimostra da solo stazionarietà o correttezza della specifica.')+
 sm('Differenziare troppo può introdurre dipendenza artificiale e aumentare la varianza. Le scelte vanno valutate insieme alla diagnostica e alla prestazione.'),
 'Ogni trasformazione si giustifica attraverso il problema e si valuta senza usare il test finale.', source=[15,16])

slide(45, 'La sigla stagionale mantiene distinti sei ordini',
 eq(r'\operatorname{SARIMA}(p,d,q)(P,D,Q)_{12}')+
 table(['Parte','Significato'],[['$p,d,q$','AR, differenze, MA ai ritardi ordinari'],['$P,D,Q$','AR, differenze, MA ai ritardi stagionali'],['12','Numero di osservazioni in un ciclo annuale']],[2.4,6.7]),
 p('Gli ordini maiuscoli descrivono la struttura stagionale. Il periodo 12 riguarda dati mensili con ciclo annuale; non è un numero universale.')+
 info('Per dati trimestrali il ciclo annuale ha periodo 4. Una frequenza dichiarata male cambia l’interpretazione dei ritardi.'),
 'Ordini ordinari, ordini stagionali e periodo del ciclo devono restare leggibili nella specifica.',
 code('specifica <- list(\n  order=c(0,1,1),\n  seasonal=list(order=c(0,1,1),\n                period=12))\nspecifica', 'R · descrivere il modello'), source=[16,17])

slide(46, 'Il modello del laboratorio è prefissato',
 eq(r'\operatorname{SARIMA}(0,1,1)(0,1,1)_{12}')+
 eq(r'(1-B)(1-B^{12})Y_t')+eq(r'=(1+\theta B)(1+\Theta B^{12})\varepsilon_t')+
 info('Una differenza ordinaria, una differenza stagionale, una componente MA ordinaria e una MA stagionale; nessuna deriva esplicita.'),
 p('La specifica riprende il laboratorio del sito. Viene stimata sui livelli del train, lasciando a stats::arima il compito di applicare le differenze.')+
 p('La crescita futura può emergere dall’integrazione e dallo stato stimato. “Senza deriva esplicita” non significa previsione piatta.'),
 'La specifica del modello deve precedere la lettura del suo errore finale.', notebook=3, source=[16,17])

slide(47, 'Il prodotto stagionale introduce anche il ritardo 13',
 eq(r'(1+\theta B)(1+\Theta B^{12})')+eq(r'=1+\theta B+\Theta B^{12}+\theta\Theta B^{13}')+
 table(['Ritardo dell’innovazione','Coefficiente'],[['0','$1$'],['1','$\\theta$'],['12','$\\Theta$'],['13','$\\theta\\Theta$']],[6,3]),
 p('La struttura moltiplicativa non stima quattro coefficienti liberi. Il termine al ritardo 13 è il prodotto delle due componenti MA.')+
 info('Espandere la formula evita di confondere il SARIMA con un MA non stagionale di ordine 13 avente tutti i coefficienti liberi.'),
 'Una struttura stagionale moltiplicativa vincola i coefficienti e conserva parsimonia.', source=[16])

slide(48, 'Passare i livelli evita di differenziare due volte',
 table(['Ingresso alla stima','Ordini coerenti'],[['Livelli $Y_t$','$d=1$, $D=1$ nel SARIMA'],['Differenze già calcolate','ARMA della trasformata, senza ripetere $d,D$'],['Livelli e trasformata insieme','Scegliere una sola procedura esplicita']],[4.6,4.5]),
 p('Nel percorso principale si passa train in livelli. Applicare prima diff e poi mantenere d=1 e D=1 nella chiamata produrrebbe ulteriori differenze.')+
 info('La trasformata serve qui all’esplorazione. L’oggetto fit conserva il modello stimato sui livelli per restituire previsioni in ppm.'),
 'I passaggi di trasformazione devono apparire una volta sola nel procedimento.',
 code('fit <- arima(train,\n  order=c(0,1,1),\n  seasonal=list(order=c(0,1,1),\n                period=12),\n  include.mean=FALSE, method="ML")', 'R · specifica completa sui livelli'), notebook=3, source=[17])

slide(49, 'La verosimiglianza valuta i parametri del modello',
 eq(r'\widehat\vartheta=\arg\max_{\vartheta}\ell(\vartheta;y_{1:T})')+
 boxes([('a',2,3.0,'Specifica\\\\e parametri candidati',3.3,'GeoA'),('b',7.3,3.0,'Verosimiglianza\\\\dei dati osservati',3.7,'GeoB'),
        ('c',4.7,.9,'Ottimizzazione numerica',4.2,'GeoC')],[('a','b',''),('b','c',''),('c','a','')],4.4),
 p('La stima ML usa la struttura probabilistica del modello. Per una serie integrata, stats::arima tratta lo stato iniziale attraverso la rappresentazione in spazio di stato.')+
 info('Un risultato numerico non basta: si controllano codice di convergenza, coefficienti e matrice di covarianza stimata.'),
 'Specificazione statistica e ottimizzazione numerica sono due passaggi da verificare entrambi.',
 code('fit$code\ncoef(fit)\nsqrt(diag(fit$var.coef))\nstopifnot(fit$code==0)', 'R · leggere la stima'), source=[17,33])

slide(50, 'I coefficienti stimati restano associati al train',
 lab('Stima ML sul periodo 1985--1998')+
 metric_table('coefficienti_SARIMA',['termine','stima','se'],['Termine','Stima','Errore standard'])+
 eq(r'\widehat\sigma^2='+value('co2','sigma2')+r'\ \mathrm{ppm}^2'),
 p('Le due componenti MA descrivono dipendenza nella serie differenziata. I coefficienti non misurano direttamente un tasso di crescita annuale della concentrazione.')+
 info('Gli errori standard dei coefficienti riassumono l’incertezza di stima sotto il modello. Non sono gli errori standard delle previsioni future.')+
 sm('Tabelle e formule numeriche sono generate dai risultati R, con arrotondamento soltanto nella presentazione.'),
 'Interpretare un coefficiente richiede di ricordare quale trasformata e quale convenzione lo definiscono.', source=[17])

slide(51, 'Media, intercetta e deriva richiedono attenzione',
 table(['Caso','Convenzione utilizzata'],[['ARMA non differenziato','include.mean può stimare una media'],['ARIMA con differenze','include.mean non aggiunge una deriva'],['Deriva esplicita','Richiede una parametrizzazione coerente'],['Modello del laboratorio','Nessun regressore di deriva esplicita']],[4.2,4.9]),
 p('In stats::arima, include.mean viene ignorato quando sono presenti differenze. Non basta impostarlo a TRUE per ottenere una deriva nel livello.')+
 info('Con più ordini di integrazione, aggiungere termini deterministici può implicare andamenti polinomiali. Serve esplicitare quale crescita si sta imponendo.'),
 'Il nome di un argomento non sostituisce la lettura della parametrizzazione del modello.', source=[16,17,33])

slide(52, 'Una famiglia piccola di candidati',
 table(['Candidato','Parte ordinaria'],[['SARIMA $(0,1,1)(0,1,1)_{12}$','MA(1)'],['SARIMA $(1,1,0)(0,1,1)_{12}$','AR(1)'],['SARIMA $(1,1,1)(0,1,1)_{12}$','ARMA(1,1)']],[6.6,2.5]),
 p('L’approfondimento confronta tre strutture mantenendo la stessa finestra, le stesse differenze e lo stesso metodo di stima.')+
 info('La specifica centrale resta quella prefissata dal sito. Il confronto illustra come documentare una scelta sul train, senza riscrivere il risultato finale dopo aver visto il test.')+
 sm('Un insieme piccolo e motivato è più leggibile di una ricerca indiscriminata su molte combinazioni.'),
 'La famiglia dei candidati deve essere motivata prima di consultare la verifica finale.', source=[15,17])

slide(53, 'AIC e BIC bilanciano adattamento e parametri',
 eq(r'\operatorname{AIC}=-2\widehat\ell+2k')+eq(r'\operatorname{BIC}=-2\widehat\ell+k\log n')+
 info('Qui $k$ include la varianza. Il campione efficace della verosimiglianza ha $n=155$, dopo le 13 posizioni iniziali associate alle differenze.'),
 p('Questi criteri confrontano modelli con verosimiglianze comparabili. Valori più bassi indicano il compromesso preferito dal criterio, non un errore futuro già misurato.')+
 info('Nel confronto usiamo lo stesso train e gli stessi $d,D$. Cambiare differenze o risposta può rendere non confrontabili i valori riportati.'),
 'Un criterio informativo orienta la scelta sul campione disponibile; non sostituisce la validazione temporale.',
 code('c(AIC=AIC(fit), BIC=BIC(fit))\nlogLik(fit)\nnobs(fit)', 'R · criteri sul train'), source=[17,33])

slide(54, 'Leggere il confronto entro le sue condizioni',
 fig('22_AIC_train','Tre specifiche sullo stesso train e con le stesse differenze. Altezze: $\\Delta$AIC; numeri: AIC assoluto.'),
 p('La graduatoria riguarda soltanto i candidati considerati. Un valore vicino fra modelli suggerisce prudenza nel trattare la scelta come definitiva.')+
 info('Convergenza, diagnostica, semplicità e prestazione interna restano elementi distinti da riportare.')+
 p('Il modello centrale conserva la specifica del laboratorio, così i risultati sono confrontabili con il sito.'),
 'Un minimo in una piccola tabella non dimostra che il modello sia universalmente migliore.', source=[17])

slide(55, 'La previsione torna nella scala dei livelli',
 boxes([('a',2.0,3.4,'Modello stimato\\\\sui livelli del train',3.3,'GeoA'),('b',7.2,3.4,'Previsione\\\\e varianza a ogni $h$',3.7,'GeoB'),
        ('c',4.6,1.0,'Date future e unità in ppm',5.4,'GeoC')],[('a','b',''),('b','c','')])+
 eq(r'\widehat y_{T+h\mid T},\qquad s_h=\sqrt{\widehat{\operatorname{Var}}(e_h)}'),
 p('predict applicato all’oggetto arima restituisce il centro e l’errore standard dei valori futuri. Non occorre sommare manualmente le differenze quando il modello è stato stimato sui livelli.')+
 info('Le date vanno assegnate e controllate esplicitamente prima di confrontare previsione e osservazione.'),
 'La scala della previsione deve coincidere con quella del valore futuro valutato.',
 code('pred <- predict(fit,n.ahead=36)\np_hat <- as.numeric(pred$pred)\ns_hat <- as.numeric(pred$se)\nstopifnot(length(p_hat)==36,\n          all(s_hat>0))', 'R · previsione e errore standard'), notebook=6, source=[22,23])

slide(56, 'Un random walk accumula incertezza senza limite',
 fig('25_random_walk_varianza','Confronto teorico con parametri noti e innovazioni di varianza unitaria.')+
 eq(r'Y_t=Y_{t-1}+\varepsilon_t,\qquad\operatorname{Var}(e_h)=h\sigma^2'),
 p('Nel random walk ogni innovazione futura entra con peso uno. La varianza dell’errore cresce linearmente con l’orizzonte.')+
 info('Il confronto con AR(1) mostra perché la presenza di una radice unitaria cambia il comportamento della previsione di lungo periodo.')+
 sm('Un SARIMA integrato può avere una crescita dell’incertezza più articolata, legata anche alla stagione.'),
 'Le radici unitarie cambiano la propagazione degli shock e l’incertezza a orizzonti lunghi.', source=[11,15,22])

slide(57, 'Laboratorio: modello e specifica insieme',
 table(['Oggetto conservato','Perché serve'],[['Dati e separazione','Ripetere esattamente la stima'],['Ordini e metodo','Ricostruire la specifica'],['Coefficienti e convergenza','Valutare la soluzione numerica'],['Modello RDS','Riprendere la previsione'],['Versione di R','Interpretare differenze numeriche']],[4.0,5.1]),
 p('M10\\_N03 costruisce il modello; M10\\_N09 esporta le previsioni. La consegna conserva sia i numeri leggibili sia gli oggetti necessari alla riproduzione.')+
 info('Un oggetto RDS è utile per riprendere il lavoro. Dati e script restano necessari per spiegare da dove proviene.'),
 'La riproducibilità richiede la procedura completa, oltre all’oggetto finale salvato.',
 code('class(fit)\nfit$call\ngetRversion()', 'R · identificare l’oggetto stimato'), notebook=9, source=[17,31,32])

slide(58, 'La diagnostica esamina ciò che il modello lascia',
 boxes([('a',2.0,3.5,'Serie osservata',3.2,'GeoA'),('b',7.1,3.5,'Modello stimato',3.5,'GeoB'),
        ('c',2.0,1.1,'Innovazioni stimate',3.2,'GeoC'),('d',7.1,1.1,'Strutture residue?',3.5,'GeoB')],[('a','b',''),('b','c',''),('c','d','')]),
 p('Le innovazioni stimate dovrebbero essere compatibili con la struttura assunta. Sequenze, dipendenze e cambiamenti di dispersione indicano aspetti da approfondire.')+
 info('Un residuo non è un’innovazione teorica osservata direttamente. Deriva dalla stima e dall’inizializzazione del modello.')+
 p('La diagnostica usa il train. Il test finale rimane disponibile per misurare la prestazione della procedura fissata.'),
 'La diagnostica cerca informazione rimasta nei residui, senza trasformarsi in una prova di perfezione.', notebook=4, source=[18])

slide(59, 'I primi residui risentono dell’inizializzazione',
 eq(r'r_t=\widehat\varepsilon_t,\qquad t=14,\ldots,168')+
 table(['Quantità','Valore nel laboratorio'],[['Residui disponibili nel fit','168 posizioni'],['Intervallo diagnostico','Dalla posizione 14'],['Residui esaminati','155 valori finiti'],['Motivazione','Convenzione coerente con l’inizializzazione']],[5.0,4.0]),
 p('Il percorso online esclude i primi 13 valori dalla diagnostica. Manteniamo questa convenzione e la rendiamo esplicita.')+
 info('Non è una regola universale per qualsiasi ARIMA. La quantità da escludere dipende dal modello, dal metodo e dalla valutazione dell’inizializzazione.'),
 'Una scelta sui residui iniziali deve essere documentata e applicata prima dei test.',
 code('res <- as.numeric(residuals(fit))\nres <- res[14:length(res)]\nstopifnot(length(res)==155,\n          all(is.finite(res)))', 'R · residui per la diagnostica'), notebook=4, source=[18])

slide(60, 'La sequenza residua mantiene il calendario',
 fig('08_residui_SARIMA','Innovazioni stimate dalla posizione 14; unità in ppm. La linea zero è il riferimento.'),
 p('Cerchiamo sequenze lunghe dello stesso segno, cambiamenti di dispersione, valori isolati e gruppi di anomalie.')+
 info('Un grafico temporale conserva l’ordine. Un istogramma degli stessi residui perderebbe queste informazioni.')+
 p('La prima lettura è descrittiva: un’anomalia visiva diventa una domanda da verificare, non una spiegazione automatica.'),
 'Un residuo anomalo va localizzato nel tempo prima di attribuirgli un significato.', source=[18])

slide(61, 'Residui centrati possono essere dipendenti',
 eq(r'\bar r=\frac{1}{n_r}\sum_{t=1}^{n_r}r_t')+
 table(['Controllo','Domanda'],[['Centro','Resta uno scostamento sistematico?'],['Dispersione','La variabilità è plausibilmente stabile?'],['Ordine','Restano sequenze o cicli?'],['Estremi','Ci sono osservazioni da esaminare?']],[3.2,5.9]),
 p('Residui mediamente vicini a zero possono essere fortemente correlati. Viceversa, una sequenza senza correlazione evidente può avere una distribuzione problematica per le bande gaussiane.')+
 info('Centro, dipendenza e distribuzione vengono controllati con strumenti diversi.'),
 'La diagnostica richiede più di un singolo numero riassuntivo.',
 code('c(media=mean(res),\n  sd=sd(res), min=min(res),\n  max=max(res))', 'R · riassunti dei residui'), source=[18,21])

slide(62, 'L’ACF residua cerca dipendenza lineare rimasta',
 fig('09_ACF_residui','ACF delle 155 innovazioni stimate. Le bande servono come riferimento approssimato.'),
 p('Una correlazione residua ai ritardi 12 o 24 suggerirebbe una struttura annuale non completamente rappresentata. Anche i ritardi brevi meritano attenzione.')+
 info('Più ritardi si guardano, più è probabile osservare qualche superamento isolato delle bande. Conta la struttura complessiva.'),
 'L’ACF residua è una verifica della dipendenza rimasta ai ritardi esaminati.',
 code('acf_res <- acf(res,lag.max=36,\n               plot=FALSE)\nacf_res$acf[c(2,13,25)]', 'R · ritardi 1, 12 e 24'), notebook=4, source=[19])

slide(63, 'Le bande dell’ACF non sono un test simultaneo',
 eq(r'\widehat\rho_k\ \approx\ 0\ \pm\ \frac{1{,}96}{\sqrt{n_r}}')+
 info('La formula è un riferimento puntuale approssimato in condizioni di rumore bianco. La stima di parametri e la lettura di molti ritardi complicano l’interpretazione.'),
 p('Un singolo superamento non basta a dichiarare il modello errato. Una successione coerente di correlazioni può essere più informativa di un picco isolato.')+
 p('La scelta dei ritardi va collegata alla domanda: breve memoria, ciclo annuale, o dipendenza più lunga.')+
 sm('Per aggregare più autocorrelazioni useremo Ljung--Box, dichiarando lag e gradi di libertà.'),
 'Una banda grafica puntuale non protegge contemporaneamente tutti i ritardi ispezionati.', source=[19,20])

slide(64, 'Ljung–Box aggrega più correlazioni residue',
 eq(r'Q=n_r(n_r+2)\sum_{k=1}^{m}\frac{\widehat\rho_k^2}{n_r-k}')+
 eq(r'Q\ \dot\sim\ \chi^2_{m-r},\qquad m=24,\quad r=2')+
 info('Nel protocollo si sottraggono i due coefficienti MA stimati. Restano 22 gradi di libertà per il riferimento asintotico.'),
 p('L’ipotesi nulla riguarda l’assenza di autocorrelazioni ai ritardi considerati. Il test riassume correlazioni al quadrato e non attribuisce un significato fisico ai loro segni.')+
 p('Il riferimento è approssimato: dimensione campionaria, stima e modello incidono sulla sua calibrazione.'),
 'Il risultato di Ljung–Box va riportato insieme a numero di residui, ritardo massimo e correzione.', source=[20,33])

slide(65, 'Il risultato diagnostico non certifica il modello',
 lab('Ljung–Box sul protocollo dichiarato')+
 table(['Quantità','Risultato'],[['Residui','155'],['Ritardo massimo','24'],['Gradi di libertà','22'],['Statistica $Q$',value('co2','LjungBox_Q')],['Valore $p$',value('co2','LjungBox_p')]], [5.2,3.8]),
 p('Il valore $p$ quantifica quanto la statistica sia compatibile con il riferimento del test. Non è la probabilità che il modello sia vero.')+
 info('Un risultato non significativo non prova indipendenza, normalità o buona previsione. Riguarda questa verifica di autocorrelazione.'),
 'La mancata evidenza contro un’ipotesi non è una dimostrazione della sua correttezza.',
 code('lb <- Box.test(res, lag=24,\n  type="Ljung-Box", fitdf=2)\nc(Q=unname(lb$statistic),\n  df=unname(lb$parameter),\n  p=lb$p.value)', 'R · Ljung–Box'), notebook=4, source=[20])

slide(66, 'Il QQ plot esamina forma e code della distribuzione',
 fig('10_QQ_residui','Quantili campionari delle innovazioni stimate contro quantili gaussiani; linea di riferimento.'),
 p('Scostamenti nelle code possono rendere meno attendibili intervalli costruiti con una distribuzione normale, anche quando l’ACF residua è modesta.')+
 info('Il grafico non dimostra normalità. Permette di localizzare quali parti della distribuzione si allontanano dal riferimento.')+
 sm('Per prevedere la media non è sempre necessaria la normalità. La probabilità attribuita agli estremi richiede ipotesi più specifiche.'),
 'La distribuzione dei residui conta soprattutto quando si interpretano probabilità e intervalli.', source=[21])

slide(67, 'Autocorrelazione e dispersione sono distinte',
 eq(r'\operatorname{Cov}(\varepsilon_t,\varepsilon_{t-k})=0')+
 eq(r'\nRightarrow\quad\operatorname{Var}(\varepsilon_t\mid\mathcal F_{t-1})=\sigma^2')+
 info('Assenza di correlazione lineare e varianza condizionata costante sono proprietà differenti.'),
 p('Periodi con residui piccoli seguiti da periodi molto dispersi possono segnalare eteroschedasticità. L’ACF dei residui al quadrato è un approfondimento descrittivo.')+
 info('In questo modulo non stimiamo una famiglia di modelli di volatilità. Registriamo il limite se la dispersione appare variabile.'),
 'Un controllo della media e dell’ACF non esaurisce la verifica della variabilità.',
 code('acf_quadrati <- acf(res^2,\n  lag.max=24, plot=FALSE)\nhead(as.numeric(acf_quadrati$acf))', 'R · dipendenza dei quadrati'), source=[18,21])

slide(68, 'Documentare l’origine delle anomalie',
 table(['Possibile origine','Azione motivata'],[['Errore di registrazione','Controllare la fonte e conservare la correzione'],['Evento reale','Mantenerlo e discuterne il significato'],['Cambio di procedura','Documentare la discontinuità'],['Modello inadeguato','Rivedere l’ipotesi usando il train']],[3.4,5.7]),
 p('Eliminare un valore perché peggiora una metrica modifica il problema dopo aver visto il risultato. Le regole di esclusione devono dipendere da una ragione verificabile.')+
 info('Se una modifica viene suggerita dal test finale, quel periodo ha partecipato allo sviluppo. Occorre dichiararlo e trovare una nuova verifica indipendente.'),
 'La pulizia dei dati è una scelta scientifica da motivare, non un modo per migliorare retroattivamente il risultato.', source=[18,31])

slide(69, 'Laboratorio: scrivere una conclusione diagnostica',
 lab('Una conclusione in quattro parti')+
 table(['Evidenza','Che cosa riportare'],[['Sequenza','Andamento e anomalie osservate'],['Dipendenza','ACF e lag esaminati'],['Test aggregato','$Q$, gradi di libertà e valore $p$'],['Distribuzione','QQ plot e limiti delle bande']],[3.1,6.0]),
 p('La conclusione unisce strumenti complementari. Per esempio: “Ai ritardi esaminati non emerge una forte struttura lineare residua; le bande restano condizionate al modello e alle sue ipotesi”.')+
 info('M10\\_N04 include l’esecuzione e l’interpretazione. La formulazione finale deve seguire i risultati realmente osservati, senza promuovere un test a certificazione generale.'),
 'Una buona conclusione diagnostica nomina sia l’evidenza sia ciò che il controllo non stabilisce.', notebook=4, source=[18,19,20,21])

slide(70, 'La validazione rispetta il tempo della decisione',
 origins()+eq(r'\widehat y_{o+h\mid o}=g_h(y_1,\ldots,y_o)'),
 p('Ogni previsione interna viene costruita usando soltanto osservazioni antecedenti o contemporanee alla propria origine. Il valore futuro serve dopo, per calcolare l’errore.')+
 info('Separare righe a caso può distribuire passato e futuro in entrambe le parti e alterare il compito di previsione temporale.'),
 'Il disegno di validazione deve imitare l’uso previsto del modello.', notebook=5, source=[8,9])

slide(71, 'Una finestra crescente conserva tutto il passato',
 origins()+sm('Origine 120: train 1--120, verifica 121--132.\\\\Origine 132: train 1--132, verifica 133--144.\\\\Origine 144: train 1--144, verifica 145--156.'),
 p('Nel protocollo principale il primo mese rimane fisso e il train si allunga. Ogni origine produce 12 previsioni.')+
 info('La stima viene ripetuta: non si usa il modello finale sui 168 mesi per fingere una previsione emessa anni prima.'),
 'La previsione storica di ogni origine richiede una stima che usi soltanto il suo passato.',
 code('origini <- c(120,132,144)\nstopifnot(all(origini+12<=\n              length(train)))\ncv <- valida_origini(train,origini)', 'R · origini del protocollo'), notebook=5, source=[8,9])

slide(72, 'Una finestra mobile dimentica il passato più remoto',
 table(['Finestra crescente','Finestra di ampiezza fissa'],[['$1,\\ldots,o$','$o-w+1,\\ldots,o$'],['Più dati a ogni origine','Stesso numero di dati'],['Adatta a struttura stabile','Può seguire cambiamenti locali'],['Conserva vecchi regimi','Aumenta sensibilità al campione recente']],[4.6,4.5]),
 p('La scelta dipende da quanto si ritiene stabile il processo. Una finestra corta può adattarsi più rapidamente e stimare i parametri con maggiore incertezza.')+
 info('Nel laboratorio usiamo la finestra crescente. Una finestra mobile è una variante da progettare e valutare all’interno del train.'),
 'Dimenticare dati è una scelta di modello sul compromesso fra stabilità e adattamento.', source=[8])

slide(73, 'Tre origini e trentasei coppie di verifica',
 fig('06_cv_origini','Calendario delle origini interne e delle rispettive verifiche a 12 mesi.'),
 p('Il confronto conserva una riga per coppia origine--orizzonte, con osservazione, previsione del SARIMA e riferimenti.')+
 info('Le tre finestre future sono distinte, ma i train sono sovrapposti. Le stime e i loro errori non diventano automaticamente repliche indipendenti.'),
 'Il numero di righe non coincide necessariamente con il numero di repliche statisticamente indipendenti.',
 code('dim(cv)\ntable(cv$origine)\nrange(cv$h)\nstopifnot(nrow(cv)==36)', 'R · struttura della validazione'), notebook=5, source=[8,9])

slide(74, 'Tutta la procedura va ripetuta dentro ogni origine',
 boxes([('a',2.1,3.65,'Passato disponibile\\\\alla singola origine',3.6,'GeoA'),('b',7.4,3.65,'Trasformazioni\\\\e stima',3.6,'GeoC'),
        ('c',2.1,1.15,'Errore sui mesi\\\\successivi',3.6,'GeoB'),('d',7.4,1.15,'Previsione\\\\per quei mesi',3.6,'GeoB')],
       [('a','b',''),('b','d',''),('d','c','')]),
 p('Se una trasformazione stima media, scala, parametri di imputazione o componenti, deve essere appresa dal train della singola origine.')+
 info('Una normalizzazione stimata sull’intera serie trasferirebbe informazioni del futuro nella procedura interna.')+
 p('Il protocollo conserva la specifica SARIMA, ma ricalcola i coefficienti per ogni passato disponibile.'),
 'La validazione riguarda una procedura intera, non soltanto l’ultima chiamata di previsione.', source=[8,9])

slide(75, 'La dispersione fra origini è parte del risultato',
 fig('07_cv_RMSE','RMSE sui 12 mesi successivi a ciascuna origine; confronti sulla stessa scala in ppm.'),
 p('Una media complessiva può nascondere origini facili e difficili. Il grafico mostra se un vantaggio è stabile oppure concentrato in una sola finestra.')+
 info('Tre origini sono poche per descrivere la variabilità delle prestazioni. Il risultato sostiene una valutazione locale del protocollo.')+
 sm('Si riportano i valori per origine e i riferimenti, evitando di presentare un solo numero come proprietà generale del modello.'),
 'La prestazione deve essere accompagnata dal periodo e dalla variabilità fra situazioni valutate.', source=[8,9])

slide(76, 'La tabella interna tiene separati i metodi',
 metric_table('validazione_interna',['origine','RMSE_SARIMA','RMSE_stagionale','RMSE_deriva'],['Origine','SARIMA','Stagionale','Deriva'])+
 sm('RMSE in ppm. Origini 120, 132 e 144: dicembre 1994, dicembre 1995 e dicembre 1996.'),
 p('I metodi sono valutati sugli stessi mesi futuri di ogni origine. Nessuna cella usa il test 1999--2001.')+
 info('La graduatoria interna è un’evidenza sul compito a 12 mesi. Non dimostra da sola il comportamento a 36 mesi.')+
 p('Se si modifica una scelta in base a questa tabella, la modifica resta parte dello sviluppo sul train.'),
 'Il confronto è equo quando origine, orizzonte, osservazioni e metrica sono gli stessi.', source=[8,9])

slide(77, 'Un approfondimento usa trentasette origini mensili',
 origins(True)+eq(r'o=120,121,\ldots,156,\qquad h=1,\ldots,12'),
 p('L’approfondimento aggiunge 37 origini e 444 coppie origine--orizzonte, tutte interne ai primi 168 mesi. Serve a osservare il comportamento per orizzonte.')+
 info('Le verifiche si sovrappongono. La stessa osservazione può comparire come futuro a orizzonti diversi: non si tratta di 444 casi indipendenti.')+
 sm('Questo ampliamento è distinto dalle tre origini del protocollo ripreso dal sito.'),
 'Più origini offrono una descrizione più ricca, ma la sovrapposizione va dichiarata.', source=[8])

slide(78, 'L’errore può cambiare con l’orizzonte',
 fig('35_rolling_orizzonte','Approfondimento: 37 origini mensili, sempre nel train. Ogni orizzonte riassume 37 previsioni.'),
 p('Un modello può essere competitivo a un mese e perdere vantaggio a un anno. Per questo una metrica aggregata su più orizzonti non basta a descrivere ogni uso.')+
 info('Le curve sono descrittive e riguardano questo archivio. La dipendenza fra origini impedisce di leggere le differenze come se fossero medie di repliche indipendenti.'),
 'L’orizzonte è parte del risultato, non una semplice etichetta della previsione.', source=[8,24])

slide(79, 'La mappa degli errori distingue periodo e orizzonte',
 fig('36_rolling_errori','Errore osservato meno previsto; scala cromatica simmetrica. Origini e orizzonti sono distinti.'),
 p('Bande verticali o orizzontali possono indicare periodi difficili o orizzonti problematici. Il segno aiuta a riconoscere sottostima e sovrastima.')+
 info('Una struttura visiva suggerisce una domanda. Non identifica automaticamente un cambiamento fisico o una causa.')+
 sm('Il grafico conserva le 444 coppie, mentre una singola RMSE ne ridurrebbe tutta l’informazione a uno scalare.'),
 'Una vista con origine e orizzonte permette di localizzare le difficoltà del modello.', source=[8,25])

slide(80, 'Il test finale si apre dopo aver fissato la procedura',
 timeline()+info('La specifica, i riferimenti e le metriche sono registrati prima di leggere i risultati 1999--2001.'),
 p('Il test finale valuta l’intera procedura sviluppata sul train. Usarlo ripetutamente per scegliere varianti lo trasforma in un ulteriore campione di sviluppo.')+
 info('Una revisione suggerita dal test può essere scientificamente utile. Va dichiarata come nuova ipotesi e verificata su altro materiale.')+
 p('La stima finale torna a usare tutti i 168 mesi, con le scelte ormai fissate.'),
 'La separazione tra sviluppo e verifica protegge l’interpretazione della prestazione.', source=[9])

slide(81, 'Verificare la separazione dal test',
 boxes([('a',2.1,3.5,'Copia dei dati\\\\con test alterato',3.6,'GeoB'),('b',7.4,3.5,'Train estratto\\\\per calendario',3.6,'GeoA'),
        ('c',2.1,1.1,'Train originale',3.6,'GeoA'),('d',7.4,1.1,'Previsioni\\\\identiche',3.6,'GeoC')],
       [('a','b',''),('b','d',''),('c','d','')]),
 p('La verifica automatica altera tutti i 36 valori futuri e ripete l’estrazione del train. Train, riferimenti e previsione SARIMA devono rimanere identici.')+
 info('Il controllo rileva una dipendenza accidentale dai valori del test nel procedimento implementato. Non sostituisce la revisione delle scelte fatte dall’analista.'),
 'Un controllo utile prova un rischio concreto e osserva un effetto che deve restare invariato.',
 code('stopifnot(max(time(train)) <\n          min(time(test)))\nstopifnot(length(intersect(\n  time(train),time(test)))==0)', 'R · separazione del calendario'), source=[9,32])

slide(82, 'Laboratorio: il disegno prima del punteggio',
 table(['Da dichiarare','Protocollo principale'],[['Origini','120, 132, 144'],['Finestra','Crescente, da gennaio 1985'],['Orizzonte interno','12 mesi'],['Aggiornamento','Nuova stima per origine'],['Test finale','36 mesi a origine fissa'],['Limite','Poche origini e errori dipendenti']],[3.5,5.5]),
 p('M10\\_N05 produce la tabella per origine. Il rapporto deve spiegare come sono stati ottenuti i numeri, oltre a indicare il modello con l’errore minore.')+
 info('L’approfondimento con 37 origini non cambia il protocollo centrale. Serve a esplorare il rapporto fra orizzonte e prestazione.'),
 'Una metrica senza il disegno di validazione non è un risultato interpretabile.', notebook=5, source=[8,9])

slide(83, 'Prima delle metriche si controllano date e segno',
 eq(r'e_h=y_{T+h}-\widehat y_{T+h\mid T}')+
 table(['Segno','Interpretazione'],[['$e_h>0$','Il modello ha sottostimato'],['$e_h<0$','Il modello ha sovrastimato'],['$e_h=0$','Previsione e osservazione coincidono']],[2.8,6.3]),
 p('La convenzione osservato meno previsto viene mantenuta in tutte le tabelle. Il confronto richiede la stessa data, la stessa unità e vettori della stessa lunghezza.')+
 info('R può riciclare vettori di lunghezze differenti. Un controllo esplicito evita che un errore di struttura produca una metrica apparentemente valida.'),
 'Una metrica corretta richiede coppie temporali corrette.',
 code('obs <- as.numeric(test)\np_hat <- as.numeric(fc$previsto)\nstopifnot(length(obs)==length(p_hat))\ne <- obs-p_hat\nstopifnot(all(is.finite(e)))', 'R · errore osservato meno previsto'), notebook=7, source=[23])

slide(84, 'MAE, RMSE e bias rispondono a domande diverse',
 eq(r'\operatorname{MAE}=\frac{1}{H}\sum_{h=1}^H|e_h|')+
 eq(r'\operatorname{RMSE}=\sqrt{\frac{1}{H}\sum_{h=1}^He_h^2}')+
 eq(r'\operatorname{bias}=\frac{1}{H}\sum_{h=1}^He_h'),
 p('MAE misura la dimensione media dell’errore assoluto. RMSE attribuisce più peso agli errori grandi. Il bias conserva il segno e rileva uno scostamento sistematico medio.')+
 info('Tutte e tre sono in ppm. Un bias piccolo può nascondere errori grandi di segno opposto; non sostituisce MAE o RMSE.'),
 'Dimensione dell’errore e direzione dello scostamento richiedono riassunti distinti.',
 code('metriche(obs, p_hat)\nc(MAE=mean(abs(e)),\n  RMSE=sqrt(mean(e^2)),\n  bias=mean(e))', 'R · tre metriche complementari'), notebook=7, source=[24,25])

slide(85, 'Il test storico misura il vantaggio sui riferimenti',
 lab('Stessa origine, stessi 36 mesi, unità ppm')+
 metric_table('metriche_CO2',['modello','MAE','RMSE','bias'],['Metodo','MAE','RMSE','Bias'])+
 sm('Bias = osservato meno previsto. Nessuna scelta del modello è aggiornata usando questa graduatoria.'),
 p('Il SARIMA migliora i riferimenti nel test dichiarato. La deriva è un confronto più esigente del ciclo stagionale ripetuto perché rappresenta una crescita del livello.')+
 info('Il vantaggio riguarda l’archivio, l’origine e gli orizzonti indicati. Non equivale a una garanzia per un’altra serie o per un’altra epoca.')+
 sm('La tabella è letta direttamente dai risultati eseguiti in R.'),
 'La prestazione è una proprietà del modello insieme al compito e al campione di verifica.', notebook=7, source=[24])

slide(86, 'Una sovrastima persistente nel test',
 fig('04_errori_CO2','Sequenza degli errori nel test; valori negativi indicano sovrastima del livello osservato.'),
 p('Il bias del SARIMA è '+value('co2','bias_SARIMA')+' ppm. La buona RMSE rispetto ai riferimenti convive quindi con uno scostamento prevalentemente negativo.')+
 info('Un’unica metrica senza segno nasconderebbe questa informazione. La sequenza temporale aiuta a distinguere errori isolati e deviazioni persistenti.')+
 sm('Una struttura nel test può suggerire nuove ipotesi, da valutare poi con un nuovo protocollo.'),
 'Migliorare un riferimento non significa aver eliminato ogni errore sistematico.', source=[25])

slide(87, 'La traiettoria prevista va letta con il suo intervallo',
 fig('03_previsione_CO2','Previsione emessa a dicembre 1998; banda puntuale al 95\\% condizionata al modello stimato.'),
 p('Il centro conserva la stagione e prolunga la dinamica del livello. L’intervallo cresce perché aumenta l’incertezza sugli shock futuri.')+
 info('I valori osservati sono aggiunti soltanto per valutare la previsione storica. Non entrano nel modello che ha prodotto questa traiettoria.')+
 p('L’ampiezza della banda va letta insieme all’errore del centro: contengono informazioni complementari.'),
 'Un grafico previsionale deve rendere visibili origine, unità, osservazioni e natura della banda.', notebook=6, source=[22,23])

slide(88, 'L’intervallo gaussiano usa l’errore standard futuro',
 fig('11_errore_standard_previsione','Errore standard previsto a ogni orizzonte; il modello tratta i parametri stimati come fissati.')+
 eq(r'I_h=\left[\widehat y_h-z_{0{,}975}s_h,\ \widehat y_h+z_{0{,}975}s_h\right]'),
 p('La banda al 95\\% usa un quantile normale e l’errore standard della previsione. Si interpreta separatamente per ciascun orizzonte.')+
 info('L’errore standard non è lo stesso numero della RMSE misurata sui 36 mesi. Il primo deriva dal modello; la seconda dagli errori realizzati.'),
 'Un intervallo predittivo combina una previsione centrale, una varianza e un’ipotesi distributiva.',
 code('z <- qnorm(0.975)\nlo <- fc$previsto-z*fc$se\nhi <- fc$previsto+z*fc$se\nstopifnot(all(lo<=hi))', 'R · intervallo al 95%'), notebook=6, source=[22])

slide(89, 'La banda è condizionata a ipotesi precise',
 table(['Incluso nel calcolo','Non propagato automaticamente'],[['Shock futuri del modello','Incertezza dei coefficienti stimati'],['Stato e dinamica stimati','Incertezza nella scelta della famiglia'],['Orizzonte e stagionalità','Cambiamenti strutturali futuri'],['Distribuzione gaussiana assunta','Errori di misura o covariate ignote non modellati']],[4.5,4.6]),
 p('La documentazione di predict.Arima specifica che gli errori standard escludono l’incertezza dei parametri ARMA e di regressione.')+
 info('La banda riguarda il modello stimato e le sue assunzioni. Una copertura nominale non è una promessa incondizionata sul mondo reale.'),
 'Un intervallo va accompagnato da ciò che la sua procedura include e da ciò che lascia fuori.', source=[22,33])

slide(90, 'Valutare copertura e ampiezza insieme',
 fig('13_ampiezza_intervalli','Ampiezza degli intervalli puntuali al 95\\% per i 36 orizzonti.')+
 eq(r'A_h=U_h-L_h'),
 p('Intervalli molto ampi possono includere molte osservazioni e offrire poca precisione. Una copertura elevata, da sola, non stabilisce l’utilità della previsione.')+
 info('Il confronto tra bande richiede lo stesso livello nominale e lo stesso compito. L’ampiezza si interpreta nella scala fisica della variabile.'),
 'Una previsione probabilistica utile deve essere valutata per affidabilità e precisione.',
 code('ampiezza <- fc$superiore-\n            fc$inferiore\nc(min=min(ampiezza),\n  media=mean(ampiezza),\n  max=max(ampiezza))', 'R · ampiezza delle bande'), notebook=8, source=[26])

slide(91, 'Copertura su più traiettorie simulate',
 fig('23_AR1_copertura_MC','2.000 traiettorie AR(1) indipendenti, con parametri noti e identica origine. Copertura per orizzonte.'),
 p('Nella simulazione conosciamo il processo che genera i dati. Ripetiamo lo stesso esperimento molte volte e contiamo quante osservazioni entrano nell’intervallo a ciascun orizzonte.')+
 info('Le repliche indipendenti sono le 2.000 traiettorie. Gli orizzonti della stessa traiettoria rimangono dipendenti.')+
 sm('Le oscillazioni attorno a 0,95 sono variabilità Monte Carlo: non una correzione applicata alla CO$_2$.'),
 'La copertura nominale si riferisce a ripetizioni del procedimento nelle condizioni del modello.', source=[11,22,26])

slide(92, 'Copertura osservata e calibrazione',
 fig('12_copertura_blocchi','Test storico diviso nei tre blocchi di 12 mesi; tutti i 36 valori risultano inclusi nelle bande.',height=4.75)+
 eq(r'\widehat C=\frac{1}{36}\sum_{h=1}^{36}\mathbf1\{y_{T+h}\in I_h\}=1'),
 p('Il risultato descrittivo è 36 su 36. I punti appartengono a una sola traiettoria con origine comune e non sono 36 prove Bernoulli indipendenti.')+
 info('Non ricaviamo da questo conteggio una prova di calibrazione al 95\\%, né la probabilità che l’intera traiettoria futura resti nella banda.')+
 sm('Una banda puntuale al 95\\% non è una banda simultanea al 95\\% per tutti gli orizzonti.'),
 'La copertura empirica di una singola traiettoria va descritta senza attribuirle una certezza che non possiede.', notebook=8, source=[26])

slide(93, 'La verifica teorica aiuta a controllare i calcoli',
 fig('24_AR1_varianza_MC','Varianza empirica su 2.000 repliche confrontata con la formula AR(1) a parametri noti.'),
 p('Nel caso simulato la formula della varianza è nota. La concordanza con il calcolo Monte Carlo controlla la ricorsione, i pesi e l’orientamento degli indici.')+
 info('Questo controllo valida un’implementazione in un caso noto. Non dimostra che il SARIMA descriva perfettamente la serie storica di CO$_2$.')+
 p('La verifica numerica e la validità scientifica hanno entrambe un ruolo, ma rispondono a domande distinte.'),
 'Un caso teorico noto è un controllo utile dei calcoli e ha un ambito di validità esplicito.', source=[11,26])

slide(94, 'Un VAR collega i passati di due variabili',
 var_network()+eq(r'\mathbf Z_t=\mathbf c+A\mathbf Z_{t-1}+\boldsymbol\varepsilon_t'),
 p('Ogni equazione usa il valore passato della variabile stessa e quello dell’altra. I coefficienti incrociati descrivono un contributo predittivo condizionato al modello.')+
 info('Il laboratorio usa x\\_VAR e y\\_VAR di un archivio simulato. I primi 250 tempi servono alla stima, i successivi 10 alla verifica.'),
 'Un modello multivariato valuta se il passato congiunto aggiunge informazione previsionale.',
 code('v <- processi[1:250,\n  c("x_VAR","y_VAR")]\nvarfit <- stima_VAR1(v)\nvarfit$A', 'R · due equazioni collegate'), notebook=14, source=[27])

slide(95, 'Le due regressioni condividono le stesse righe',
 eq(r'X_t=c_x+a_{11}X_{t-1}+a_{12}Y_{t-1}+\varepsilon_{x,t}')+
 eq(r'Y_t=c_y+a_{21}X_{t-1}+a_{22}Y_{t-1}+\varepsilon_{y,t}')+
 table(['Risposte','Regressori'],[['Tempi 2--250','Tempi 1--249'],['249 coppie complete','Stessa matrice per entrambe le equazioni']],[4.5,4.6]),
 p('Il ritardo si costruisce mantenendo l’allineamento. Eliminare valori mancanti separatamente nelle due serie potrebbe produrre coppie temporali scorrette.')+
 info('Nel dataset del laboratorio le righe usate sono complete. Con lo stesso insieme di regressori, si possono stimare le due equazioni separatamente con lm.'),
 'Una regressione con ritardi deve conservare il significato temporale di ogni coppia.',
 code('dv <- varfit$dati_ritardati\nstopifnot(nrow(dv)==249)\ncoef(varfit$x)\ncoef(varfit$y)', 'R · equazioni sulle stesse coppie'), notebook=14, source=[27,30])

slide(96, 'La stabilità VAR riguarda gli autovalori della matrice',
 fig('31_VAR_autovalori','Autovalori della matrice VAR(1) stimata rispetto al cerchio unitario.')+
 eq(r'\rho(A)=\max_j|\lambda_j|='+value('VAR','raggio_spettrale')+r'<1'),
 p('Per un VAR(1) stabile, le potenze di A si attenuano. Gli autovalori della matrice dinamica devono stare dentro il cerchio unitario.')+
 info('Per l’AR avevamo chiesto radici del polinomio fuori dal cerchio. Non è una contraddizione: le due convenzioni sono reciproche.'),
 'La stabilità VAR si controlla sugli autovalori della matrice, distinguendoli dalle radici del polinomio AR.',
 code('lambda <- eigen(varfit$A,\n                only.values=TRUE)$values\nMod(lambda)\nstopifnot(all(Mod(lambda)<1))', 'R · raggio spettrale'), notebook=15, source=[27,28])

slide(97, 'Le equazioni multivariate richiedono diagnostica',
 fig('33_VAR_ACF_residui','ACF dei residui delle due equazioni, stimati sui primi 250 tempi.'),
 p('Per ogni equazione si esaminano sequenza, dispersione e autocorrelazione residua. In un sistema multivariato possono restare anche dipendenze incrociate.')+
 info('Le due ACF marginali sono un primo controllo. Non costituiscono da sole una diagnostica multivariata completa né un test di indipendenza congiunta.')+
 sm('L’esempio resta una base didattica: rende verificabili allineamento, stabilità e contributo del ritardo dell’altra variabile.'),
 'Passare a due variabili amplia anche le strutture residue che devono essere controllate.', notebook=15, source=[27])

slide(98, 'Granger confronta due modelli annidati',
 lab('Il passato di X aggiunge informazione per Y?')+
 eq(r'M_R:\ Y_t=c+aY_{t-1}+u_t')+
 eq(r'M_F:\ Y_t=c+aY_{t-1}+bX_{t-1}+u_t')+
 eq(r'H_0:b=0'),
 p('Il modello ridotto usa il solo passato di Y. Quello completo aggiunge il passato di X. Il confronto richiede la stessa risposta e le stesse osservazioni.')+
 info('Una significatività indica contributo predittivo nella specifica considerata. Non dimostra causalità fisica né esclude variabili comuni omesse.'),
 'Il risultato di Granger è condizionato a variabili, ritardi, periodo e ipotesi del modello.',
 code('ridotto_y <- lm(y~y_lag,data=dv)\ncompleto_y <- varfit$y\nanova(ridotto_y, completo_y)', 'R · confronto X verso Y'), notebook=16, source=[29,30])

slide(99, 'Le due direzioni richiedono una lettura congiunta',
 lab('Confronti sui medesimi 249 tempi')+
 metric_table('Granger',['direzione','F','p','p_Holm'],['Direzione','F','p','p Holm'])+
 info('La correzione di Holm riguarda la famiglia delle due direzioni esaminate. Le ipotesi dei test F restano necessarie.'),
 p('Nell’archivio simulato emerge un contributo del passato di X alla previsione di Y, mentre la direzione opposta non presenta evidenza analoga.')+
 info('La conclusione riguarda il sistema simulato e il VAR(1). Non attribuisce un effetto causale a una misura ambientale reale.'),
 'L’interpretazione scientifica deve restare più specifica dell’etichetta “causalità di Granger”.',
 code('g1 <- anova(ridotto_y,varfit$y)\ng2 <- anova(lm(x~x_lag,data=dv),\n            varfit$x)\np_g <- c(g1$`Pr(>F)`[2],\n         g2$`Pr(>F)`[2])\np.adjust(p_g,method="holm")', 'R · due direzioni, correzione Holm'), notebook=16, source=[29,30])

slide(100, 'La previsione VAR usa i propri valori futuri',
 eq(r'\widehat{\mathbf Z}_{T+1\mid T}=\widehat{\mathbf c}+\widehat A\mathbf Z_T')+
 eq(r'\widehat{\mathbf Z}_{T+h\mid T}=\widehat{\mathbf c}+\widehat A\widehat{\mathbf Z}_{T+h-1\mid T}')+
 info('Dopo il primo passo si riusano le previsioni, non le osservazioni future del file.'),
 p('Una previsione ricorsiva a 10 passi parte dal tempo 250. Usare il vero valore del tempo 251 per prevedere 252 cambierebbe il compito in una sequenza di previsioni aggiornate.')+
 info('La risposta a uno shock fissato si propaga come $A^h\\mathbf u$. Attribuire agli shock un significato strutturale richiederebbe ulteriori ipotesi.'),
 'La ricorsione multistep deve rispettare l’informazione disponibile all’unica origine dichiarata.',
 code('varpred <- previsione_VAR1(\n  varfit,ultimo=v[250,],h=10)\nstopifnot(all(dim(varpred)==c(10,2)))\nhead(varpred)', 'R · dieci passi ricorsivi'), notebook=17, source=[27,28])

slide(101, 'Il test VAR conserva due errori e un riferimento',
 fig('32_VAR_previsioni','Verifica ricorsiva ai tempi 251--260: osservazioni e previsioni per X e Y.'),
 p('RMSE per X: '+value('VAR','RMSE_X')+' con VAR, '+value('VAR','RMSE_ultimo_X')+' con ultimo valore. Per Y: '+value('VAR','RMSE_Y')+' e '+value('VAR','RMSE_ultimo_Y')+'.')+
 info('Dieci tempi costituiscono una verifica breve. Il vantaggio in questo esempio non dimostra superiorità generale del VAR.')+
 sm('Il notebook conserva la tabella completa e il confronto nelle unità originali del generatore.'),
 'Un’estensione multivariata deve mostrare il beneficio osservato per ciascuna variabile.', notebook=17, source=[27,30])

slide(102, 'Il progetto parte da una domanda',
 table(['Percorso','Domanda verificabile'],[['Previsione ambientale','Migliora un riferimento a un orizzonte fissato?'],['Morfometria','Una misura disponibile predice un’altra?'],['Struttura dei campioni','Quali raggruppamenti sono stabili e interpretabili?']],[3.7,5.4])+
 info('La CO$_2$ guida la lezione. Il progetto di base dei notebook riguarda la morfometria; l’estensione VAR resta facoltativa.'),
 p('Il progetto integra domanda, dati, metodo, verifica e conclusione. La scelta del metodo segue la quantità da studiare e il modo in cui saranno disponibili i dati.')+
 info('Nel clustering manca una risposta futura da prevedere: stabilità e interpretazione dei gruppi richiedono criteri diversi da MAE o RMSE.')+
 sm('M10\\_N10 aiuta a delimitare il progetto; il rapporto evita di includere analisi che non contribuiscono alla domanda.'),
 'Un progetto convincente mantiene allineati domanda, informazione, metodo e criterio di valutazione.', notebook=10, source=[31])

slide(103, 'I fossili offrono un secondo compito predittivo',
 fig('26_fossili_train_test','Archivio simulato di 160 fossili: 128 per la stima e 32 per il test, una riga su cinque riservata.'),
 p('Prevediamo il diametro interno dalla misura del diametro totale. Il confronto è fra una retta stimata sul train e la media dei diametri interni del train.')+
 info('La separazione deterministica riprende il sito ed è riproducibile. Non equivale a un campionamento indipendente da popolazioni o laboratori nuovi.'),
 'Un secondo caso aiuta a distinguere le regole comuni di previsione dalle caratteristiche del tempo.',
 code('fossilifit <- lm(\n  diametro_int_um~diametro_tot_um,\n  data=fossilitrain)\np_fos <- predict(fossilifit,\n                 newdata=fossilitest)', 'R · retta sui fossili simulati'), notebook=11, source=[31])

slide(104, 'La geometria aiuta a prevedere i fossili',
 fig('29_fossili_RMSE','RMSE sul test di 32 fossili, in micrometri; confronto con la media del train.',height=4.7)+
 eq(r'd_{\mathrm{interno}}=d_{\mathrm{totale}}-2s'),
 p('La retta ottiene RMSE '+value('fossili','RMSE_retta')+' µm; la media del train '+value('fossili','RMSE_media')+' µm. L’archivio rispetta un’identità geometrica fra diametri e spessore.')+
 info('Il risultato è quindi coerente con il generatore. Non costituisce una scoperta biologica su fossili reali.')+
 sm('Rapporto interno/totale o spessore possono rivelare direttamente la risposta: la loro disponibilità va definita prima del modello.'),
 'Un risultato accurato deve essere interpretato alla luce di come i dati sono stati costruiti.', notebook=11, source=[31])

slide(105, 'Residui e diagonale completano la metrica',
 fig('28_fossili_residui','Residui del modello sul train: controllare andamento e dispersione rispetto ai valori adattati.'),
 '\\includegraphics[width=7.4cm,height=3.45cm,keepaspectratio]{Risultati/Figure/27_fossili_osservato_previsto.pdf}\n'+
 p('Nel test, la diagonale indica previsione perfetta. Scostamenti sistematici possono essere poco visibili in una sola RMSE.')+
 info('Il modello usa soltanto il diametro totale. Le proprietà del generatore delimitano l’interpretazione scientifica.'),
 'Un numero di prestazione va accompagnato da grafici che rendano visibili direzione e struttura dell’errore.', notebook=12, source=[31])

slide(106, 'Una relazione sostenuta dai risultati',
 table(['Parte','Contenuto richiesto'],[['Domanda','Variabile, popolazione o periodo, uso previsto'],['Dati','Fonte, unità, esclusioni e disponibilità'],['Metodo','Ipotesi, riferimenti e scelte'],['Verifica','Disegno, metriche e diagnostica'],['Conclusione','Risposta alla domanda e limiti osservati']],[2.6,6.4]),
 p('Una conclusione sul caso guida può affermare che il SARIMA migliora i riferimenti nei 36 mesi riservati, con un bias di '+value('co2','bias_SARIMA')+' ppm in convenzione osservato meno previsto.')+
 info('Va aggiunto che 36 valori coperti non dimostrano calibrazione e che il test riguarda una sola origine storica.')+
 sm('M10\\_N13 costruisce il testo usando i risultati realmente calcolati.'),
 'Una conclusione forte è precisa sul risultato e precisa sui suoi limiti.', notebook=13, source=[31])

slide(107, 'Esportare numeri, date e provenienza',
 table(['File','Contenuto'],[['CSV','Date, osservato, previsto, errore e bande'],['RDS','Oggetti stimati per riprendere il lavoro'],['R / Rmd','Procedura leggibile ed eseguibile'],['HTML / PDF','Risultato consultabile senza esecuzione'],['Metadati','Versioni, fonti e impronte dei file']],[2.4,6.7]),
 p('I file hanno nomi stabili e percorsi relativi al progetto. Una tabella esportata non deve perdere l’origine della previsione o l’orientamento dell’errore.')+
 info('M10\\_N19 controlla duplicati e integrità delle chiavi; M10\\_N09 prepara l’esportazione dei risultati.'),
 'Un file riutilizzabile deve conservare il significato delle colonne insieme ai valori.',
 code('tab <- data.frame(\n  data=co2$data[169:204],\n  osservato=as.numeric(test), fc)\nstopifnot(!anyDuplicated(tab$data))\nnames(tab)', 'R · tabella pronta per l’esportazione'), notebook=19, source=[23,32])

slide(108, 'La consegna deve funzionare da una cartella pulita',
 lab('Quattro prove di riproducibilità')+
 table(['Prova','Evidenza da conservare'],[['Riesecuzione','Log e versione di R'],['Dati locali','Nessun download implicito'],['Coerenza numerica','Tabelle e figure dagli stessi calcoli'],['Integrità','Manifest SHA-256 e file richiesti']],[3.4,5.7]),
 p('Il progetto contiene dati, codice, risultati e istruzioni. Il notebook HTML permette la lettura offline; il Rmd conserva il percorso per ripetere il lavoro.')+
 info('Una verifica dei file non sostituisce la valutazione scientifica. Completa il controllo di formule, unità, date e conclusioni.')+
 sm('M10\\_N18 accompagna la consegna. Il pacchetto include gli esiti delle esecuzioni svolte per questa edizione.'),
 'Un risultato riproducibile può essere ricostruito e interpretato senza dipendere dalla memoria dell’autore.', notebook=18, source=[32])

slide(109, 'Riferimenti per teoria, software e dati',
 lab('Fonti primarie e documentazione')+
 p('Hyndman e Athanasopoulos, \\emph{Forecasting: Principles and Practice}, 3ª edizione: riferimenti, errori, validazione temporale, ARIMA e intervalli.')+
 sm('\\href{https://otexts.com/fpp3/}{otexts.com/fpp3/}')+
 p('R Core Team, documentazione di stats: arima, predict.Arima, Box.test, ARMAacf, ARMAtoMA, lm e anova.')+
 sm('\\href{https://stat.ethz.ch/R-manual/R-devel/library/stats/html/arima.html}{Manuale R: arima} · \\href{https://stat.ethz.ch/R-manual/R-devel/library/stats/html/predict.arima.html}{predict.Arima} · \\href{https://stat.ethz.ch/R-manual/R-devel/library/stats/html/box.test.html}{Box.test}'),
 p('GeoStat Lab, modulo M10 e laboratori M10\\_N01--M10\\_N20: programma, convenzioni e specifica centrale.')+
 sm('\\href{https://marzione00.github.io/Lab_Geo/percorso/M10.html}{Modulo M10 sul sito}')+
 info('Dati locali: CO$_2$ storica da M09, fossili simulati da M07, processi simulati da M09. Fonti, hash e dettagli sono in FONTI\\_E\\_NOTE.md e Dati/PROVENIENZA.json.')+
 sm('Snapshot del sito: 20 novembre 2026. Revisione identificata nei metadati del pacchetto.'),
 'Le fonti rendono verificabili sia le scelte teoriche sia le convenzioni del calcolo.', source=[33])

slide(110, 'Prevedere, discutere, ricostruire',
 lab('Criteri per valutare il progetto')+
 table(['Criterio','Evidenza osservabile'],[['Domanda chiara','Quantità e uso della previsione espliciti'],['Metodo coerente','Ipotesi e riferimenti motivati'],['Verifica corretta','Separazione dei dati e metriche adeguate'],['Interpretazione','Risultati collegati alla domanda'],['Riproducibilità','Dati, codice, fonti e istruzioni completi']],[3.6,5.5]),
 p('Il progetto conclude il percorso unendo descrizione, modello e verifica. La complessità aggiunta deve produrre informazione utile e comprensibile.')+
 info('Prima della consegna: un’altra persona può capire la domanda, ripetere i calcoli e individuare quali conclusioni sono sostenute dai dati?')+
 sm('\\href{https://marzione00.github.io/Lab_Geo/\\#indice}{Indice del corso} · \\hyperlink{slide2}{Indice di Futura}'),
 'Prevedere significa rendere esplicito ciò che sappiamo, misurare gli errori e motivare ciò che concludiamo.', notebook=18, source=[31,32])

# Tre figure composte hanno una pagina panoramica per mantenere leggibili gli assi.
for page, name, caption in [
 (29,'14_AR1_traiettorie','Simulazioni con innovazioni di varianza unitaria. Un coefficiente positivo alto produce persistenza; un coefficiente negativo produce alternanza. I percorsi sono simulati, con semi registrati.'),
 (44,'21_differenze_CO2','Tre differenze sui soli 168 mesi di train. Il confronto motiva la trasformazione e non dimostra da solo stazionarietà. Ogni differenza cambia la variabile analizzata.'),
 (101,'32_VAR_previsioni','Verifica ricorsiva ai tempi 251--260. RMSE X: '+value('VAR','RMSE_X')+' (VAR) e '+value('VAR','RMSE_ultimo_X')+' (ultimo valore); RMSE Y: '+value('VAR','RMSE_Y')+' e '+value('VAR','RMSE_ultimo_Y')+'. Dieci tempi descrivono un test breve, non una superiorità generale.')]:
    s=next(x for x in SLIDES if x['page']==page)
    s.update(layout='panorama',figure=name,caption=caption)

assert len(SLIDES)==109
