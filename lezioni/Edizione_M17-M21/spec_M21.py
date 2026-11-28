# Specifica della lezione Credentia (M21): inferenza bayesiana come stima. Valori da R/M21_figure.R, Codice/ e Esperimenti/.
LEZIONE = {
 'planet': 'Credentia',
 'title': 'Inferenza bayesiana',
 'copertina': {'titolo': r'Inferenza\\bayesiana', 'sottotitolo': 'Stimare con la distribuzione a posteriori',
               'riga': 'Griglie, distribuzioni coniugate, scelta della distribuzione a priori e algoritmo di Metropolis'},
 'percorso': r'Il registro storico di un vulcano conta nove eruzioni in 375 anni; quattordici vulcani analoghi forniscono '
             r'un’informazione preliminare sul tasso eruttivo e sulla frazione di eruzioni esplosive. Il percorso va dal '
             r'teorema di Bayes su una griglia alle distribuzioni coniugate, alla scelta della distribuzione a priori e '
             r'all’algoritmo di Metropolis per i tempi di riposo.',
 'caso': {
  'domanda': 'Quanto è probabile un’eruzione nei prossimi cinquant’anni?',
  'ricorda': 'Una distribuzione a posteriori descrive l’incertezza sul parametro dopo aver visto i dati.',
  'body': r'Un vulcano sintetico ha eruttato nove volte fra il 1650 e il 2025, l’ultima nel 1988; quattro eruzioni sono '
          r'state esplosive. Quattordici vulcani analoghi, osservati per 140–440 anni, hanno da tre a sedici eruzioni '
          r'ciascuno. Con un registro così breve l’informazione dei vulcani analoghi pesa sulla stima.',
  'info': r'Seguiremo i dati dalla griglia al teorema di Bayes in forma chiusa, alla probabilità di un’eruzione esplosiva e '
          r'a un modello dei tempi di riposo stimato con una catena di Markov.'},
 'capitoli': [
  {'titolo': 'Il teorema di Bayes', 'pagine': [
   {'tipo': 'domanda', 'titolo': 'Che cosa dice il solo registro?', 'codice': 'capitolo-01.R',
    'ricorda': 'Sostituire il tasso stimato nella formula della probabilità ignora l’incertezza della stima.',
    'domanda_testo': r'Nove eruzioni in 3,75 secoli danno un tasso di 2,4 eruzioni per secolo. Quanto è incerto? Che '
                     r'probabilità di almeno un’eruzione in mezzo secolo si ottiene inserendo il tasso stimato nella formula di Poisson?',
    'interpretazione': r'L’intervallo esatto di Garwood al 95\% va da 1,10 a 4,56 eruzioni per secolo: un fattore quattro. La formula '
                       r'$1-e^{-0{,}5\lambda}$ con $\lambda=2{,}4$ dà 0,699, un numero che non porta traccia di questa incertezza.'},
   {'tipo': 'schema', 'titolo': 'Distribuzione a priori, verosimiglianza e distribuzione a posteriori', 'diag': 'Diagrammi/D01.tex',
    'ricorda': 'La distribuzione a posteriori è proporzionale al prodotto di distribuzione a priori e verosimiglianza.',
    'didascalia': 'Il teorema di Bayes applicato al tasso eruttivo.',
    'body': r'Thomas Bayes affrontò il problema di risalire da un numero di successi alla probabilità che li ha prodotti; il '
            r'saggio fu pubblicato nel 1763, dopo la sua morte. In forma moderna il parametro ha una distribuzione di '
            r'probabilità: quella a priori riassume l’informazione disponibile prima dei dati, e i dati la aggiornano '
            r'attraverso la verosimiglianza.',
    'formula': r'\pi(\lambda\mid N)=\frac{p(N\mid\lambda)\,\pi(\lambda)}{p(N)}'},
   {'tipo': 'codice', 'titolo': 'La distribuzione a posteriori su una griglia', 'codice': 'capitolo-02.R',
    'ricorda': 'Su una griglia il teorema di Bayes è un prodotto seguito da una normalizzazione.',
    'body': r'Il codice valuta distribuzione a priori uniforme e verosimiglianza di Poisson in 4001 punti fra 0 e 10 eruzioni '
            r'per secolo, divide il prodotto per la sua area e ricava media e quantili. La media a posteriori vale 2,67 e '
            r'l’intervallo di credibilità al 95\% va da 1,28 a 4,56: c’è una probabilità di 0,95 che il tasso stia in questo intervallo.',
    'formula': r'\pi(\lambda_j\mid N)\approx\frac{p(N\mid\lambda_j)\,\pi(\lambda_j)}{\sum_i p(N\mid\lambda_i)\,\pi(\lambda_i)\,\Delta}'},
   {'tipo': 'figura', 'titolo': 'Prima e dopo il registro storico', 'fig': 'Figure/F01.pdf',
    'ricorda': 'La distribuzione a posteriori sta fra la distribuzione a priori e la verosimiglianza, ed è più stretta di entrambe.',
    'didascalia': 'Densità a priori dai vulcani analoghi, verosimiglianza normalizzata e densità a posteriori del tasso eruttivo.',
    'body': r'La distribuzione a priori dei vulcani analoghi ha media 2,85 eruzioni per secolo ed è larga, da 0,94 a 5,78. '
            r'La verosimiglianza del registro è centrata su 2,4. La distribuzione a posteriori ha media 2,55 e intervallo '
            r'da 1,40 a 4,03, più stretto di entrambe: combina due fonti di informazione.',
    'symbols': r'La verosimiglianza normalizzata coincide con la distribuzione a posteriori ottenuta da una distribuzione a priori uniforme.'},
   {'tipo': 'scenario', 'titolo': 'Distribuzione a posteriori e lunghezza del registro', 'esperimento': 'm21-registro',
    'ricorda': 'Valutare quanto la distribuzione a posteriori dipende dalla distribuzione a priori al variare della quantità di dati.',
    'didascalia': 'Registro di un secolo; tasso vero 2,5 eruzioni per secolo. Seme: 17.',
    'body': r'L’esperimento genera il numero di eruzioni di un registro della durata scelta e aggiorna la distribuzione a '
            r'priori dei vulcani analoghi. Con un secolo di registro si osserva un’eruzione: la media a posteriori vale 2,19 '
            r'e l’intervallo al 95\% è ampio 3,41 eruzioni per secolo.',
    'formula': r'\lambda\mid N\sim\mathrm{Gamma}(a+N,\;b+T)',
    'symbols': r'Il peso della distribuzione a priori nella media a posteriori vale $b/(b+T)=0{,}644$.'},
   {'tipo': 'confronto', 'titolo': 'Confronto | Lunghezza del registro', 'esperimento': 'm21-registro',
    'ricorda': 'Con più dati la distribuzione a priori conta meno e l’intervallo si restringe.',
    'didascalia': r'Durata del registro: 1 $\to$ 10 secoli. Il seme è fisso.',
    'righe': [('Eruzioni osservate', 'Eruzioni osservate'), ('Media a posteriori', 'Media a posteriori'),
              ('Ampiezza dell’intervallo', 'Ampiezza dell’intervallo al 95%'),
              ('Peso della distribuzione a priori', 'Peso della distribuzione a priori')],
    'body': r'Con dieci secoli si osservano 19 eruzioni contro 25 attese, e la media a posteriori vale 2,04. Il peso della '
            r'distribuzione a priori scende a 0,153 e l’intervallo si restringe a 1,63.'},
  ]},
  {'titolo': 'Coniugate e intervalli di credibilità', 'pagine': [
   {'tipo': 'schema', 'titolo': 'Un aggiornamento in forma chiusa', 'diag': 'Diagrammi/D02.tex',
    'ricorda': 'Con una distribuzione a priori coniugata la distribuzione a posteriori appartiene alla stessa famiglia.',
    'didascalia': 'Aggiornamento della gamma con un registro di Poisson.',
    'body': r'Se la distribuzione a priori del tasso è una gamma e le eruzioni seguono un processo di Poisson, anche la '
            r'distribuzione a posteriori è una gamma: la forma aumenta del numero di eruzioni, il parametro di scala '
            r'inverso della durata. I due parametri della distribuzione a priori si leggono come un registro immaginario '
            r'di $a$ eruzioni in $b$ secoli.',
    'formula': r'\mathrm{Gamma}(a,b)\to\mathrm{Gamma}(a+N,b+T)'},
   {'tipo': 'codice', 'titolo': 'La distribuzione a priori dei vulcani analoghi', 'codice': 'capitolo-03.R',
    'ricorda': 'Se i tassi seguono una gamma, i conteggi dei vulcani analoghi seguono una binomiale negativa.',
    'body': r'Il codice stima i parametri della gamma massimizzando la verosimiglianza binomiale negativa dei conteggi dei '
            r'quattordici vulcani analoghi: $a=5{,}15$ e $b=1{,}81$ secoli. Aggiunge poi le nove eruzioni del caso: la '
            r'distribuzione a posteriori è una gamma con parametri 14,15 e 5,56, media 2,55 e intervallo da 1,40 a 4,03.',
    'formula': r'N_j\sim\mathrm{BN}\Big(a,\;\mu_j=\frac{a}{b}\,T_j\Big)'},
   {'tipo': 'figura', 'titolo': 'Quattordici vulcani analoghi', 'fig': 'Figure/F02.pdf',
    'ricorda': 'I vulcani analoghi differiscono fra loro più di quanto spieghino i loro registri.',
    'didascalia': r'Tassi dei vulcani analoghi e del caso con intervalli esatti al 95\%; fascia: intervallo della gamma a priori; tratteggio: sua media.',
    'body': r'I tassi dei vulcani analoghi vanno da 0,68 a 7,14 eruzioni per secolo. La gamma stimata descrive questa '
            r'variabilità fra vulcani: è la distribuzione dei tassi da cui il vulcano del caso è pensato come estratto. Il '
            r'registro del caso, 2,4 eruzioni per secolo, cade vicino alla media dei vulcani analoghi.',
    'symbols': r'Questo uso dei dati per costruire la distribuzione a priori si chiama bayesiano empirico.'},
   {'tipo': 'domanda', 'titolo': 'Qual è la probabilità di un’eruzione in mezzo secolo?', 'codice': 'capitolo-04.R',
    'ricorda': 'La distribuzione predittiva media la probabilità su tutti i valori plausibili del parametro.',
    'domanda_testo': r'La distribuzione a posteriori del tasso è una gamma con parametri 14,15 e 5,56. Qual è la probabilità '
                     r'di almeno un’eruzione nei prossimi cinquant’anni, mediata sull’incertezza del tasso?',
    'interpretazione': r'La media di $1-e^{-0{,}5\lambda}$ sulla distribuzione a posteriori ha una formula chiusa e vale 0,704; '
                       r'centomila estrazioni dalla gamma danno 0,705. Con il solo tasso stimato si otteneva 0,699.'},
   {'tipo': 'figura', 'titolo': 'Quante eruzioni nei prossimi cinquant’anni', 'fig': 'Figure/F03.pdf',
    'ricorda': 'L’incertezza sul tasso allarga la distribuzione dei conteggi futuri.',
    'didascalia': 'Distribuzione predittiva a posteriori e distribuzione di Poisson con il tasso stimato.',
    'body': r'La distribuzione predittiva a posteriori è una binomiale negativa. Rispetto alla distribuzione di Poisson con il '
            r'tasso stimato assegna una probabilità minore a una o due eruzioni e maggiore a tre o più: 0,143 contro 0,121. '
            r'La probabilità di nessuna eruzione cambia poco, 0,296 contro 0,301.',
    'formula': r'P(M=0)=\Big(\frac{b+T}{b+T+h}\Big)^{a+N}'},
   {'tipo': 'scenario', 'titolo': 'Intervalli per un tasso con pochi eventi', 'esperimento': 'm21-copertura',
    'ricorda': 'Confrontare la copertura di intervalli frequentisti e di credibilità quando gli eventi sono pochi.',
    'didascalia': 'Trenta eventi attesi; quattromila registri. Seme: 17.',
    'body': r'L’esperimento genera quattromila conteggi di Poisson e costruisce tre intervalli al 95\%: Wald, credibilità con '
            r'la distribuzione a priori di Jeffreys, esatto. Con trenta eventi attesi le coperture valgono 0,933, 0,959 e 0,959.',
    'formula': r'\lambda\mid N\sim\mathrm{Gamma}\big(N+\tfrac12,\;1\big)',
    'symbols': r'La distribuzione a priori di Jeffreys per un tasso di Poisson è proporzionale a $\lambda^{-1/2}$.'},
   {'tipo': 'confronto', 'titolo': 'Confronto | Intervalli con pochi eventi', 'esperimento': 'm21-copertura',
    'ricorda': 'Con pochi eventi l’approssimazione normale fallisce; l’intervallo di Jeffreys tiene.',
    'didascalia': r'Eventi attesi: 30 $\to$ 3. Il seme è fisso.',
    'righe': [('Copertura, Wald', 'Copertura dell’intervallo di Wald'), ('Copertura, Jeffreys', 'Copertura dell’intervallo di Jeffreys'),
              ('Copertura, esatto', 'Copertura dell’intervallo esatto'), ('Registri senza eventi', 'Quota di registri senza eventi')],
    'body': r'Con tre eventi attesi l’intervallo di Wald contiene il valore vero nel 79,6\% dei registri, quello di Jeffreys '
            r'nel 91,5\%, quello esatto nel 98,7\%. Il 5,1\% dei registri non ha eventi.'},
  ]},
  {'titolo': 'Sensibilità alla distribuzione a priori', 'pagine': [
   {'tipo': 'codice', 'titolo': 'La frazione di eruzioni esplosive', 'codice': 'capitolo-05.R',
    'ricorda': 'Per una proporzione la distribuzione beta è coniugata della binomiale.',
    'body': r'Quattro eruzioni su nove sono state esplosive. Il codice aggiorna tre distribuzioni beta a priori: uniforme, '
            r'di Jeffreys e quella stimata dai vulcani analoghi, con media 0,334 e forza pari a 20 eruzioni. Le prime due '
            r'danno medie a posteriori di 0,455 e 0,450 con intervalli larghi; la terza 0,368, da 0,206 a 0,548.',
    'formula': r'p\mid k\sim\mathrm{Beta}(\alpha+k,\;\beta+n-k)'},
   {'tipo': 'figura', 'titolo': 'Tre distribuzioni a posteriori per la frazione esplosiva', 'fig': 'Figure/F04.pdf',
    'ricorda': 'Con pochi dati la scelta della distribuzione a priori cambia la distribuzione a posteriori.',
    'didascalia': 'Densità a posteriori della frazione esplosiva con tre distribuzioni a priori; tratteggio: beta a priori dei vulcani analoghi.',
    'body': r'Le distribuzioni a posteriori uniforme e di Jeffreys quasi coincidono: con nove eruzioni la differenza fra '
            r'le due distribuzioni a priori conta poco. La distribuzione dei vulcani analoghi vale quanto venti eruzioni, più '
            r'del doppio del registro, e sposta la media a posteriori verso 0,33.',
    'symbols': r'La forza di una beta a priori è $\alpha+\beta$, il numero di eruzioni a cui equivale.'},
   {'tipo': 'domanda', 'titolo': 'E un’eruzione esplosiva?', 'codice': 'capitolo-06.R',
    'ricorda': 'La simulazione dalle distribuzioni a posteriori propaga l’incertezza di più parametri.',
    'domanda_testo': r'Le eruzioni esplosive formano un processo di Poisson con tasso $\lambda p$. Qual è la probabilità di '
                     r'almeno un’eruzione esplosiva nei prossimi cinquant’anni?',
    'interpretazione': r'Estraendo centomila coppie dalle due distribuzioni a posteriori, la probabilità media vale 0,365. Con '
                       r'le stime puntuali, 2,4 eruzioni per secolo e frazione 4/9, si otterrebbe 0,413.'},
   {'tipo': 'figura', 'titolo': 'Quanto conta la distribuzione a priori', 'fig': 'Figure/F05.pdf',
    'ricorda': 'Una distribuzione a priori informativa e sbagliata sposta la stima più di quanto i dati possano correggere.',
    'didascalia': r'Media e intervallo al 95\% del tasso eruttivo con quattro distribuzioni a priori e stima di massima verosimiglianza.',
    'body': r'Uniforme, Jeffreys e vulcani analoghi danno medie fra 2,53 e 2,67. Una distribuzione a priori tratta da vulcani '
            r'di altro tipo, gamma con media 10 eruzioni per secolo e forza pari a un secolo, porta la media a 4,00 con '
            r'intervallo da 2,41 a 5,99. La verosimiglianza normalizzata assegna ai valori oltre 4 una probabilità di 0,07.',
    'formula': r'\frac{a+N}{b+T}=\frac{10+9}{1+3{,}75}=4{,}00'},
   {'tipo': 'testo', 'titolo': 'Che cosa contiene una distribuzione a priori',
    'ricorda': 'Una distribuzione a priori va dichiarata, giustificata e confrontata con i dati.',
    'sinistra': {'label': 'Dati immaginari', 'body': r'Una gamma con parametri $a$ e $b$ pesa quanto un registro di $b$ '
                 r'secoli con $a$ eruzioni; una beta con parametri $\alpha$ e $\beta$ quanto $\alpha+\beta$ eruzioni. '
                 r'Tradurre la distribuzione a priori in dati equivalenti permette di giudicare se la sua forza è '
                 r'ragionevole: i vulcani analoghi valgono 1,8 secoli e venti eruzioni.',
                 'formula': r'w=\frac{b}{b+T}=0{,}325'},
    'destra': {'label': 'Controllo predittivo a priori', 'body': r'Prima dell’aggiornamento si chiede quanto sia probabile '
               r'il dato osservato secondo la distribuzione predittiva a priori. Con i vulcani analoghi un registro con al '
               r'più nove eruzioni ha probabilità 0,48; con i vulcani di altro tipo 0,0024. Il secondo valore segnala un '
               r'conflitto fra distribuzione a priori e dati.',
               'symbols': r'Il controllo segnala un’incoerenza: decidere quale delle due parti sia sbagliata richiede conoscenza geologica.'}},
   {'tipo': 'scenario', 'titolo': 'Distribuzione a priori in conflitto con i dati', 'esperimento': 'm21-priori',
    'ricorda': 'Valutare l’effetto di una distribuzione a priori sbagliata e la capacità del controllo predittivo di rilevarla.',
    'didascalia': r'Media a priori uguale al tasso vero; forza 1,8 secoli; mille registri. Seme: 17.',
    'body': r'L’esperimento genera mille registri di 3,75 secoli con tasso vero 2,5 e aggiorna una gamma con la media e la '
            r'forza scelte. Con una distribuzione a priori centrata sul valore vero la media delle medie a posteriori vale '
            r'2,48, la copertura 0,974 e il controllo non segnala conflitti.',
    'formula': r'p=2\min\{P(N^\prime\le N),\,P(N^\prime\ge N)\}',
    'symbols': r'$N^\prime$ segue la distribuzione predittiva a priori, una binomiale negativa.'},
   {'tipo': 'confronto', 'titolo': 'Confronto | Distribuzione a priori in conflitto', 'esperimento': 'm21-priori',
    'ricorda': 'Una distribuzione a priori sbagliata riduce la copertura; il controllo predittivo la segnala spesso.',
    'didascalia': r'Media a priori: 1 $\to$ 3 volte il tasso vero. Forza e seme fissi.',
    'righe': [('Media a priori', 'Media a priori'), ('Media delle medie a posteriori', 'Media delle medie a posteriori'),
              (r'Copertura al 95\%', 'Copertura dell’intervallo al 95%'), ('Conflitti segnalati', 'Quota di conflitti segnalati')],
    'body': r'Con una media a priori di 7,5 la media a posteriori sale a 4,1 e l’intervallo contiene il valore vero soltanto '
            r'nel 41,6\% dei registri. Il controllo predittivo segnala il conflitto nel 77,3\% dei casi.'},
  ]},
  {'titolo': 'Monte Carlo a catena di Markov', 'pagine': [
   {'tipo': 'domanda', 'titolo': 'Le eruzioni sono regolari?', 'codice': 'capitolo-07.R',
    'ricorda': 'Nel processo di Poisson i tempi di riposo sono esponenziali; la Weibull permette tempi più regolari.',
    'domanda_testo': r'Gli otto tempi di riposo vanno da 20 a 54 anni, e dall’ultima eruzione ne sono passati 37. Il '
                     r'coefficiente di variazione di un processo di Poisson vale 1: quanto vale qui? Che forma stima la Weibull?',
    'interpretazione': r'Il coefficiente di variazione vale 0,34, e la stima di massima verosimiglianza della forma è 3,96, '
                       r'con scala 44,6 anni. Una forma maggiore di 1 indica un rischio che cresce con il tempo trascorso dall’ultima eruzione.'},
   {'tipo': 'schema', 'titolo': 'L’algoritmo di Metropolis', 'diag': 'Diagrammi/D03.tex',
    'ricorda': 'Metropolis richiede la densità a posteriori soltanto a meno di una costante.',
    'didascalia': 'Le quattro fasi di un passo della catena.',
    'body': r'Con due parametri e una distribuzione a priori non coniugata la distribuzione a posteriori non ha una forma '
            r'nota. Nicholas Metropolis e colleghi proposero nel 1953 una catena di Markov che ha come distribuzione '
            r'stazionaria quella voluta; W. K. Hastings la generalizzò nel 1970 a proposte asimmetriche.',
    'formula': r'\alpha=\min\Big\{1,\frac{\pi(\theta^*\mid y)}{\pi(\theta^{(t)}\mid y)}\Big\}'},
   {'tipo': 'codice', 'titolo': 'Una catena per la Weibull', 'codice': 'capitolo-08.R',
    'ricorda': 'L’intervallo ancora aperto entra nella verosimiglianza come dato censurato.',
    'body': r'La log-densità a posteriori somma le densità degli otto riposi, la probabilità che il riposo in corso superi '
            r'37 anni e due distribuzioni a priori normali sui logaritmi dei parametri. La catena accetta il 41\% delle '
            r'proposte. Dopo cinquecento iterazioni iniziali la media di $k$ vale 3,15, e $P(k>1)=0{,}994$.',
    'formula': r'\log\pi=\sum_i\log f(r_i)+\log S(37)+\log\pi_0'},
   {'tipo': 'figura', 'titolo': 'La catena e la distribuzione a posteriori della forma', 'fig': 'Figure/F06.pdf',
    'ricorda': 'Una traccia stabile e ben mescolata è una condizione necessaria per usare i valori della catena.',
    'didascalia': r'Sinistra: prime duemila iterazioni di $k$. Destra: istogramma dei valori dopo le prime cinquecento; tratteggio: $k=1$.',
    'body': r'La traccia oscilla attorno a 3 senza tendenze dopo le prime iterazioni. L’intervallo al 95\% della forma va da '
            r'1,39 a 5,89: i dati escludono il processo di Poisson e lasciano incerta la regolarità. Un’integrazione '
            r'numerica su griglia dà una media di 3,17.',
    'symbols': r'Il generatore dei dati usa $k=1{,}8$: otto riposi non bastano a fissare la forma.'},
   {'tipo': 'testo', 'titolo': 'Diagnostica e uso della catena',
    'ricorda': 'Valori autocorrelati contengono meno informazione di altrettante estrazioni indipendenti.',
    'sinistra': {'label': 'Controllare la catena', 'body': r'I valori iniziali dipendono dal punto di partenza e si '
                 r'scartano. I valori successivi sono autocorrelati: la dimensione campionaria efficace dei 4500 valori di $k$ '
                 r'è circa 170. A. Gelman e D. B. Rubin proposero nel 1992 di lanciare più catene da punti di partenza '
                 r'dispersi e di confrontare la variabilità fra catene ed entro catene.',
                 'formula': r'n_{\mathrm{eff}}=\frac{n}{1+2\sum_{l}\rho_l}'},
    'destra': {'label': 'Una probabilità condizionata', 'body': r'Ogni valore della catena dà una probabilità di eruzione '
               r'nei prossimi cinquant’anni, dati i 37 anni già trascorsi; la media vale 0,97. Il processo di Poisson, privo '
               r'di memoria, dà 0,70. Con la forma del generatore, 1,8, la probabilità vera è 0,91.',
               'symbols': r'$P=1-\exp\{(37/\eta)^k-(87/\eta)^k\}$, mediata sui valori della catena.'}},
   {'tipo': 'scenario', 'titolo': 'Passo della proposta e mescolamento della catena', 'esperimento': 'm21-metropolis',
    'ricorda': 'Valutare come il passo della proposta cambia accettazione, autocorrelazione e precisione.',
    'didascalia': 'Passo 0,25 sulla scala logaritmica; quattromila iterazioni. Seme: 17.',
    'body': r'L’esperimento esegue l’algoritmo di Metropolis sui tempi di riposo del caso con il passo scelto. Con passo '
            r'0,25 la catena accetta il 43\% delle proposte, la media di $k$ vale 3,10 e la dimensione campionaria efficace 212.',
    'formula': r'\theta^*=\theta^{(t)}+\varepsilon,\quad\varepsilon\sim N(0,s^2I)',
    'symbols': r'Il valore di riferimento, 3,17, viene dall’integrazione su griglia.'},
   {'tipo': 'confronto', 'titolo': 'Confronto | Passo della proposta', 'esperimento': 'm21-metropolis',
    'ricorda': 'Un passo troppo piccolo accetta quasi tutto ed esplora poco.',
    'didascalia': r'Passo della proposta: 0,25 $\to$ 0,02. Il seme è fisso.',
    'righe': [('Tasso di accettazione', 'Tasso di accettazione'), ('Media a posteriori di k', 'Media a posteriori di k'),
              ('Dimensione campionaria efficace', 'Dimensione campionaria efficace'), ('Riferimento su griglia', 'Riferimento su griglia')],
    'body': r'Con passo 0,02 la catena accetta il 94,6\% delle proposte ma si sposta di poco a ogni passo: la dimensione '
            r'campionaria efficace scende a 11,9 e la media di $k$, 2,78, risente ancora del punto di partenza.'},
  ]},
 ],
 'sintesi': {
  'titolo': 'Dal risultato alla relazione',
  'ricorda': 'Riporta distribuzione a priori e sua origine, distribuzione a posteriori, controlli e probabilità predittive.',
  'risultato': r'Il tasso eruttivo ha media a posteriori di 2,55 eruzioni per secolo, con intervallo di credibilità al 95\% da 1,4 a 4,0; la '
               r'probabilità di almeno un’eruzione nei prossimi cinquant’anni è 0,70 con il processo di Poisson, e quella di '
               r'un’eruzione esplosiva 0,37. I tempi di riposo sono più regolari di un processo di Poisson, e con 37 anni già '
               r'trascorsi il modello di Weibull porta la probabilità a 0,97.',
  'limiti': r'I dati sono sintetici e il registro storico è considerato completo. La forma della Weibull è incerta, da 1,4 '
            r'a 5,9, e la probabilità condizionata dipende da essa; i vulcani analoghi sono scambiabili con il caso per ipotesi.'},
 'riferimenti': {
  'titolo': 'Fonti, dati e codice per riprodurre le figure',
  'ricorda': 'I risultati numerici si riferiscono ai dati e alle ipotesi dichiarate nel caso.',
  'fonti': r'T. Bayes, Philosophical Transactions of the Royal Society 53, 370–418, 1763.\par '
           r'F. Garwood, Biometrika 28(3–4), 437–442, 1936.\par '
           r'H. Jeffreys, Proceedings of the Royal Society A 186, 453–461, 1946.\par '
           r'N. Metropolis, A. W. Rosenbluth, M. N. Rosenbluth, A. H. Teller e E. Teller, Journal of Chemical Physics 21(6), 1087–1092, 1953.\par '
           r'W. K. Hastings, Biometrika 57(1), 97–109, 1970.\par '
           r'A. Gelman e D. B. Rubin, Statistical Science 7(4), 457–472, 1992.\par '
           r'C. G. Newhall e R. P. Hoblitt, Bulletin of Volcanology 64, 3–20, 2002.\par '
           r'W. Marzocchi, L. Sandri e J. Selva, Bulletin of Volcanology 70(5), 623–632, 2008.\par '
           r'M. S. Bebbington, Statistics in Volcanology 1, 1–24, 2013.',
  'dati': r'Dati sintetici del corso (eruzioni\_v1.csv, analoghi\_v1.csv), generati da R/genera\_dati.R. Codice contiene i '
          r'frammenti delle pagine; R/M21\_figure.R ricostruisce figure e valori; Esperimenti contiene i programmi dei due '
          r'scenari e Diagrammi i disegni TikZ.'},
}
