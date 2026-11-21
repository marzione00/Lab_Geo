"""Associazione spaziale e semivarianza: pagine 56–81."""
from componenti import *

slide(56,'Valori vicini possono essere simili o dissimili',
 grid('neighbors')+
 eq(r'v_i=z_i-\bar z,\qquad v_iv_j\gtrless0'),
 p(r'Due scarti con lo stesso segno producono un contributo positivo. Scarti di segno opposto producono un contributo negativo.')+
 info(r'Un indice globale combina questi contributi sui collegamenti del grafo. Può riassumere una struttura forte senza descrivere ogni singola zona.')+
 p(r'Per interpretarlo servono sia i pesi sia un termine di confronto per il valore osservato.'),
 r'L’associazione spaziale riguarda l’accoppiamento dei valori nei siti collegati.', source=[16])

slide(57,'Moran I: la formula e i suoi ingredienti',
 eq(r'I_H=\frac{n}{S_0}\frac{\sum_i\sum_jh_{ij}(z_i-\bar z)(z_j-\bar z)}{\sum_i(z_i-\bar z)^2}')+
 eq(r'S_0=\sum_i\sum_jh_{ij},\qquad h_{ii}=0')+
 table(['Ingrediente','Ruolo'],[
 [r'$v^\top Hv$','Somma pesata dei prodotti fra scarti'],
 [r'$v^\top v$','Variabilità complessiva dei valori'],
 [r'$n/S_0$','Normalizzazione del peso totale']], [3.0,6.0]),
 p(r'H indica la matrice scelta: A binaria oppure W normalizzata. La variabile deve avere variabilità non nulla e il peso totale deve essere positivo.')+
 info(r'Moran I non è in generale un coefficiente di correlazione limitato a $[-1,1]$. I suoi limiti dipendono dalla matrice e dal dominio ammesso.')+
 sm(r'La definizione dell’indice e il riferimento inferenziale sono due passaggi distinti.'),
 r'Il nome della statistica non sostituisce la specificazione dei pesi.', notebook=13, source=[16,17])

slide(58,'Il calcolo esplicito rende visibili i pesi',
 eq(r'I_A=\frac{64}{224}\frac{v^\top Av}{v^\top v}')+
 eq(r'I_W=\frac{v^\top Wv}{v^\top v}\quad\text{se tutte le somme di riga sono 1}')+
 info(r'Nel caso guida $S_0(A)=224$ e $S_0(W)=64$. L’autocontributo è escluso dalla diagonale nulla.'),
 p(r'Calcoliamo l’indice sia con il prodotto matriciale sia con la somma dei prodotti. Le due implementazioni devono coincidere a tolleranza numerica.')+
 p(r'Il notebook N13 conserva la versione binaria del laboratorio originale. La versione di riga è un confronto esplicito.'),
 r'Confrontare due implementazioni della stessa formula aiuta a riconoscere errori di normalizzazione.',
 code('v <- z-mean(z)\nI_A <- n/sum(A)*sum(A*outer(v,v))/\n       sum(v^2)\nI_W <- drop(t(v)%*%W%*%v)/sum(v^2)\nc(binaria=I_A,riga=I_W)','R · Moran con A e W'), notebook=13, source=[17])

slide(59,'Pesi differenti producono indici differenti',
 fig('18_Moran_confronto',r'Confronto degli indici calcolati sugli stessi 64 siti con matrice binaria e normalizzazione di riga.'),
 p(r'Il calcolo restituisce $I_A='+value('Moran','I_A')+r'$ e $I_W='+value('Moran','I_W')+r'$. Entrambi sono positivi: tendono a essere collegati scarti dello stesso segno.')+
 info(r'La differenza fra i due indici non è un errore di calcolo. I siti con gradi diversi ricevono contributi differenti.')+
 p(r'Per stabilire quanto un valore sia insolito, occorre confrontarlo con un riferimento costruito usando gli stessi pesi.'),
 r'Un indice di associazione è inseparabile dalla matrice con cui è stato calcolato.', notebook=13, source=[16,17])

