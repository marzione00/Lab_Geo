"""Apertura e geometria raster: pagine 2–19."""
from componenti import *

slide(2,'Dalle celle alle grandezze derivate',
 lab('Il percorso di Tessera')+table(['Passaggio','p.'],[
 [internal_link(6,'Definire la geometria raster'),'6'],
 [internal_link(20,'Conservare maschere e dominio'),'20'],
 [internal_link(33,'Cambiare risoluzione e allineare'),'33'],
 [internal_link(49,'Calcolare e verificare le derivate'),'49'],
 [internal_link(67,'Illuminare il rilievo'),'67'],
 [internal_link(77,'Confrontare bande spettrali'),'77'],
 [internal_link(91,'Riassumere zone e dipendenza'),'91'],
 [internal_link(103,'Esportare e rileggere i risultati'),'103']], [8.3,.7]),
 p(r'Locus ha collegato campioni, posizioni e relazioni spaziali. Tessera segue i valori quando il territorio è rappresentato da una griglia.')+
 info(r'Il caso guida è un terreno sintetico di 24 righe e 30 colonne. La georeferenziazione del GeoTIFF è fittizia: il file serve a verificare operazioni e convenzioni.')+
 p(r'I 20 notebook conservano gli identificativi M12\_N01--M12\_N20. Ogni attività collega un problema, il codice eseguito e una conclusione circoscritta.'),
 r'La geometria della griglia entra nel significato dei valori e delle grandezze derivate.',source=[2,30])

slide(3,'Dai campioni di Locus alle celle di Tessera',
 boxes([('a',2.1,3.8,'M11: campioni e supporti',3.7,'GeoA'),
        ('b',7.3,3.8,'M12: celle e geometria',3.7,'GeoB'),
        ('c',2.1,1.2,'Copertura e dipendenza',3.7,'GeoA'),
        ('d',7.3,1.2,'Scale e misure derivate',3.7,'GeoB')],
       [('a','b',''),('a','c',''),('b','d',''),('c','d','')])+
 eq(r"""Z(s)\quad\longrightarrow\quad Z_{ij}\text{ su una griglia dichiarata}"""),
 p(r'Un raster organizza il dominio in celle. Il valore di ogni cella può essere una misura, una categoria, una previsione o una sintesi su un supporto.')+
 info(r'La disposizione regolare facilita il calcolo, ma non rende indipendenti le osservazioni e non garantisce che ogni cella contenga una misura diretta.')+
 p(r'Coordinate, supporto e provenienza restano necessari anche quando la superficie appare continua sullo schermo.'),
 r'La continuità della carta è una proprietà della rappresentazione da interpretare insieme al dato.',source=[3,11,27])

slide(4,'Quattro domande prima del calcolo',
 table(['Domanda','Evidenza da conservare'],[
 ['Dove si trova ogni cella?','Riferimento, origine, passo e orientamento'],
 ['Che cosa significa il valore?','Variabile, unità, supporto e provenienza'],
 ['Quali celle sono valide?','Maschere, cause di esclusione e dominio'],
 ['Come cambia il risultato?','Metodo, parametri e scala di elaborazione']], [4.1,4.9]),
 p(r'La stessa matrice numerica può essere collocata in luoghi differenti. La stessa immagine può mostrare quote, intensità luminose oppure un indice spettrale.')+
 info(r'Il progetto conserverà dati, griglia e regole di trasformazione. La verifica finale rileggerà anche i file esportati.')+
 p(r'La copertina richiama celle e forme del paesaggio. Nelle figure scientifiche ogni colore e ogni misura avranno unità e metodo espliciti.'),
 r'Prima dell’algoritmo occorre dichiarare geometria, significato dei valori e dominio valido.',source=[3,6,30])

slide(5,'Il caso guida: 720 celle di terreno sintetico',
 fig('dem_quota',r'24 righe, 30 colonne, passo 30 m. I centri locali vanno da 0 a 870 m verso Est e da 0 a 690 m verso Nord.'),
 p(r'Il file contiene quota e appartenenza alle zone didattiche A e B. Le bande spettrali saranno costruite in un esperimento distinto.')+
 info(r'Le quote non sono misure di un rilievo reale. La collocazione UTM del GeoTIFF è convenzionale e non coincide con i siti di Locus.')+
 p(r'Il terreno consente di riconoscere errori di orientamento, modifiche della scala e conseguenze del trattamento dei mancanti.'),
 r'Un caso sintetico rende verificabili i passaggi senza attribuire ai risultati una provenienza osservativa.',notebook=1,source=[3])

