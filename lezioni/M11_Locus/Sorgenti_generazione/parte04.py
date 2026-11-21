"""Copertura del campione, interpolazione e verifica: pagine 82–105."""
from componenti import *

slide(82,'Il campione deve rappresentare un dominio',
 table(['Scelta','Domanda da risolvere'],[
 ['Dominio','Quale territorio interessa la conclusione?'],
 ['Unità','Che cosa costituisce un campione?'],
 ['Accessibilità','Quali aree sono più facili da osservare?'],
 ['Distanze','Quali scale di variazione sono coperte?'],
 ['Bersaglio','Media dei siti, media areale o previsione?']], [3.2,5.8]),
 p(r'La posizione dei campioni non è un semplice dettaglio del file. Determina quali parti del territorio e quali distanze sono rappresentate.')+
 info(r'Un numero elevato di osservazioni vicino a una strada può descrivere bene quel corridoio e male il resto del dominio.')+
 p(r'La qualità del campione va discussa rispetto al bersaglio dell’analisi.'),
 r'La rappresentatività dipende da come i siti sono stati scelti e dalla popolazione a cui si vuole riferire il risultato.', source=[23])

slide(83,'Campionare lungo una strada seleziona un’area',
 fig('28_strada_campione',r'Campione di convenienza: i 16 siti con $y\le250$ m. Gli altri 48 siti descrivono il territorio escluso.'),
 p(r'La media del corridoio è '+value('copertura','media_strada',2)+r' u.a.; quella dell’intera griglia è '+value('copertura','media_reticolo',2)+r' u.a. La differenza è '+value('copertura','scarto_strada',2)+r' u.a.')+
 info(r'In un’indagine reale il valore medio del territorio escluso non sarebbe noto. Il dataset completo permette qui di osservare l’effetto della selezione.'),
 r'La facilità di accesso può rendere il campione spazialmente selettivo.',
 code('strada <- d$y_m<=250\nc(n_strada=sum(strada),\n media_strada=mean(z[strada]),\n media_griglia=mean(z),\n media_altrove=mean(z[!strada]))','R · confronto descrittivo'), notebook=16, source=[23])

slide(84,'La copertura richiede una misura geografica',
 fig('29_copertura',r'La copertura dipende dalla distribuzione dei siti e dalle distanze dalle aree non campionate.'),
 p(r'Conteggio, estensione e distanza dal campione più vicino descrivono aspetti diversi. Una nuvola densa in un angolo può lasciare una vasta regione scoperta.')+
 info(r'La distanza al sito più vicino è una misura geometrica, non una stima completa dell’errore di previsione. La relazione con l’errore dipende dal fenomeno e dal modello.')+
 p(r'Per progettare nuovi campioni, consideriamo anche direzioni, litologie e accessibilità.'),
 r'Il numero dei siti deve essere letto insieme alla loro distribuzione sul dominio.', notebook=16, source=[23])

slide(85,'Bilanciare gli strati rende esplicito il disegno',
 grid('split')+
 sm(r'Il disegno documenta probabilità di inclusione, definizione degli strati oppure passo e origine della griglia, secondo la procedura adottata.'),
 p(r'Una stratificazione può garantire osservazioni in zone scientificamente diverse. La ripartizione del campione deve essere collegata al bersaglio e ai costi.')+
 info(r'Un’allocazione uguale per strato facilita alcuni confronti. Per una media dell’intero territorio possono servire pesi proporzionali alle aree o alle probabilità di inclusione.')+
 p(r'La griglia del modulo è una costruzione didattica, non una garanzia generale contro distorsioni del campionamento.'),
 r'Il disegno chiarisce quali unità possono entrare nel campione e con quale peso.', source=[23,24])

