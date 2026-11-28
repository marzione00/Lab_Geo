# Specifica della lezione Numerus (M20): modelli lineari generalizzati. Valori da R/M20_figure.R, Codice/ e Esperimenti/.
LEZIONE = {
 'planet': 'Numerus',
 'title': 'Modelli lineari generalizzati',
 'copertina': {'titolo': r'Modelli lineari\\generalizzati', 'sottotitolo': 'Conteggi e proporzioni',
               'riga': 'Poisson, offset, sovradispersione e regressione logistica'},
 'percorso': r'Novantasei celle di un bacino riportano il numero di frane, la superficie, la pendenza e la litologia; '
             r'trentasei sezioni sottili riportano un conteggio per punti del feldspato lungo un percorso di trasporto. Il '
             r'percorso va dai limiti della retta per i conteggi al modello di Poisson, alla sovradispersione e alle proporzioni.',
 'caso': {
  'domanda': 'Quanto aumenta il tasso di frane con la pendenza?',
  'ricorda': 'Un conteggio è un intero non negativo: la sua varianza dipende dalla media.',
  'body': r'Novantasei celle sintetiche di un bacino, con superfici fra 0,44 e 4 km$^2$, contengono in tutto 321 frane '
          r'cartografate; ventuno celle non ne hanno nessuna. Per ogni cella sono note la pendenza media e la litologia '
          r'prevalente: argille, flysch o calcari. Un secondo file riporta i punti di feldspato contati in 36 sezioni sottili.',
  'info': r'Seguiremo i dati dalla retta dei minimi quadrati al modello di Poisson con offset, alla sovradispersione con '
          r'quasi-Poisson e binomiale negativa, fino alla regressione logistica per le proporzioni.'},
 'capitoli': [
  {'titolo': 'Conteggi e regressione lineare', 'pagine': [
   {'tipo': 'domanda', 'titolo': 'Che cosa prevede una retta per i conteggi?', 'codice': 'capitolo-01.R',
    'ricorda': 'Una retta non conosce i vincoli di un conteggio: può prevedere valori negativi.',
    'domanda_testo': r'Il numero di frane per cella ha media 3,34. Che varianza hanno i conteggi? Che cosa prevede la retta '
                     r'dei minimi quadrati per una cella con pendenza di 4 gradi?',
    'interpretazione': r'La varianza vale 15,07, quattro volte e mezzo la media, e ventuno celle hanno zero frane. La retta '
                       r'prevede $-0{,}60$ frane per una cella con pendenza di 4 gradi: un valore impossibile.'},
   {'tipo': 'figura', 'titolo': 'Frane, pendenza e litologia', 'fig': 'Figure/F01.pdf',
    'ricorda': 'La densità di frane cresce con la pendenza in modo moltiplicativo, e il livello dipende dalla litologia.',
    'didascalia': r'Frane per km$^2$ e pendenza; curve: modello di Poisson per litologia nell’intervallo osservato; tratteggio: retta dei minimi quadrati.',
    'body': r'Il bacino conta 2,36 frane per km$^2$ di superficie totale. Le curve del modello di Poisson crescono in modo esponenziale e '
            r'restano positive; la retta tratteggiata attraversa lo zero a bassa pendenza. A parità di pendenza le argille '
            r'hanno le densità maggiori e i calcari le minori.',
    'symbols': r'La densità è il conteggio diviso per la superficie della cella.'},
   {'tipo': 'schema', 'titolo': 'Le tre parti di un modello lineare generalizzato', 'diag': 'Diagrammi/D01.tex',
    'ricorda': 'Distribuzione, predittore lineare e funzione di legame si scelgono separatamente.',
    'didascalia': 'Componente casuale, predittore lineare e funzione di legame.',
    'body': r'John Nelder e Robert Wedderburn riunirono nel 1972 modelli per dati normali, binomiali, di Poisson e gamma in '
            r'un’unica classe. La distribuzione descrive la variabilità di ogni osservazione, il predittore lineare combina i '
            r'predittori, il legame collega la media al predittore. Per i conteggi il legame logaritmico mantiene positiva '
            r'la media.',
    'formula': r'\log\mu_i=\log A_i+\mathbf x_i^{\mathsf T}\boldsymbol\beta',
    'symbols': r'$Y_i\sim\mathrm{Poisson}(\mu_i)$; $A_i$ è la superficie della cella e $\log A_i$ l’offset.'},
   {'tipo': 'codice', 'titolo': 'Il modello di Poisson con offset', 'codice': 'capitolo-02.R',
    'ricorda': 'L’offset $\\log A_i$ trasforma il modello dei conteggi in un modello dei tassi per unità di superficie.',
    'body': r'Il codice adatta il modello con \texttt{glm}, famiglia di Poisson e offset \texttt{log(area\_km2)}. Il '
            r'coefficiente della pendenza vale 0,0895 per grado: ogni 10 gradi il tasso di frane per km$^2$ si moltiplica '
            r'per $e^{0{,}895}=2{,}45$. I coefficienti delle litologie sono negativi rispetto alle argille.',
    'formula': r'\frac{\mu(x+10)}{\mu(x)}=e^{10\beta_1}'},
   {'tipo': 'scenario', 'titolo': 'Retta e modello di Poisson per i conteggi', 'esperimento': 'm20-lineare',
    'ricorda': 'Confrontare retta e modello di Poisson su conteggi che crescono in modo esponenziale.',
    'didascalia': 'Pendenza del logaritmo della media: 0,03. Seme: 17.',
    'body': r'L’esperimento genera ottanta conteggi di Poisson con media $3e^{b(x-20)}$ e adatta una retta e un modello di '
            r'Poisson. Con $b=0{,}03$ la retta non prevede valori negativi, e la varianza dei residui passa da 1,83 a 3,34 '
            r'fra le due metà dell’intervallo.',
    'formula': r'\log\mu_i=\beta_0+\beta_1x_i,\qquad \operatorname{var}(Y_i)=\mu_i',
    'symbols': r'Il rapporto di tasso stimato, 1,20, e quello vero, 1,35, differiscono per la variabilità campionaria.'},
   {'tipo': 'confronto', 'titolo': 'Confronto | Retta e modello di Poisson', 'esperimento': 'm20-lineare',
    'ricorda': 'Con una crescita forte la retta prevede conteggi negativi e ignora la varianza crescente.',
    'didascalia': r'Pendenza del logaritmo della media: 0,03 $\to$ 0,12. Il seme è fisso.',
    'righe': [('Previsioni negative', 'Quota dell’intervallo con previsioni negative'),
              (r'Varianza dei residui, $x<20$', 'Varianza dei residui, x < 20'),
              (r'Varianza dei residui, $x\ge20$', 'Varianza dei residui, x ≥ 20'),
              ('Rapporto di tasso, Poisson', 'Rapporto di tasso per 10 unità, Poisson'),
              ('Rapporto di tasso vero', 'Rapporto di tasso vero')],
    'body': r'Con $b=0{,}12$ la retta prevede valori negativi nel 21,5\% dell’intervallo e la varianza dei residui passa da '
            r'9,45 a 43,5; il modello di Poisson stima 3,19 contro 3,32.'},
  ]},
  {'titolo': 'Il modello di Poisson', 'pagine': [
   {'tipo': 'schema', 'titolo': 'Minimi quadrati pesati ripetuti', 'diag': 'Diagrammi/D02.tex',
    'ricorda': 'Un modello lineare generalizzato si adatta con una sequenza di regressioni pesate.',
    'didascalia': 'Le quattro fasi dell’algoritmo per il modello di Poisson con legame logaritmico.',
    'body': r'Nelder e Wedderburn mostrarono che le stime di massima verosimiglianza si ottengono ripetendo una regressione '
            r'lineare pesata su una variabile di lavoro. \texttt{M20\_figure.R} implementa l’algoritmo in poche righe e '
            r'ottiene gli stessi coefficienti di \texttt{glm} entro $10^{-8}$.',
    'formula': r'\boldsymbol\beta\leftarrow(X^{\mathsf T}WX)^{-1}X^{\mathsf T}W\mathbf z'},
   {'tipo': 'figura', 'titolo': 'Rapporti fra tassi', 'fig': 'Figure/F02.pdf',
    'ricorda': 'Su scala logaritmica un rapporto di tasso pari a 1 indica nessun effetto.',
    'didascalia': r'Rapporti fra tassi del modello di Poisson con intervalli di Wald al 95\%; asse logaritmico.',
    'body': r'Dieci gradi di pendenza in più moltiplicano il tasso per 2,45, con intervallo da 1,98 a 3,03. A parità di '
            r'pendenza il flysch ha un tasso pari a 0,54 volte quello delle argille, i calcari 0,25 volte. Gli intervalli '
            r'presuppongono che i conteggi seguano una distribuzione di Poisson.',
    'symbols': r'L’intervallo di Wald è $e^{\hat\beta\pm1{,}96\,\mathrm{se}}$, asimmetrico sulla scala dei rapporti.'},
   {'tipo': 'domanda', 'titolo': 'Come si leggono i coefficienti?', 'codice': 'capitolo-03.R',
    'ricorda': 'L’esponenziale di un coefficiente è un rapporto fra tassi, a parità degli altri predittori.',
    'domanda_testo': r'Il coefficiente del flysch vale $-0{,}623$. Che cosa significa per il tasso di frane di una cella di '
                     r'flysch rispetto a una cella di argille con la stessa pendenza?',
    'interpretazione': r'Il tasso vale $e^{-0{,}623}=0{,}536$ volte quello delle argille, con intervallo da 0,390 a 0,739: '
                       r'circa la metà. Un grado di pendenza in più moltiplica il tasso per 1,094.'},
   {'tipo': 'codice', 'titolo': 'La devianza e il test del rapporto di verosimiglianza', 'codice': 'capitolo-04.R',
    'ricorda': 'La differenza di devianza fra modelli annidati segue approssimativamente una chi quadrato.',
    'body': r'La devianza misura la distanza fra il modello e un modello con un parametro per ogni osservazione. Togliendo '
            r'la litologia la devianza passa da 153,21 a 195,13: la differenza, 41,92 con due gradi di libertà, ha '
            r'probabilità di coda $7{,}9\cdot10^{-10}$. La litologia migliora il modello.',
    'formula': r'D=2\sum_i\Big[y_i\log\frac{y_i}{\hat\mu_i}-(y_i-\hat\mu_i)\Big]'},
   {'tipo': 'figura', 'titolo': 'Frequenze osservate e attese', 'fig': 'Figure/F03.pdf',
    'ricorda': 'Troppi zeri e troppi valori grandi rispetto al modello segnalano sovradispersione.',
    'didascalia': 'Numero di celle per numero di frane: barre osservate, punti attesi dal modello di Poisson.',
    'body': r'Il modello di Poisson attende 16,6 celle senza frane: ce ne sono 21. Le celle con 12 frane o più sono 6 '
            r'contro 3,4 attese, e quelle con 4, 5 e 6 frane sono meno del previsto. I conteggi sono più dispersi di quanto '
            r'il modello preveda. La devianza residua vale 153,2 con 92 gradi di libertà.',
    'symbols': r'Le frequenze attese sommano le probabilità di Poisson delle 96 celle.'},
   {'tipo': 'scenario', 'titolo': 'Offset e superfici diverse', 'esperimento': 'm20-offset',
    'ricorda': 'Valutare la stima del rapporto di tasso con e senza offset quando la superficie dipende dal predittore.',
    'didascalia': 'Superficie indipendente dal predittore. Seme: 17.',
    'body': r'L’esperimento genera centoventi celle con un tasso che cresce con $x$, rapporto vero 1,65 per 10 unità. Se '
            r'la superficie non dipende da $x$, le stime con offset e senza valgono 1,63 e 1,56.',
    'formula': r'\log\mu_i=\log A_i+\beta_0+\beta_1x_i',
    'symbols': r'Senza offset la superficie entra nell’errore del modello.'},
   {'tipo': 'confronto', 'titolo': 'Confronto | Offset e superfici diverse', 'esperimento': 'm20-offset',
    'ricorda': 'Senza offset il predittore assorbe l’effetto della superficie a cui è correlato.',
    'didascalia': r'Dipendenza di log(area) dal predittore: 0 $\to$ 0,6 per 10 unità. Il seme è fisso.',
    'righe': [('Rapporto vero', 'Rapporto di tasso vero per 10 unità'), ('Stima con offset', 'Stima con offset'),
              ('Stima senza offset', 'Stima senza offset'), (r'Correlazione $x$, log(area)', 'Correlazione fra x e log(area)')],
    'body': r'Con superfici correlate al predittore la stima senza offset sale a 2,72; quella con offset resta 1,58, vicina '
            r'al valore vero.'},
  ]},
  {'titolo': 'Sovradispersione', 'pagine': [
   {'tipo': 'codice', 'titolo': 'Stimare la dispersione', 'codice': 'capitolo-05.R',
    'ricorda': 'La statistica di Pearson divisa per i gradi di libertà vale circa 1 per dati di Poisson.',
    'body': r'Per il modello delle frane la dispersione vale 1,62: la varianza è circa il 60\% più grande di quella prevista. '
            r'Robert Wedderburn introdusse nel 1974 la quasi-verosimiglianza, che richiede soltanto la relazione fra media '
            r'e varianza. Il modello quasi-Poisson ha gli stessi coefficienti ed errori standard moltiplicati per '
            r'$\sqrt{\hat\phi}$: per la pendenza da 0,0108 a 0,0138.',
    'formula': r'\hat\phi=\frac{1}{n-p}\sum_i\frac{(y_i-\hat\mu_i)^2}{\hat\mu_i},\qquad \operatorname{var}(Y_i)=\phi\,\mu_i'},
   {'tipo': 'figura', 'titolo': 'Come cresce la varianza con la media', 'fig': 'Figure/F04.pdf',
    'ricorda': 'Quasi-Poisson e binomiale negativa differiscono nel modo in cui la varianza cresce con la media.',
    'didascalia': 'Varianza dei residui in otto gruppi di celle ordinate per media stimata e tre funzioni di varianza.',
    'body': r'Jay Ver Hoef e Peter Boveng confrontarono nel 2007 i due approcci: la varianza quasi-Poisson è lineare nella '
            r'media, quella della binomiale negativa quadratica, e i pesi delle osservazioni cambiano di conseguenza. Nel '
            r'caso i punti dei gruppi stanno fra le due curve; la binomiale negativa ha parametro di forma 6,19.',
    'formula': r'\operatorname{var}(Y)=\mu+\frac{\mu^2}{\theta}'},
   {'tipo': 'codice', 'titolo': 'La binomiale negativa per massima verosimiglianza', 'codice': 'capitolo-06.R',
    'ricorda': 'La binomiale negativa è un modello completo: stima anche il parametro di forma.',
    'body': r'Il codice scrive la log-verosimiglianza con \texttt{dnbinom} e la massimizza con \texttt{optim}; l’inversa '
            r'dell’hessiana fornisce gli errori standard. La pendenza vale 0,0918 con errore standard 0,0141 e il parametro '
            r'di forma 6,19. \texttt{M20\_figure.R} verifica che il risultato coincide con \texttt{MASS::glm.nb}.',
    'formula': r'P(Y=y)=\frac{\Gamma(y+\theta)}{\Gamma(\theta)\,y!}\Big(\frac{\theta}{\theta+\mu}\Big)^{\theta}\Big(\frac{\mu}{\theta+\mu}\Big)^{y}'},
   {'tipo': 'figura', 'titolo': 'Tre intervalli per lo stesso effetto', 'fig': 'Figure/F05.pdf',
    'ricorda': 'Con sovradispersione l’intervallo di Poisson è troppo stretto.',
    'didascalia': r'Rapporto fra tassi per 10 gradi di pendenza con intervalli al 95\% dei tre modelli.',
    'body': r'Le stime puntuali sono simili: 2,45 con Poisson e quasi-Poisson, 2,50 con la binomiale negativa. Gli '
            r'intervalli si allargano: da 1,98–3,03 a 1,87–3,21 e 1,90–3,30. Il criterio di Akaike preferisce la binomiale '
            r'negativa, 378,1 contro 387,1.',
    'symbols': r'Il criterio di Akaike non è definito per il modello quasi-Poisson, privo di una verosimiglianza.'},
   {'tipo': 'testo', 'titolo': 'Da dove nasce la sovradispersione',
    'ricorda': 'La sovradispersione segnala variabilità non spiegata: va descritta e, se possibile, spiegata.',
    'sinistra': {'label': 'Fattori non misurati', 'body': r'Il tasso di frane di una cella dipende anche da fattori assenti '
                 r'dal modello: piovosità, uso del suolo, fratturazione. Celle con la stessa pendenza e litologia hanno '
                 r'tassi diversi, e la loro miscela produce più zeri e più valori grandi di una Poisson. Nel generatore il '
                 r'fattore di cella segue una distribuzione gamma, che dà proprio una binomiale negativa.'},
    'destra': {'label': 'Che cosa scegliere', 'body': r'Quasi-Poisson e binomiale negativa hanno lo stesso numero di '
               r'parametri. La scelta dipende da come la varianza cresce con la media nei dati, da controllare con un grafico '
               r'come quello della tappa 18. Una sovradispersione può anche segnalare un predittore mancante o una forma '
               r'sbagliata del predittore lineare.',
               'symbols': r'Dipendenza spaziale fra celle vicine produce effetti simili e richiede modelli spaziali.'}},
   {'tipo': 'scenario', 'titolo': 'Sovradispersione e copertura degli intervalli', 'esperimento': 'm20-dispersione',
    'ricorda': 'Misurare la copertura degli intervalli di Poisson e quasi-Poisson con conteggi sovradispersi.',
    'didascalia': r'Parametro di forma: 100; 96 celle; trecento campioni. Seme: 17.',
    'body': r'L’esperimento genera conteggi da una binomiale negativa e adatta il modello di Poisson. Con $\theta=100$ la '
            r'dispersione media è 1,03, e gli intervalli contengono la pendenza vera nel 93,7\% e nel 95,3\% dei campioni.',
    'formula': r'\hat\beta_1\pm1{,}96\,\mathrm{se}\sqrt{\max(1,\hat\phi)}',
    'symbols': r'Con media 3 la varianza della binomiale negativa è $3+9/\theta$.'},
   {'tipo': 'confronto', 'titolo': 'Confronto | Sovradispersione e copertura', 'esperimento': 'm20-dispersione',
    'ricorda': 'Correggere gli errori standard per la dispersione riporta la copertura vicino al valore nominale.',
    'didascalia': r'Parametro di forma: 100 $\to$ 2. Tutti gli altri parametri e il seme sono fissi.',
    'righe': [('Dispersione media', 'Dispersione media'), ('Varianza attesa a media 3', 'Varianza attesa a media 3'),
              ('Copertura, Poisson', 'Copertura dell’intervallo di Poisson'),
              ('Copertura, quasi-Poisson', 'Copertura dell’intervallo quasi-Poisson')],
    'body': r'Con $\theta=2$ la dispersione media sale a 2,75 e l’intervallo di Poisson contiene la pendenza vera soltanto '
            r'nel 75,7\% dei campioni; quello quasi-Poisson nel 93,3\%.'},
  ]},
  {'titolo': 'Proporzioni e regressione logistica', 'pagine': [
   {'tipo': 'domanda', 'titolo': 'Una retta per le proporzioni?', 'codice': 'capitolo-07.R',
    'ricorda': 'Una proporzione sta fra 0 e 1; una retta no.',
    'domanda_testo': r'Il feldspato diminuisce lungo il percorso di trasporto. Che cosa prevede una retta adattata alle '
                     r'frazioni misurate per una stazione a 90 km, oltre l’ultima stazione campionata?',
    'interpretazione': r'La retta prevede 0,309 all’origine, 0,040 a 60 km e $-0{,}095$ a 90 km: una frazione negativa. '
                       r'Anche dentro l’intervallo la retta ignora che la variabilità di una frazione dipende dal suo valore.'},
   {'tipo': 'figura', 'titolo': 'Il feldspato lungo il trasporto', 'fig': 'Figure/F06.pdf',
    'ricorda': 'La curva logistica si avvicina a zero senza attraversarlo.',
    'didascalia': 'Frazione di feldspato nelle 36 sezioni; curva: modello logistico; tratteggio: retta dei minimi quadrati.',
    'body': r'Il modello logistico stima una frazione di 0,343 all’origine, 0,061 a 60 km e 0,023 a 90 km. David Cox '
            r'pubblicò nel 1958 la regressione per risposte binarie con il legame logistico, la forma usata qui per '
            r'conteggi di successi su un numero noto di prove.',
    'formula': r'\log\frac{p_i}{1-p_i}=\beta_0+\beta_1d_i',
    'symbols': r'$K_i\sim\mathrm{Bin}(n_i,p_i)$: punti di feldspato $K_i$ su $n_i$ punti contati alla distanza $d_i$.'},
   {'tipo': 'codice', 'titolo': 'Il modello binomiale e la sua dispersione', 'codice': 'capitolo-08.R',
    'ricorda': 'Le sezioni di una stessa roccia differiscono più di quanto il solo conteggio preveda.',
    'body': r'Il coefficiente della distanza vale $-0{,}0346$ per km: ogni 10 km le probabilità a favore del feldspato si '
            r'moltiplicano per 0,707. La dispersione vale 3,56, e l’errore standard quasi-binomiale passa da 0,0016 a '
            r'0,0029. Le sezioni hanno una variabilità oltre quella del conteggio.',
    'formula': r'\frac{p/(1-p)\,\big|_{d+10}}{p/(1-p)\,\big|_{d}}=e^{10\beta_1}'},
   {'tipo': 'testo', 'titolo': 'Errore di conteggio ed errore di campione',
    'ricorda': 'L’errore binomiale del conteggio è soltanto una parte dell’incertezza di una frazione.',
    'sinistra': {'label': 'Errore di conteggio', 'body': r'L. van der Plas e A. C. Tobi pubblicarono nel 1965 un diagramma per '
                 r'giudicare l’affidabilità del conteggio per punti, basato su due deviazioni standard binomiali; la distanza '
                 r'fra i punti deve superare la dimensione del granulo più grande. Con 300 punti e una frazione del 25\% '
                 r'la deviazione standard è 0,025.',
                 'formula': r'\sigma_p=\sqrt{\frac{p(1-p)}{n}}'},
    'destra': {'label': 'Errore di campione', 'body': r'F. Chayes scompose nel 1956 l’errore di un’analisi modale in errore '
               r'di conteggio ed errore di campione. M. J. Neilson e G. F. Brockman raccomandarono nel 1977 di contare i punti '
               r'in più serie e di stimare l’errore dalla deviazione standard campionaria. Nel caso la varianza fra le tre '
               r'sezioni di una stazione è 1,46 volte quella binomiale.',
               'symbols': r'Nel generatore ogni stazione ha un effetto casuale sulla scala logit e ogni sezione un piccolo scarto proprio.'}},
   {'tipo': 'schema', 'titolo': 'Probabilità, probabilità a favore e logit', 'diag': 'Diagrammi/D03.tex',
    'ricorda': 'Un coefficiente logistico moltiplica le probabilità a favore, $p/(1-p)$.',
    'didascalia': 'Curva logistica fra il predittore lineare e la probabilità.',
    'body': r'Il legame logistico porta una probabilità fra 0 e 1 sull’intera retta reale. Una variazione unitaria del '
            r'predittore moltiplica le probabilità a favore per $e^{\beta}$; l’effetto sulla probabilità dipende dal punto '
            r'della curva, massimo attorno a 0,5 e piccolo vicino a 0 e a 1.',
    'formula': r'p=\frac{1}{1+e^{-\eta}},\qquad \frac{dp}{d\eta}=p(1-p)'},
   {'tipo': 'scenario', 'titolo': 'Punti contati e variabilità fra stazioni', 'esperimento': 'm20-punti',
    'ricorda': 'Valutare quanto contare più punti per sezione migliora la stima quando le stazioni differiscono.',
    'didascalia': r'Cento punti per sezione; variabilità fra stazioni 0,25 sulla scala logit. Seme: 17.',
    'body': r'L’esperimento simula trecento rilievi di dodici stazioni con tre sezioni ciascuna. Con cento punti per sezione '
            r'la deviazione standard delle pendenze è 0,00485, l’errore standard binomiale medio 0,00265 e quello '
            r'quasi-binomiale 0,00346.',
    'formula': r'\operatorname{logit}p_{ij}=\beta_0+\beta_1d_j+u_j',
    'symbols': r'$u_j$ è l’effetto della stazione $j$, comune alle sue tre sezioni.'},
   {'tipo': 'confronto', 'titolo': 'Confronto | Punti contati e variabilità fra stazioni', 'esperimento': 'm20-punti',
    'ricorda': 'Oltre un certo numero di punti l’incertezza dipende dal numero di stazioni.',
    'didascalia': r'Punti per sezione: 100 $\to$ 1000. Tutti gli altri parametri e il seme sono fissi.',
    'righe': [('Dev. standard delle pendenze', 'Deviazione standard delle pendenze'),
              ('Errore standard binomiale', 'Errore standard binomiale medio'),
              ('Errore standard quasi-binomiale', 'Errore standard quasi-binomiale medio'), ('Dispersione media', 'Dispersione media')],
    'body': r'Con mille punti l’incertezza reale resta 0,00472: l’errore binomiale scende a 0,00084 e quello quasi-binomiale '
            r'a 0,00237. Le sezioni di una stazione condividono lo stesso effetto e le loro frazioni sono correlate.'},
  ]},
 ],
 'sintesi': {
  'titolo': 'Dal risultato alla relazione',
  'ricorda': 'Riporta distribuzione, legame, offset, dispersione e intervalli dei rapporti stimati.',
  'risultato': r'Dieci gradi di pendenza moltiplicano il tasso di frane per circa 2,5, con intervallo da 1,9 a 3,3 se si '
               r'tiene conto della sovradispersione; flysch e calcari hanno tassi pari a circa metà e un quarto di quello delle '
               r'argille. Lungo il trasporto le probabilità a favore del feldspato si riducono del 29\% ogni 10 km.',
  'limiti': r'I dati sono sintetici e le celle indipendenti. La sovradispersione è trattata con modelli che non spiegano '
            r'la sua origine, e il conteggio per punti ha una struttura per stazioni che un modello a effetti casuali '
            r'descriverebbe meglio.'},
 'riferimenti': {
  'titolo': 'Fonti, dati e codice per riprodurre le figure',
  'ricorda': 'I risultati numerici si riferiscono ai dati e alle ipotesi dichiarate nel caso.',
  'fonti': r'S. D. Poisson, Recherches sur la probabilité des jugements, Bachelier, 1837.\par '
           r'F. Chayes, Petrographic Modal Analysis, Wiley, 1956.\par '
           r'D. R. Cox, Journal of the Royal Statistical Society B 20(2), 215–242, 1958.\par '
           r'L. van der Plas e A. C. Tobi, American Journal of Science 263(1), 87–90, 1965.\par '
           r'J. A. Nelder e R. W. M. Wedderburn, Journal of the Royal Statistical Society A 135(3), 370–384, 1972.\par '
           r'R. W. M. Wedderburn, Biometrika 61(3), 439–447, 1974.\par '
           r'M. J. Neilson e G. F. Brockman, American Mineralogist 62, 1238–1244, 1977.\par '
           r'P. McCullagh e J. A. Nelder, Generalized Linear Models, 2ª ed., Chapman and Hall, 1989.\par '
           r'J. M. Ver Hoef e P. L. Boveng, Ecology 88(11), 2766–2772, 2007.',
  'dati': r'Dati sintetici del corso (frane\_v1.csv, conteggi\_v1.csv), generati da R/genera\_dati.R. Codice contiene i '
          r'frammenti delle pagine; R/M20\_figure.R ricostruisce figure e valori; Esperimenti contiene i programmi dei due '
          r'scenari e Diagrammi i disegni TikZ.'},
}