slide(6,'Il raster conserva valori e geometria',
 table(['Elemento','Nel caso guida'],[
 ['Dimensioni','24 righe e 30 colonne'],
 ['Passo della griglia','30 m lungo entrambi gli assi'],
 ['Valori','Quote sintetiche in metri'],
 ['Georeferenziazione','UTM 32N convenzionale, EPSG:32632'],
 ['Variabile categoriale','Zone sintetiche A e B'],
 ['Mancanti','Regola NoData dichiarata nel file']], [4.2,4.8]),
 p(r'La matrice raccoglie i valori. Origine, risoluzione, riferimento e orientamento stabiliscono la posizione delle celle.')+
 info(r'Due oggetti con 720 valori possono rappresentare griglie diverse. Confrontiamo i metadati prima di combinarli.')+
 sm(r'Gli originali sono conservati con revisione Git e impronte verificabili nel pacchetto.'),
 r'Numero di valori e dimensioni della matrice non identificano da soli un raster.',notebook=1,source=[3,6])

slide(7,'Righe e colonne diventano posizioni',
 fig('03_celle_centri',r'Dettaglio del raster locale: croci nei centri, bordi a mezzo passo. La cella centrata in $(0,0)$ si estende da −15 a 15 m sui due assi.',height=4.65)+
 eq(r"""x_j=x_0+j\Delta x,\qquad y_i=y_0+i\Delta y"""),
 p(r'Nella tabella originale gli indici partono da zero. Il centro della cella $(0,0)$ ha coordinate locali $(0,0)$ m.')+
 info(r'Qui $x$ cresce verso Est e $y$ verso Nord. Una convenzione diversa per le righe richiederebbe un segno diverso nella seconda relazione.')+
 p(r'La griglia disegnata è uno schema: il dataset completo contiene 24 righe e 30 colonne.'),
 r'Gli indici descrivono l’ordine in tabella; le coordinate descrivono la geometria dichiarata.',notebook=1,source=[4])

slide(8,'Il centro della cella e il suo angolo sono distinti',
 corner_centre(),
 p(r'La georeferenziazione del GeoTIFF parte dall’angolo superiore sinistro della cella in alto a sinistra. Il centro si trova mezzo passo all’interno.')+
 info(r'Con celle di 30 m, la differenza è 15 m in ciascuna direzione. Confondere angolo e centro sposta l’intera griglia di mezzo pixel.')+
 p(r'Nel file originale la convenzione è PixelIsArea. Il significato fisico del valore dipende comunque dal prodotto e dalla sua documentazione.'),
 r'Origine degli angoli e coordinate dei centri devono essere riconoscibili nei metadati.',notebook=3,source=[4,6])

slide(9,'La prima riga del GeoTIFF si trova a Nord',
 eq(r"""E_j=E_{\min}+\left(j+\tfrac12\right)\Delta x""")+
 eq(r"""N_i=N_{\max}-\left(i+\tfrac12\right)\Delta y""")+
 info(r'Indici $i,j$ da zero. Griglia senza rotazione: $E$ cresce verso Est, $N$ verso Nord; il numero di riga aumenta andando verso Sud.'),
 p(r'Il file ha angolo superiore sinistro $(500000,5000000)$ m. Il primo centro è quindi $(500015,4999985)$ m.')+
 p(r'Il segno meno nella coordinata Nord è una conseguenza dell’ordine delle righe. Non indica una distanza fisica negativa.')+
 sm(r'Per griglie ruotate la trasformazione affine comprende anche i termini incrociati fra riga e colonna.'),
 r'La formula dei centri dipende dal punto di origine e dall’orientamento delle righe.',notebook=3,source=[4,6])

slide(10,'L’estensione comprende celle intere',
 table(['Limite','Coordinata UTM convenzionale'],[
 ['Ovest / Est','500000 / 500900 m'],
 ['Sud / Nord','4999280 / 5000000 m'],
 ['Larghezza','30 colonne × 30 m = 900 m'],
 ['Altezza','24 righe × 30 m = 720 m'],
 ['Primo centro a Nord-Ovest','500015 / 4999985 m']], [4.1,4.9]),
 p(r'La distanza fra il primo e l’ultimo centro è inferiore alla dimensione del dominio di un passo intero.')+
 info(r'Nel piano locale l’estensione è $[-15,885]\times[-15,705]$ m. I limiti dei centri sono invece $[0,870]\times[0,690]$ m.'),
 r'Per calcolare l’estensione usiamo i bordi esterni, non soltanto gli estremi delle coordinate dei centri.',
 code('c(righe=nrow(r),colonne=ncol(r))\nterra::res(r)\nas.vector(terra::ext(r))','R · dimensioni e dominio'),notebook=3,source=[6,9])