slide(86,'Con blocchi bilanciati le due medie coincidono',
 fig('30_medie_blocchi',r'Quattro blocchi definiti dalle soglie $x=1000$ e $y=1000$ m; 16 siti in ciascuno.')+
 eq(r'\bar z=\sum_b\frac{n_b}{n}\bar z_b'),
 p(r'La media di tutti i siti è sempre la media delle medie di blocco pesata per le numerosità, quando ogni sito appartiene a un solo blocco.')+
 info(r'Se tutti gli $n_b$ sono uguali, i pesi sono uguali. La media non pesata dei blocchi coincide quindi con la media dei siti.'),
 r'L’uguaglianza fra media dei siti e media semplice dei blocchi dipende dal bilanciamento.',
 code('blocco <- interaction(d$x_m>=1000,\n                      d$y_m>=1000)\nnb <- table(blocco)\nmb <- tapply(z,blocco,mean)\nc(siti=mean(z),blocchi=mean(mb))','R · il caso bilanciato'), notebook=17, source=[24])

slide(87,'Con blocchi sbilanciati bisogna scegliere i pesi',
 fig('31_pesi_squilibrati',r'Esempio costruito: 2 osservazioni con media 10 e 8 osservazioni con media 20.',height=4.3)+
 eq(r'\bar z_{\mathrm{siti}}=\frac{2\cdot10+8\cdot20}{10}=18')+
 eq(r'\bar z_{\mathrm{blocchi}}=\frac{10+20}{2}=15'),
 p(r'La prima quantità assegna uguale peso ai siti. La seconda assegna uguale peso ai due blocchi.')+
 info(r'Nessuna delle due è una media areale per definizione. Per interpretarla come tale occorre collegare i blocchi alle aree rappresentate e al campionamento.'),
 r'Il peso definisce quale popolazione viene rappresentata nella media.',
 code('n_b <- c(2,8)\nmedia_b <- c(10,20)\nc(siti=weighted.mean(media_b,n_b),\n  blocchi=mean(media_b))','R · due bersagli distinti'), notebook=17, source=[24])

slide(88,'La dipendenza entra nella varianza della media',
 eq(r'\operatorname{Var}(\bar Z)=\frac{1}{n^2}\sum_i\sum_j\operatorname{Cov}(Z_i,Z_j)')+
 eq(r'=\frac{1}{n^2}\left\{\sum_i\operatorname{Var}(Z_i)+2\sum_{i<j}\operatorname{Cov}(Z_i,Z_j)\right\}')+
 info(r'La formula include i termini fra siti diversi. Con covarianze positive, ignorarli può sottostimare la varianza della media.'),
 p(r'Non esiste una numerosità effettiva universale ricavabile dal solo conteggio dei punti. Dipende dai pesi, dalla geometria e dalla covarianza del bersaglio.')+
 p(r'La formula $\sigma^2/n$ è un caso particolare con varianze uguali e covarianze nulle fra osservazioni distinte.'),
 r'La precisione della media dipende anche dalla relazione fra le osservazioni, oltre che dal loro numero.', source=[23,24])

slide(89,'Nuovi campioni: copertura e piccole distanze',
 table(['Obiettivo','Posizioni utili da valutare'],[
 ['Ridurre aree scoperte','Siti lontani dai campioni disponibili'],
 ['Studiare piccole scale','Coppie ravvicinate e repliche progettate'],
 ['Confrontare ambienti','Copertura degli strati scientifici'],
 ['Verificare la previsione','Siti riservati secondo il compito']], [4.0,5.0]),
 p(r'Aggiungere soltanto siti molto distanti migliora la copertura, ma può lasciare poco informata la struttura a piccola scala. Aggiungere soltanto siti ravvicinati ha il limite opposto.')+
 info(r'Il disegno può combinare una copertura del dominio con coppie e repliche mirate. La scelta deve essere motivata rispetto al budget e alla domanda.')+
 p(r'Le nuove misure vanno considerate prima della previsione finale se servono per scegliere il modello.'),
 r'Copertura del dominio e informazione sulle piccole scale sono obiettivi complementari.', source=[21,23])