slide(60,'Lo scatter di Moran usa il ritardo spaziale',
 fig('19_Moran_scatter',r'Ascissa: $v=z-\bar z$; ordinata: $Wv$. La pendenza della regressione con intercetta è $I_W$.'),
 p(r'Il grafico confronta lo scarto del sito con la media pesata degli scarti dei suoi vicini.')+
 info(r'Poiché la media di v è zero, la pendenza coincide con $v^\top Wv/v^\top v$. La media di $Wv$ può non essere zero: W non è necessariamente doppiamente stocastica.'),
 r'La pendenza dello scatter coincide con l’indice basato sugli stessi pesi di riga.',
 code('lag_v <- drop(W%*%v)\nbeta_scatter <- unname(coef(\n lm(lag_v~v))[2])\nstopifnot(abs(beta_scatter-I_W)\n          <1e-12)','R · verificare la pendenza'), notebook=13, source=[18])

slide(61,'I quadranti descrivono configurazioni locali',
 fig('20_quadranti',r'La classificazione usa il segno dello scarto e del ritardo. È descrittiva.'),
 p(r'Due segni positivi descrivono un valore alto con vicini mediamente alti; due segni negativi indicano basso con basso. Segni opposti descrivono un contrasto fra sito e vicinato.')+
 info(r'Un quadrante non è un test locale. Per inferenze sito per sito servono una statistica locale, un riferimento appropriato e attenzione ai confronti multipli.')+
 p(r'Alto e basso si riferiscono alla media globale. Non indicano soglie scientifiche esterne.'),
 r'Una classificazione descrittiva dei siti non equivale a una mappa di significatività.', source=[18])

slide(62,'Moran è invariante a traslazione e scala',
 eq(r'z^\star=a+bz,\qquad b\ne0\quad\Longrightarrow\quad I_H(z^\star)=I_H(z)')+
 info(r'Gli scarti vengono moltiplicati per b. Numeratore e denominatore sono quindi moltiplicati per $b^2$.'),
 p(r'Cambiare l’unità con una trasformazione affine non cambia l’indice. Una trasformazione non lineare può invece modificarlo.')+
 p(r'Questa proprietà non rende irrilevanti le unità per tutte le analisi: semivarianze, errori e soglie scientifiche mantengono unità proprie.'),
 r'L’invarianza di una statistica non si estende automaticamente a tutte le quantità dell’analisi.',
 code('stopifnot(abs(moran_I(100+2*z,A)-\n              moran_I(z,A))<1e-12)\nstopifnot(abs(moran_I(-z,A)-\n              moran_I(z,A))<1e-12)','R · invarianza affine'), notebook=13, source=[16,17])

slide(63,'Permutare mantiene fissa la geometria',
 permutation(),
 p(r'Il riferimento riassegna gli stessi valori ai siti, mantenendo coordinate e matrice dei pesi. Ogni permutazione produce un nuovo indice.')+
 info(r'La domanda è se l’associazione osservata sia insolita rispetto alla riassegnazione dei valori ammessa dall’ipotesi nulla.')+
 p(r'La permutazione non simula nuovi campioni geologici: costruisce un riferimento condizionato ai valori osservati.'),
 r'Nel test per permutazione restano fissi valori disponibili, siti e pesi; cambia la loro associazione.', notebook=14, source=[19])

slide(64,'L’ipotesi nulla richiede scambiabilità',
 eq(r'H_0:\ (Z(s_1),\ldots,Z(s_n))\ \text{è scambiabile rispetto ai siti}')+
 eq(r'\mathbb E_{\mathrm{perm}}(I_H)=-\frac{1}{n-1}\quad\text{con diagonale nulla}')+
 info(r'Il valore atteso riguarda la permutazione completa delle etichette, per valori non costanti e pesi fissati. Non è una descrizione universale di ogni processo spaziale.'),
 p(r'Un trend legato alla posizione rende i valori di luoghi diversi non equivalenti. La riassegnazione libera rompe anche quel trend.')+
 p(r'Un rifiuto dell’ipotesi nulla non separa automaticamente gradiente, dipendenza residua e altre cause della disposizione osservata.'),
 r'Il significato del test dipende da quali riassegnazioni sono giustificate dall’ipotesi nulla.', notebook=14, source=[19,20])