slide(11,'Invertire le righe cambia l’orientamento',
 orientation(),
 p(r'La prima riga della matrice locale rappresenta il margine Sud. La prima riga restituita dal GeoTIFF rappresenta il margine Nord.')+
 info(r'Il diagramma mostra l’ordine degli elementi in memoria. Per confrontare le quote occorre invertire le righe di una delle due matrici.'),
 r'Media e istogramma non riconoscono l’inversione Nord–Sud: occorrono celle di posizione nota.',
 code('M <- as.matrix(r,wide=TRUE)\nZ_nord <- Z[nrow(Z):1,]\nmax(abs(M-Z_nord))','R · confrontare lo stesso ordine'),notebook=2,source=[5,6])

slide(12,'Una griglia completa richiede celle uniche',
 table(['Controllo','Problema riconosciuto'],[
 ['Coppia riga–colonna unica','Duplicato della stessa cella'],
 ['24 × 30 coppie attese','Cella assente nella tabella'],
 ['Passo di 30 m su ogni asse','Coordinate irregolari'],
 ['Ordinamento esplicito','Riempimento della matrice errato'],
 ['Mancanti conservati','Scorrimento dei valori successivi']], [4.3,4.7]),
 p(r'Una riga assente e una riga presente con valore mancante non hanno lo stesso effetto sulla ricostruzione della matrice.')+
 info(r'Il controllo delle chiavi viene prima di matrix(). Un ordinamento plausibile non basta a garantire che ogni valore occupi la propria cella.')+
 p(r'Per questo caso rettangolare confrontiamo la tabella con tutte le combinazioni ammesse di riga e colonna.'),
 r'La struttura della griglia va verificata prima di trasformare una colonna di valori in una matrice.',notebook=1,source=[4,5])

slide(13,'L’ordinamento rende riproducibile la ricostruzione',
 eq(r"""Z_{i+1,j+1}=z_{ij},\quad i=0,\ldots,23,\quad j=0,\ldots,29""")+
 info(r'Gli indici del file partono da zero; quelli della matrice R partono da uno. La corrispondenza esplicita evita uno spostamento di una cella.'),
 p(r'Ordiniamo prima le righe della tabella. Il riempimento per righe segue poi la convenzione locale da Sud verso Nord.')+
 sm(r'La proprietà byrow=TRUE deve essere letta insieme all’ordinamento del file.'),
 r'La stessa procedura deve ricostruire la griglia anche se l’ordine iniziale delle righe cambia.',
 code('d <- d[order(d$riga,d$colonna),]\nstopifnot(nrow(d)==720,\n !anyDuplicated(d[c("riga","colonna")]))\nZ <- matrix(d$quota_m,24,30,byrow=TRUE)\nstopifnot(Z[1,1]==d$quota_m[1])','R · ricostruire e controllare'),notebook=1,source=[5])

slide(14,'Un’inversione conserva l’istogramma',
 fig('orientamento_angoli',r'Controllo dei quattro angoli. La posizione dei valori viene confrontata dopo la conversione fra ordine locale e ordine Nord–Sud.'),
 p(r'Confrontare una cella riconoscibile mette alla prova la geometria. La media globale potrebbe restare identica anche con righe o colonne invertite.')+
 info(r'Il controllo usa identificativi e coordinate, oltre ai valori. La tolleranza numerica deve essere dichiarata separatamente dalla convenzione geometrica.')+
 p(r'Una mappa apparentemente regolare può conservare un errore sistematico di orientamento.'),
 r'La plausibilità visiva acquista valore quando è accompagnata da corrispondenze verificabili.',notebook=2,source=[5,6])

slide(15,'Un riferimento assegnato non sposta le celle',
 boxes([('a',2.1,3.8,'Coordinate e griglia esistenti',3.7,'GeoA'),
        ('b',7.3,3.8,'Riferimento dichiarato',3.7,'GeoC'),
        ('c',2.1,1.2,'Trasformazione delle posizioni',3.7,'GeoB'),
        ('d',7.3,1.2,'Griglia obiettivo e ricampionamento',3.7,'GeoB')],
       [('a','c',''),('b','d',''),('c','d','')]),
 p(r'Assegnare un CRS descrive l’interpretazione delle coordinate già presenti. Una riproiezione richiede invece di trasformare le posizioni e scegliere la griglia di uscita.')+
 info(r'Il GeoTIFF del corso possiede già un riferimento UTM fittizio. Non lo usiamo come prova che il terreno rappresenti una località reale.')+
 p(r'Per combinare raster servono anche estensione, origine, risoluzione e allineamento compatibili.'),
 r'Un codice EPSG comune è necessario in molte operazioni, ma non garantisce la coincidenza delle celle.',notebook=3,source=[6,13])