slide(90,'La scheda del disegno rende visibili le esclusioni',
 table(['Voce','Da registrare'],[
 ['Dominio e supporto','Area, profondità, periodo della misura'],
 ['Selezione','Procedura e probabilità note, se disponibili'],
 ['Esclusioni','Siti inaccessibili o rimossi con motivo'],
 ['Repliche','Sito, strumento e occasione di misura'],
 ['Dati riservati','Regola geografica di separazione']], [3.4,5.6]),
 p(r'Una mappa dei siti mancanti può essere informativa quanto la mappa dei siti misurati. L’assenza di dati può dipendere da condizioni legate al fenomeno.')+
 info(r'La selezione per accessibilità non viene corretta automaticamente da un’interpolazione successiva.')+
 p(r'La scheda distingue ciò che il campione rappresenta da ciò che si vorrebbe conoscere.'),
 r'Le esclusioni e il processo di selezione fanno parte dei dati necessari a interpretare l’analisi.', source=[23,31])

slide(91,'Laboratorio: campione e unità della sintesi',
 experiment('copertura','Esperimento online · copertura geografica')+
 table(['Attività','Risultato da discutere'],[
 ['N16: strada','Media del corridoio e dominio escluso'],
 ['Mappa della copertura','Aree e distanze poco rappresentate'],
 ['N17: blocchi','Numerosità, medie e pesi'],
 ['Esempio sbilanciato','18 per sito, 15 per blocco']], [4.0,5.0]),
 p(r'La relazione finale deve nominare il bersaglio: media dei siti osservati, confronto fra blocchi o stima di una quantità territoriale.')+
 info(r'Nel dataset sintetico conosciamo tutti i 64 valori. Il confronto con una selezione serve a vedere una distorsione che, con soli dati parziali, potrebbe restare invisibile.')+
 p(r'La previsione nello spazio deve rispettare gli stessi limiti di copertura.'),
 r'La media e la carta acquistano significato quando sono collegate a un bersaglio e a un disegno.', notebook=17, source=[23,24,32])

slide(92,'IDW: prevedere con pesi di distanza',
 eq(r'\widehat z(s_0)=\sum_iw_i(s_0)z_i')+
 eq(r'w_i(s_0)=\frac{d(s_i,s_0)^{-p}}{\sum_jd(s_j,s_0)^{-p}},\qquad p>0')+
 info(r'La formula vale quando tutte le distanze dal bersaglio sono positive. La coincidenza con un campione richiede una regola separata.'),
 p(r'IDW assegna maggiore peso ai campioni vicini. L’esponente p regola la concentrazione dei pesi attorno al bersaglio.')+
 p(r'È una regola di interpolazione. Non fornisce da sola un modello probabilistico dell’errore o un intervallo predittivo.'),
 r'IDW deve dichiarare metrica, esponente, campioni utilizzati e trattamento delle coincidenze.', notebook=18, source=[25,26])

slide(93,'Pesi positivi conservano costanti e intervalli',
 fig('32_idw_pesi',r'Pesi verso $(900,900)$ m per p=1, 2 e 3. Ciascun vettore di pesi somma a uno.')+
 eq(r'\min_i z_i\le\widehat z(s_0)\le\max_i z_i'),
 p(r'Con pesi non negativi che sommano a uno, la previsione è una combinazione convessa dei valori utilizzati. Una variabile costante viene riprodotta.')+
 info(r'La proprietà non dimostra accuratezza. Fuori dall’area coperta dai dati, il vincolo può impedire di seguire un gradiente oltre i livelli osservati.'),
 r'I vincoli dei pesi spiegano sia proprietà utili sia limiti dell’interpolazione.',
 code('w0 <- idw_weights(xy,c(900,900),p=2)\nstopifnot(all(w0>=0),\n          abs(sum(w0)-1)<1e-12)\nc(stima=sum(w0*z),min=min(z),max=max(z))','R · controllare i pesi'), notebook=18, source=[26])