slide(65,'Il p-value Monte Carlo include il caso osservato',
 eq(r'p_{\mathrm{MC}}=\frac{1+\sum_{b=1}^{B}\mathbf1(I^{(b)}\ge I_{\mathrm{obs}})}{B+1}')+
 info(r'Usiamo l’alternativa unilaterale di associazione positiva. La direzione viene dichiarata prima di leggere il risultato.'),
 p(r'Il numeratore conta le permutazioni almeno tanto estreme quanto l’osservazione, più il caso osservato. Il p-value non è mai zero.')+
 p(r'Le 100 permutazioni originali usano blocchi di uniformi salvati nel CSV.'),
 r'Il p-value misura compatibilità con un riferimento esplicito e ha una risoluzione finita.',
 code('u <- casuali$u\nI_null <- sapply(1:100,function(b) {\n ii <- ((b-1)*n+1):(b*n)\n moran_I(z[order(u[ii])],A)\n})\np_MC <- (1+sum(I_null>=I_A))/101','R · riferimento originale N14'), notebook=14, source=[19])

slide(66,'Il numero di permutazioni limita la risoluzione',
 fig('21_permutazioni100_999',r'Protocollo originale con B=100 e approfondimento con B=999. Pesi e alternativa restano dichiarati.'),
 p(r'Con 100 permutazioni la risoluzione minima è $1/101$. Con 999 diventa $1/1000$. Aumentare B rende più fine la stima Monte Carlo.')+
 info(r'Più permutazioni non correggono un’ipotesi di scambiabilità sbagliata. Il seme riproduce l’estrazione, ma non garantisce la validità dell’inferenza.'),
 r'La precisione Monte Carlo e l’adeguatezza del riferimento inferenziale sono proprietà distinte.',
 code('set.seed(20261109)\nI_999 <- replicate(999,\n moran_I(sample(z),A))\nc(p_100=p_MC,\n p_999=(1+sum(I_999>=I_A))/1000)','R · approfondimento dichiarato'), notebook=14, source=[19])

slide(67,'Un gradiente può generare associazione globale',
 fig('22_trend_residui',r'Valori originali e residui di una tendenza piana. La rimozione della media stimata cambia la struttura descritta.'),
 p(r'Sui dati $I_A='+value('Moran','I_A')+r'$; sui residui del piano $I_A='+value('Moran','I_residui_A')+r'$. Il gradiente della media spiega una parte rilevante dell’associazione globale osservata.')+
 info(r'La domanda “esiste una disposizione spaziale?” è diversa da “resta dipendenza dopo aver descritto la media?”.')+
 p(r'Per la seconda domanda occorrono una specifica della media e una diagnosi dei residui coerente con la stima.'),
 r'L’associazione globale non distingue da sola un trend da una dipendenza residua.', source=[20])

slide(68,'I residui sono stimati e hanno vincoli',
 eq(r'Z(s)=m(s)+\varepsilon(s),\qquad \widehat e_i=z_i-\widehat m(s_i)')+
 eq(r'\widehat{\boldsymbol e}=(I-H)\boldsymbol z')+
 info(r'Anche con errori indipendenti omoschedastici, i residui OLS hanno covarianza proporzionale a $I-H$. Non sono automaticamente scambiabili.'),
 p(r'Il confronto degli indici sui dati e sui residui è descrittivo. Una permutazione libera dei residui non fornisce in generale un test esatto.')+
 p(r'Per l’inferenza occorre un metodo giustificato dal modello: per esempio una simulazione coerente con l’ipotesi nulla e con la stima.'),
 r'La stima della tendenza modifica la struttura probabilistica dei residui.',
 code('trend <- lm(concentrazione~x_m+y_m,\n            data=d)\ne_trend <- residuals(trend)\nc(dati=moran_I(z,A),\n  residui=moran_I(e_trend,A))','R · diagnosi descrittiva'), source=[20])

