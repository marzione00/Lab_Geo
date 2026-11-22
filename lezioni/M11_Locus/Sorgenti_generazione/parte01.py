"""Dato, supporto, coordinate e distanze: pagine 2–31."""
from componenti import *

slide(2,'Dai campioni alle relazioni spaziali',
 lab('Il percorso di Locus')+table(['Passaggio','p.'],[
 [internal_link(5,'Definire dato e supporto'),'5'],
 [internal_link(17,'Leggere coordinate e distanze'),'17'],
 [internal_link(32,'Costruire carte e appartenenze'),'32'],
 [internal_link(44,'Dichiarare vicinati e pesi'),'44'],
 [internal_link(56,'Misurare l’associazione spaziale'),'56'],
 [internal_link(71,'Studiare la semivarianza'),'71'],
 [internal_link(82,'Valutare la copertura del campione'),'82'],
 [internal_link(92,'Prevedere e verificare nello spazio'),'92'],
 [internal_link(106,'Consegnare un’analisi riproducibile'),'106']], [8.3,.7]),
 p(r'Futura ha collegato previsione e verifica temporale. Locus applica lo stesso rigore a posizioni, relazioni di vicinato e aree lasciate fuori dalla stima.')+
 info(r'Il caso guida comprende 64 siti sintetici. Le misure di concentrazione sono espresse in unità arbitrarie; le coordinate locali sono in metri.')+
 p(r'I 20 notebook mantengono gli identificativi M11\_N01--M11\_N20 del sito. Ogni attività contiene codice, risultati eseguiti e interpretazione.'),
 r'Prima di calcolare una relazione spaziale, bisogna dichiarare che cosa rappresentano i campioni.', source=[2,32])

slide(3,'Dal tempo alle posizioni sul territorio',
 boxes([('a',2.1,3.7,'M10: ordine temporale',3.7,'GeoA'),
        ('b',7.3,3.7,'M11: geometria dei siti',3.7,'GeoB'),
        ('c',2.1,1.15,'Passato disponibile',3.7,'GeoA'),
        ('d',7.3,1.15,'Campioni disponibili',3.7,'GeoB')],
       [('a','b',''),('a','c',''),('b','d',''),('c','d','')])+
 eq(r'Y_t\quad\longrightarrow\quad Z(s),\qquad s\in D\subset\mathbb R^2'),
 p(r'Nel tempo esiste un ordine naturale. Nello spazio la vicinanza richiede una metrica, una scala e talvolta una direzione.')+
 info(r'Due siti separati dalla stessa distanza possono appartenere a versanti, litologie o bacini diversi. La distanza geometrica non esaurisce la relazione scientifica.')+
 p(r'La previsione resta legata all’informazione disponibile: la geometria dei punti tenuti fuori deve rappresentare il compito da valutare.'),
 r'Nello spazio occorre costruire la nozione di vicino prima di usare un modello di dipendenza.', source=[3,29])

slide(4,'Quale domanda deve risolvere la carta?',
 table(['Domanda','Oggetto da dichiarare'],[
 ['Dove sono le misure?','Posizione, unità e copertura'],
 ['Quali siti si assomigliano?','Vicinato e riferimento inferenziale'],
 ['Quanto cambia il fenomeno?','Distanza, direzione e supporto'],
 ['Che cosa prevedo altrove?','Bersaglio e verifica geografica']], [4.5,4.5]),
 p(r'Una carta può descrivere campioni, confrontare aree oppure mostrare previsioni. Sono operazioni che richiedono dati e assunzioni differenti.')+
 info(r'Nel caso guida prevediamo la concentrazione in siti a Est usando solo i campioni a Ovest. Il protocollo separa questa verifica dalle carte descrittive dell’intero insieme.')+
 p(r'La copertina richiama campioni e connessioni. Nelle figure scientifiche ogni collegamento avrà una regola esplicita.'),
 r'La domanda scientifica stabilisce quali distanze, supporti e verifiche servono.', source=[3,30])

