"""Memoria, esportazione e conclusione: pagine 103–110."""
from componenti import *

slide(103,'La memoria cresce con celle, bande e precisione',
 fig('39_memoria',r'Dimensione teorica dei valori numerici. File compresso, oggetti in memoria e copie temporanee hanno costi differenti.')+
 eq(r"""B=n_r\,n_c\,n_b\,q"""),
 p(r'$q$ è il numero di byte per valore. Dimezzare il passo su entrambi gli assi quadruplica le celle sullo stesso dominio.')+
 info(r'La formula conta soltanto i valori: non include metadati, maschere, indici e copie temporanee. Aprire un SpatRaster non carica automaticamente tutti i pixel.'),
 r'La strategia di memoria deve essere dimensionata prima di materializzare grandi array.',
 code('nr <- 10000; nc <- 10000; nb <- 4\nbyte_valori <- nr*nc*nb*8\nc(GB=byte_valori/1e9,\n GiB=byte_valori/1024^3)','R · stima senza allocazione'),notebook=18,source=[29])

slide(104,'Leggere una finestra conserva ordine e posizioni',
 fig('40_finestra_halo',r'La finestra centrale contiene 6×8 celle. Il contorno aggiuntivo permette di calcolare le derivate senza perdere i vicini.'),
 p(r'Leggiamo 48 valori dal GeoTIFF e li confrontiamo con le stesse celle della matrice completa.')+
 sm(r'Questo riferimento completo è praticabile sul piccolo dataset didattico.'),
 r'Una lettura parziale deve restituire gli stessi valori e lo stesso ordine della porzione corrispondente.',
 code('terra::readStart(r)\nwin <- terra::readValues(r,row=5,\n nrows=6,col=10,ncols=8,mat=FALSE)\nterra::readStop(r)\nattesi <- as.vector(t(M[5:10,10:17]))\nstopifnot(length(win)==48,\n max(abs(win-attesi))<1e-10)','R · finestra realmente letta'),notebook=18,source=[29])

slide(105,'Le operazioni locali richiedono un bordo di lettura',
 halo(),
 p(r'Per calcolare le differenze centrate sulle 6×8 celle richieste, leggiamo anche una cella di contorno: una finestra di 8×10, pari a 80 valori.')+
 info(r'Calcoliamo sul dominio allargato e conserviamo soltanto il nucleo. La dimensione del contorno dipende dal vicinato dell’algoritmo.')+
 p(r'Il confronto con il calcolo completo verifica che la strategia per finestre non introduca discontinuità artificiali.'),
 r'Ridurre la memoria deve preservare i vicinati necessari al procedimento scientifico.',notebook=18,source=[14,29])

slide(106,'Geometria della pendenza esportata',
 fig('41_export_pendenze',r'Griglia completa con 104 celle di bordo NoData. Il riquadro identifica il prodotto interno di 22×28 celle, con passo 30 m.'),
 p(r'Il prodotto interno contiene 616 valori. Il prodotto completo conserva invece la griglia 24×30 e 104 celle di bordo NoData.')+
 info(r'La geometria viene costruita dai centri e dai mezzi passi. Esportare la sola matrice senza questi metadati perderebbe la collocazione.'),
 r'Il raster derivato deve rappresentare gli stessi luoghi ai quali il calcolo si riferisce.',
 code('r_out <- raster_locale(slope_deg,\n x[2:29],y[2:23])\nstopifnot(terra::ncell(r_out)==616,\n all(terra::res(r_out)==30))','R · ricostruire il raster interno'),notebook=20,source=[30])

slide(107,'Il GeoTIFF conserva geometria e NoData',
 table(['Elemento','Scelta della consegna'],[
 ['Variabile','Pendenza in gradi'],
 ['Algoritmo','Differenze centrate, quattro vicini'],
 ['Riferimento','EPSG:32632, collocazione fittizia'],
 ['Tipo numerico','FLOAT64 / FLT8S'],
 ['NoData','−9999, distinto dai valori validi'],
 ['Accompagnamento','CSV, metadati e verifiche']], [3.8,5.2]),
 p(r'Scriviamo esplicitamente formato numerico e codice mancante. Il GeoTIFF mantiene la geometria, mentre la documentazione conserva il significato scientifico.')+
 sm(r'Il percorso mostrato è locale e separato dagli originali.'),
 r'Il file esportato è una parte della consegna: metodo, unità e provenienza devono accompagnarlo.',
 code('file_tif <- file.path("Risultati",\n "pendenze_slide.tif")\nterra::writeRaster(r_out,file_tif,\n overwrite=TRUE,datatype="FLT8S",\n NAflag=-9999,gdal="COMPRESS=NONE")','R · scrittura verificabile'),notebook=20,source=[30])