slide(94,'L’esponente controlla quanto conta la vicinanza',
 fig('33_idw_potenze',r'Confronto dichiarato tra p=1, p=2 e p=3 sugli stessi campioni e bersagli.'),
 p(r'Valori maggiori di p concentrano il peso sui campioni più vicini. Valori più piccoli distribuiscono maggiormente l’influenza.')+
 info(r'Il valore esteticamente più gradevole non è necessariamente quello più accurato. Se p viene scelto dai dati, la scelta deve avvenire all’interno dell’addestramento.'),
 r'La sensibilità all’esponente va valutata senza usare il test finale per scegliere il modello.',
 code('sapply(1:3,function(p)\n idw_pred(xy,z,\n          matrix(c(900,900),nrow=1),\n          p=p))','R · confronto allo stesso bersaglio'), notebook=18, source=[25,26])

panorama(95,'Una superficie contiene previsioni, non nuovi dati',
 '34_idw_superficie',
 r'IDW con p=2 sui 64 siti: la griglia di 45$\times$45 posizioni rende visibile la regola di interpolazione. I simboli indicano i campioni. Questa carta descrittiva usa l’intero dataset e non è la previsione del test geografico. La gestione delle coincidenze riproduce il valore osservato, oppure la media delle repliche coincidenti secondo la convenzione dichiarata.',
 r'Una griglia più fitta rende più fine il disegno, ma non aumenta l’informazione osservata.', notebook=18, source=[26,27])

slide(96,'Lasciare fuori Est verifica un trasferimento',
 fig('35_split_spaziale',r'Addestramento: $x<1250$ m, 40 siti. Test: $x\ge1250$ m, 24 siti. La linea $x=1250$ appartiene al test.'),
 p(r'I siti del test sono oltre l’estensione orientale del train. La prova valuta un trasferimento geografico, con extrapolazione verso Est.')+
 info(r'La geometria della separazione deve rappresentare il compito. Il protocollo principale fissa p=2 prima di leggere il test.'),
 r'La geometria della separazione determina quale capacità previsionale viene valutata.',
 code('train <- d[d$x_m<1250,]\ntest <- d[d$x_m>=1250,]\nstopifnot(nrow(train)==40L,\n          nrow(test)==24L,\n !any(train$id %in% test$id))','R · separazione geografica'), notebook=19, source=[29])

slide(97,'I riferimenti usano gli stessi campioni disponibili',
 fig('36_previsioni_confronto',r'Media dell’addestramento, vicino più prossimo e IDW p=2: stesso insieme di 24 siti da prevedere.'),
 p(r'RMSE sul test: vicino più prossimo '+value('IDW','RMSE_NN',2)+r', IDW '+value('IDW','RMSE',2)+r', media del train '+value('IDW','RMSE_media',2)+r' u.a. Il riferimento più semplice può quindi essere competitivo.')+
 info(r'IDW combina tutti i campioni del train con pesi di distanza. Nessuno dei tre metodi usa le concentrazioni del test per costruire la previsione.')+
 p(r'Il vicino più prossimo è il migliore dei tre in questo test. La graduatoria riguarda questa geometria, questi dati e questa metrica.'),
 r'Metodi confrontabili devono prevedere gli stessi bersagli usando lo stesso insieme di informazioni.', notebook=19, source=[25,29,30])

slide(98,'Gli errori hanno grandezza, segno e posizione',
 fig('37_errori_spaziali',r'Errori $e_i=z_i-\widehat z_i$ nei siti tenuti fuori. Il segno positivo indica sottostima.',height=5.0)+
 eq(r'\mathrm{MAE}=\frac1m\sum_i|e_i|,\qquad \mathrm{RMSE}=\sqrt{\frac1m\sum_ie_i^2}'),
 p(r'Per IDW p=2, MAE='+value('IDW','MAE',2)+r' e bias='+value('IDW','bias',2)+r' u.a. Il segno positivo indica una sottostima media dei siti Est.')+
 info(r'I 24 errori possono essere spazialmente dipendenti. Non sono 24 repliche indipendenti del protocollo di trasferimento.'),
 r'Le metriche riassumono la prestazione; la carta degli errori ne mostra i limiti geografici.',
 code('pred <- idw_pred(xy[train_idx,],\n z[train_idx],xy[test_idx,],p=2)\ne <- z[test_idx]-pred\nc(MAE=mean(abs(e)),\n RMSE=sqrt(mean(e^2)),bias=mean(e))','R · valutare il test riservato'), notebook=19, source=[30])