slide(5,'Il caso guida: 64 siti sintetici',
 table(['Campo','Significato'],[
 [r'\texttt{id}','Identificativo stabile S01--S64'],
 [r'\texttt{x\_m}, \texttt{y\_m}','Piano locale, metri, passo 250 m'],
 [r'\texttt{concentrazione}','Variabile sintetica, unità arbitrarie'],
 [r'\texttt{quota\_m}','Quota sintetica in metri'],
 [r'\texttt{lon}, \texttt{lat}','Coordinate geografiche sintetiche'],
 [r'\texttt{area}','Ovest/Est con soglia a 1000 m']], [3.6,5.5]),
 p(r'La griglia contiene otto posizioni per asse, da 0 a 1750 m. Il dataset permette di seguire gli stessi campioni attraverso tutte le operazioni.')+
 info(r'Il piano locale ha un’origine convenzionale. Il nome della colonna e l’unità metro non autorizzano ad assegnargli un codice EPSG.')+
 sm(r'Il file originale, la revisione Git e le impronte dei dati accompagnano il pacchetto. Nessun risultato richiede un download durante la lettura.'),
 r'I dati sintetici sono un esperimento didattico: le loro unità e la loro origine restano esplicite.', notebook=1, source=[3,6])

slide(6,'Valore, posizione e supporto formano il dato',
 boxes([('a',2.1,3.8,r'Valore\\$z_i$',3.5,'GeoB'),
        ('b',7.3,3.8,r'Posizione\\$s_i=(x_i,y_i)$',3.5,'GeoA'),
        ('c',2.1,1.15,'Supporto della misura',3.5,'GeoC'),
        ('d',7.3,1.15,'Identità e metadati',3.5,'GeoA')],
       [('a','c',''),('b','d',''),('c','d','')],4.8)+
 eq(r'\mathcal D=\{(\mathrm{id}_i,s_i,B_i,z_i)\}_{i=1}^{n}'),
 p(r'La posizione è il riferimento geometrico. Il supporto è la porzione di spazio e, quando rilevante, di tempo a cui si riferisce la misura.')+
 info(r'Una carota, una porzione di suolo e la media di un bacino possono avere lo stesso numero come valore. Non rappresentano la stessa quantità.')+
 p(r'Identificativo e metadati permettono di riconoscere la misura dopo ordinamenti, proiezioni e join.'),
 r'Una coordinata da sola non descrive il processo con cui il valore è stato misurato.', source=[3,5])

slide(7,'La carta iniziale mostra ciò che osserviamo',
 fig('01_mappa_punti',r'64 siti della griglia locale. Stessa scala metrica sui due assi; colore = concentrazione in u.a.'),
 p(r'I simboli rappresentano campioni. Tra due simboli non è stata osservata una misura aggiuntiva.')+
 info(r'Una griglia regolare facilita il controllo dei passaggi. Non implica che il fenomeno naturale sia regolare o che ogni cella abbia lo stesso valore.')+
 p(r'Prima di interpolare controlliamo estensione, punti mancanti, duplicati e leggibilità della scala cromatica.'),
 r'Una carta di punti deve rendere visibili i campioni e la copertura, prima di suggerire continuità.', notebook=7, source=[10])

slide(8,'La distribuzione marginale non conserva i luoghi',
 fig('02_marginale_permutata',r'Gli stessi valori possono essere disposti diversamente. L’istogramma resta invariato.'),
 p(r'La permutazione conserva media, quantili e varianza. Cambia l’accoppiamento dei valori con le posizioni.')+
 info(r'Due carte con lo stesso istogramma possono avere concentrazioni simili raccolte in gruppi oppure alternate fra vicini.')+
 p(r'L’analisi spaziale usa l’informazione congiunta di valori e luoghi.'),
 r'La relazione tra valori e posizioni contiene informazione che l’istogramma non descrive.',
 code('z_perm <- z[order(casuali$u[1:n])]\nstopifnot(identical(sort(z),\n                    sort(z_perm)))','R · stessi valori, altri luoghi'), source=[4])

