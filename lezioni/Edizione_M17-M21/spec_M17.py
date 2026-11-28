# Specifica della lezione Simplex (M17): dati composizionali. Valori da R/M17_figure.R, Codice/ e Esperimenti/.
LEZIONE = {
 'planet': 'Simplex',
 'title': 'Dati composizionali',
 'copertina': {'titolo': r'Dati\\composizionali', 'sottotitolo': 'Percentuali che sommano a cento',
               'riga': 'Chiusura, log-rapporti e geometria di Aitchison'},
 'percorso': r'Centoquarantaquattro analisi sintetiche di diciotto stazioni riportano sei parti in percentuale in massa. '
             r'Il percorso parte dagli effetti della somma costante, introduce i log-rapporti, descrive centri e '
             r'variabilità e chiude con i valori sotto il limite di rivelabilità e con un modello per la densità.',
 'caso': {
  'domanda': 'La correlazione di −0,92 fra SiO$_2$ e CaO descrive la geochimica o la somma a cento?',
  'ricorda': 'Una percentuale è una parte di un intero: il suo significato dipende dalle altre parti.',
  'body': r'Centoquarantaquattro campioni sintetici di arenaria, basalto e calcare, otto per ciascuna di diciotto stazioni, '
          r'riportano SiO$_2$, Al$_2$O$_3$, CaO, MgO, FeO e una parte residua in percentuale in massa, con somma cento. '
          r'Quindici campioni hanno una parte sotto il limite di rivelabilità di 0,1\%, registrata come zero.',
  'info': r'Seguiremo i dati dalla chiusura ai log-rapporti, ai centri composizionali e alla sostituzione degli zeri, fino '
          r'a un modello della densità scritto in coordinate di bilancio.'},
 'capitoli': [
  {'titolo': 'La chiusura e i suoi effetti', 'pagine': [
   {'tipo': 'domanda', 'titolo': 'Che cosa resta se cambia la base di calcolo?', 'codice': 'capitolo-01.R',
    'ricorda': 'I rapporti fra le parti restano gli stessi quando la composizione viene riferita a un intero diverso.',
    'domanda_testo': r'Un basalto contiene il 46,7\% di SiO$_2$ e il 10,4\% di CaO. Riferito alla sola frazione dei cinque '
                     r'ossidi, i due valori diventano più grandi. Quale quantità non cambia?',
    'interpretazione': r'Il rapporto SiO$_2$/CaO vale 4,49 in entrambe le basi. Le percentuali dipendono dall’intero scelto, '
                       r'il rapporto dipende soltanto dalle due parti.'},
   {'tipo': 'figura', 'titolo': 'Il simplesso è lo spazio delle composizioni', 'fig': 'Figure/F01.pdf',
    'ricorda': 'Una composizione a $D$ parti ha $D-1$ gradi di libertà: l’ultima parte è determinata dalle altre.',
    'didascalia': r'Sottocomposizione SiO$_2$, CaO, MgO+FeO chiusa a cento, dopo la sostituzione degli zeri.',
    'body': r'Una composizione a $D$ parti è un vettore di numeri positivi con somma costante $\kappa$, qui cento. L’insieme '
            r'di questi vettori è il simplesso. Il diagramma ternario rappresenta una sottocomposizione a tre parti: ogni '
            r'vertice corrisponde a una parte pura e la distanza da un lato misura la quota della parte opposta. Le arenarie '
            r'si raccolgono vicino al vertice della silice, i calcari vicino a quello del calcio, i basalti all’interno.',
    'formula': r'\mathcal S^D=\Big\{x\in\mathbb R^D:\ x_i>0,\ \sum_{i=1}^D x_i=\kappa\Big\}'},
   {'tipo': 'schema', 'titolo': 'La somma costante impone covarianze negative', 'diag': 'Diagrammi/D01.tex',
    'ricorda': 'In dati chiusi una parte non può crescere senza che le altre, insieme, diminuiscano.',
    'didascalia': 'Composizione a tre parti prima e dopo l’aumento della prima parte.',
    'body': r'Poiché la somma delle parti è costante, la sua covarianza con qualunque parte è nulla. Ne segue l’identità '
            r'osservata da Felix Chayes nel 1960: la somma delle covarianze di una parte con tutte le altre è uguale '
            r'all’opposto della sua varianza. Nei campioni completi del caso la varianza di SiO$_2$ è 993 e la somma delle sue '
            r'cinque covarianze vale $-993$. Almeno una covarianza deve quindi essere negativa, qualunque sia la geochimica.',
    'formula': r'\sum_{j\ne i}\operatorname{cov}(x_i,x_j)=-\operatorname{var}(x_i)',
    'symbols': r'$x_i$ e $x_j$ sono due parti della composizione chiusa; la relazione vale per ogni parte $i$.'},
   {'tipo': 'domanda', 'titolo': 'Le correlazioni cambiano con la sottocomposizione', 'codice': 'capitolo-02.R',
    'ricorda': 'Un log-rapporto fra due parti è lo stesso in ogni sottocomposizione che le contiene.',
    'domanda_testo': r'Nei basalti, MgO e FeO sono correlati positivamente o negativamente? La risposta può dipendere da '
                     r'quali altre parti vengono incluse nell’intero?',
    'interpretazione': r'La correlazione vale 0,373 nella composizione a sei parti e $-0{,}177$ nella sottocomposizione CaO, '
                       r'MgO, FeO. La varianza di $\log(\mathrm{MgO}/\mathrm{FeO})$ resta 0,175 nei due casi.'},
   {'tipo': 'figura', 'titolo': 'Parti indipendenti diventano correlate', 'fig': 'Figure/F02.pdf',
    'ricorda': 'Una correlazione fra percentuali va confrontata con quella che la sola chiusura produrrebbe.',
    'didascalia': 'Trecento composizioni simulate da tre parti lognormali indipendenti, chiuse a cento.',
    'body': r'Karl Pearson descrisse nel 1897 la correlazione spuria che nasce fra indici con lo stesso denominatore. Nella '
            r'simulazione tre parti indipendenti hanno correlazione 0,045 fra le prime due; dopo la chiusura la stessa coppia '
            r'ha correlazione $-0{,}519$. Quando le parti hanno la stessa varianza e le stesse covarianze, il vincolo di '
            r'Chayes fissa la correlazione media fra coppie al valore riportato sotto.',
    'formula': r'\bar r=-\frac{1}{D-1}',
    'symbols': r'$D$ è il numero delle parti; con tre parti il valore è $-0{,}5$, con dieci parti $-0{,}11$.'},
   {'tipo': 'scenario', 'titolo': 'Chiusura e correlazione spuria', 'esperimento': 'm17-chiusura',
    'ricorda': 'Osservare le correlazioni che la chiusura a cento introduce fra parti generate indipendenti.',
    'didascalia': 'Numero delle parti: 3. Seme: 17.',
    'body': r'L’esperimento genera duecento campioni con $D$ parti lognormali indipendenti e con la stessa dispersione, poi '
            r'li chiude a cento. Confronta la correlazione media fra le coppie di parti prima e dopo la chiusura con il '
            r'valore imposto dal vincolo.',
    'formula': r'\sum_{j\ne i}\operatorname{cov}(x_i,x_j)=-\operatorname{var}(x_i)',
    'symbols': r'$D$ parti scambiabili: la correlazione media dopo la chiusura tende a $-1/(D-1)$.'},
   {'tipo': 'confronto', 'titolo': 'Confronto | Chiusura e correlazione spuria', 'esperimento': 'm17-chiusura',
    'ricorda': 'La chiusura produce correlazioni negative anche fra parti indipendenti; la loro entità dipende da $D$.',
    'didascalia': r'Numero delle parti: 3 $\to$ 8. Tutti gli altri parametri e il seme sono fissi.',
    'righe': [('Correlazione media prima', 'Correlazione media prima della chiusura'),
              ('Correlazione media dopo', 'Correlazione media dopo la chiusura'),
              (r'Valore $-1/(D-1)$', 'Valore −1/(D−1)'), ('Coppie di parti', 'Coppie di parti')],
    'body': r'Con otto parti il vincolo si distribuisce su ventotto coppie e la correlazione media dopo la chiusura scende in '
            r'valore assoluto da circa 0,50 a 0,14. Prima della chiusura le medie restano vicine a zero.'},
  ]},
  {'titolo': 'Rapporti logaritmici', 'pagine': [
   {'tipo': 'schema', 'titolo': 'Il log-rapporto non dipende dalla chiusura', 'diag': 'Diagrammi/D02.tex',
    'ricorda': 'I log-rapporti sono invarianti di scala, simmetrici e additivi lungo una catena di parti.',
    'didascalia': 'Tre parti e i loro log-rapporti.',
    'body': r'John Aitchison propose nel 1982 di analizzare le composizioni attraverso i logaritmi dei rapporti fra le parti. '
            r'Un log-rapporto non cambia se tutte le parti vengono moltiplicate per la stessa costante, per cui è lo stesso '
            r'nei dati grezzi, in quelli chiusi a cento e in ogni sottocomposizione. Scambiare le parti cambia soltanto il '
            r'segno, e i log-rapporti si sommano lungo una catena.',
    'formula': r'\log\frac{\lambda x_i}{\lambda x_j}=\log\frac{x_i}{x_j},\qquad \lambda>0'},
   {'tipo': 'codice', 'titolo': 'Due trasformazioni dei log-rapporti', 'codice': 'capitolo-03.R',
    'ricorda': 'La trasformazione alr dipende dalla parte scelta come denominatore; la clr tratta tutte le parti allo stesso modo.',
    'body': r'La trasformazione alr divide le prime $D-1$ parti per l’ultima e ne prende il logaritmo; il risultato cambia '
            r'con la parte scelta come denominatore. La trasformazione clr divide ogni parte per la media geometrica di '
            r'tutte le parti. Per lo stesso basalto il codice calcola le due trasformazioni con Altro come denominatore '
            r'della alr: le coordinate clr sommano a zero.',
    'formula': r'\operatorname{clr}_i(x)=\log\frac{x_i}{g(x)},\qquad g(x)=\Big(\prod_{j=1}^D x_j\Big)^{1/D}'},
   {'tipo': 'testo', 'titolo': 'Proprietà delle coordinate clr',
    'ricorda': 'Le coordinate clr sono vincolate a somma zero: la loro matrice di covarianza è singolare.',
    'sinistra': {'label': 'Geometria', 'body': r'Le operazioni naturali del simplesso sono la perturbazione, prodotto parte per '
                 r'parte seguito dalla chiusura, e la potenza, elevamento di ogni parte allo stesso esponente seguito dalla '
                 r'chiusura. Con queste operazioni il simplesso è uno spazio vettoriale, e la trasformazione clr lo porta in '
                 r'un sottospazio di $\mathbb R^D$ conservando somme e prodotti per uno scalare.',
                 'formula': r'x\oplus y=\mathcal C(x_1y_1,\ldots,x_Dy_D),\qquad \alpha\odot x=\mathcal C(x_1^\alpha,\ldots,x_D^\alpha)'},
    'destra': {'label': 'Conseguenze per l’analisi', 'body': r'Le coordinate clr sommano a zero, e una qualunque di esse è '
               r'determinata dalle altre. La loro matrice di covarianza ha quindi determinante nullo e nessuna inversa: '
               r'i metodi che richiedono l’inversa, come la regressione multipla o la distanza di Mahalanobis, usano $D-1$ '
               r'coordinate indipendenti. Le varianze delle coordinate clr dipendono dall’insieme completo delle parti.',
               'symbols': r'$\mathcal C$ indica la chiusura a somma $\kappa$; $\oplus$ è la perturbazione, $\odot$ la potenza.'}},
   {'tipo': 'schema', 'titolo': 'I bilanci separano gruppi di parti', 'diag': 'Diagrammi/D04.tex',
    'ricorda': 'Una partizione binaria sequenziale definisce $D-1$ coordinate ortonormali, ciascuna interpretabile.',
    'didascalia': 'Partizione binaria sequenziale delle sei parti e i primi tre bilanci.',
    'body': r'Juan José Egozcue e colleghi introdussero nel 2003 le trasformazioni isometriche, che forniscono $D-1$ '
            r'coordinate ortonormali; nel 2005 Egozcue e Vera Pawlowsky-Glahn le costruirono con una partizione binaria '
            r'sequenziale, che divide le parti in due gruppi e poi ogni gruppo in due, fino a parti singole. Ogni divisione '
            r'produce un bilancio, il log-rapporto fra le medie geometriche dei due gruppi con un fattore di normalizzazione.',
    'formula': r'b=\sqrt{\frac{rs}{r+s}}\,\log\frac{g(x_+)}{g(x_-)}',
    'symbols': r'$x_+$ e $x_-$ sono i due gruppi di parti, con $r$ e $s$ parti; $g$ è la media geometrica.'},
   {'tipo': 'codice', 'titolo': 'Lo stesso spostamento pesa in modo diverso', 'codice': 'capitolo-04.R',
    'ricorda': 'La distanza di Aitchison misura variazioni relative delle parti.',
    'body': r'La distanza di Aitchison è la distanza euclidea fra le coordinate clr. Nel codice due coppie di composizioni '
            r'differiscono per 0,1 punti percentuali spostati fra due parti, con la stessa distanza euclidea di 0,141. Nella '
            r'prima coppia MgO passa da 0,1 a 0,2 e raddoppia; nella seconda SiO$_2$ passa da 50 a 50,1. Le distanze di '
            r'Aitchison valgono 0,633 e 0,005.',
    'formula': r'd_A(x,y)=\big\lVert\operatorname{clr}(x)-\operatorname{clr}(y)\big\rVert'},
   {'tipo': 'scenario', 'titolo': 'Distanza euclidea e distanza di Aitchison', 'esperimento': 'm17-distanze',
    'ricorda': 'Confrontare l’effetto dello stesso spostamento assoluto su una parte minore e su una parte maggiore.',
    'didascalia': 'Livello della parte minore: 0,2\\%. Seme: 17.',
    'body': r'Due composizioni a quattro parti differiscono per 0,1 punti percentuali spostati dalla parte maggiore alla parte '
            r'minore. La distanza euclidea resta costante; la curva riporta la distanza di Aitchison per livelli della parte '
            r'minore fra 0,05 e 20\%.',
    'formula': r'd_A(x,y)=\Big[\sum_{i=1}^D\big(\operatorname{clr}_i(x)-\operatorname{clr}_i(y)\big)^2\Big]^{1/2}',
    'symbols': r'Il calcolo è deterministico: il seme non cambia il risultato.'},
   {'tipo': 'confronto', 'titolo': 'Confronto | Distanza euclidea e distanza di Aitchison', 'esperimento': 'm17-distanze',
    'ricorda': 'Lo stesso spostamento in punti percentuali pesa molto di più su una parte in traccia.',
    'didascalia': r'Livello della parte minore: 0,2 $\to$ 5\%. Tutti gli altri parametri sono fissi.',
    'righe': [('Distanza euclidea', 'Distanza euclidea'), ('Distanza di Aitchison', 'Distanza di Aitchison'),
              ('Rapporto Aitchison/euclidea', 'Rapporto Aitchison/euclidea')],
    'body': r'Con la parte minore allo 0,2\% lo spostamento ne aumenta la quota della metà e la distanza di Aitchison vale '
            r'0,352. Con la parte al 5\% lo stesso spostamento è del 2\% e la distanza scende a 0,018.'},
  ]},
  {'titolo': 'Descrivere un insieme di composizioni', 'pagine': [
   {'tipo': 'codice', 'titolo': 'Il centro è una media geometrica chiusa', 'codice': 'capitolo-05.R',
    'ricorda': 'Il centro composizionale media i log-rapporti; la media aritmetica media le percentuali.',
    'body': r'Il centro di un insieme di composizioni è la media geometrica di ogni parte, chiusa a cento. Equivale alla '
            r'media delle coordinate clr riportata nel simplesso. Per i quarantotto basalti la media aritmetica di MgO vale '
            r'8,95\% e il centro 8,39\%; per SiO$_2$ i due valori sono 46,37 e 47,25\%. Le parti più disperse in termini '
            r'relativi mostrano le differenze maggiori.',
    'formula': r'\operatorname{cen}(X)=\mathcal C\big(g_1,\ldots,g_D\big),\quad g_j=\Big(\prod_{k=1}^n x_{kj}\Big)^{1/n}'},
   {'tipo': 'figura', 'titolo': 'La matrice di variazione riassume la dispersione', 'fig': 'Figure/F04.pdf', 'h': '6.3cm',
    'ricorda': 'Una varianza di log-rapporto vicina a zero indica due parti quasi proporzionali.',
    'didascalia': r'Varianze di $\log(x_i/x_j)$ sui 144 campioni, dopo la sostituzione degli zeri.',
    'body': r'Aitchison descrisse la variabilità con le varianze di tutti i log-rapporti. Un valore vicino a zero indica parti '
            r'che variano in proporzione: SiO$_2$ e Al$_2$O$_3$ hanno varianza 0,48, CaO e Altro 0,58, perché nei calcari la '
            r'parte residua contiene soprattutto la CO$_2$ legata al calcio. I valori maggiori, 7,64 per CaO e FeO, separano '
            r'le litologie. La variabilità totale vale 8,98.',
    'formula': r'\tau_{ij}=\operatorname{var}\Big(\log\frac{x_i}{x_j}\Big),\qquad \operatorname{totvar}=\frac{1}{2D}\sum_{i,j}\tau_{ij}'},
   {'tipo': 'figura', 'titolo': 'Il biplot delle coordinate clr', 'fig': 'Figure/F05.pdf',
    'ricorda': 'Il biplot composizionale si costruisce sulle coordinate clr centrate, mai sulle percentuali.',
    'didascalia': 'Biplot di covarianza delle coordinate clr: punteggi standardizzati, raggi scalati con le deviazioni standard delle componenti.',
    'body': r'Le componenti principali delle coordinate clr riassumono la variabilità totale. Nel caso la prima componente ne '
            r'spiega il 69,4\% e la seconda il 28,9\%: i tre gruppi di campioni occupano regioni separate, e i raggi indicano '
            r'le parti che li distinguono. I raggi di SiO$_2$ e Al$_2$O$_3$ quasi coincidono, coerenti con la piccola '
            r'varianza del loro log-rapporto.',
    'symbols': r'Le quote si riferiscono all’insieme delle tre litologie: la dispersione è dominata dalle differenze fra i gruppi.'},
   {'tipo': 'schema', 'titolo': 'Leggere i collegamenti fra i raggi', 'diag': 'Diagrammi/D03.tex',
    'ricorda': 'Nel biplot clr si leggono i collegamenti fra le punte dei raggi, più informativi dei singoli raggi.',
    'didascalia': 'Schema dei raggi di tre parti e di due collegamenti.',
    'body': r'John Aitchison e Michael Greenacre mostrarono nel 2002 che, in un biplot delle coordinate clr centrate, il '
            r'segmento che unisce le punte di due raggi approssima la deviazione standard del log-rapporto fra le due parti. '
            r'Nel caso il collegamento fra CaO e FeO misura 2,76 contro una deviazione standard di 2,77; quello fra SiO$_2$ '
            r'e Al$_2$O$_3$ misura 0,63 contro 0,69. Collegamenti corti indicano parti quasi proporzionali.',
    'formula': r'\lVert \mathbf v_i-\mathbf v_j\rVert\approx\operatorname{sd}\Big(\log\frac{x_i}{x_j}\Big)',
    'symbols': r'$\mathbf v_i$ è la punta del raggio della parte $i$ nel biplot di covarianza; l’approssimazione migliora con la '
               r'quota di varianza spiegata dalle due componenti, qui il 98,3\%.'},
   {'tipo': 'scenario', 'titolo': 'Media aritmetica e centro composizionale', 'esperimento': 'm17-centro',
    'ricorda': 'Confrontare media aritmetica e media geometrica chiusa quando una parte è piccola e dispersa.',
    'didascalia': 'Deviazione standard dei logaritmi: 0,3. Seme: 17.',
    'body': r'Il generatore produce centocinquanta composizioni a tre parti attorno al centro (80, 15, 5), con errori '
            r'gaussiani sui logaritmi delle parti. L’istogramma riporta la parte minore con la media aritmetica, linea '
            r'continua, e il centro geometrico chiuso, linea tratteggiata.',
    'formula': r'\operatorname{cen}(X)=\mathcal C\Big[\exp\Big(\tfrac1n\sum_k\log x_{k1}\Big),\ldots,\exp\Big(\tfrac1n\sum_k\log x_{kD}\Big)\Big]',
    'symbols': r'$\mathcal C$ è la chiusura a cento; il centro del generatore è noto per costruzione.'},
   {'tipo': 'confronto', 'titolo': 'Confronto | Media e centro composizionale', 'esperimento': 'm17-centro',
    'ricorda': 'La media aritmetica di una parte asimmetrica si allontana dal centro al crescere della dispersione.',
    'didascalia': r'Deviazione standard dei logaritmi: 0,3 $\to$ 1,2. Tutti gli altri parametri e il seme sono fissi.',
    'righe': [('Centro del generatore, parte 3', 'Centro del generatore, parte 3'),
              ('Media aritmetica, parte 3', 'Media aritmetica, parte 3'),
              ('Centro geometrico, parte 3', 'Centro geometrico chiuso, parte 3'),
              ('Media aritmetica, parte 1', 'Media aritmetica, parte 1'),
              ('Centro geometrico, parte 1', 'Centro geometrico chiuso, parte 1')],
    'body': r'Con dispersione 1,2 la media aritmetica della parte minore sale a 8,25\% e quella della parte maggiore scende a '
            r'69,1\%; il centro geometrico chiuso resta vicino a (80, 15, 5).'},
  ]},
  {'titolo': 'Zeri, limiti di rivelabilità e modelli', 'pagine': [
   {'tipo': 'domanda', 'titolo': 'Uno zero impedisce ogni log-rapporto', 'codice': 'capitolo-06.R',
    'ricorda': 'Prima di trasformare, conta gli zeri e chiarisci da che cosa nascono.',
    'domanda_testo': r'Quanti campioni hanno una parte registrata come zero, e in quali litologie? Uno zero indica '
                     r'un’assenza o una misura sotto il limite?',
    'interpretazione': r'Otto arenarie hanno MgO e sette calcari FeO sotto 0,1\%. Le loro somme vanno da 99,90 a 99,95: gli '
                       r'zeri sono valori piccoli non misurati, e la parte esiste.'},
   {'tipo': 'codice', 'titolo': 'La sostituzione moltiplicativa', 'codice': 'capitolo-07.R',
    'ricorda': 'La sostituzione moltiplicativa conserva i rapporti fra le parti misurate e la somma a cento.',
    'body': r'Josep Antoni Martín-Fernández, Carles Barceló-Vidal e Vera Pawlowsky-Glahn proposero nel 2003 di sostituire '
            r'gli zeri con un valore $\delta$ e di ridurre le parti misurate dello stesso fattore. Nel codice $\delta$ vale '
            r'0,65 volte il limite, una scelta frequente in letteratura; il rapporto SiO$_2$/Al$_2$O$_3$ resta 13,7258 e la '
            r'somma 100.',
    'formula': r'y_j=\begin{cases}\delta & x_j=0\\[2pt] x_j\Big(1-\dfrac{\sum_{k:x_k=0}\delta}{\kappa}\Big) & x_j>0\end{cases}'},
   {'tipo': 'figura', 'titolo': 'Il valore sostitutivo sposta i risultati', 'fig': 'Figure/F06.pdf',
    'ricorda': 'Un risultato che dipende dagli zeri si riporta con la sua sensibilità al valore sostitutivo.',
    'didascalia': r'Media della coordinata clr di MgO nelle 48 arenarie al variare di $\delta$; la linea tratteggiata usa '
                  r'le sole 40 arenarie senza zeri.',
    'body': r'Nelle arenarie la media della coordinata clr di MgO vale $-3{,}39$ con $\delta=0{,}01$, $-3{,}13$ con '
            r'$\delta=0{,}065$ e $-3{,}07$ con $\delta=0{,}1$. Escludere gli otto campioni con lo zero dà $-3{,}01$, un '
            r'valore più alto perché elimina proprio le arenarie più povere di magnesio.',
    'symbols': r'$\delta$ è espresso in percentuale in massa; il limite di rivelabilità è 0,1\%.'},
   {'tipo': 'figura', 'titolo': 'Una composizione come predittore', 'fig': 'Figure/F03.pdf',
    'ricorda': 'In un modello lineare le parti di una composizione entrano attraverso $D-1$ coordinate.',
    'didascalia': r'Densità e bilancio $b_3$ fra SiO$_2$, Al$_2$O$_3$ e MgO, FeO, per litologia.',
    'body': r'Le sei percentuali non possono entrare insieme in una regressione, perché la loro somma è costante. I cinque '
            r'bilanci della partizione sono coordinate libere: il modello della densità con i bilanci spiega il 97,3\% della '
            r'varianza, quello con cinque percentuali il 94,8\%. Il bilancio $b_3$ confronta silicati e ossidi femici.',
    'formula': r'b_3=\log\frac{(x_{\mathrm{SiO_2}}x_{\mathrm{Al_2O_3}})^{1/2}}{(x_{\mathrm{MgO}}x_{\mathrm{FeO}})^{1/2}}'},
   {'tipo': 'codice', 'titolo': 'Interpretare un coefficiente di bilancio', 'codice': 'capitolo-08.R',
    'ricorda': 'Un coefficiente di bilancio descrive l’effetto di un cambiamento relativo fra due gruppi di parti.',
    'body': r'Il codice stima la densità con il bilancio $b_3$ e la litologia. A parità di litologia, un aumento unitario di '
            r'$b_3$ moltiplica per $e\approx2{,}72$ il rapporto fra la media geometrica di silice e allumina e quella degli '
            r'ossidi femici, e corrisponde a una densità più bassa di 0,057 g/cm$^3$.',
    'formula': r'\rho=\beta_0+\beta_1 b_3+\gamma_{\mathrm{Bas}}+\gamma_{\mathrm{Cal}}+\varepsilon'},
   {'tipo': 'scenario', 'titolo': 'Valori sotto il limite e sostituzione', 'esperimento': 'm17-zeri',
    'ricorda': 'Valutare come la sostituzione dei valori sotto il limite sposta la media di un log-rapporto.',
    'didascalia': r'Limite di rivelabilità: 0,1\%; valore sostitutivo 0,65 volte il limite. Seme: 17.',
    'body': r'Il generatore produce duecento composizioni a quattro parti con una traccia di mediana 0,2\%. Le misure della '
            r'traccia sotto il limite diventano zero e vengono sostituite in modo moltiplicativo; il grafico confronta il '
            r'log-rapporto simulato con quello dopo la sostituzione.',
    'formula': r'\bar\ell=\frac1n\sum_{k=1}^n\log\frac{y_{k4}}{y_{k1}}',
    'symbols': r'$y_{k4}$ è la traccia del campione $k$ dopo la sostituzione e $y_{k1}$ la parte maggiore.'},
   {'tipo': 'confronto', 'titolo': 'Confronto | Valori sotto il limite e sostituzione', 'esperimento': 'm17-zeri',
    'ricorda': 'La media dopo la sostituzione dipende dal valore scelto e dalla quota di campioni sotto il limite.',
    'didascalia': r'Limite di rivelabilità: 0,1 $\to$ 0,25\%. Tutti gli altri parametri e il seme sono fissi.',
    'righe': [('Quota sotto il limite', 'Quota sotto il limite'), ('Media simulata', 'Media simulata del log-rapporto'),
              ('Media con sostituzione', 'Media con sostituzione'), ('Media escludendo i campioni', 'Media escludendo i campioni')],
    'body': r'Con il limite a 0,25\% il 62\% dei campioni è sotto il limite. La sostituzione sposta la media da $-5{,}79$ a '
            r'$-5{,}61$; escludere i campioni la porta a $-4{,}96$.'},
  ]},
 ],
 'sintesi': {
  'titolo': 'Dal risultato alla relazione',
  'ricorda': 'Riporta i log-rapporti usati, il trattamento degli zeri e la sensibilità dei risultati.',
  'risultato': r'La correlazione di $-0{,}92$ fra SiO$_2$ e CaO nasce soprattutto dal confronto fra arenarie e calcari e dal '
               r'vincolo della somma: nei basalti vale 0,07. I log-rapporti descrivono le relazioni fra le parti senza '
               r'dipendere dalla chiusura, e la densità dipende dal bilancio fra silicati e ossidi femici.',
  'limiti': r'I campioni sono sintetici, generati con errori indipendenti sui logaritmi. Le quindici misure sotto il limite '
            r'sono sostituite con un valore convenzionale, e le stime che le coinvolgono vanno lette con la loro sensibilità '
            r'a $\delta$.'},
 'riferimenti': {
  'titolo': 'Fonti, dati e codice per riprodurre le figure',
  'ricorda': 'I risultati numerici si riferiscono ai dati e alle ipotesi dichiarate nel caso.',
  'fonti': r'K. Pearson, Proceedings of the Royal Society of London 60, 489–498, 1897.\par '
           r'F. Chayes, Journal of Geophysical Research 65(12), 4185–4193, 1960.\par '
           r'J. Aitchison, Journal of the Royal Statistical Society B 44(2), 139–160, 1982.\par '
           r'J. Aitchison e M. Greenacre, Applied Statistics 51(4), 375–392, 2002.\par '
           r'J. J. Egozcue e colleghi, Mathematical Geology 35(3), 279–300, 2003.\par '
           r'J. J. Egozcue e V. Pawlowsky-Glahn, Mathematical Geology 37(7), 795–828, 2005.\par '
           r'J. A. Martín-Fernández, C. Barceló-Vidal e V. Pawlowsky-Glahn, Mathematical Geology 35(3), 253–278, 2003.',
  'dati': r'Dati sintetici del corso (composizioni\_v1.csv), generati da R/genera\_dati.R. Codice contiene i frammenti delle '
          r'pagine; R/M17\_figure.R ricostruisce figure e valori; Esperimenti contiene i programmi dei due scenari e '
          r'Diagrammi i disegni TikZ.'},
}