slide(108,'Rileggere verifica ciò che verrà consegnato',
 fig('42_controllo_roundtrip',r'Confronto fra valori prima della scrittura e dopo la rilettura, insieme ai controlli della geometria e della maschera.'),
 p(r'Controlliamo numero di celle, CRS, risoluzione, estensione, NoData e valori. La sola presenza del file non verifica il contenuto.')+
 info(r'Per il prodotto completo verifichiamo anche le 104 celle di bordo mancanti e la corrispondenza delle 616 celle interne.'),
 r'Il controllo finale deve riguardare il file effettivamente destinato alla consegna.',
 code('rr <- terra::rast(file_tif)\nstopifnot(terra::compareGeom(r_out,rr),\n max(abs(terra::values(rr)-\n         terra::values(r_out)))<1e-10)','R · rilettura e confronto'),notebook=20,source=[30])

slide(109,'I 20 notebook seguono le decisioni della lezione',
 table(['Notebook','Tema','Slide'],[
 ['N01–N03','Griglia, orientamento, GeoTIFF','5–19'],
 ['N04–N06','Maschere, dominio e area','20–32'],
 ['N07–N08, N19','Aggregazione e allineamento','33–48'],
 ['N09–N11','Derivate, pendenza e direzione','49–66'],
 ['N12','Illuminazione del rilievo','67–76'],
 ['N13–N14','Bande e indice normalizzato','77–90'],
 ['N15–N17','Zone, dipendenza e blocchi','91–102'],
 ['N18, N20','Finestre ed esportazione','103–108']], [2.2,4.9,1.6]),
 p(r'Ogni notebook combina domanda, codice eseguito, risultati e interpretazione. Le risorse necessarie alla lettura sono incorporate negli HTML.')+
 info(r'I collegamenti nei piè di pagina aprono le attività nell’archivio estratto. Il formato R Markdown permette di modificare e rieseguire il lavoro.')+
 p(r'Per studiare: dichiarare il risultato atteso, ricostruire il controllo e spiegare quale errore sarebbe in grado di riconoscere.'),
 r'Il codice serve a rendere controllabile l’argomento scientifico, dalla geometria al risultato.',source=[30])

slide(110,'Griglia, metodo e significato restano collegati',
 boxes([('a',2.1,3.8,'Geometria e supporto',3.7,'GeoA'),
        ('b',7.3,3.8,'Valori e maschere',3.7,'GeoB'),
        ('c',2.1,1.2,'Metodo e scala',3.7,'GeoC'),
        ('d',7.3,1.2,'Risultato e verifica',3.7,'GeoA')],
       [('a','b',''),('a','c',''),('b','d',''),('c','d','')])+
 sm(r'Riferimenti: documentazione \href{https://rspatial.github.io/terra/}{terra}, '
    r'\href{https://gdal.org/en/stable/tutorials/geotransforms_tut.html}{GDAL}, '
    r'\href{https://www.usgs.gov/landsat-missions/landsat-normalized-difference-vegetation-index}{USGS}. '
    r'Fonti, versioni e verifiche complete accompagnano il pacchetto.'),
 p(r'Una buona analisi raster conserva il legame fra la posizione delle celle, il significato dei valori e le trasformazioni applicate.')+
 info(r'Prima di interpretare un risultato, chiedere: cambierebbe con un’altra risoluzione, una maschera diversa o un altro metodo?')+
 p(r'La consegna finale rende riconoscibili le scelte e permette di ripetere i controlli sui dati esportati.'),
 r'La geometria della griglia condiziona il significato delle misure che ricaviamo dal territorio.',source=[30])