slide(9,'Un punto e una media areale hanno supporti diversi',
 supports(),
 p(r'Il dato puntuale approssima la misura in una posizione. Il dato areale riassume una regione; richiede una definizione della media sul supporto.')+
 info(r'Un simbolo al centro di un poligono può rappresentare la media del poligono. Il punto disegnato non trasforma quella media in una misura puntuale.')+
 p(r'Prima di confrontare osservazioni provenienti da strumenti diversi, verifichiamo se misurano lo stesso supporto.'),
 r'Il supporto appartiene alla definizione della variabile e deve accompagnare ogni confronto.', source=[5])

slide(10,'Cambiare supporto cambia la quantità studiata',
 eq(r'Z(B)=\frac{1}{|B|}\int_B Z(s)\,ds')+
 eq(r'\operatorname{Var}\{Z(B)\}=\frac{1}{|B|^2}\int_B\int_B C(s,t)\,ds\,dt')+
 info(r'La seconda relazione assume una covarianza integrabile. La variabilità della media dipende dalla forma del supporto e dalla covarianza tra le posizioni.'),
 p(r'Una media su un’area non coincide automaticamente con il valore nel suo centro. Per stimarla da campioni occorre considerare come quei campioni coprono l’area.')+
 p(r'L’aggregazione spesso attenua le oscillazioni, ma l’effetto quantitativo dipende dalla struttura del processo e dal supporto.')+
 sm(r'Nel modulo distinguiamo medie dei siti osservati e medie territoriali. Non attribuiamo loro lo stesso significato senza un disegno di campionamento.'),
 r'La scala del supporto entra sia nella media sia nella sua variabilità.', source=[5,22])

slide(11,'Dai siti ai blocchi: esplicitare i pesi',
 fig('03_supporto_blocchi',r'Quattro blocchi della griglia. Ogni blocco contiene 16 siti nel disegno bilanciato.'),
 p(r'La media dei 64 valori assegna lo stesso peso a ogni sito. La media delle quattro medie assegna lo stesso peso a ogni blocco.')+
 info(r'Qui i due risultati coincidono perché i blocchi hanno uguale numerosità. Con conteggi diversi, le due operazioni rispondono a pesature diverse.')+
 p(r'Per una media areale servono pesi coerenti con le aree rappresentate o con il disegno di campionamento.'),
 r'La coincidenza tra due medie può dipendere dal bilanciamento del disegno, non da un’identità generale.', notebook=17, source=[5,24])

slide(12,'Repliche nello stesso luogo e nuovi siti',
 table(['Operazione','Informazione aggiunta'],[
 ['Ripetere una misura nello stesso sito','Ripetibilità della misura, a condizioni fissate'],
 ['Campionare un luogo distante','Copertura di un’altra parte del dominio'],
 ['Dividere una misura in più righe','Nessuna nuova osservazione indipendente'],
 ['Aggregare più campioni','Nuovo supporto, perdita di dettaglio']], [4.2,4.8]),
 p(r'La numerosità delle righe non misura da sola l’informazione spaziale. Occorre sapere se i dati provengono da nuovi luoghi o da ripetizioni della stessa unità.')+
 info(r'I duplicati possono essere errori, repliche vere oppure esiti di un join con più appartenenze. Il trattamento dipende dal motivo della duplicazione.')+
 p(r'Non eliminiamo righe automaticamente prima di aver chiarito che cosa rappresentano.'),
 r'Nuove righe e nuove unità campionate sono concetti da verificare separatamente.', source=[5,11,26])