slide(16,'Leggere il GeoTIFF conserva i metadati',
 table(['Proprietà','Che cosa verificare'],[
 ['CRS','Riferimento e unità metriche'],
 ['Risoluzione','Passo di 30 m sui due assi'],
 ['Estensione','Bordi esterni convenzionali'],
 ['Tipo numerico','Precisione delle quote'],
 ['NoData','Codice distinto dai valori validi']], [3.4,5.6]),
 p(r'terra restituisce un oggetto SpatRaster che collega valori e geometria. L’apertura del file non richiede necessariamente di caricare tutti i valori in memoria.')+
 info(r'Il percorso è locale. Il pacchetto include il GeoTIFF originale e ne documenta la natura sintetica.'),
 r'Un file leggibile deve ancora essere confrontato con le caratteristiche attese.',
 code('r <- terra::rast("Dati/raster_v3.tif")\nterra::crs(r,describe=TRUE)\nstopifnot(terra::ncell(r)==720,\n all(terra::res(r)==30))','R · leggere dati e riferimento'),notebook=3,source=[6])

slide(17,'Collegare coordinate locali e GeoTIFF',
 eq(r"""E=x_{\mathrm{locale}}+500015""")+
 eq(r"""N=y_{\mathrm{locale}}+4999295""")+
 info(r'Questa relazione riguarda i centri delle celle del dataset sintetico. È una traslazione convenzionale, non una proiezione di coordinate geografiche.'),
 p(r'Il centro locale $(0,0)$ m corrisponde alla cella Sud-Ovest del GeoTIFF. Il centro locale $(870,690)$ m corrisponde alla cella Nord-Est.')+
 p(r'La relazione è ricavata dai bordi del file e dal mezzo passo. Verrà riutilizzata per esportare le celle interne senza traslarle.'),
 r'La conversione fra griglia locale e file georeferenziato deve conservare le posizioni dei centri.',notebook=3,source=[4,6,30])

slide(18,'Pixel e supporto della misura',
 table(['Valore nella cella','Interpretazione possibile'],[
 ['Quota di un DEM','Stima della superficie a una posizione'],
 ['Riflettanza','Segnale riferito al supporto del sensore'],
 ['Classe litologica','Categoria assegnata alla cella'],
 ['Media di quattro celle','Sintesi su un supporto più grande']], [4.2,4.8]),
 p(r'La cella è una parte della geometria raster. Il supporto fisico o statistico del valore dipende da come il prodotto è stato ottenuto.')+
 info(r'Nel caso guida le quote sono sintetiche e associate ai centri. L’aggregazione produce una media dei valori: non la confondiamo con una nuova misura sul terreno.')+
 p(r'Pixel più piccoli e sensori con maggiore capacità di risolvere dettagli sono proprietà da documentare separatamente.'),
 r'Per confrontare prodotti diversi servono il significato dei valori e la loro scala di rappresentazione.',source=[3,11])

slide(19,'Laboratorio: rendere riconoscibile ogni cella',
 experiment('griglia','Esperimento online · geometria raster')+
 table(['Attività','Risultato da conservare'],[
 ['N01: audit','720 coppie uniche, passo regolare'],
 ['N02: orientamento','Confronto dei quattro angoli'],
 ['N03: GeoTIFF','Dimensioni, CRS, estensione e risoluzione'],
 ['Corrispondenza','Centri locali e centri georeferenziati'],
 ['Conclusione','Natura sintetica e convenzioni esplicite']], [4.2,4.8]),
 p(r'Il primo prodotto del modulo è una scheda della griglia. Deve permettere a un’altra persona di ricostruire dove si trova ciascun valore.')+
 info(r'Se il controllo degli angoli fallisce, fermiamo la catena di elaborazione: pendenze, indici e sintesi erediteranno la geometria errata.')+
 p(r'Passiamo ora alle celle escluse e al dominio effettivamente descritto.'),
 r'Il controllo iniziale della geometria protegge tutte le elaborazioni successive.',notebook=3,source=[6,30])
