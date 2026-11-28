# Specifica della lezione Azimut (M18): dati direzionali. Valori da R/M18_figure.R, Codice/ e Esperimenti/.
LEZIONE = {
 'planet': 'Azimut',
 'title': 'Dati direzionali',
 'copertina': {'titolo': r'Dati\\direzionali', 'sottotitolo': 'Angoli che si chiudono su sé stessi',
               'riga': 'Medie circolari, von Mises, assi e direzioni nello spazio'},
 'percorso': r'Centoventi azimut di paleocorrenti, centodieci direzioni di fratture, quattordici direzioni '
             r'paleomagnetiche e sessanta giaciture di strati descrivono quattro modi di misurare un orientamento. Il '
             r'percorso parte dalla media di angoli sul cerchio, introduce un modello e un test, tratta le linee senza '
             r'verso e chiude con le direzioni nello spazio.',
 'caso': {
  'domanda': 'Le paleocorrenti erano dirette verso 202,5 gradi?',
  'ricorda': 'Un azimut è un punto su un cerchio: la sua scala numerica ha un inizio arbitrario.',
  'body': r'In sei stazioni di un’unità fluviale sintetica sono stati misurati venti azimut di immersione delle lamine '
          r'oblique, in gradi da nord in senso orario. La media aritmetica dei centoventi valori è 202,5 gradi. Il caso '
          r'comprende anche centodieci tracce di fratture, quattordici colate con direzione di magnetizzazione nota e '
          r'sessanta giaciture di strati piegati.',
  'info': r'Seguiremo i dati dalle medie circolari alla distribuzione di von Mises e al test di Rayleigh, poi agli angoli '
          r'raddoppiati per le fratture e alla geometria delle direzioni nello spazio.'},
 'capitoli': [
  {'titolo': 'Angoli e direzioni medie', 'pagine': [
   {'tipo': 'domanda', 'titolo': 'Dove punta la media degli azimut?', 'codice': 'capitolo-01.R',
    'ricorda': 'La media aritmetica di angoli dipende dalla posizione dello zero della scala.',
    'domanda_testo': r'Le lamine oblique immergono per lo più fra nord-ovest e nord-est. Che cosa rappresenta la media '
                     r'aritmetica dei loro azimut, e quale grandezza descrive la direzione prevalente?',
    'interpretazione': r'La media aritmetica vale 202,5 gradi e punta verso sud-sud-ovest, dove quasi nessuna lamina '
                       r'immerge. La direzione media circolare vale 352,4 gradi: le misure vicine a 350 e quelle vicine a '
                       r'10 gradi sono direzioni contigue.'},
   {'tipo': 'schema', 'titolo': 'La direzione media è quella della risultante', 'diag': 'Diagrammi/D01.tex',
    'ricorda': 'Ogni misura diventa un vettore unitario; la direzione media è quella della loro somma.',
    'didascalia': 'Due misure a 350 e a 10 gradi, la loro risultante e la media aritmetica.',
    'body': r'Ogni azimut $\theta_i$ corrisponde al vettore unitario $(\cos\theta_i,\sin\theta_i)$. La somma dei vettori '
            r'ha una direzione che non dipende dallo zero della scala, e il suo modulo diviso per $n$ è la lunghezza media '
            r'risultante $\bar R$: vale 1 se tutte le misure coincidono e si avvicina a 0 quando le direzioni si compensano. '
            r'Joseph Curray applicò nel 1956 questa media vettoriale alle orientazioni geologiche.',
    'formula': r'\bar\theta=\operatorname{atan2}\big(\bar S,\bar C\big),\qquad \bar R=\sqrt{\bar C^2+\bar S^2}',
    'symbols': r'$\bar C$ e $\bar S$ sono le medie di $\cos\theta_i$ e $\sin\theta_i$; la funzione atan2 restituisce '
               r'l’angolo nel quadrante corretto.'},
   {'tipo': 'figura', 'titolo': 'La rosa a settori di uguale area', 'fig': 'Figure/F01.pdf', 'h': '6.3cm',
    'ricorda': 'In una rosa il raggio di ogni settore va preso proporzionale alla radice della frequenza.',
    'didascalia': r'Centoventi azimut in classi di 15 gradi; le frecce indicano la direzione media e la media aritmetica.',
    'body': r'La rosa è l’istogramma di dati circolari. Se il raggio di un settore cresce con la frequenza, la sua area cresce '
            r'con il quadrato e la classe modale appare esagerata: Wojciech Nemec lo osservò nel 1988, e David Sanderson e '
            r'David Peacock hanno ripreso il problema nel 2020. Qui il raggio è proporzionale alla radice della frequenza. '
            r'La lunghezza media risultante dei centoventi azimut è 0,756.',
    'symbols': r'Come per un istogramma, la forma della rosa dipende dall’ampiezza e dall’origine delle classi.'},
   {'tipo': 'codice', 'titolo': 'Direzione, concentrazione e dispersione per stazione', 'codice': 'capitolo-02.R',
    'ricorda': 'La deviazione standard circolare si ricava da $\\bar R$ e si esprime in gradi.',
    'body': r'Per ogni stazione il codice calcola direzione media, lunghezza media risultante e deviazione standard '
            r'circolare. Cinque stazioni hanno $\bar R$ fra 0,82 e 0,95 e direzioni fra 349 e 14 gradi. La stazione S6 ha '
            r'$\bar R=0{,}31$ e una deviazione standard di 88 gradi: le sue direzioni sono molto disperse. La varianza '
            r'circolare $1-\bar R$ vale 0,244 per l’insieme delle misure.',
    'formula': r'\sigma_c=\sqrt{-2\log\bar R}'},
   {'tipo': 'scenario', 'titolo': 'Media aritmetica e direzione media', 'esperimento': 'm18-media',
    'ricorda': 'Confrontare le due medie quando la direzione del generatore si avvicina allo zero della scala.',
    'didascalia': 'Direzione del generatore: 90 gradi; concentrazione 2. Seme: 17.',
    'body': r'L’esperimento genera sessanta azimut da una distribuzione di von Mises con direzione $\mu$ e concentrazione '
            r'$\kappa$. L’istogramma riporta la media aritmetica, linea continua, e la direzione media circolare, linea '
            r'tratteggiata. Con $\mu=90^\circ$ le due medie distano 11 gradi.',
    'formula': r'\bar\theta=\operatorname{atan2}\Big(\frac1n\sum_i\sin\theta_i,\ \frac1n\sum_i\cos\theta_i\Big)',
    'symbols': r'Lo scarto della media aritmetica cresce con la quota di misure che superano lo zero della scala.'},
   {'tipo': 'confronto', 'titolo': 'Confronto | Media aritmetica e direzione media', 'esperimento': 'm18-media',
    'ricorda': 'La direzione media non cambia se si sposta l’origine della scala; la media aritmetica sì.',
    'didascalia': r'Direzione del generatore: 90 $\to$ 355 gradi. Tutti gli altri parametri e il seme sono fissi.',
    'righe': [('Direzione del generatore', 'Direzione del generatore'),
              ('Media aritmetica', 'Media aritmetica degli azimut'),
              ('Direzione media circolare', 'Direzione media circolare'),
              ('Scarto della media aritmetica', 'Scarto della media aritmetica'),
              (r'$\bar R$', 'Lunghezza media risultante')],
    'body': r'Con lo stesso seme i due scenari hanno le stesse direzioni ruotate di 265 gradi: $\bar R$ e lo scarto della '
            r'direzione media restano uguali, lo scarto della media aritmetica sale a 162 gradi.'},
  ]},
  {'titolo': 'La distribuzione di von Mises', 'pagine': [
   {'tipo': 'figura', 'titolo': 'Un modello per direzioni concentrate', 'fig': 'Figure/F02.pdf',
    'ricorda': 'La von Mises ha lo stesso ruolo della normale per i dati circolari: due parametri, $\\mu$ e $\\kappa$.',
    'didascalia': r'Densità di von Mises per tre valori della concentrazione $\kappa$.',
    'body': r'Richard von Mises introdusse nel 1918 una distribuzione sul cerchio con direzione media $\mu$ e concentrazione '
            r'$\kappa$. Con $\kappa=0$ la distribuzione è uniforme; al crescere di $\kappa$ la densità si raccoglie attorno '
            r'a $\mu$ e per valori grandi si avvicina a una normale con varianza $1/\kappa$. La costante $I_0$ è la funzione '
            r'di Bessel modificata di ordine zero.',
    'formula': r'f(\theta)=\frac{e^{\kappa\cos(\theta-\mu)}}{2\pi I_0(\kappa)},\qquad 0\le\theta<2\pi'},
   {'tipo': 'codice', 'titolo': 'Stimare la concentrazione', 'codice': 'capitolo-03.R',
    'ricorda': 'La stima di massima verosimiglianza di $\\kappa$ risolve $A_1(\\kappa)=\\bar R$.',
    'body': r'La stima di massima verosimiglianza di $\mu$ è la direzione media; quella di $\kappa$ si ottiene uguagliando '
            r'il rapporto fra due funzioni di Bessel alla lunghezza media risultante. Il codice risolve l’equazione per '
            r'ogni stazione: S2 ha $\hat\kappa=10{,}84$, S6 soltanto 0,64. Per l’insieme delle misure $\hat\kappa$ vale 2,42.',
    'formula': r'A_1(\kappa)=\frac{I_1(\kappa)}{I_0(\kappa)}=\bar R',
    'symbols': r'Con poche misure e $\bar R$ piccolo la stima di $\kappa$ è distorta verso l’alto.'},
   {'tipo': 'domanda', 'titolo': 'Le direzioni di S6 hanno una direzione preferenziale?', 'codice': 'capitolo-04.R',
    'ricorda': 'Il test di Rayleigh confronta $\\bar R$ con i valori attesi da direzioni uniformi.',
    'domanda_testo': r'In S1 venti lamine hanno $\bar R=0{,}86$, in S6 venti lamine hanno $\bar R=0{,}31$. Con venti misure, '
                     r'quale valore di $\bar R$ potrebbe nascere da direzioni distribuite in modo uniforme?',
    'interpretazione': r'Per S1 la statistica $Z$ vale 14,8 e la probabilità di coda è inferiore a $10^{-4}$. Per S6 $Z=1{,}87$ '
                       r'e $p=0{,}155$: i dati di S6 sono compatibili con l’uniformità.'},
   {'tipo': 'figura', 'titolo': 'Il test di Rayleigh nelle sei stazioni', 'fig': 'Figure/F03.pdf',
    'ricorda': 'Con $n$ fissato, il test di Rayleigh equivale a confrontare $\\bar R$ con una soglia.',
    'didascalia': r'Lunghezza media risultante per stazione; linea tratteggiata: valore critico 0,385 per $n=20$ al 5\%.',
    'body': r'Lord Rayleigh studiò nel 1880 la somma di vibrazioni con fasi casuali, il problema da cui deriva il test. Sotto '
            r'l’ipotesi di uniformità $2n\bar R^2$ segue approssimativamente una chi quadrato con due gradi di libertà; per '
            r'campioni piccoli il codice della pagina precedente usa una correzione. Con venti misure la soglia al 5\% è $\bar R=0{,}385$: '
            r'una simulazione di ventimila campioni uniformi dà 0,381.',
    'formula': r'Z=n\bar R^2,\qquad 2Z\approx\chi^2_2'},
   {'tipo': 'testo', 'titolo': 'Che cosa dice un test di uniformità',
    'ricorda': 'Un $p$ grande descrive dati compatibili con l’uniformità; la potenza dice quanto il test poteva vedere.',
    'sinistra': {'label': 'Alternative unimodali', 'body': r'Il test di Rayleigh è costruito contro un’alternativa con una sola '
                 r'direzione preferenziale. Lamine oblique di ambiente tidale, con correnti di flusso e riflusso opposte, '
                 r'producono distribuzioni bimodali con modi a 180 gradi: la risultante si annulla e $\bar R$ resta piccolo '
                 r'anche se le direzioni sono concentrate. Per queste distribuzioni si usano gli angoli raddoppiati del '
                 r'capitolo successivo.'},
    'destra': {'label': 'Il caso di S6', 'body': r'Con venti misure il test ha potenza bassa per concentrazioni piccole: '
               r'se le lamine di S6 seguissero una von Mises con $\kappa=0{,}64$, il test respingerebbe l’uniformità in '
               r'circa quattro campioni su dieci. Il risultato di S6 indica direzioni molto disperse, e la direzione media '
               r'di 309 gradi va riportata con la sua incertezza, oppure omessa.',
               'symbols': r'La potenza è la probabilità di respingere l’uniformità quando i dati hanno una direzione preferenziale.'}},
   {'tipo': 'scenario', 'titolo': 'Potenza del test di Rayleigh', 'esperimento': 'm18-rayleigh',
    'ricorda': 'Stimare con una simulazione la probabilità che il test riconosca una direzione preferenziale.',
    'didascalia': 'Concentrazione 0,3; venti misure; quattrocento campioni per ipotesi. Seme: 17.',
    'body': r'L’esperimento simula quattrocento campioni da una von Mises e quattrocento da una distribuzione uniforme, con '
            r'lo stesso $n$. L’istogramma confronta le due distribuzioni di $\bar R$ con il valore critico; la potenza è la '
            r'quota di campioni von Mises con $p<0{,}05$.',
    'formula': r'\text{potenza}=P\big(p<0{,}05\mid\kappa,n\big)',
    'symbols': r'La quota di rifiuti con dati uniformi controlla il livello del test, atteso al 5\%.'},
   {'tipo': 'confronto', 'titolo': 'Confronto | Potenza del test di Rayleigh', 'esperimento': 'm18-rayleigh',
    'ricorda': 'Con venti misure il test riconosce una direzione preferenziale soltanto se la concentrazione è sufficiente.',
    'didascalia': r'Concentrazione: 0,3 $\to$ 1. Tutti gli altri parametri e il seme sono fissi.',
    'righe': [('Potenza stimata', 'Potenza stimata'), ('Rifiuti con dati uniformi', 'Quota di rifiuti con dati uniformi'),
              (r'Valore critico di $\bar R$', 'Valore critico di R'), (r'$\bar R$ medio, von Mises', 'R medio sotto von Mises')],
    'body': r'Con $\kappa=0{,}3$ la potenza è 0,113, poco sopra il livello; con $\kappa=1$ sale a 0,748. In entrambi gli '
            r'scenari la quota di rifiuti con dati uniformi resta vicina a 0,05.'},
  ]},
  {'titolo': 'Dati assiali', 'pagine': [
   {'tipo': 'schema', 'titolo': 'Una linea non ha verso', 'diag': 'Diagrammi/D02.tex',
    'ricorda': 'Per dati assiali si raddoppiano gli angoli, si calcola la media e si divide per due.',
    'didascalia': 'La traccia di una frattura e il suo angolo raddoppiato.',
    'body': r'La traccia di una frattura, un asse di piega o l’allungamento di un ciottolo sono linee: 40 e 220 gradi '
            r'descrivono lo stesso oggetto. Raddoppiando gli angoli le due estremità coincidono, e i metodi per direzioni '
            r'si applicano agli angoli $2\theta_i$. L’asse medio è metà della loro direzione media, fra 0 e 180 gradi.',
    'formula': r'\bar\theta_{\mathrm{asse}}=\tfrac12\operatorname{atan2}\big(\bar S_2,\bar C_2\big)',
    'symbols': r'$\bar C_2$ e $\bar S_2$ sono le medie di $\cos2\theta_i$ e $\sin2\theta_i$.'},
   {'tipo': 'codice', 'titolo': 'La famiglia J1 prima e dopo il raddoppio', 'codice': 'capitolo-05.R',
    'ricorda': 'Un $\\bar R$ vicino a zero può nascere da estremità registrate a caso.',
    'body': r'Le settanta fratture della famiglia J1 sono annotate con l’una o l’altra estremità. Gli angoli registrati '
            r'hanno $\bar R=0{,}036$, un valore che suggerirebbe direzioni uniformi. Gli angoli raddoppiati hanno '
            r'$\bar R_2=0{,}930$ e l’asse medio è 42,6 gradi: la famiglia è fortemente orientata.',
    'formula': r'\bar R_2=\Big|\frac1n\sum_i\big(\cos2\theta_i,\ \sin2\theta_i\big)\Big|'},
   {'tipo': 'figura', 'titolo': 'Due famiglie di fratture', 'fig': 'Figure/F04.pdf',
    'ricorda': 'Una rosa assiale riporta ogni misura alle due estremità della linea.',
    'didascalia': 'Rosa assiale a settori di uguale area delle 110 fratture, in classi di 10 gradi, per famiglia.',
    'body': r'La rosa mostra due famiglie. J1, settanta misure, ha asse medio 42,6 gradi; J2, quaranta misure, ha asse '
            r'132,0 gradi e $\bar R_2=0{,}871$. Gli assi delle due famiglie formano un angolo di 89,4 gradi. La rosa è '
            r'simmetrica per costruzione, perché ogni linea compare due volte.',
    'symbols': r'L’attribuzione alle famiglie proviene dal rilievo di campagna, per esempio dai rapporti di intersezione.'},
   {'tipo': 'testo', 'titolo': 'Riassumere prima di separare le famiglie',
    'ricorda': 'Due famiglie ortogonali diventano opposte negli angoli raddoppiati.',
    'sinistra': {'label': 'Famiglie ortogonali', 'body': r'Il raddoppio trasforma una differenza di 90 gradi fra assi in una '
                 r'differenza di 180 gradi fra angoli raddoppiati. Le due famiglie del caso, prese insieme, hanno '
                 r'$\bar R_2=0{,}275$ e un asse medio di 43,3 gradi: il valore descrive J1, la famiglia più numerosa, e la '
                 r'concentrazione risulta molto più bassa di quella di ciascuna famiglia.',
                 'formula': r'2(\theta+90^\circ)=2\theta+180^\circ'},
    'destra': {'label': 'Separare prima di riassumere', 'body': r'Un asse medio e una concentrazione hanno senso per una '
               r'distribuzione unimodale. Con più famiglie si riassume ciascuna dopo averle separate con criteri di '
               r'campagna o con un modello a miscela di distribuzioni di von Mises sugli angoli raddoppiati. La rosa '
               r'assiale è il primo controllo della forma della distribuzione.',
               'symbols': r'Le stesse considerazioni valgono per assi di pieghe, lineazioni e orientazioni di clasti.'}},
   {'tipo': 'scenario', 'titolo': 'Angoli raddoppiati e famiglie di fratture', 'esperimento': 'm18-assiali',
    'ricorda': 'Osservare il raddoppio degli angoli con una famiglia e con due famiglie.',
    'didascalia': 'Una famiglia a 40 gradi; concentrazione degli angoli raddoppiati 6. Seme: 17.',
    'body': r'L’esperimento genera cento direzioni attorno a una famiglia a 40 gradi e registra ogni misura con '
            r'un’estremità scelta a caso. Con un angolo fra le famiglie maggiore di zero, metà delle misure forma una '
            r'seconda famiglia. La rosa assiale ha settori di uguale area.',
    'formula': r'\bar R_2=\Big|\frac1n\sum_k e^{2\mathrm{i}\theta_k}\Big|',
    'symbols': r'La notazione $e^{\mathrm{i}\theta_k}$ indica il vettore unitario $(\cos\theta_k,\sin\theta_k)$.'},
   {'tipo': 'confronto', 'titolo': 'Confronto | Angoli raddoppiati e famiglie', 'esperimento': 'm18-assiali',
    'ricorda': 'Il raddoppio risolve l’ambiguità delle estremità; la multimodalità resta da trattare.',
    'didascalia': r'Angolo fra le famiglie: 0 $\to$ 90 gradi. Tutti gli altri parametri e il seme sono fissi.',
    'righe': [(r'$\bar R$ degli angoli registrati', 'R degli angoli registrati'),
              (r'$\bar R_2$ degli angoli raddoppiati', 'R degli angoli raddoppiati'),
              ('Asse medio (gradi)', 'Asse medio (gradi)'), ('Angolo fra le famiglie', 'Angolo fra le famiglie (gradi)')],
    'body': r'Con una famiglia $\bar R_2$ vale 0,901 e l’asse medio 39,3 gradi. Con due famiglie a 90 gradi $\bar R_2$ scende '
            r'a 0,060 e l’asse medio di 173 gradi non descrive nessuna delle due.'},
  ]},
  {'titolo': 'Direzioni nello spazio', 'pagine': [
   {'tipo': 'schema', 'titolo': 'Coordinate e proiezione equivalente', 'diag': 'Diagrammi/D03.tex', 'scala': '0.97',
    'ricorda': 'Nella proiezione equivalente aree uguali sulla sfera restano uguali nel piano.',
    'didascalia': 'Sezione verticale dell’emisfero inferiore attraverso la direzione $OP$.',
    'body': r'Una direzione nello spazio è data da un azimut, la declinazione $D$, e da un’inclinazione $I$ sotto '
            r'l’orizzontale. I suoi coseni direttori sono le componenti verso nord, est e il basso. La proiezione '
            r'equivalente di Lambert, il reticolo di Schmidt dei geologi, rappresenta l’emisfero inferiore conservando le '
            r'aree: la densità dei punti nel piano rispecchia quella sulla sfera.',
    'formula': r'\mathbf x=(\cos I\cos D,\ \cos I\sin D,\ \sin I)'},
   {'tipo': 'codice', 'titolo': 'La media di Fisher delle quattordici colate', 'codice': 'capitolo-06.R',
    'ricorda': 'La direzione media nello spazio è quella della somma dei vettori unitari, come nel piano.',
    'body': r'Ronald Fisher propose nel 1953 una distribuzione per direzioni disperse attorno a una media, discutendo dati '
            r'paleomagnetici. La direzione media delle colate ha $D=344{,}8^\circ$ e $I=59{,}0^\circ$; la risultante '
            r'misura 13,73 su 14 e la concentrazione stimata è $k=(N-1)/(N-R)=47{,}3$. Il cono di confidenza al 95\% ha semiangolo '
            r'5,84 gradi; l’approssimazione $140/\sqrt{kN}$ dà 5,44.',
    'formula': r'\cos\alpha_{95}=1-\frac{N-R}{R}\Big(20^{1/(N-1)}-1\Big)'},
   {'tipo': 'figura', 'titolo': 'Le colate sul reticolo equivalente', 'fig': 'Figure/F05.pdf',
    'ricorda': 'Il cono $\\alpha_{95}$ è una regione di confidenza al 95\\% per la direzione media, se il modello di Fisher è adeguato.',
    'didascalia': r'Particolare della proiezione equivalente, emisfero inferiore, con linee di uguale declinazione e '
                  r'cerchi di uguale inclinazione.',
    'body': r'I quattordici punti sono le direzioni delle colate; il quadrato è la media di Fisher e il cerchio il cono '
            r'$\alpha_{95}$. L’asterisco è la direzione del campo di un dipolo assiale geocentrico alla latitudine del '
            r'sito, 42 gradi nord: declinazione 0, inclinazione 60,96 gradi. L’asterisco cade fuori dal cono.',
    'symbols': r'Nel paleomagnetismo $N$ conta le colate, perché ogni colata registra un istante del campo.'},
   {'tipo': 'domanda', 'titolo': 'Il sito ha ruotato attorno a un asse verticale?', 'codice': 'capitolo-07.R',
    'ricorda': 'Per un dipolo assiale geocentrico l’inclinazione dipende soltanto dalla latitudine.',
    'domanda_testo': r'Per un dipolo assiale geocentrico $\tan I=2\tan\lambda$ e la declinazione è zero. La direzione media '
                     r'delle colate è compatibile con il campo atteso alla latitudine del sito?',
    'interpretazione': r'L’inclinazione attesa è 60,96 gradi e la direzione attesa dista 7,83 gradi dalla media, più del '
                       r'raggio del cono. La declinazione di 344,8 gradi suggerisce una rotazione antioraria di circa 15 '
                       r'gradi, da confermare con altri siti.'},
   {'tipo': 'figura', 'titolo': 'I poli degli strati descrivono una cintura', 'fig': 'Figure/F06.pdf',
    'ricorda': 'In una piega cilindrica i poli degli strati giacciono su un cerchio massimo normale all’asse.',
    'didascalia': 'Poli dei sessanta strati, cerchio massimo meglio adattato e asse della piega.',
    'body': r'I poli della stratificazione si dispongono lungo un cerchio massimo: i due fianchi formano due gruppi e la '
            r'cerniera li collega. La loro lunghezza media risultante, 0,64, rende la media di Fisher poco informativa. '
            r'L’asse della piega è la direzione normale al cerchio massimo meglio adattato ai poli.',
    'symbols': r'I poli sono assi: il segno del vettore non conta, e il loro riassunto usa prodotti $\mathbf x\mathbf x^{\mathsf T}$.'},
   {'tipo': 'codice', 'titolo': 'Il tensore di orientazione e l’asse della piega', 'codice': 'capitolo-08.R',
    'ricorda': 'Autovalori del tensore di orientazione: forma della distribuzione; autovettori: direzioni principali.',
    'body': r'Il tensore di orientazione è la media dei prodotti $\mathbf x_i\mathbf x_i^{\mathsf T}$ e tratta allo stesso '
            r'modo un polo e il suo opposto. Gli autovalori valgono 0,564, 0,422 e 0,014: l’ultimo, quasi nullo, indica una '
            r'cintura. L’autovettore corrispondente fornisce l’asse della piega, 298 gradi con immersione di 16 gradi. '
            r'Nigel Woodcock propose nel 1977 il parametro $K$, qui 0,086: valori minori di 1 indicano cinture.',
    'formula': r'T=\frac1n\sum_i\mathbf x_i\mathbf x_i^{\mathsf T},\qquad K=\frac{\log(S_1/S_2)}{\log(S_2/S_3)}'},
   {'tipo': 'scenario', 'titolo': 'Cono di confidenza di Fisher', 'esperimento': 'm18-fisher',
    'ricorda': 'Osservare come il cono di confidenza si restringe al crescere del numero di direzioni.',
    'didascalia': 'Otto direzioni; concentrazione 30. Seme: 17.',
    'body': r'L’esperimento genera $N$ direzioni da una distribuzione di Fisher attorno a una direzione vera con '
            r'declinazione 0 e inclinazione 60 gradi. Il grafico riporta le direzioni, il cono $\alpha_{95}$ attorno alla '
            r'media stimata e la direzione vera.',
    'formula': r'\alpha_{95}\approx\frac{140^\circ}{\sqrt{kN}}',
    'symbols': r'$k$ è stimato dai dati simulati; il valore del generatore è fissato dal controllo.'},
   {'tipo': 'confronto', 'titolo': 'Confronto | Cono di confidenza di Fisher', 'esperimento': 'm18-fisher',
    'ricorda': 'Il cono si restringe circa come $1/\\sqrt N$; con poche direzioni l’approssimazione lo sottostima.',
    'didascalia': r'Numero di direzioni: 8 $\to$ 30. Tutti gli altri parametri e il seme sono fissi.',
    'righe': [(r'$\alpha_{95}$ (gradi)', 'alfa95 (gradi)'), (r'$140/\sqrt{kN}$ (gradi)', 'Approssimazione 140/radice(kN) (gradi)'),
              (r'$k$ stimato', 'k stimato'), ('Distanza dalla direzione vera', 'Distanza dalla direzione vera (gradi)')],
    'body': r'Con otto direzioni $\alpha_{95}$ vale 9,84 gradi e l’approssimazione 8,66; con trenta direzioni i due valori '
            r'sono 5,40 e 5,15. In entrambi i casi la direzione vera cade dentro il cono.'},
  ]},
 ],
 'sintesi': {
  'titolo': 'Dal risultato alla relazione',
  'ricorda': 'Riporta direzione media, $\\bar R$ o $k$, numero di misure e cono di confidenza.',
  'risultato': r'Le paleocorrenti hanno direzione media di 352,4 gradi, verso nord: la media aritmetica di 202,5 gradi '
               r'nasce dalla posizione dello zero della scala. Cinque stazioni hanno una direzione preferenziale netta; S6 è '
               r'compatibile con l’uniformità. Le fratture formano due famiglie quasi ortogonali, le colate suggeriscono una '
               r'rotazione antioraria di circa 15 gradi e la piega ha asse 298/16.',
  'limiti': r'I dati sono sintetici. Il test di Rayleigh e il cono di Fisher presuppongono misure indipendenti e '
            r'distribuzioni unimodali e simmetriche; con venti misure per stazione la potenza è bassa per concentrazioni '
            r'piccole, e una sola località paleomagnetica non basta a stabilire una rotazione.'},
 'riferimenti': {
  'titolo': 'Fonti, dati e codice per riprodurre le figure',
  'ricorda': 'I risultati numerici si riferiscono ai dati e alle ipotesi dichiarate nel caso.',
  'fonti': r'Lord Rayleigh, Philosophical Magazine 10(60), 73–78, 1880.\par '
           r'R. A. Fisher, Proceedings of the Royal Society of London A 217, 295–305, 1953.\par '
           r'J. R. Curray, Journal of Geology 64(2), 117–131, 1956.\par '
           r'N. H. Woodcock, Geological Society of America Bulletin 88, 1231–1236, 1977.\par '
           r'D. J. Best e N. I. Fisher, Applied Statistics 28(2), 152–157, 1979.\par '
           r'W. Nemec, Sedimentary Geology 59, 149–152, 1988.\par '
           r'R. F. Butler, Paleomagnetism: Magnetic Domains to Geologic Terranes, Blackwell, 1992.\par '
           r'N. I. Fisher, Statistical Analysis of Circular Data, Cambridge University Press, 1993.\par '
           r'K. V. Mardia e P. E. Jupp, Directional Statistics, Wiley, 2000.\par '
           r'D. J. Sanderson e D. C. P. Peacock, Earth-Science Reviews 201, 103055, 2020.',
  'dati': r'Dati sintetici del corso (correnti\_v1.csv, fratture\_v1.csv, paleomag\_v1.csv, strati\_v1.csv), generati da '
          r'R/genera\_dati.R. Codice contiene i frammenti delle pagine; R/M18\_figure.R ricostruisce figure e valori; '
          r'Esperimenti contiene i programmi dei due scenari e Diagrammi i disegni TikZ.'},
}