slide(13,'L’identificativo protegge l’allineamento',
 eq(r'z_i\longleftrightarrow s_i\longleftrightarrow W_{i\cdot}')+
 boxes([('a',2.1,3.1,'Tabella delle misure',3.7,'GeoB'),
        ('b',7.3,3.1,'Tabella delle geometrie',3.7,'GeoA'),
        ('c',4.7,.8,'Corrispondenza per ID',4.0,'GeoC')],
       [('a','c',''),('b','c','')],4.2),
 p(r'Le distanze e i pesi dipendono dall’ordine delle coordinate. Il vettore delle misure deve seguire esattamente lo stesso ordine.')+
 info(r'Una matrice quadrata della dimensione giusta può essere associata ai valori sbagliati. Il controllo delle dimensioni non basta.'),
 r'L’allineamento per identificativo è parte della correttezza del calcolo spaziale.',
 code('stopifnot(!anyDuplicated(d$id))\nrownames(xy) <- d$id\ndimnames(D) <- list(d$id,d$id)\nstopifnot(identical(rownames(D),\n                    d$id))','R · legare righe e geometria'), notebook=1, source=[3,14])

slide(14,'L’audit precede ogni trasformazione',
 table(['Controllo','Criterio nel caso guida'],[
 ['Identità','64 ID distinti, nessun ID mancante'],
 ['Coordinate','Valori numerici e finiti'],
 ['Estensione locale','0--1750 m per asse'],
 ['Griglia','8 valori distinti per asse'],
 ['Variabile','64 concentrazioni finite'],
 ['Metadati','Unità e origine dichiarate']], [3.2,5.8]),
 p(r'Un audit combina controlli automatici e conoscenza del contesto. Il programma riconosce molti errori di formato; non può ricostruire da solo un CRS ignoto.')+
 info(r'Il notebook N01 salva un riepilogo dei campi. I controlli trasformano assunzioni del caso didattico in condizioni verificabili.'),
 r'Controlli semplici eseguiti all’ingresso impediscono che un errore di coordinate attraversi l’intera analisi.',
 code('stopifnot(nrow(d)==64L,\n all(is.finite(xy)),\n all(is.finite(z)),\n !anyDuplicated(d$id))\nsapply(d[c("x_m","y_m")],range)','R · audit minimo'), notebook=1, source=[3,6])

slide(15,'Due rappresentazioni con origini distinte',
 table(['Coordinate locali','Coordinate geografiche'],[
 [r'$x,y$ in metri',r'Longitudine, latitudine in gradi'],
 ['Origine convenzionale','Collocazione sintetica vicino a 9° E, 45° N'],
 ['Distanza euclidea del laboratorio','Proiezioni e distanze sulla Terra'],
 ['Nessun EPSG dedotto dai numeri','CRS geografico dichiarato nell’esercizio']], [4.5,4.5]),
 p(r'Il dataset contiene due rappresentazioni didattiche. Le coordinate geografiche derivano da una collocazione sintetica approssimata della griglia.')+
 info(r'Proiettare longitudine e latitudine produce coordinate UTM. Non ricostruisce esattamente le colonne locali per semplice sottrazione di un’origine.')+
 p(r'Conserveremo le colonne originali e indicheremo in ogni figura quale sistema è stato usato.'),
 r'Coordinate espresse in metri possono appartenere a sistemi diversi e non essere intercambiabili.', notebook=5, source=[6,7])