slide(69,'Associazione, significatività e meccanismo',
 table(['Risultato','Che cosa consente di dire'],[
 ['Indice positivo','Scarti simili contribuiscono sul grafo'],
 ['p-value piccolo','Risultato insolito sotto il riferimento scelto'],
 ['Mappa dei quadranti','Descrizione delle configurazioni'],
 ['Spiegazione causale','Richiede disegno ed evidenze ulteriori']], [4.2,4.8]),
 p(r'Un indice globale non identifica un processo di trasporto, una sorgente o una causa. La geometria può essere compatibile con meccanismi diversi.')+
 info(r'Nel dataset sintetico conosciamo il contesto didattico. La discussione serve a distinguere ciò che la statistica misura da ciò che una ricerca reale dovrebbe dimostrare.')+
 p(r'Riportiamo insieme grandezza dell’indice, pesi, ipotesi nulla e limite interpretativo.'),
 r'Una conclusione deve restare proporzionata alla domanda e al riferimento che sono stati verificati.', source=[16,19,20])

slide(70,'Laboratorio: una frase completa su Moran',
 experiment('moran','Esperimento online · associazione e permutazioni')+
 table(['Elemento della conclusione','Specificazione'],[
 ['Dati','64 concentrazioni sintetiche'],
 ['Geometria','Piano locale, soglia 260 m'],
 ['Pesi','Binari A per il risultato principale'],
 ['Riferimento','Permutazione libera delle etichette'],
 ['Alternativa','Associazione positiva'],
 ['Limite','Trend e dipendenza residua non separati']], [3.1,5.9]),
 p(r'N13 calcola e verifica l’indice. N14 costruisce il riferimento e conserva il numero di permutazioni.')+
 info(r'Lo scatter usa W e la sua pendenza corrisponde a $I_W$. Questa specificazione deve comparire nella didascalia.')+
 p(r'Il passo successivo studia come la dissimilarità cambi con la distanza.'),
 r'Un risultato inferenziale leggibile include dati, pesi, ipotesi, alternativa e limiti.', notebook=14, source=[16,17,18,19,20,32])

slide(71,'La semivarianza parte dalle coppie',
 pairs()+eq(r'g_{ij}=\tfrac12(z_i-z_j)^2,\qquad i<j'),
 p(r'Per ogni coppia distinta calcoliamo distanza e metà del quadrato della differenza dei valori. Il contributo aumenta quando i campioni sono dissimili.')+
 info(r'Con 64 siti ci sono $64\cdot63/2=2016$ coppie non ordinate. La diagonale e le coppie replicate in ordine inverso vengono escluse.')+
 p(r'La semivarianza ha unità pari al quadrato dell’unità della variabile: qui $(\mathrm{u.a.})^2$.'),
 r'Le coppie descrivono dissimilarità a diverse separazioni, ma riutilizzano gli stessi siti.', notebook=15, source=[21])

slide(72,'La nube delle coppie precede la media per classe',
 fig('23_coppie_semivarianza',r'Ogni punto rappresenta una coppia: distanza in ascissa e semidifferenza quadratica in ordinata.'),
 p(r'Alla stessa distanza i contributi possono variare molto. La nube mostra dispersione e coppie influenti; le direzioni saranno analizzate a parte.')+
 info(r'Raggruppare le distanze riassume questa variabilità. Il riassunto non sostituisce l’ispezione dei dati da cui deriva.'),
 r'Una curva media può nascondere una nube di coppie molto eterogenea.',
 code('G <- 0.5*outer(z,z,"-")^2\nupper <- upper.tri(D)\nh_pair <- D[upper]\ng_pair <- G[upper]\nstopifnot(length(h_pair)==2016L)','R · coppie non ordinate'), notebook=15, source=[21])