slide(99,'Le scelte del modello restano dentro il train',
 fig('38_tuning_blocchi',r'Approfondimento: confronto degli esponenti con separazioni geografiche interne ai 40 siti di addestramento.'),
 p(r'Tre frontiere interne: x=500, 750 e 1000 m. Per ciascuna si stima sui siti a Ovest e si prevedono gli 8 siti della colonna alla frontiera.')+
 info(r'Si confrontano p=1, 2 e 3 su 24 previsioni interne con RMSE; viene scelto p=3. Il risultato principale sul test resta quello con p=2 prefissato, distinto dall’approfondimento.')+
 p(r'Una partizione casuale può lasciare campioni molto vicini fra train e verifica e misurare un compito più facile del trasferimento ad Est.'),
 r'La selezione dei parametri deve ricostruire una separazione spaziale coerente con il compito.', notebook=19, source=[29,30])

slide(100,'Il kriging aggiunge un modello di covarianza',
 eq(r'\widehat Z(s_0)=\sum_{i=1}^{m}\lambda_iY(s_i),\qquad \sum_i\lambda_i=1')+
 table(['Esempio verificabile','Specificazione'],[
 ['Siti sulla linea','0, 500, 1000 m'],
 ['Valori osservati','10, 15, 12 u.a.'],
 ['Bersaglio','250 m'],
 ['Covarianza dichiarata',r'$C(h)=4\exp\{-(h/800)^2\}$']], [4.0,5.0]),
 p(r'Il kriging ordinario assume una media costante ignota. Cerca il predittore lineare non distorto con minima varianza dell’errore, sotto la covarianza specificata.')+
 info(r'Il piccolo esempio è separato dai dati con gradiente del caso guida. La covarianza è dichiarata per rendere controllabile il calcolo; non viene presentata come stimata dai tre valori.')+
 sm(r'La linearità e la covarianza bastano per il criterio di minima varianza; intervalli gaussiani richiedono ulteriori assunzioni.'),
 r'La proprietà di ottimalità del kriging è condizionata al modello della media e della covarianza.', source=[28])

slide(101,'Il sistema impone la non distorsione',
 eq(r'\begin{bmatrix}C&\mathbf1\\\mathbf1^\top&0\end{bmatrix}\begin{bmatrix}\boldsymbol\lambda\\ \nu\end{bmatrix}=\begin{bmatrix}\boldsymbol c_0\\1\end{bmatrix}')+
 table(['Simbolo','Significato'],[
 [r'$C_{ij}$','Covarianza fra osservazioni'],
 [r'$(c_0)_i$','Covarianza fra osservazione e bersaglio'],
 [r'$\mathbf1^\top\lambda=1$','Vincolo per la media costante ignota'],
 [r'$\nu$','Moltiplicatore con il segno del sistema scritto']], [3.2,5.8]),
 p(r'Il sistema viene risolto insieme, senza calcolare esplicitamente l’inversa. Devono essere controllati soluzione, vincolo e stabilità numerica.')+
 info(r'La convenzione di segno del moltiplicatore deve restare coerente quando si scrive la varianza del kriging.'),
 r'La matrice dei pesi nasce dal modello e dalla geometria, con un vincolo esplicito.',
 code('s <- c(0,500,1000); s0 <- 250\nC <- 4*exp(-(outer(s,s,"-")/800)^2)\nc0 <- 4*exp(-((s-s0)/800)^2)\nK <- rbind(cbind(C,1),c(1,1,1,0))\nsol <- solve(K,c(c0,1))\nstopifnot(abs(sum(sol[1:3])-1)<1e-12)','R · risolvere il sistema ordinario'), source=[28])