slide(16,'Primo laboratorio: descrivere il dato',
 experiment('supporto','Esperimento online · dato e supporto')+
 table(['Consegna','Evidenza richiesta'],[
 ['Una tabella documentata','ID, unità, supporto e provenienza'],
 ['Una carta di punti','Assi, scala cromatica, siti visibili'],
 ['Un controllo di integrità','Conteggi e valori mancanti'],
 ['Una domanda scientifica','Quantità da descrivere o prevedere']], [3.7,5.3]),
 p(r'N01 verifica la tabella; N07 costruisce la carta iniziale. N17 tornerà sulla distinzione tra medie dei siti e medie dei blocchi.')+
 info(r'Prima di procedere, spiegare a parole che cosa rappresenta ogni punto. Se la risposta cambia dopo un’aggregazione, deve cambiare anche la descrizione del risultato.')+
 p(r'Il fascicolo passa ora dai luoghi come metadati ai luoghi come oggetti su cui calcolare distanze.'),
 r'Un’analisi spaziale comincia con una descrizione verificabile dell’unità osservata.', notebook=1, source=[3,5,32])

slide(17,'I numeri delle coordinate richiedono una metrica',
 coordinates(),
 p(r'Un numero come 9 o 500000 non identifica un luogo senza sistema di riferimento e ordine degli assi. Anche l’unità deve essere nota.')+
 info(r'La distanza euclidea tra due colonne numeriche è sempre calcolabile. Il suo significato fisico dipende da ciò che rappresentano quelle colonne.')+
 p(r'Per le operazioni locali usiamo metri nel piano. Per longitudine e latitudine dichiariamo la geometria terrestre adottata.'),
 r'La metrica traduce coordinate in distanze interpretabili.', source=[6,8])

slide(18,'Invertire gli assi può superare i controlli globali',
 fig('04_coordinate_invertite',r'Le coppie (9°,45°) e (45°,9°) rispettano entrambe i limiti globali, ma indicano luoghi diversi.'),
 p(r'La longitudine deve trovarsi tra $-180^\circ$ e $180^\circ$; la latitudine tra $-90^\circ$ e $90^\circ$. Sono condizioni necessarie, non una prova dell’ordine corretto.')+
 info(r'Nel caso guida servono anche un’area attesa e metadati affidabili. Scambiare le colonne può spostare i punti senza generare un errore numerico.'),
 r'Un valore plausibile per intervallo può essere sbagliato per posizione.',
 code('ok_limiti <- function(lon,lat) {\n all(abs(lon)<=180 & abs(lat)<=90)\n}\nc(corretti=ok_limiti(d$lon,d$lat),\n invertiti=ok_limiti(d$lat,d$lon))','R · limiti necessari, non sufficienti'), notebook=2, source=[6])

slide(19,'La distanza euclidea nel piano locale',
 eq(r'd_{ij}=\sqrt{(x_i-x_j)^2+(y_i-y_j)^2}')+
 fig('05_distanze_piano',r'Distanze in metri. Il passo ortogonale è 250 m; la diagonale della cella è $250\sqrt 2$ m.',height=4.6),
 p(r'La metrica usa la stessa unità sui due assi. La matrice delle distanze deve essere simmetrica, non negativa e nulla sulla diagonale.')+
 info(r'La diagonale principale collega ogni sito a se stesso. La escluderemo quando cercheremo vicini o coppie distinte.'),
 r'Il calcolo della distanza richiede assi e unità coerenti.',
 code('D <- as.matrix(dist(xy))\nstopifnot(all(diag(D)==0),\n isTRUE(all.equal(D,t(D))),\n all(D>=0))','R · matrice delle distanze'), notebook=3, source=[8])

slide(20,'Traslazioni e rotazioni conservano le distanze',
 eq(r's_i^\star=Q\,s_i+b,\qquad Q^\top Q=I')+
 eq(r'\|s_i^\star-s_j^\star\|=\|s_i-s_j\|')+
 info(r'Cambiare origine o ruotare rigidamente gli assi non cambia le distanze. Moltiplicare tutte le coordinate per un fattore $a$ moltiplica le distanze per $|a|$.'),
 p(r'Queste proprietà offrono controlli del programma. Una conversione da metri a chilometri deve ridurre tutte le distanze di un fattore mille.')+
 p(r'Una proiezione geografica non è in generale una rotazione rigida: la sua distorsione va valutata nell’area d’uso.'),
 r'Gli invarianti geometrici sono controlli concreti della funzione di distanza.',
 code('shift <- sweep(xy,2,c(200,-300),"+")\nstopifnot(isTRUE(all.equal(\n as.matrix(dist(shift)),D)))\nstopifnot(isTRUE(all.equal(\n as.matrix(dist(xy/1000)),D/1000)))','R · verificare traslazione e scala'), notebook=3, source=[8])

