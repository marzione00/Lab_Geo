"""Consegna, controlli e studio autonomo: pagine 106–110."""
from componenti import *

slide(106,'Il progetto conserva dati, scelte e risultati',
 table(['Elemento','Contenuto minimo'],[
 ['Dati','ID, unità, supporto, CRS e provenienza'],
 ['Geometrie','Coordinate originali e trasformate'],
 ['Relazioni','Metrica, soglia, matrice e ordine degli ID'],
 ['Modelli','Formula, parametri, dominio di stima'],
 ['Verifica','Separazione geografica ed errori per sito'],
 ['Riproducibilità','Codice, versioni, risultati e limiti']], [3.4,5.6]),
 p(r'Il progetto parte da una domanda e termina con una conclusione circoscritta. Tabelle e figure devono permettere al lettore di verificare i passaggi.')+
 info(r'Il pacchetto contiene dati locali, sorgenti R, notebook eseguiti, figure e sorgenti XeLaTeX. Le mappe di raccordo collegano le nuove slide ai laboratori e alle pagine originali del sito.')+
 p(r'Il file geografico di consegna viene riletto prima di essere considerato pronto.'),
 r'Un risultato riproducibile conserva anche le convenzioni che collegano i numeri ai luoghi.', notebook=20, source=[31,32])

slide(107,'GeoJSON: geometrie geografiche e attributi',
 table(['Campo','Convenzione della consegna'],[
 ['Geometria','Point per ogni sito'],
 ['Coordinate','Longitudine, latitudine in gradi'],
 ['Riferimento','WGS 84 secondo RFC 7946'],
 ['Attributi','ID, concentrazione, quota e area'],
 ['Numero di elementi','64 feature con ID univoci']], [3.3,5.7]),
 p(r'GeoJSON conforme a RFC 7946 usa WGS 84 in ordine longitudine--latitudine. Le coordinate locali in metri non devono essere interpretate come gradi.')+
 p(r'Gli attributi restano associati agli ID.'),
 r'La consegna geografica deve conservare sia le posizioni sia l’identità delle osservazioni.',
 code('file_geo <- "Risultati/siti.geojson"\nsf::st_write(geo,file_geo,\n driver="GeoJSON",delete_dsn=TRUE,\n layer_options=c("RFC7946=YES",\n "COORDINATE_PRECISION=10"),quiet=TRUE)\ngeo_read <- sf::st_read(file_geo,\n                        quiet=TRUE)','R · scrivere e rileggere GeoJSON'), notebook=20, source=[31])

slide(108,'Rileggere verifica il contenuto consegnato',
 table(['Controllo','Esito atteso'],[
 ['Conteggio','64 feature'],
 ['Identità','Stesso insieme di ID, senza duplicati'],
 ['Attributi','Valori preservati con tolleranza dichiarata'],
 ['Coordinate','Errore entro la precisione di scrittura'],
 ['Riferimento','Geografico WGS 84'],
 ['Versioni','R, sf, GDAL, GEOS e PROJ registrati']], [3.4,5.6]),
 p(r'La rilettura può cambiare l’ordine delle righe. Confrontiamo quindi le osservazioni dopo averle allineate per ID.')+
 info(r'La presenza del file non garantisce che contenga geometrie, attributi e riferimento corretti. Il controllo deve riguardare il contenuto.'),
 r'Una consegna è verificata quando il file riletto rappresenta le stesse osservazioni.',
 code('j <- match(d$id,geo_read$id)\nstopifnot(!anyNA(j),\n !anyDuplicated(geo_read$id),\n nrow(geo_read)==nrow(d))\nstopifnot(max(abs(\n geo_read$concentrazione[j]-z))<1e-8)\nsf::sf_extSoftVersion()','R · controllo per identificativo'), notebook=20, source=[31])

slide(109,'I 20 notebook seguono il percorso della lezione',
 table(['Notebook','Tema','Slide'],[
 ['N01--N02','Audit e ordine degli assi','5--18'],
 ['N03--N04','Distanze nel piano e sulla sfera','19--24'],
 ['N05--N06','Proiezione e rietichettatura','25--31'],
 ['N07--N10','Carte, confini, join e buffer','32--43'],
 ['N11--N12','Vicinati e matrici dei pesi','44--55'],
 ['N13--N14','Moran e permutazioni','56--70'],
 ['N15','Coppie e semivarianza','71--81'],
 ['N16--N17','Copertura e medie di blocco','82--91'],
 ['N18--N20','Previsione, verifica e consegna','92--108']], [2.1,5.05,1.6]),
 p(r'Ogni notebook combina una domanda, il codice eseguito, risultati leggibili, controlli e commento scientifico. Gli HTML includono le risorse necessarie alla consultazione offline.')+
 info(r'I collegamenti nel piè di pagina aprono le attività corrispondenti nell’archivio estratto. Il formato R Markdown permette di modificare e rieseguire il lavoro.')+
 p(r'Per studiare: ricostruire prima la previsione o il conteggio atteso; poi leggere il risultato ed esplicitare una possibile causa di errore.'),
 r'Il codice serve a rendere controllabile l’argomento scientifico, non soltanto a produrre una figura.', source=[32])

slide(110,'Una conclusione che conserva i luoghi',
 boxes([('a',2.1,3.7,'Campioni e supporti',3.7,'GeoA'),
        ('b',7.3,3.7,'Relazioni dichiarate',3.7,'GeoC'),
        ('c',2.1,1.15,'Modello e bersaglio',3.7,'GeoB'),
        ('d',7.3,1.15,'Verifica geografica',3.7,'GeoA')],
       [('a','b',''),('a','c',''),('b','d',''),('c','d','')])+
 sm(r'Riferimenti: documentazione \href{https://r-spatial.github.io/sf/}{sf}, \href{https://r-spatial.github.io/spdep/}{spdep}, \href{https://r-spatial.github.io/gstat/}{gstat}; \href{https://www.rfc-editor.org/rfc/rfc7946}{RFC 7946}. Fonti e convenzioni complete nel pacchetto.'),
 p(r'Una buona analisi spaziale tiene insieme ciò che è stato misurato, dove è stato misurato e quali relazioni sono state assunte.')+
 info(r'Prima di accettare una conclusione, chiedere: cambierebbe con un altro supporto, un altro vicinato o una diversa zona di verifica?')+
 p(r'La carta finale deve rendere riconoscibili i campioni osservati, le quantità stimate e il territorio a cui la conclusione può essere riferita.'),
 r'La posizione non è un accessorio del dato: entra nella domanda, nel modello e nella verifica.', source=[3,5,29,30,31,32])