slide(102,'I pesi del kriging possono essere negativi',
 fig('39_kriging_pesi',r'Nel caso dichiarato i tre pesi sommano a uno; il sito a 1000 m riceve un peso negativo.'),
 p(r'I pesi sono circa 0,465; 0,692; $-0,157$. La previsione è '+value('kriging','previsione',3)+r' u.a. La somma unitaria non impone la non negatività.')+
 info(r'Il kriging può produrre valori fuori dall’intervallo osservato. Un peso negativo non è automaticamente un errore: va letto nel contesto del modello.'),
 r'La somma dei pesi uguale a uno non basta a garantire una combinazione convessa.',
 code('lambda <- sol[1:3]\nz_toy <- c(10,15,12)\nc(lambda,previsione=sum(lambda*z_toy))\nstopifnot(any(lambda<0))','R · leggere pesi e previsione'), source=[28])

slide(103,'La varianza è condizionata alla covarianza scelta',
 fig('40_kriging_varianza',r'Varianza dell’errore per il campo dell’esempio, con covarianza nota e assenza di errore di misura.')+
 eq(r'\sigma_K^2=C_{00}-2\lambda^\top c_0+\lambda^\top C\lambda'),
 p(r'Nel bersaglio a 250 m la varianza è '+value('kriging','varianza',5)+r' $(\mathrm{u.a.})^2$. Con il sistema scritto, coincide con $C_{00}-\lambda^\top c_0-\nu$.')+
 info(r'La varianza dipende da geometria, covarianza e bersaglio. Non include automaticamente l’incertezza dei parametri stimati o l’errore di scelta del modello.'),
 r'Una varianza di kriging va interpretata insieme alle ipotesi che la rendono calcolabile.',
 code('varK <- 4-2*sum(lambda*c0)+\n drop(t(lambda)%*%C%*%lambda)\nstopifnot(abs(varK-\n (4-sum(lambda*c0)-sol[4]))<1e-10,\n varK>=0)\nvarK','R · verificare la varianza'), source=[28])

slide(104,'Metodo e bersaglio devono restare coerenti',
 table(['Aspetto','IDW','Kriging ordinario'],[
 ['Pesi','Distanze e p','Covarianza e vincolo'],
 ['Segno','Non negativi','Possono essere negativi'],
 ['Media','Nessun modello esplicito','Costante ignota'],
 ['Incertezza','Non fornita dalla regola','Condizionata al modello']], [2.4,3.05,3.05]),
 p(r'Per dati con un gradiente serve discutere il modello della media: per esempio covariate esplicite o una procedura di detrending coerente con la previsione.')+
 info(r'Prevedere un punto, una media di blocco o una nuova misura cambia covarianze e varianze coinvolte. Il bersaglio deve essere definito prima del calcolo.')+
 p(r'La scelta del metodo richiede anche una verifica su dati tenuti fuori secondo una geometria appropriata.'),
 r'La complessità del metodo non sostituisce coerenza del modello e verifica geografica.', source=[5,20,28,29])

slide(105,'Laboratorio: prevedere senza usare il test',
 experiment('interpolazione','Esperimento online · interpolazione e verifica')+
 experiment('kriging','Esperimento online · kriging e incertezza')+
 table(['Passaggio','Evidenza da conservare'],[
 ['N18: IDW','Pesi, coincidenze, esponente, superficie'],
 ['N19: test Est','40 siti ammessi e 24 bersagli riservati'],
 ['Confronto','Stesse metriche e stessi bersagli'],
 ['Kriging illustrativo','Covarianza, sistema, pesi e varianza'],
 ['Conclusione','Dominio di validità e limiti']], [3.7,5.3]),
 p(r'La carta sui 64 siti e il test costruito con i 40 siti del train ($x<1250$ m) devono rimanere riconoscibili. Sono due usi differenti dello stesso dataset.')+
 info(r'La consegna include errori per ID. Questo permette di verificare sia le metriche sia la loro distribuzione geografica.')+
 p(r'Un risultato riproducibile conserva tutte le scelte necessarie a ricostruire la previsione.'),
 r'La verifica riguarda una procedura fissata e un compito geografico dichiarato.', notebook=19, source=[25,26,27,28,29,30,32])