slide(21,'Distanza orizzontale, tridimensionale o di percorso',
 table(['Metrica','Che cosa rappresenta'],[
 [r'$\sqrt{\Delta x^2+\Delta y^2}$','Separazione orizzontale nel piano'],
 [r'$\sqrt{\Delta x^2+\Delta y^2+\Delta h^2}$','Segmento tridimensionale'],
 ['Lunghezza su una rete','Percorso vincolato a collegamenti'],
 ['Distanza di costo','Percorso pesato da resistenze dichiarate']], [4.1,4.9]),
 p(r'La quota può entrare nella distanza, ma cambia il significato di vicino. Una distanza lungo il reticolo idrografico richiede una rete e una regola di percorso.')+
 info(r'In questo modulo i pesi principali usano la distanza orizzontale locale. La scelta resta costante quando confrontiamo Moran, copertura e interpolazione.')+
 p(r'Non aggiungiamo una variabile al calcolo della distanza soltanto perché è numerica.'),
 r'La distanza deve rappresentare la relazione fisica o il compito che si vuole studiare.', source=[8,13])

slide(22,'Sulla sfera si misura un arco',
 sphere(),
 p(r'Longitudine e latitudine sono angoli. Sulla sfera, la separazione più breve lungo la superficie è un arco di cerchio massimo.')+
 info(r'La Terra non è una sfera perfetta. Il modello sferico è un’approssimazione esplicita; un calcolo ellissoidale richiede i parametri del riferimento adottato.')+
 p(r'La funzione del laboratorio usa un raggio sferico dichiarato pari a 6\,371\,000 m. L’uscita è quindi in metri.'),
 r'La scelta della geometria terrestre appartiene alla definizione della distanza.', notebook=4, source=[8,9])

slide(23,'Haversine: angoli in radianti e unità esplicite',
 eq(r'a=\sin^2\frac{\Delta\varphi}{2}+\cos\varphi_1\cos\varphi_2\sin^2\frac{\Delta\lambda}{2}')+
 eq(r'd=2R\operatorname{atan2}\!\left(\sqrt a,\sqrt{1-a}\right)')+
 info(r'$\varphi$ indica la latitudine e $\lambda$ la longitudine, entrambe in radianti. Per stabilità numerica si limita $a$ all’intervallo $[0,1]$.'),
 p(r'La distanza deve essere zero tra punti coincidenti, simmetrica e finita. Il notebook controlla anche un arco semplice di ampiezza nota.')+
 p(r'La funzione esplicita permette di vedere la conversione dei gradi. L’ordine degli argomenti resta longitudine, latitudine.'),
 r'Una formula corretta produce distanze sbagliate se riceve gradi al posto di radianti.',
 code('h <- haversine(d$lon[1],d$lat[1],\n               d$lon[2],d$lat[2])\nstopifnot(is.finite(h),h>0)\nhaversine(0,0,1,0) # arco di 1 grado','R · arco sulla sfera'), notebook=4, source=[9])

slide(24,'Un grado non rappresenta una lunghezza fissa',
 fig('06_distanze_geografiche',r'Scarti delle distanze sferiche e UTM rispetto alle distanze locali, sulle stesse coppie di siti.'),
 p(r'La lunghezza di un grado di longitudine dipende dalla latitudine. Applicare una sola conversione ai due assi trascura questa geometria.')+
 info(r'In una piccola area una proiezione adatta offre coordinate metriche comode. L’adeguatezza resta legata all’area e alla precisione richiesta.')+
 p(r'Il confronto tra distanze locali, sferiche e proiettate serve a capire le assunzioni, non a imporre un’identità tra rappresentazioni costruite diversamente.'),
 r'Le differenze angolari devono essere trasformate con una geometria dichiarata.', notebook=4, source=[8,9])