slide(73,'Il semivariogramma empirico raggruppa distanze',
 fig('24_semivariogramma',r'Classi $(0,300]$, $(300,600]$, $(600,1000]$, $(1000,2500]$ m. L’ascissa è la distanza media delle coppie.')+
 eq(r'\widehat\gamma_k=\frac{1}{2N_k}\sum_{(i,j)\in\mathcal P_k}(z_i-z_j)^2'),
 p(r'Ogni classe contiene $N_k$ coppie. Il valore stimato è la media dei loro contributi, non il contributo della coppia alla distanza centrale.')+
 info(r'Numero e ampiezza delle classi controllano il compromesso fra dettaglio e stabilità descrittiva. Le classi finali non devono essere interpretate senza i conteggi.'),
 r'Il semivariogramma empirico deve mostrare come sono costruite le classi di distanza.',
 code('classe <- cut(h_pair,\n breaks=c(0,300,600,1000,2500))\naggregate(cbind(h=h_pair,gamma=g_pair),\n          list(classe=classe),mean)','R · medie per classe'), notebook=15, source=[21])

slide(74,'Molte coppie non sono molte repliche indipendenti',
 fig('25_numerosita_coppie',r'I conteggi per classe sommano a 2016. Coppie non ordinate distinte possono condividere un sito.'),
 p(r'Le coppie $(i,j)$ e $(i,k)$ contengono la stessa osservazione $z_i$. I loro contributi possono quindi essere dipendenti.')+
 info(r'Non è giustificato trattare tutte le coppie come osservazioni indipendenti per ottenere intervalli stretti della curva.')+
 p(r'Il conteggio delle coppie è utile per leggere la stabilità del riassunto. L’incertezza richiede un metodo coerente con la struttura spaziale.'),
 r'2016 coppie costruite da 64 siti non equivalgono a 2016 nuovi campioni indipendenti.', notebook=15, source=[21])

slide(75,'Semivarianza e covarianza sono collegate',
 eq(r'\gamma(h)=\tfrac12\operatorname{Var}\{Z(s+h)-Z(s)\}')+
 eq(r'\gamma(h)=C(0)-C(h)')+
 info(r'La seconda uguaglianza vale per un processo stazionario al secondo ordine con la stessa varianza nei due siti. In presenza di anisotropia h è un vettore.'),
 p(r'Se la covarianza diminuisce con la separazione, aumenta la variabilità delle differenze. La relazione collega una descrizione delle coppie a un modello probabilistico.')+
 p(r'La media empirica delle differenze quadratiche stima questo oggetto quando le ipotesi sulla media e sugli incrementi sono adeguate.'),
 r'La relazione con la covarianza richiede ipotesi sul processo, non soltanto una formula applicata ai dati.', source=[22])

slide(76,'La stazionarietà distingue media e dipendenza',
 table(['Ipotesi','Contenuto'],[
 ['Secondo ordine',r'$\mathbb E[Z(s)]=\mu$, covarianza dipendente dallo spostamento'],
 ['Intrinseca',r'Incrementi a media zero e varianza dipendente dallo spostamento'],
 ['Isotropia','Dipendenza dalla lunghezza dello spostamento'],
 ['Trend spaziale','Media che varia con la posizione']], [3.1,5.9]),
 p(r'La stazionarietà intrinseca è una condizione diversa, più debole di quella al secondo ordine. Non impone l’esistenza di una covarianza stazionaria finita.')+
 info(r'Nel caso guida il gradiente della media rende prudente interpretare la curva grezza. Un aumento della semivarianza può riflettere anche quel gradiente.')+
 p(r'Prima di adattare un modello, valutiamo media, direzione, supporto e copertura delle coppie.'),
 r'Il modello di semivarianza deve essere coerente con ciò che è stato rimosso o mantenuto nella media.', source=[20,22])

slide(77,'L’isotropia è un’ipotesi aggiuntiva',
 fig('26_direzionali',r'Confronto descrittivo delle coppie orientate lungo direzioni diverse nel piano locale.'),
 p(r'Un semivariogramma omnidirezionale riunisce coppie con la stessa distanza e direzioni diverse. Questo può nascondere una struttura orientata.')+
 info(r'Confrontare direzioni richiede tolleranze angolari e classi dichiarate. Differenze apparenti possono dipendere anche da conteggi, trend e geometria del campione.')+
 p(r'La direzione può essere scientificamente rilevante per stratificazione, flusso o orientamento strutturale.'),
 r'L’assenza della direzione dal grafico non dimostra che il processo sia isotropo.', source=[22])

