# Specifica della lezione Isocrona (M19): datazione radiometrica. Valori da R/M19_figure.R, Codice/ e Esperimenti/.
LEZIONE = {
 'planet': 'Isocrona',
 'title': 'Datazione radiometrica',
 'copertina': {'titolo': r'Datazione\\radiometrica', 'sottotitolo': 'Rapporti isotopici che diventano età',
               'riga': 'Isocrone, regressione di York, MSWD e incertezza delle età'},
 'percorso': r'Dieci campioni di un granito e otto di un filone riportano i rapporti isotopici del sistema Rb-Sr con le '
             r'loro incertezze; quindici zirconi dello stesso granito hanno una data U-Pb. Il percorso va dalla legge del '
             r'decadimento all’isocrona, alla regressione con errori su entrambi gli assi, alla MSWD e al confronto fra età.',
 'caso': {
  'domanda': 'Quanti anni ha il granito, e con quale incertezza?',
  'ricorda': 'Un’età radiometrica è una stima: va riportata con la sua incertezza e con il modello che la produce.',
  'body': r'Dieci campioni sintetici di un granito e otto di un filone che lo attraversa riportano i rapporti '
          r'${}^{87}$Rb/${}^{86}$Sr e ${}^{87}$Sr/${}^{86}$Sr misurati, con le deviazioni standard analitiche. Quindici '
          r'zirconi del granito hanno una data U-Pb ciascuno. I dati sono generati con età note, per confrontare le stime '
          r'con i valori veri.',
  'info': r'Seguiremo i dati dalla legge del decadimento all’isocrona, alla regressione di York, alla MSWD e alla '
          r'combinazione delle incertezze, fino al confronto fra l’età Rb-Sr e quella degli zirconi.'},
 'capitoli': [
  {'titolo': 'Il decadimento come orologio', 'pagine': [
   {'tipo': 'domanda', 'titolo': 'Quanto lentamente decade il rubidio?', 'codice': 'capitolo-01.R',
    'ricorda': 'Il tempo di dimezzamento è $\\log 2/\\lambda$; un rapporto figlio/genitore si traduce in un’età.',
    'domanda_testo': r'La costante di decadimento di ${}^{87}$Rb raccomandata nel 2015 da IUPAC e IUGS è '
                     r'$1{,}3972\cdot10^{-11}$ per anno. Qual è il tempo di dimezzamento? Che età corrisponde a un rapporto '
                     r'fra ${}^{87}$Sr radiogenico e ${}^{87}$Rb di 0,0042?',
    'interpretazione': r'Il tempo di dimezzamento è 49,61 miliardi di anni. Un rapporto di 0,0042 corrisponde a circa 300 '
                       r'milioni di anni: in questo intervallo decade lo 0,42\% del rubidio.'},
   {'tipo': 'schema', 'titolo': 'Il genitore decade, il figlio si accumula', 'diag': 'Diagrammi/D01.tex',
    'ricorda': 'In un sistema chiuso l’età dipende dal rapporto fra figlio radiogenico e genitore rimasto.',
    'didascalia': 'Atomi del nuclide genitore e del figlio radiogenico in funzione del tempo.',
    'body': r'Ogni nucleo radioattivo ha la stessa probabilità di decadere nell’unità di tempo, la costante $\lambda$. Il '
            r'numero di nuclei genitori diminuisce in modo esponenziale e il figlio radiogenico cresce di altrettanto. Se il '
            r'sistema resta chiuso, il rapporto fra figlio radiogenico e genitore rimasto dipende soltanto dal tempo '
            r'trascorso.',
    'formula': r't=\frac1\lambda\log\Big(1+\frac{D^*}{N}\Big)'},
   {'tipo': 'codice', 'titolo': 'L’età di un campione richiede il rapporto iniziale', 'codice': 'capitolo-02.R',
    'ricorda': 'Un’età modello dipende dal rapporto iniziale assunto, tanto più quanto il campione è povero di rubidio.',
    'body': r'Il ${}^{87}$Sr misurato somma lo stronzio presente alla formazione e quello radiogenico. Per calcolare l’età '
            r'di un solo campione serve il rapporto iniziale ${}^{87}$Sr/${}^{86}$Sr. Il codice usa 0,704 per tre campioni '
            r'del granito, che hanno rapporto iniziale vero 0,7085: le età modello sono 2433, 432 e 328 milioni di anni, '
            r'contro un’età vera di 300.',
    'formula': r'\frac{{}^{87}\mathrm{Sr}}{{}^{86}\mathrm{Sr}}=r_0+\frac{{}^{87}\mathrm{Rb}}{{}^{86}\mathrm{Sr}}\big(e^{\lambda t}-1\big)'},
   {'tipo': 'figura', 'titolo': 'L’errore sul rapporto iniziale pesa sui campioni poveri', 'fig': 'Figure/F01.pdf',
    'ricorda': 'Un campione ricco di rubidio dà un’età modello robusta rispetto al rapporto iniziale.',
    'didascalia': r'Età modello con rapporto iniziale assunto 0,704, in scala logaritmica; punti: i dieci campioni del granito; tratteggio: 300 Ma.',
    'body': r'Con un rapporto iniziale sottostimato di 0,0045, l’età modello di un campione con ${}^{87}$Rb/${}^{86}$Sr di '
            r'0,15 supera i due miliardi di anni; per il campione più ricco di rubidio, con rapporto 11,5, l’errore si '
            r'riduce a 28 milioni di anni. L’errore sul rapporto iniziale si divide per ${}^{87}$Rb/${}^{86}$Sr.',
    'symbols': r'L’isocrona del capitolo successivo stima insieme età e rapporto iniziale.'},
   {'tipo': 'scenario', 'titolo': 'Età modello e rapporto iniziale', 'esperimento': 'm19-modello',
    'ricorda': 'Valutare come un errore sul rapporto iniziale sposta l’età modello al variare di ${}^{87}$Rb/${}^{86}$Sr.',
    'didascalia': 'Errore sul rapporto iniziale: 0,0045; età vera 300 Ma.',
    'body': r'L’esperimento calcola le età modello di campioni con ${}^{87}$Rb/${}^{86}$Sr fra 0,05 e 50, generati senza '
            r'errori di misura da un sistema con età e rapporto iniziale noti, usando un rapporto iniziale assunto più '
            r'basso della quantità impostata.',
    'formula': r't_{\mathrm{mod}}=\frac1\lambda\log\Big(1+\frac{y-r_0}{x}\Big)',
    'symbols': r'$x$ e $y$ sono ${}^{87}$Rb/${}^{86}$Sr e ${}^{87}$Sr/${}^{86}$Sr; il calcolo è deterministico.'},
   {'tipo': 'confronto', 'titolo': 'Confronto | Età modello e rapporto iniziale', 'esperimento': 'm19-modello',
    'ricorda': 'L’errore sull’età modello è circa proporzionale all’errore sul rapporto iniziale.',
    'didascalia': r'Errore sul rapporto iniziale: 0,0045 $\to$ 0,0005. L’età vera resta 300 Ma.',
    'righe': [('Età vera (Ma)', 'Età vera (Ma)'), (r'Età modello, $x=0{,}5$', 'Età modello, 87Rb/86Sr = 0,5'),
              (r'Età modello, $x=5$', 'Età modello, 87Rb/86Sr = 5'), (r'Età modello, $x=50$', 'Età modello, 87Rb/86Sr = 50')],
    'body': r'Con un errore di 0,0005 l’età modello di un campione con rapporto 0,5 scende da 939 a 371 milioni di anni; '
            r'per un rapporto 50 resta entro 1 milione di anni dal valore vero.'},
  ]},
  {'titolo': 'L’isocrona', 'pagine': [
   {'tipo': 'schema', 'titolo': 'Campioni coevi stanno su una retta', 'diag': 'Diagrammi/D02.tex',
    'ricorda': 'La pendenza dell’isocrona dà l’età, l’intercetta il rapporto iniziale.',
    'didascalia': 'Campioni con lo stesso rapporto iniziale, alla formazione e oggi.',
    'body': r'Minerali e rocce che si formano insieme dallo stesso fuso hanno lo stesso ${}^{87}$Sr/${}^{86}$Sr e rapporti '
            r'${}^{87}$Rb/${}^{86}$Sr diversi. Con il tempo ogni campione aumenta il suo ${}^{87}$Sr/${}^{86}$Sr in '
            r'proporzione al rubidio che contiene: i punti restano su una retta che ruota attorno al rapporto iniziale.',
    'formula': r'y=r_0+\big(e^{\lambda t}-1\big)\,x',
    'symbols': r'Dalla pendenza $b$ l’età si ottiene come $t=\log(1+b)/\lambda$.'},
   {'tipo': 'figura', 'titolo': 'L’isocrona del granito', 'fig': 'Figure/F02.pdf',
    'ricorda': 'Un’isocrona richiede campioni coevi, cogenetici e rimasti sistemi chiusi.',
    'didascalia': r'Dieci campioni del granito con barre di due deviazioni standard su ${}^{87}$Rb/${}^{86}$Sr e la retta di York.',
    'body': r'I dieci campioni del granito hanno ${}^{87}$Rb/${}^{86}$Sr fra 0,15 e 11,5. Le incertezze dichiarate sono '
            r'dell’1\% su ${}^{87}$Rb/${}^{86}$Sr e di $1{,}1\cdot10^{-5}$ su ${}^{87}$Sr/${}^{86}$Sr: le barre verticali '
            r'sono più piccole dei simboli. I punti sono allineati entro gli errori, e la retta stima insieme età e '
            r'rapporto iniziale.',
    'symbols': r'La correlazione fra gli errori dei due rapporti è posta a zero nel file del caso.'},
   {'tipo': 'codice', 'titolo': 'La retta dei minimi quadrati ordinari', 'codice': 'capitolo-03.R',
    'ricorda': 'I minimi quadrati ordinari ignorano le incertezze dichiarate dei campioni.',
    'body': r'Il codice adatta una retta con \texttt{lm}: pendenza 0,0042129, rapporto iniziale 0,70852, età 300,9 milioni '
            r'di anni. Il metodo tratta ${}^{87}$Rb/${}^{86}$Sr come noto senza errore, dà lo stesso peso a tutti i '
            r'campioni e stima la dispersione dai residui: le incertezze analitiche dichiarate non entrano nel calcolo.',
    'formula': r'\min_{a,b}\sum_i\big(y_i-a-bx_i\big)^2'},
   {'tipo': 'schema', 'titolo': 'Errori su entrambi gli assi', 'diag': 'Diagrammi/D03.tex',
    'ricorda': 'La regressione di York minimizza la somma dei residui pesati con gli errori dei due rapporti.',
    'didascalia': 'Un campione, la sua ellisse di errore e il punto corretto sulla retta.',
    'body': r'Derek York e colleghi pubblicarono nel 2004 equazioni unificate per la retta con errori su $x$ e $y$, '
            r'anche correlati. Ogni campione riceve un peso $W_i$ che combina i due errori secondo la pendenza; l’algoritmo '
            r'aggiorna pendenza e pesi fino alla convergenza e calcola gli errori standard nei punti corretti.',
    'formula': r'W_i=\frac{\omega(X_i)\,\omega(Y_i)}{\omega(X_i)+b^2\,\omega(Y_i)},\qquad \omega=\frac1{\sigma^2}'},
   {'tipo': 'codice', 'titolo': 'La retta di York del granito', 'codice': 'capitolo-04.R',
    'ricorda': 'L’errore standard dell’età si ottiene da quello della pendenza.',
    'body': r'La funzione \texttt{york} in \texttt{R/york.R} applica l’algoritmo. Per il granito la pendenza vale '
            r'$0{,}0042158\pm0{,}0000166$, il rapporto iniziale $0{,}708506\pm0{,}000012$ e l’età $301{,}1\pm1{,}2$ milioni '
            r'di anni, con MSWD 0,50. Su duemila isocrone simulate la deviazione standard delle pendenze è $1{,}64\cdot10^{-5}$.',
    'formula': r'\sigma_t=\frac{\sigma_b}{\lambda\,(1+b)}'},
   {'tipo': 'scenario', 'titolo': 'Minimi quadrati ordinari e regressione di York', 'esperimento': 'm19-york',
    'ricorda': 'Confrontare le età dei due metodi quando anche ${}^{87}$Rb/${}^{86}$Sr ha errori di misura.',
    'didascalia': r'Errore relativo su ${}^{87}$Rb/${}^{86}$Sr: 1\%; dieci campioni. Seme: 17.',
    'body': r'L’esperimento simula trecento isocrone di un sistema di 300 milioni di anni e calcola l’età con i minimi '
            r'quadrati ordinari e con la regressione di York. Con errori dell’1\% le due età medie coincidono; la '
            r'deviazione standard è 1,82 milioni di anni con i minimi quadrati e 1,03 con York.',
    'formula': r'\hat t=\frac{\log(1+\hat b)}{\lambda}',
    'symbols': r'$\hat b$ è la pendenza stimata in ciascuna isocrona simulata.'},
   {'tipo': 'confronto', 'titolo': 'Confronto | Minimi quadrati ordinari e York', 'esperimento': 'm19-york',
    'ricorda': 'Errori grandi sull’asse orizzontale rendono i minimi quadrati ordinari distorti verso il basso.',
    'didascalia': r'Errore relativo su ${}^{87}$Rb/${}^{86}$Sr: 1 $\to$ 15\%. Tutti gli altri parametri e il seme sono fissi.',
    'righe': [('Età media, minimi quadrati', 'Età media, minimi quadrati'), ('Età media, York', 'Età media, York'),
              ('Dev. standard, minimi quadrati', 'Deviazione standard, minimi quadrati'),
              ('Dev. standard, York', 'Deviazione standard, York')],
    'body': r'Con errori del 15\% l’età media dei minimi quadrati scende a 286 milioni di anni; quella di York resta '
            r'vicina a 300, con una dispersione minore.'},
  ]},
  {'titolo': 'MSWD e dispersione in eccesso', 'pagine': [
   {'tipo': 'figura', 'titolo': 'Che valori può avere la MSWD', 'fig': 'Figure/F03.pdf',
    'ricorda': 'La MSWD vale in media 1 se gli errori dichiarati descrivono la dispersione; la sua variabilità dipende da $f$.',
    'didascalia': r'Distribuzioni della MSWD per 8 e 6 gradi di libertà, soglie di Wendt e Carl (tratteggio) e valori osservati (triangoli).',
    'body': r'La MSWD è la somma dei residui pesati al quadrato divisa per i gradi di libertà $f=n-2$. I. Wendt e '
            r'C. Carl mostrarono nel 1991 che il suo valore atteso è 1 per ogni $f$ e la sua deviazione standard '
            r'$\sqrt{2/f}$; un valore oltre $1+2\sqrt{2/f}$ ha probabilità inferiore al 5\%. Il granito ha MSWD 0,50 con '
            r'soglia 2,00; il filone 3,94 con soglia 2,15.',
    'formula': r'\mathrm{MSWD}=\frac{1}{f}\sum_{i=1}^n W_i\big(Y_i-a-bX_i\big)^2'},
   {'tipo': 'domanda', 'titolo': 'I campioni del filone formano un’isocrona?', 'codice': 'capitolo-05.R',
    'ricorda': 'Una MSWD oltre la soglia indica una dispersione che gli errori analitici non spiegano.',
    'domanda_testo': r'Gli otto campioni del filone hanno le stesse incertezze analitiche del granito. La loro dispersione '
                     r'attorno alla retta di York è compatibile con quelle incertezze?',
    'interpretazione': r'La MSWD vale 3,94 con sei gradi di libertà, oltre la soglia di 2,15; la probabilità di un valore '
                       r'così grande con i soli errori analitici è 0,0006. I campioni del filone hanno una dispersione in eccesso.'},
   {'tipo': 'figura', 'titolo': 'Dove sta la dispersione in eccesso', 'fig': 'Figure/F04.pdf',
    'ricorda': 'I residui pesati si leggono in unità di deviazione standard: oltre $\\pm2$ sono rari se gli errori sono corretti.',
    'didascalia': r'Residui pesati degli otto campioni del filone rispetto alla retta di York; fascia: $\pm2$.',
    'body': r'Il residuo pesato divide lo scarto verticale dalla retta per la sua deviazione standard combinata. Due '
            r'campioni, F03 e F04, hanno residui di $-2{,}73$ e $+3{,}49$; gli altri restano entro $\pm1{,}4$. Nel '
            r'generatore il rapporto iniziale del filone varia da campione a campione, come in un fuso non omogeneo.',
    'formula': r'e_i=\big(Y_i-a-bX_i\big)\sqrt{W_i}'},
   {'tipo': 'codice', 'titolo': 'Scalare l’incertezza con la MSWD', 'codice': 'capitolo-06.R',
    'ricorda': 'Scalare per $\\sqrt{\\mathrm{MSWD}}$ presuppone una dispersione in eccesso proporzionale agli errori analitici.',
    'body': r'Una pratica diffusa moltiplica l’errore standard per la radice della MSWD, attribuendo l’eccesso a errori '
            r'analitici sottostimati in modo uniforme. Per il filone l’età è 247,5 milioni di anni; l’incertezza passa da '
            r'1,23 a 2,44 milioni di anni. Il valore del generatore, 250, cade entro due incertezze scalate.',
    'formula': r'\sigma_t^{*}=\sigma_t\sqrt{\mathrm{MSWD}}'},
   {'tipo': 'testo', 'titolo': 'Che cosa può significare una MSWD lontana da 1',
    'ricorda': 'Una MSWD vicina a 1 è compatibile con il modello; da sola non lo conferma.',
    'sinistra': {'label': 'MSWD grande', 'body': r'Una MSWD oltre la soglia può nascere da errori analitici sottostimati o da '
                 r'una dispersione geologica: rapporti iniziali diversi, sistemi aperti dopo la formazione, campioni di età '
                 r'diverse. Le due spiegazioni portano a modelli diversi, e la scelta richiede informazioni geologiche '
                 r'oltre al valore della statistica.'},
    'destra': {'label': 'MSWD piccola', 'body': r'Pieter Vermeesch ha osservato nel 2025 che una MSWD piccola merita '
               r'altrettanta attenzione: può indicare errori sovrastimati o un campione troppo piccolo per rivelare una '
               r'dispersione reale. Raccomanda di quantificare la dispersione e scoraggia l’esclusione di dati al solo scopo '
               r'di ridurre la MSWD.',
               'symbols': r'Nel granito la MSWD di 0,50 ha probabilità di coda 0,855: un valore comune con otto gradi di libertà.'}},
   {'tipo': 'scenario', 'titolo': 'MSWD con errori sottostimati', 'esperimento': 'm19-mswd',
    'ricorda': 'Osservare la MSWD quando gli errori dichiarati sono corretti e quando sono troppo piccoli.',
    'didascalia': 'Errori reali uguali a quelli dichiarati; dieci campioni; quattrocento isocrone. Seme: 17.',
    'body': r'L’esperimento simula quattrocento isocrone con errori reali pari agli errori dichiarati moltiplicati per un '
            r'fattore. Con fattore 1 la MSWD media è 0,94 e l’intervallo di due errori standard contiene l’età vera nel '
            r'95,5\% dei casi.',
    'formula': r'E[\mathrm{MSWD}]=k^2',
    'symbols': r'$k$ è il rapporto fra errori reali ed errori dichiarati; con molte simulazioni la quota oltre la soglia è circa il 4\%.'},
   {'tipo': 'confronto', 'titolo': 'Confronto | MSWD con errori sottostimati', 'esperimento': 'm19-mswd',
    'ricorda': 'Errori dichiarati troppo piccoli producono intervalli di confidenza troppo stretti.',
    'didascalia': r'Errori reali / dichiarati: 1 $\to$ 1,5. Tutti gli altri parametri e il seme sono fissi.',
    'righe': [('MSWD medio', 'MSWD medio'), ('Soglia', 'Soglia 1+2√(2/f)'), ('Quota oltre la soglia', 'Quota oltre la soglia'),
              (r'Copertura a $2\sigma$', 'Copertura dell’intervallo a 2σ')],
    'body': r'Con errori reali 1,5 volte quelli dichiarati la MSWD media sale a 2,12, metà delle isocrone supera la soglia '
            r'e la copertura dell’intervallo scende all’82\%.'},
  ]},
  {'titolo': 'Incertezza e confronto delle età', 'pagine': [
   {'tipo': 'codice', 'titolo': 'L’incertezza della costante di decadimento', 'codice': 'capitolo-07.R',
    'ricorda': 'Per confrontare età di sistemi isotopici diversi si includono le incertezze delle costanti di decadimento.',
    'body': r'La costante raccomandata ha incertezza $\pm0{,}0045\cdot10^{-11}$ con fattore di copertura 2, cioè lo 0,16\% '
            r'a una deviazione standard. Sull’età del granito pesa 0,48 milioni di anni, contro 1,18 dell’errore '
            r'analitico; combinate in quadratura danno 1,28. Nel confronto fra due età Rb-Sr questo contributo è comune.',
    'formula': r'\sigma_{t,\mathrm{tot}}=\sqrt{\sigma_t^2+\big(t\,\sigma_\lambda/\lambda\big)^2}'},
   {'tipo': 'figura', 'titolo': 'Le date dei singoli zirconi', 'fig': 'Figure/F05.pdf',
    'ricorda': 'Un grafico delle date ordinate con le loro barre mostra subito dispersione e valori anomali.',
    'didascalia': 'Date U-Pb dei quindici zirconi con barre di due deviazioni standard; linea e fascia: media pesata di quattordici zirconi.',
    'body': r'Quattordici zirconi hanno date fra 297,4 e 301,1 milioni di anni, con incertezze fra 0,8 e 2 milioni di anni. '
            r'Lo zircone Z15 ha una data di 316,9 milioni di anni, lontana dalle altre di molte deviazioni standard. Uno '
            r'zircone ereditato è un cristallo più antico che il magma ha incorporato da rocce preesistenti.',
    'symbols': r'Nel generatore Z15 è un granulo ereditato con età di 318 milioni di anni.'},
   {'tipo': 'domanda', 'titolo': 'La media pesata deve includere Z15?', 'codice': 'capitolo-08.R',
    'ricorda': 'Un dato si esclude per una ragione documentata: la MSWD segnala il problema, la geologia lo spiega.',
    'domanda_testo': r'Con tutti i quindici zirconi, la media pesata è coerente con le incertezze? Che cosa cambia escludendo '
                     r'Z15?',
    'interpretazione': r'Con quindici zirconi la media è $301{,}59\pm0{,}34$ milioni di anni e la MSWD 19,4, oltre la soglia '
                       r'di 1,76. Senza Z15 la media è $299{,}65\pm0{,}36$ e la MSWD 0,58: le date restanti sono coerenti.'},
   {'tipo': 'testo', 'titolo': 'Quando escludere un dato',
    'ricorda': 'La ragione per escludere un dato precede il calcolo; la MSWD da sola non basta.',
    'sinistra': {'label': 'Ragioni geologiche', 'body': r'Uno zircone può essere più antico del magma, se ereditato, o più '
                 r'giovane, se ha perso piombo. Le immagini dei cristalli, la posizione dell’analisi e la composizione chimica '
                 r'documentano queste situazioni. Z15 è un caso netto: la sua data dista dalla media di oltre 17 milioni di '
                 r'anni, più di dieci volte la sua incertezza.'},
    'destra': {'label': 'Il rischio della selezione', 'body': r'Escludere le date che allontanano la MSWD da 1 finché il '
               r'valore rientra sotto la soglia produce medie troppo precise. I criteri di esclusione vanno dichiarati prima '
               r'del calcolo e applicati a tutti i cristalli, e la relazione riporta anche le date escluse.',
               'formula': r'\mathrm{MSWD}=\frac{1}{n-1}\sum_{i=1}^n\frac{(t_i-\bar t)^2}{\sigma_i^2}'}},
   {'tipo': 'figura', 'titolo': 'Rb-Sr e U-Pb a confronto', 'fig': 'Figure/F06.pdf',
    'ricorda': 'Due età si confrontano con la differenza divisa per la sua incertezza combinata.',
    'didascalia': 'Età del granito con barre di due deviazioni standard: isocrona Rb-Sr senza e con la costante di decadimento, media U-Pb.',
    'body': r'L’isocrona dà $301{,}1\pm1{,}3$ milioni di anni con la costante di decadimento, gli zirconi $299{,}65\pm0{,}48$ '
            r'includendo l’incertezza della costante di ${}^{238}$U. La differenza, 1,46 milioni di anni, vale 1,07 volte '
            r'la sua incertezza combinata: le due età sono compatibili.',
    'formula': r'z=\frac{t_1-t_2}{\sqrt{\sigma_1^2+\sigma_2^2}}'},
   {'tipo': 'scenario', 'titolo': 'Media pesata e dispersione geologica', 'esperimento': 'm19-media',
    'ricorda': 'Valutare la media pesata quando le date hanno una dispersione reale oltre a quella analitica.',
    'didascalia': 'Dispersione geologica: 0 Ma; quindici cristalli; cinquecento gruppi. Seme: 17.',
    'body': r'L’esperimento simula cinquecento gruppi di date attorno a 300 milioni di anni, con incertezze analitiche fra '
            r'0,8 e 2 e una dispersione geologica impostata. Senza dispersione la MSWD media è 0,97 e l’intervallo nominale '
            r'contiene 300 nel 95,6\% dei gruppi.',
    'formula': r'\bar t=\frac{\sum_i t_i/\sigma_i^2}{\sum_i 1/\sigma_i^2}',
    'symbols': r'L’errore scalato moltiplica l’errore standard per $\sqrt{\mathrm{MSWD}}$ quando la MSWD supera 1.'},
   {'tipo': 'confronto', 'titolo': 'Confronto | Media pesata e dispersione geologica', 'esperimento': 'm19-media',
    'ricorda': 'Con dispersione geologica l’errore nominale della media pesata è troppo piccolo.',
    'didascalia': r'Dispersione geologica: 0 $\to$ 2 Ma. Tutti gli altri parametri e il seme sono fissi.',
    'righe': [('MSWD medio', 'MSWD medio'), ('Quota oltre la soglia', 'Quota oltre la soglia'),
              ('Copertura, errore nominale', 'Copertura con l’errore nominale'), ('Copertura, errore scalato', 'Copertura con l’errore scalato')],
    'body': r'Con 2 milioni di anni di dispersione la MSWD media sale a 3,46 e la copertura nominale scende al 65\%; '
            r'l’errore scalato la riporta all’88,6\%, ancora sotto il 95\%.'},
  ]},
 ],
 'sintesi': {
  'titolo': 'Dal risultato alla relazione',
  'ricorda': 'Riporta età, incertezza, MSWD, numero di campioni, costante di decadimento e criteri di esclusione.',
  'risultato': r'L’isocrona Rb-Sr del granito dà $301{,}1\pm1{,}2$ milioni di anni con MSWD 0,50 e rapporto iniziale '
               r'0,708506; con la costante di decadimento l’incertezza è 1,3. Gli zirconi, escluso il granulo ereditato, '
               r'danno $299{,}65\pm0{,}36$. Il filone ha una dispersione in eccesso e un’età di $247{,}5\pm2{,}4$ con '
               r'l’incertezza scalata.',
  'limiti': r'I dati sono sintetici e gli errori dei due rapporti sono indipendenti. Le incertezze sono a una deviazione '
            r'standard; la scalatura per la MSWD presuppone un eccesso proporzionale agli errori analitici, e l’esclusione '
            r'di Z15 si basa sul modello che ha generato i dati.'},
 'riferimenti': {
  'titolo': 'Fonti, dati e codice per riprodurre le figure',
  'ricorda': 'I risultati numerici si riferiscono ai dati e alle ipotesi dichiarate nel caso.',
  'fonti': r'G. A. McIntyre e colleghi, Journal of Geophysical Research 71(22), 5459, 1966.\par '
           r'I. Wendt e C. Carl, Chemical Geology 86(4), 275–285, 1991.\par '
           r'A. P. Dickin, Radiogenic Isotope Geology, Cambridge University Press, 1995.\par '
           r'D. York e colleghi, American Journal of Physics 72(3), 367–375, 2004.\par '
           r'I. M. Villa e colleghi, Geochimica et Cosmochimica Acta 164, 382–385, 2015.\par '
           r'I. M. Villa e colleghi, Pure and Applied Chemistry 94(9), 1085–1092, 2022.\par '
           r'P. Vermeesch, High MSWDs are not the problem, low ones are, 2025.',
  'dati': r'Dati sintetici del corso (isocrone\_v1.csv, date\_v1.csv), generati da R/genera\_dati.R. R/york.R contiene la '
          r'regressione di York; Codice contiene i frammenti delle pagine; R/M19\_figure.R ricostruisce figure e valori; '
          r'Esperimenti contiene i programmi dei due scenari e Diagrammi i disegni TikZ.'},
}