slide(25,'Il CRS è un insieme di regole, non un’etichetta',
 table(['Elemento','Funzione'],[
 ['Riferimento geodetico','Colloca il sistema rispetto alla Terra'],
 ['Assi e unità','Definiscono ordine e significato dei numeri'],
 ['Proiezione, se presente','Trasforma la superficie in un piano'],
 ['Area d’uso','Indica dove il sistema è appropriato']], [3.3,5.7]),
 p(r'Il sistema di riferimento delle coordinate descrive come interpretare le geometrie. Il codice di un catalogo ne identifica una definizione.')+
 info(r'Per rendere esplicito l’ordine longitudine--latitudine usiamo \texttt{OGC:CRS84}. Il bersaglio proiettato del laboratorio è WGS 84 / UTM zona 32N, EPSG:32632.')+
 p(r'La scelta è riferita all’esempio sintetico vicino a 9° E e 45° N. Non costituisce una regola universale per ogni dataset.'),
 r'Un CRS corretto deve essere noto dalla provenienza dei dati o da una verifica indipendente.', notebook=5, source=[7])

slide(26,'Costruire una geometria conservando la tabella',
 eq(r'(\mathrm{id},z,\lambda,\varphi)\quad\longrightarrow\quad \text{oggetto sf}')+
 table(['Controllo','Risultato atteso'],[
 ['Numero di geometrie','64 punti'],
 ['Attributi','ID e misure preservati'],
 ['Ordine degli assi','Longitudine, latitudine'],
 ['CRS dichiarato','OGC:CRS84']], [3.5,5.5]),
 p(r'La geometria viene creata dalle colonne geografiche. Con \texttt{remove=FALSE} conserviamo anche i valori originari nella tabella.')+
 info(r'La creazione dell’oggetto assegna il significato dichiarato ai numeri. Non corregge un ordine degli assi sbagliato.'),
 r'Costruire una geometria richiede dati interpretabili prima della chiamata al software.',
 code('geo <- sf::st_as_sf(d,\n coords=c("lon","lat"),\n crs="OGC:CRS84",remove=FALSE)\nstopifnot(nrow(geo)==64L)\nsf::st_crs(geo)$input','R · punti geografici'), notebook=5, source=[7])

slide(27,'Trasformare cambia i numeri, conserva il luogo',
 fig('07_proiezione_UTM',r'Geometria sintetica in UTM 32N. Gli assi sottraggono origini dichiarate per rendere leggibili le coordinate.'),
 p(r'\texttt{st\_transform} calcola nuove coordinate usando il CRS di origine e quello di destinazione. Le unità del bersaglio diventano metri.')+
 info(r'Il calcolo è verificato con \texttt{sf} e le librerie geografiche effettivamente caricate. Le versioni sono registrate con i risultati.'),
 r'La trasformazione usa due definizioni di riferimento; non basta cambiare il nome del CRS.',
 code('utm <- sf::st_transform(geo,32632)\nhead(sf::st_coordinates(utm))\nstopifnot(!sf::st_is_longlat(utm))','R · proiettare i punti'), notebook=5, source=[7])

slide(28,'Il controllo di ritorno verifica la trasformazione',
 projection(),
 p(r'Trasformiamo i punti in UTM e torniamo a OGC:CRS84. La tolleranza del confronto è in gradi.')+
 info(r'Un ritorno accurato mostra coerenza numerica delle trasformazioni. La correttezza del CRS iniziale richiede una verifica della provenienza.'),
 r'Il controllo di ritorno verifica il procedimento numerico, mentre la provenienza verifica il riferimento.',
 code('rt <- sf::st_transform(utm,"OGC:CRS84")\ncr0 <- sf::st_coordinates(geo)\ncr1 <- sf::st_coordinates(rt)\nerr <- max(abs(cr1-cr0))\nstopifnot(err<1e-7); err','R · ritorno alle coordinate iniziali'), notebook=5, source=[7])