slide(78,'Nugget, sill e range dipendono dal modello',
 fig('27_modelli_variogramma',r'Modelli teorici illustrativi con parametri dichiarati; non sono adattamenti automatici ai 64 valori.'),
 p(r'Il nugget descrive un salto all’origine, interpretabile secondo il modello come errore di misura o variazione a scale non risolte. Il sill è il livello limite quando esiste.')+
 info(r'Per il modello esponenziale la scala a non è un range finito: a $3a$ si raggiunge circa il 95\% del sill strutturale.')+
 sm(r'Un modello sferico raggiunge il sill a distanza finita. Specificare sempre la convenzione usata dal software.'),
 r'I nomi dei parametri devono accompagnare la formula che ne definisce il significato.', source=[22,28])

slide(79,'Il nugget cambia il bersaglio della previsione',
 eq(r'Y(s)=X(s)+\eta(s),\qquad \operatorname{Var}\{\eta(s)\}=\tau^2')+
 eq(r'\operatorname{Cov}\{Y(s_i),Y(s_j)\}=C_X(s_i,s_j)+\tau^2\mathbf1(i=j)')+
 info(r'La formula assume errori di misura indipendenti fra osservazioni e indipendenti dal campo latente X. Sono ipotesi del modello.'),
 p(r'Prevedere il campo latente X in un sito non equivale a prevedere una nuova misura Y nello stesso sito. La seconda include una nuova componente di errore.')+
 p(r'Per repliche nello stesso luogo bisogna distinguere identità del sito e identità dell’osservazione. La covarianza dell’errore non si deduce dalla sola distanza.'),
 r'La varianza predittiva dipende dal fatto che il bersaglio sia un campo latente o una nuova misura.', source=[22,28])

slide(80,'Adattare una curva richiede un modello valido',
 eq(r'\sum_k q_k\{\widehat\gamma_k-\gamma(h_k;\theta)\}^2')+
 table(['Scelta','Controllo'],[
 ['Famiglia di modelli','Validità della covarianza o del variogramma'],
 ['Pesi delle classi','Criterio dichiarato, conteggi disponibili'],
 ['Parametri','Vincoli e convenzioni esplicite'],
 ['Dominio di stima','Solo dati ammessi dal protocollo']], [3.4,5.6]),
 p(r'Un criterio pesato può descrivere l’adattamento della curva. Non rende indipendenti le classi e non garantisce un’inferenza corretta sui parametri.')+
 info(r'Una curva visivamente liscia non è necessariamente una covarianza valida. Il sistema di kriging richiede un modello matematicamente ammissibile.')+
 p(r'Nel piccolo esempio di kriging useremo una covarianza gaussiana dichiarata, così da isolare e verificare il sistema dei pesi.'),
 r'Il modello deve essere valido e stimato con informazioni compatibili con la verifica previsionale.', source=[22,28])

slide(81,'Laboratorio: dalle coppie alle ipotesi',
 experiment('variogramma','Esperimento online · coppie e semivariogramma')+
 table(['Consegna N15','Controllo'],[
 ['Tabella delle coppie','2016 coppie, senza diagonale'],
 ['Classi di distanza','Estremi e inclusione del bordo'],
 ['Curva empirica','Distanza media, semivarianza, conteggi'],
 ['Interpretazione','Trend, direzione e dipendenza fra coppie'],
 ['Modello eventuale','Formula, parametri e dominio di validità']], [4.0,5.0]),
 p(r'Il grafico deve rendere visibili le scale in metri e in $(\mathrm{u.a.})^2$. La discussione precisa ciò che il campionamento permette di osservare.')+
 info(r'Più classi non aggiungono dati. Un modello della dipendenza richiede anche una copertura adeguata di distanze e direzioni.')+
 p(r'Passiamo quindi dalla geometria delle coppie al disegno del campionamento.'),
 r'Un semivariogramma utile unisce curva, conteggi, supporto e ipotesi sul processo.', notebook=15, source=[21,22,32])