slide(29,'Rietichettare lascia invariati i numeri',
 table(['Operazione','Effetto'],[
 [r'\texttt{st\_set\_crs}','Assegna o sostituisce la definizione del CRS'],
 [r'\texttt{st\_transform}','Calcola coordinate nel CRS di destinazione'],
 ['Assegnazione errata','Numeri invariati, significato geografico alterato'],
 ['Correzione documentata','Richiede conoscere il vero CRS dei numeri']], [4.0,5.0]),
 p(r'Assegnare EPSG:32632 a una coppia di gradi non la converte in metri. La geometria diventa numericamente identica e semanticamente errata.')+
 info(r'Nel notebook N06 l’operazione sbagliata è costruita in un oggetto separato e il relativo avviso è acquisito come parte dell’esperimento.'),
 r'Cambiare la definizione del CRS e trasformare le coordinate sono operazioni distinte.',
 code('bad_crs <- suppressWarnings(\n sf::st_set_crs(geo,32632))\nstopifnot(identical(\n sf::st_coordinates(bad_crs),\n sf::st_coordinates(geo)))','R · osservare prima di rietichettare'), notebook=6, source=[7])

slide(30,'Confrontare distanze senza confondere i sistemi',
 table(['Calcolo','Interpretazione'],[
 ['Euclidea locale','Metri nel sistema convenzionale della griglia'],
 ['Haversine','Arco nel modello terrestre sferico'],
 ['Euclidea in UTM','Distanza nel piano della proiezione'],
 ['Geodetica ellissoidale','Richiede riferimento e algoritmo espliciti']], [3.8,5.2]),
 p(r'Le distanze vanno confrontate sulla stessa coppia di ID, mantenendo visibile il metodo usato.')+
 info(r'Una differenza piccola non autorizza a confondere i sistemi. Una differenza inattesa richiede di verificare unità, ordine degli assi, riferimento e area d’uso.'),
 r'Le unità uguali rendono possibile un confronto, ma non garantiscono l’equivalenza dei calcoli.',
 code('u_xy <- sf::st_coordinates(utm)\nd_utm <- as.matrix(dist(u_xy))\nc(locale=D[1,2],UTM=d_utm[1,2],\n sfera=haversine(d$lon[1],d$lat[1],\n                d$lon[2],d$lat[2]))','R · la stessa coppia di siti'), notebook=5, source=[8,9])

slide(31,'Laboratorio: coordinate sotto controllo',
 experiment('coordinate','Esperimento online · coordinate e metrica')+
 table(['Attività','Prova da conservare'],[
 ['N02: assi invertiti','Limiti globali e posizione attesa'],
 ['N03: distanza euclidea','Simmetria, diagonale, invarianti'],
 ['N04: haversine','Radianti, raggio, casi semplici'],
 ['N05: trasformazione','CRS di origine e controllo di ritorno'],
 ['N06: rietichettatura','Numeri invariati, significato alterato']], [4.1,4.9]),
 p(r'La consegna include una piccola tabella delle distanze fra coppie note. Ogni colonna deve indicare unità e metodo.')+
 info(r'La precisione numerica della trasformazione e l’accuratezza geografica dei dati sono due proprietà diverse. Il controllo deve nominarle correttamente.')+
 p(r'Con riferimenti e distanze definiti possiamo passare a confini, appartenenze e vicinati.'),
 r'Le operazioni spaziali diventano interpretabili quando i riferimenti sono espliciti e verificati.', notebook=6, source=[6,7,8,9,32])
