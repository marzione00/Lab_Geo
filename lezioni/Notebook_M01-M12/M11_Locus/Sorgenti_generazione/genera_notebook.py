from pathlib import Path
import json,re,hashlib,csv,textwrap,shutil
HERE=Path(__file__).resolve().parent
BASE=HERE.parent if HERE.name=='Sorgenti_generazione' else HERE.parent/'M11/03_Notebook_svolti/M11_Locus'
N=[]
T=[(BASE/'R/Originali_corso'/f'M11_N{i:02d}.R').read_text(encoding='utf-8').splitlines()[0].lstrip('# ') for i in range(1,21)]
def step(title,text,code,reading):return dict(title=title,text=text,code=textwrap.dedent(code).strip(),reading=reading)
def nb(question,objectives,data,steps,variant,error,answer):N.append(dict(title=T[len(N)],question=question,objectives=objectives,data=data,steps=steps,variant=variant,error=error,answer=answer))
DATA='64 siti sintetici su una griglia 8 × 8, con passo 250 m e coordinate locali x_m e y_m fra 0 e 1750 m. Questo piano locale non ha un codice EPSG. La concentrazione è sintetica, in unità arbitrarie (u.a.); la quota è in metri sintetici. Ogni riga descrive un sito e il suo valore puntuale, non la media di una cella.'
GEO=DATA+' Le colonne lon e lat forniscono un georiferimento sintetico separato, vicino a 9° E e 45° N, costruito con una relazione approssimata. Non sono coordinate UTM ottenute aggiungendo un’origine alle coordinate locali. Nel percorso geografico l’ordine è sempre longitudine, latitudine.'
LOAD='d <- carica_dati("spazio_v3.csv")\naudit_spazio(d)'
SF=LOAD+'\nrichiedi_sf()'

nb('Quali controlli rendono interpretabili le coordinate prima di una mappa?',
 ['Verificare identità, completezza e unità.','Riconoscere la griglia locale e il georiferimento separato.','Esportare un audit leggibile.'],GEO,[
 step('Identità e completezza','Un numero finito non garantisce una posizione corretta, ma duplicati e valori mancanti vanno individuati prima dell’analisi.',LOAD+'''
 controlli <- data.frame(controllo=c("64 siti","ID unici","Posizioni locali uniche",
   "Coordinate complete","Concentrazione completa"),
   esito=c(nrow(d)==64L,!anyDuplicated(d$id),!anyDuplicated(d[c("x_m","y_m")]),
     !anyNA(d[c("x_m","y_m","lon","lat")]),all(is.finite(d$concentrazione))))
 controlli
 stopifnot(all(controlli$esito))
 ''','I controlli verificano proprietà del file. Non dimostrano che le coordinate rappresentino un rilievo reale: il dataset è esplicitamente sintetico.'),
 step('Le colonne hanno unità diverse','Riportiamo gli intervalli senza usare la sola grandezza dei numeri per attribuire un sistema di riferimento.','''
 assi <- c("x_m","y_m","lon","lat")
 intervalli <- data.frame(asse=assi,
   minimo=vapply(d[assi],min,numeric(1)),massimo=vapply(d[assi],max,numeric(1)),
   unita=c("m locali","m locali","gradi Est","gradi Nord"))
 intervalli
 data.frame(asse=c("x_m","y_m"),livelli=c(length(unique(d$x_m)),length(unique(d$y_m))),
   passo_m=c(unique(diff(sort(unique(d$x_m)))),unique(diff(sort(unique(d$y_m))))))
 ''','La griglia ha otto livelli per asse. Per lon e lat, l’interpretazione geografica deriva dalla provenienza dichiarata e dall’ordine degli assi, non da un riconoscimento automatico.'),
 step('L’audit accompagna il dato','Una carta delle posizioni permette di riconoscere configurazioni inattese. L’aspetto uguale degli assi conserva la geometria locale.','''
 stile_grafico()
 plot(d$x_m,d$y_m,pch=19,col=palette_geo[1],asp=1,ylim=c(0,1900),
   xlab="x locale (m)",ylab="y locale (m)",main="64 siti su una griglia locale")
 text(d$x_m[c(1,8,57,64)],d$y_m[c(1,8,57,64)],d$id[c(1,8,57,64)],pos=3,cex=.8)
 write.csv(controlli,percorso_risultati("audit.csv"),row.names=FALSE)
 write.csv(intervalli,percorso_risultati("intervalli_coordinate.csv"),row.names=FALSE)
 ''','Il disegno mostra posizioni campionate. Il vuoto fra i punti non viene riempito con valori non osservati.')],
 step('Un duplicato introdotto in memoria','Aggiungere una copia del primo sito e individuarne tutte le occorrenze, senza modificare il CSV.','''
 copia <- rbind(d,d[1,])
 duplicati <- duplicated(copia$id)|duplicated(copia$id,fromLast=TRUE)
 copia[duplicati,c("id","x_m","y_m")]
 data.frame(righe=nrow(copia),id_distinti=length(unique(copia$id)),occorrenze_coinvolte=sum(duplicati))
 stopifnot(sum(duplicati)==2L,nrow(d)==64L)
 ''','Due righe non sono necessariamente due unità campionarie. L’audit deve identificare l’unità osservata prima di attribuire pesi alle righe.'),
 'Assegnare un EPSG alle coordinate locali soltanto perché sono espresse in metri, oppure chiamare media areale il valore di un sito.',
 'Un audit utile collega ID, coordinate, unità, supporto e provenienza. Qui distinguiamo un piano metrico locale senza EPSG da un georiferimento sintetico lon–lat: entrambi sono dichiarati, nessuno certifica un rilievo reale.')

nb('Un controllo dei limiti globali riconosce longitudine e latitudine scambiate?',
 ['Applicare controlli globali e contestuali.','Produrre un esempio che passa il controllo globale.','Esplicitare il ruolo della zona attesa.'],GEO,[
 step('I limiti ammissibili non bastano','Costruiamo la copia errata dello script originale: la longitudine riceve la latitudine e viceversa.',LOAD+'''
 invertite <- data.frame(lon=d$lat,lat=d$lon)
 globale <- abs(invertite$lon)<=180 & abs(invertite$lat)<=90
 locale <- invertite$lon>8 & invertite$lon<10 & invertite$lat>44 & invertite$lat<46
 data.frame(controllo=c("Limiti globali","Zona sintetica attesa"),
   passano=c(sum(globale),sum(locale)),totale=nrow(d))
 stopifnot(all(globale),!any(locale))
 ''','Tutti i valori scambiati sono ammissibili sul globo, ma nessuno cade nella zona attesa. La plausibilità numerica globale è un controllo debole.'),
 step('Il contesto è una condizione dichiarata','La zona 8–10° E e 44–46° N è un controllo del nostro esempio. Va scelta dalla fonte e dalla domanda, prima di guardare la mappa.','''
 corretta <- d$lon>8 & d$lon<10 & d$lat>44 & d$lat<46
 data.frame(caso=c("Originale","Invertito"),
   lon_primo=c(d$lon[1],invertite$lon[1]),lat_primo=c(d$lat[1],invertite$lat[1]),
   siti_nella_zona=c(sum(corretta),sum(locale)))
 stopifnot(all(corretta))
 ''','Una zona attesa non sostituisce i metadati del CRS. Riconosce questa inversione perché il contesto geografico è sufficientemente informativo.'),
 step('Il grafico rende visibile lo scambio','Mostriamo due insiemi di coppie ordinate sullo stesso piano angolare. È un controllo di coordinate, non una carta metrica per calcolare distanze.','''
 stile_grafico()
 plot(c(d$lon,invertite$lon),c(d$lat,invertite$lat),type="n",asp=1,
   xlab="Longitudine dichiarata (gradi)",ylab="Latitudine dichiarata (gradi)",
   main="Coordinate corrette e assi scambiati")
 points(d$lon,d$lat,pch=19,col=palette_geo[1])
 points(invertite$lon,invertite$lat,pch=17,col=palette_geo[2])
 legend("center",c("Ordine lon, lat","Ordine invertito"),pch=c(19,17),col=palette_geo[1:2],bty="n")
 write.csv(data.frame(id=d$id,globale=globale,locale=locale),
   percorso_risultati("controllo_inversione.csv"),row.names=FALSE)
 ''','Una mappa può disegnare correttamente numeri sbagliati. Il controllo della coppia ordinata deve precedere l’interpretazione geografica.')],
 step('Una zona troppo ampia perde potere diagnostico','Usare un intervallo che include sia 9 sia 45 per entrambi gli assi.','''
 zona_larga <- invertite$lon>0 & invertite$lon<50 & invertite$lat>0 & invertite$lat<50
 data.frame(siti_errati_accettati=sum(zona_larga),totale=nrow(d))
 stopifnot(all(zona_larga))
 ''','Il controllo perde efficacia quando la sua regione di accettazione è troppo ampia. La scelta del controllo è parte del ragionamento sul dato.'),
 'Considerare corretti tutti i punti che rispettano −180≤lon≤180 e −90≤lat≤90.',
 'Il controllo globale non riconosce questa inversione. Serve un controllo coerente con la zona attesa, accompagnato da metadati e ordine degli assi espliciti. Non tutti gli errori di coordinate sono individuabili dai soli intervalli.')

nb('Quali proprietà deve conservare una distanza euclidea nel piano locale?',
 ['Costruire una matrice di distanze in metri.','Controllare simmetria, diagonale e una distanza nota.','Verificare traslazioni, rotazioni e cambi di unità.'],DATA,[
 step('La matrice confronta tutte le coppie',r'Nel piano metrico usiamo $d_{ij}=\sqrt{(x_i-x_j)^2+(y_i-y_j)^2}$. La matrice ha 64 righe e 64 colonne, ma le coppie non ordinate sono molte meno.',LOAD+'''
 xy <- as.matrix(d[c("x_m","y_m")])
 D <- as.matrix(dist(xy))
 stopifnot(max(abs(D-t(D)))<1e-12,all(diag(D)==0),D[1,2]==250)
 data.frame(siti=nrow(D),celle=length(D),coppie_non_ordinate=choose(nrow(D),2),
   distanza_S01_S64_m=D[1,64])
 head(data.frame(id=d$id,distanza_da_S01_m=D[,1]),10)
 ''','La diagonale confronta ciascun sito con sé stesso. Le due metà della matrice ripetono le stesse distanze, quindi non rappresentano confronti distinti.'),
 step('Traslazioni e rotazioni conservano la geometria','Aggiungere un’origine o ruotare entrambi gli assi non deve cambiare le distanze. Il controllo è numerico, con una tolleranza esplicita.','''
 traslate <- sweep(xy,2,c(500000,4980000),"+")
 alfa <- pi/6;rotazione <- matrix(c(cos(alfa),sin(alfa),-sin(alfa),cos(alfa)),2,2)
 ruotate <- xy%*%rotazione
 confronto <- data.frame(trasformazione=c("Traslazione","Rotazione 30 gradi"),
   scarto_massimo_m=c(max(abs(as.matrix(dist(traslate))-D)),max(abs(as.matrix(dist(ruotate))-D))))
 confronto
 stopifnot(all(confronto$scarto_massimo_m<1e-8))
 ''','Aggiungere numeri alle coordinate conserva la distanza euclidea, ma non attribuisce al piano locale un CRS. Un’origine UTM apparentemente plausibile non costituisce un georiferimento.'),
 step('Il cambio di unità ha un effetto prevedibile','Convertire entrambi gli assi da metri a chilometri divide tutte le distanze per mille.','''
 D_km <- as.matrix(dist(xy/1000))
 stopifnot(max(abs(D_km-D/1000))<1e-12)
 stile_grafico()
 plot(d$x_m,d$y_m,pch=19,col=palette_geo[1],asp=1,
   xlab="x locale (m)",ylab="y locale (m)",main="Distanza fra due siti estremi")
 segments(d$x_m[1],d$y_m[1],d$x_m[64],d$y_m[64],col=palette_geo[2],lwd=2)
 write.csv(data.frame(id=d$id,distanza_da_S01_m=D[,1]),
   percorso_risultati("distanze_da_S01.csv"),row.names=FALSE)
 ''','La conversione usa la stessa scala su entrambi gli assi. Mescolare metri e chilometri nello stesso calcolo cambia la geometria in modo scorretto.')],
 step('Una scala diversa per un solo asse','Raddoppiare x mantenendo y invariata e confrontare tre distanze.','''
 deformate <- xy;deformate[,1] <- 2*deformate[,1]
 D2 <- as.matrix(dist(deformate))
 data.frame(coppia=c("S01-S02","S01-S09","S01-S64"),
   prima=D[1,c(2,9,64)],dopo=D2[1,c(2,9,64)])
 stopifnot(D2[1,2]==2*D[1,2],D2[1,9]==D[1,9])
 ''','La deformazione non è un semplice cambio di unità comune: favorisce una direzione rispetto all’altra.'),
 'Usare dist su lon e lat e chiamare metri il risultato, oppure interpretare le due metà di D come coppie indipendenti.',
 'Una distanza locale verificabile conserva simmetria, diagonale nulla e invarianti geometrici. Le coordinate devono avere unità compatibili; un calcolo in gradi richiede un modello geografico diverso.')

nb('Come si trasforma una separazione angolare in un arco di lunghezza dichiarata?',
 ['Convertire gradi in radianti.','Applicare haversine con il raggio dello script originale.','Distinguere modello sferico, piano locale ed ellissoide.'],GEO,[
 step('L’arco usa angoli in radianti',r'La formula sferica è $d=2R\arcsin\sqrt{h}$, con $h=\sin^2(\Delta\varphi/2)+\cos\varphi_1\cos\varphi_2\sin^2(\Delta\lambda/2)$. Qui $R=6371$ km, come nel laboratorio originale.',LOAD+'''
 lon <- d$lon*pi/180;lat <- d$lat*pi/180
 h <- sin((lat-lat[1])/2)^2+cos(lat)*cos(lat[1])*sin((lon-lon[1])/2)^2
 km <- 2*6371*asin(sqrt(pmin(1,pmax(0,h))))
 stopifnot(km[1]==0,all(km>=0))
 head(data.frame(id=d$id,distanza_sferica_km=km),10)
 ''','Il limite fra zero e uno protegge la funzione inversa da piccoli errori numerici. Il risultato è un arco su una sfera del raggio dichiarato, non una geodetica ellissoidale.'),
 step('Una seconda implementazione controlla il calcolo','La funzione di servizio usa la stessa formula. Il confronto con le distanze locali riguarda due rappresentazioni sintetiche collegate approssimativamente.','''
 altro <- haversine_km(d$lon[1],d$lat[1],d$lon,d$lat)
 euclidea_m <- sqrt((d$x_m-d$x_m[1])^2+(d$y_m-d$y_m[1])^2)
 stopifnot(max(abs(km-altro))<1e-10)
 confronto <- data.frame(id=d$id,locale_m=euclidea_m,sfera_m=1000*km,
   differenza_m=1000*km-euclidea_m)
 confronto[c(1,8,57,64),]
 ''','Una differenza piccola in questo esempio non rende intercambiabili le coordinate. Il georiferimento lon–lat è stato costruito con una relazione approssimata e il modello terrestre è esplicito.'),
 step('Il confronto conserva le unità','Confrontiamo le due distanze nella stessa unità e scriviamo entrambe le colonne.','''
 stile_grafico()
 plot(confronto$locale_m,confronto$sfera_m,pch=19,col=palette_geo[1],
   xlab="Distanza nel piano locale (m)",ylab="Arco sferico (m)",main="Due metriche dichiarate")
 abline(0,1,lty=2,col=palette_geo[2])
 write.csv(confronto,percorso_risultati("distanze_confrontate.csv"),row.names=FALSE)
 data.frame(massimo_scarto_m=max(abs(confronto$differenza_m)))
 ''','La bisettrice aiuta a vedere l’ordine di grandezza. Per quantificare uno scarto piccolo si usa la tabella, non lo spessore della linea.')],
 step('Cambiare il raggio dichiarato','Usare 6371.0088 km e misurare l’effetto del parametro, senza chiamarlo una trasformazione ellissoidale.','''
 km2 <- haversine_km(d$lon[1],d$lat[1],d$lon,d$lat,R=6371.0088)
 data.frame(raggio_originale_km=6371,raggio_variante_km=6371.0088,
   variazione_massima_m=max(abs(km2-km))*1000)
 stopifnot(max(abs(km2-km*(6371.0088/6371)))<1e-10)
 ''','La distanza scala linearmente con il raggio. Restano invariati gli angoli e l’ipotesi sferica.'),
 'Passare gradi a funzioni trigonometriche che aspettano radianti oppure confrontare chilometri e metri senza conversione.',
 'Haversine produce una lunghezza solo dopo aver dichiarato raggio e unità degli angoli. Il controllo su un punto coincidente e la conversione delle unità rendono il risultato verificabile; la sfera resta un modello geometrico.')

nb('Una trasformazione geografica può essere controllata tornando alle coordinate iniziali?',
 ['Eseguire st_transform con sf reale.','Controllare il ritorno in longitudine–latitudine.','Distinguere reversibilità numerica e validità del CRS sorgente.'],GEO,[
 step('L’oggetto geografico dichiara l’ordine','Usiamo OGC:CRS84 per rendere esplicito l’ordine longitudine, latitudine. È una precisazione dell’ingresso WGS84 del laboratorio originale. Nessun CRS viene assegnato a x_m/y_m.',SF+'''
 p <- sf::st_as_sf(d,coords=c("lon","lat"),crs="OGC:CRS84",remove=FALSE)
 data.frame(oggetti=nrow(p),geometria=as.character(unique(sf::st_geometry_type(p))),
   longlat=sf::st_is_longlat(p),sf_version=as.character(packageVersion("sf")))
 sf::sf_extSoftVersion()
 stopifnot(identical(sf::st_coordinates(p)[,1],d$lon),
   identical(sf::st_coordinates(p)[,2],d$lat))
 ''','L’output registra anche le librerie geografiche effettivamente utilizzate. Il codice richiede sf installato e non sostituisce la trasformazione con una formula manuale.'),
 step('La trasformazione cambia i numeri e le unità','EPSG:32632 identifica UTM zona32 Nord. I valori trasformati provengono dalla geometria lon–lat sintetica.','''
 q <- sf::st_transform(p,32632)
 xy <- sf::st_coordinates(q)
 risultato <- data.frame(id=d$id,est_UTM32N_m=xy[,1],nord_UTM32N_m=xy[,2])
 head(risultato,6)
 data.frame(EPSG=sf::st_crs(q)$epsg,unita=sf::st_crs(q)$units_gdal)
 stopifnot(!sf::st_is_longlat(q),sf::st_crs(q)$epsg==32632)
 ''','La proiezione produce metri in un sistema di riferimento specificato. Il fatto che anche le coordinate locali siano in metri non le rende coordinate UTM.'),
 step('Il ritorno misura la reversibilità numerica','Trasformiamo nuovamente in OGC:CRS84 e confrontiamo le due colonne originali con tolleranza 10⁻⁷ gradi.','''
 ritorno <- sf::st_coordinates(sf::st_transform(q,"OGC:CRS84"))
 scarti <- data.frame(asse=c("longitudine","latitudine"),
   massimo_scarto_gradi=c(max(abs(ritorno[,1]-d$lon)),max(abs(ritorno[,2]-d$lat))))
 scarti
 stopifnot(all(scarti$massimo_scarto_gradi<1e-7))
 stile_grafico()
 par(mar=c(4.6,8,3,1.2))
 plot(xy[,1],xy[,2],asp=1,pch=19,col=palette_geo[1],xaxt="n",
   xlab="Est UTM32N (m)",ylab="",main="Georiferimento sintetico trasformato")
 axis(1,at=pretty(xy[,1],n=3))
 mtext("Nord UTM32N (m)",side=2,line=6,las=0)
 write.csv(risultato,percorso_risultati("coordinate_UTM32N.csv"),row.names=FALSE)
 write.csv(scarti,percorso_risultati("controllo_ritorno.csv"),row.names=FALSE)
 ''','Il ritorno controlla il percorso numerico. Una trasformazione reversibile può comunque partire da un CRS attribuito erroneamente: la fonte va verificata separatamente.')],
 step('Sottrarre un’origine non ricostruisce il piano locale','Confrontare gli scostamenti UTM dal primo punto con x_m/y_m.','''
 delta <- sweep(xy,2,xy[1,],"-")
 confronto <- data.frame(asse=c("x","y"),
   massimo_scarto_m=c(max(abs(delta[,1]-d$x_m)),max(abs(delta[,2]-d$y_m))))
 confronto
 ''','Lo scarto riflette la relazione approssimata usata per costruire lon e lat. L’esempio vieta di presentare la griglia locale come semplice traslazione della griglia UTM.'),
 'Assegnare EPSG:32632 al piano locale oppure interpretare un ritorno preciso come prova che il CRS sorgente fosse giusto.',
 'Il controllo di ritorno documenta la reversibilità di st_transform. La validità geografica richiede ancora fonte, CRS e ordine degli assi corretti. Il georiferimento sintetico e il piano locale restano due rappresentazioni distinte.')

nb('Cambiare l’etichetta del CRS cambia davvero le coordinate?',
 ['Confrontare st_set_crs e st_transform.','Mostrare numericamente una rietichettatura errata.','Riconoscere il limite di un piano locale senza CRS.'],GEO,[
 step('La trasformazione corretta parte da un riferimento noto','Prepariamo la geometria lon–lat e la sua trasformazione metrica di confronto.',SF+'''
 p <- sf::st_as_sf(d,coords=c("lon","lat"),crs="OGC:CRS84")
 corretto <- sf::st_transform(p,32632)
 originali <- sf::st_coordinates(p)
 xy_corrette <- sf::st_coordinates(corretto)
 data.frame(caso=c("WGS84 lon-lat","UTM32N trasformato"),
   x=c(originali[1,1],xy_corrette[1,1]),y=c(originali[1,2],xy_corrette[1,2]))
 ''','L’operazione di trasformazione usa la relazione fra due sistemi di riferimento. I numeri cambiano perché cambia la rappresentazione della stessa geometria dichiarata.'),
 step('La rietichettatura conserva i numeri','Riproduciamo intenzionalmente l’errore del laboratorio. Togliere il CRS prima della rietichettatura evita un avviso del software, ma non rende corretta l’operazione.','''
 errato <- sf::st_set_crs(sf::st_set_crs(p,NA),32632)
 xy_errate <- sf::st_coordinates(errato)
 stopifnot(max(abs(xy_errate-originali))==0)
 data.frame(caso=c("ERRATO: etichetta 32632","Corretto: trasformazione"),
   primo_x=c(xy_errate[1,1],xy_corrette[1,1]),
   primo_y=c(xy_errate[1,2],xy_corrette[1,2]),unita_dichiarata="metri")
 ''','Nel caso errato, circa9 e45 vengono chiamati metri UTM senza aver subito una proiezione. L’assenza di un avviso non certifica la qualità dei metadati.'),
 step('La conseguenza si osserva tornando in gradi','Trasformiamo l’oggetto errato in coordinate geografiche e controlliamo la zona sintetica attesa.','''
 falsi <- sf::st_coordinates(sf::st_transform(errato,"OGC:CRS84"))
 in_zona <- falsi[,1]>8 & falsi[,1]<10 & falsi[,2]>44 & falsi[,2]<46
 risultato <- data.frame(id=d$id,lon_errata=falsi[,1],lat_errata=falsi[,2],nella_zona=in_zona)
 head(risultato,4)
 data.frame(siti_nella_zona=sum(in_zona),totale=nrow(d))
 stopifnot(!any(in_zona))
 write.csv(risultato,percorso_risultati("effetto_rietichettatura.csv"),row.names=FALSE)
 ''','La trasformazione interpreta fedelmente un’etichetta sbagliata e produce un’altra posizione. Per trovare l’errore serve un controllo esterno coerente con il contesto.')],
 step('Un piano senza CRS non si trasforma per tentativi','Chiedere a sf di trasformare il piano locale privo di CRS e catturare l’errore atteso, lasciando invariati i dati.','''
 locale <- sf::st_as_sf(d,coords=c("x_m","y_m"),crs=NA)
 errore_atteso <- tryCatch({sf::st_transform(locale,32632);NA_character_},
   error=function(e) conditionMessage(e))
 errore_atteso
 stopifnot(is.character(errore_atteso),!is.na(errore_atteso))
 ''','Questo errore è intenzionale e gestito nel codice. La soluzione scientifica richiede informazioni sul georiferimento; un EPSG inventato non risolve la mancanza di metadati.'),
 'Usare st_set_crs per «convertire in metri» oppure assegnare una zona UTM a una griglia locale perché i valori sembrano plausibili.',
 'st_set_crs modifica la dichiarazione; st_transform ricalcola la geometria fra CRS noti. La distinzione è verificabile nei numeri. Un piano locale senza riferimento va mantenuto tale finché manca una relazione geografica giustificata.')

nb('Che cosa mostra una carta di valori puntuali e che cosa rimane non osservato?',
 ['Associare colori a concentrazioni con una scala esplicita.','Conservare geometria e supporto puntuale.','Distinguere distribuzione marginale e disposizione spaziale.'],DATA,[
 step('Valori e scala cromatica','Prima della mappa riassumiamo l’intervallo e il numero di misure, mantenendo le unità arbitrarie del dato sintetico.',LOAD+'''
 data.frame(n=nrow(d),minimo=min(d$concentrazione),massimo=max(d$concentrazione),
   media=mean(d$concentrazione),deviazione_standard=sd(d$concentrazione),unita="u.a.")
 quantile(d$concentrazione,c(0,.25,.5,.75,1))
 ''','La sintesi marginale non usa le coordinate. Due configurazioni geografiche possono avere lo stesso istogramma e un’associazione spaziale diversa.'),
 step('I punti conservano il supporto osservato','Il grafico disegna soltanto i64 siti e usa una legenda continua per i20 intervalli cromatici.','''
 mappa_valori(d,"Valori puntuali: nessuna superficie interpolata")
 ''','Il colore si riferisce a un sito. Il bianco fra i punti non indica concentrazione nulla e non costituisce una previsione: rappresenta assenza di osservazione nella carta.'),
 step('La tabella rende la scala ricostruibile','Registriamo classe e colore di ogni misura senza sostituire il valore numerico originale.','''
 limiti <- seq(min(d$concentrazione),max(d$concentrazione),length.out=21)
 classe <- cut(d$concentrazione,limiti,include.lowest=TRUE,labels=FALSE)
 tab <- data.frame(id=d$id,x_m=d$x_m,y_m=d$y_m,concentrazione=d$concentrazione,
   classe=classe,colore=hcl.colors(20,"Viridis")[classe])
 head(tab,6)
 write.csv(tab,percorso_risultati("mappa_punti.csv"),row.names=FALSE)
 write.csv(data.frame(limite=limiti),percorso_risultati("scala_cromatica.csv"),row.names=FALSE)
 ''','La tabella permette di controllare il colore di un punto e di riutilizzare la stessa scala in un confronto.')],
 step('Stessi valori, altra disposizione','Invertire l’ordine dei valori sulle posizioni, conservando esattamente la distribuzione marginale.','''
 altra <- d;altra$concentrazione <- rev(d$concentrazione)
 stopifnot(identical(sort(altra$concentrazione),sort(d$concentrazione)))
 mappa_valori(altra,"Valori ricollocati, distribuzione marginale invariata")
 data.frame(media_originale=mean(d$concentrazione),media_ricollocata=mean(altra$concentrazione))
 ''','Questa ricollocazione è deterministica e illustrativa. Non è una procedura inferenziale e non rappresenta nuove misure.'),
 'Leggere come osservata tutta una superficie colorata o cambiare la scala cromatica fra due carte senza dichiararlo.',
 'Una carta di punti collega posizione e misura, lasciando visibili i luoghi non osservati. Distribuzione marginale, configurazione spaziale e superficie prevista sono tre oggetti distinti.')

nb('Come si assegna una posizione sul confine a una sola area?',
 ['Costruire una partizione esaustiva e disgiunta.','Dichiarare a quale lato appartiene x=1000.','Distinguere la partizione descrittiva dal test geografico.'],DATA,[
 step('Il confine usa una regola semiaperta','Nel laboratorio descrittivo Ovest significa x<1000 ed Est x≥1000. È una partizione32/32, diversa dallo split40/24 della validazione N19.',LOAD+'''
 ovest <- d$x_m<1000;est <- !ovest
 stopifnot(!any(ovest&est),all(ovest|est),sum(ovest)==32L,sum(est)==32L)
 aree <- ifelse(ovest,"Ovest","Est")
 table(aree)
 stopifnot(identical(aree,d$area))
 ''','L’uguaglianza con la colonna area controlla la convenzione del file. I punti sul confine sono assegnati a Est e non duplicati.'),
 step('La sintesi dipende dall’appartenenza','Calcoliamo la media puntuale in ciascuna area e conserviamo anche le numerosità.','''
 risultato <- data.frame(area=c("Ovest","Est"),n=c(sum(ovest),sum(est)),
   media=c(mean(d$concentrazione[ovest]),mean(d$concentrazione[est])))
 risultato
 data.frame(siti_sul_confine=sum(d$x_m==1000),area_assegnata=unique(aree[d$x_m==1000]))
 write.csv(risultato,percorso_risultati("sintesi_aree.csv"),row.names=FALSE)
 ''','La media descrive le misure dei siti assegnati. Non è automaticamente una media dell’intera superficie territoriale.'),
 step('Il disegno conserva il confine','La linea passa attraverso una colonna di punti: la regola logica specifica il lato a cui appartengono.','''
 stile_grafico()
 plot(d$x_m,d$y_m,pch=19,col=palette_geo[ifelse(ovest,1,2)],asp=1,
   xlab="x locale (m)",ylab="y locale (m)",main="Ovest x<1000; Est x>=1000")
 abline(v=1000,lty=2,col="grey40")
 data.frame(id=d$id[d$x_m==1000],x_m=d$x_m[d$x_m==1000],area=aree[d$x_m==1000])
 ''','Un confine disegnato non risolve da solo l’appartenenza. La regola deve essere parte del codice e dei metadati.')],
 step('Due disuguaglianze inclusive duplicano il confine','Usare x≤1000 e x≥1000 e contare le appartenenze doppie.','''
 A <- d$x_m<=1000;B <- d$x_m>=1000
 data.frame(punti=nrow(d),appartenenze=sum(A)+sum(B),punti_doppi=sum(A&B))
 stopifnot(sum(A&B)==8L)
 ''','La sovrapposizione può essere corretta se le aree sono intenzionalmente sovrapposte. È un errore se si voleva costruire una partizione.'),
 'Usare due limiti inclusivi e poi trattare la tabella come una partizione, oppure riutilizzare area per lo split predittivo di N19.',
 'Una partizione assegna ogni sito una sola volta. La regola x<1000 / x≥1000 documenta il confine; ha finalità descrittiva e non sostituisce il protocollo di validazione con soglia1250.')

nb('Perché unire punti e aree sovrapposte può produrre più righe che punti?',
 ['Costruire una relazione di appartenenza molti-a-molti.','Controllare le molteplicità prima di una media.','Conservare l’ID del sito come unità osservativa.'],DATA,[
 step('La relazione non è una partizione','Replichiamo il join didattico attraverso predicati sulle coordinate: A include x≤1250, B include x≥750. Le zone si sovrappongono; qui non si invoca st_join.',LOAD+'''
 a <- data.frame(id=d$id[d$x_m<=1250],zona="A")
 b <- data.frame(id=d$id[d$x_m>=750],zona="B")
 relazioni <- rbind(a,b)
 frequenze <- table(relazioni$id)
 data.frame(punti=nrow(d),relazioni=nrow(relazioni),siti_con_piu_appartenenze=sum(frequenze>1))
 stopifnot(nrow(relazioni)==88L,sum(frequenze>1)==24L)
 ''','Le88 righe descrivono relazioni sito–zona, non88 osservazioni indipendenti. Ventiquattro siti appartengono a entrambe le zone.'),
 step('La molteplicità modifica il peso delle osservazioni','Uniamo gli attributi per ID e confrontiamo la media sulle righe del join con quella sui siti.','''
 unione <- merge(relazioni,d,by="id",sort=FALSE)
 data.frame(unita=c("Sito originale","Relazione sito-zona"),
   n=c(nrow(d),nrow(unione)),media=c(mean(d$concentrazione),mean(unione$concentrazione)))
 aggregate(concentrazione~zona,data=unione,mean)
 table(unione$zona)
 ''','La media del join dà peso doppio ai siti sovrapposti. La differenza può essere piccola o grande; il problema è la modifica dell’unità e dei pesi, non una soglia numerica fissa.'),
 step('L’audit rende visibile la sovrapposizione','La mappa usa il numero di appartenenze per distinguere i siti ripetuti.','''
 molteplicita <- as.integer(frequenze[d$id])
 stile_grafico()
 plot(d$x_m,d$y_m,pch=19,col=palette_geo[molteplicita],asp=1,
   xlab="x locale (m)",ylab="y locale (m)",main="Sovrapposizione fra 750 e 1250 m")
 abline(v=c(750,1250),lty=2,col="grey50")
 write.csv(unione,percorso_risultati("relazioni_sito_zona.csv"),row.names=FALSE)
 data.frame(appartenenze=as.integer(names(table(molteplicita))),siti=as.integer(table(molteplicita)))
 ''','Le soglie sono inclusive, quindi anche le colonne sui confini contribuiscono alla sovrapposizione.')],
 step('Un riepilogo con una riga per sito','Conservare tutte le zone in un campo testuale per ID, evitando di scegliere arbitrariamente la prima relazione.','''
 elenco <- aggregate(zona~id,relazioni,function(x) paste(sort(unique(x)),collapse="+"))
 unico <- merge(d,elenco,by="id")
 head(unico[,c("id","zona","concentrazione")],8)
 stopifnot(nrow(unico)==64L,!anyDuplicated(unico$id))
 ''','La rappresentazione conserva la molteplicità senza cambiare il peso di un sito nelle sintesi. Per analisi specifiche delle zone si torna alla tabella delle relazioni.'),
 'Eliminare duplicati dopo il join senza capire perché esistono oppure trattare ogni relazione come un nuovo sito campionato.',
 'La cardinalità del join dipende dalla geometria e dal predicato. Le righe possono rappresentare relazioni, mentre l’unità campionaria resta il sito. ID e numerosità devono essere controllati prima di interpretare una sintesi.')

nb('Come cambia una sintesi quando aumenta il raggio attorno allo stesso centro?',
 ['Costruire appartenenze a dischi nel piano locale.','Confrontare numerosità e medie a tre raggi.','Riconoscere gli effetti di bordo e il supporto della media.'],DATA,[
 step('Il centro e il raggio definiscono la selezione','Il centro è(750,750)m e i raggi sono300,600,900m, come nel laboratorio originale. Il calcolo è euclideo nel piano locale.',LOAD+'''
 centro <- c(750,750);raggi <- c(300,600,900)
 dist0 <- sqrt((d$x_m-centro[1])^2+(d$y_m-centro[2])^2)
 selezione <- sapply(raggi,function(r) dist0<=r)
 risultato <- data.frame(raggio_m=raggi,n=colSums(selezione),
   media=vapply(seq_along(raggi),function(j) mean(d$concentrazione[selezione[,j]]),numeric(1)))
 risultato
 stopifnot(all(diff(risultato$n)>=0),all(!selezione[,1]|selezione[,2]),all(!selezione[,2]|selezione[,3]))
 ''','I dischi sono annidati e il numero di siti non può diminuire. La media, invece, può aumentare o diminuire perché cambia l’insieme selezionato.'),
 step('La scala cambia l’oggetto riassunto','La mappa mostra i dischi e i siti disponibili. Le parti di un disco fuori dalla griglia non contengono dati nel nostro archivio.','''
 stile_grafico()
 plot(d$x_m,d$y_m,pch=19,col="grey55",asp=1,xlim=c(-200,1800),ylim=c(-200,1800),
   xlab="x locale (m)",ylab="y locale (m)",main="Tre raggi, stesso centro")
 angolo <- seq(0,2*pi,length.out=201)
 for(j in seq_along(raggi)) lines(centro[1]+raggi[j]*cos(angolo),
   centro[2]+raggi[j]*sin(angolo),col=palette_geo[j],lwd=2)
 points(centro[1],centro[2],pch=4,cex=1.5,lwd=2)
 ''','Il buffer geometrico non crea copertura campionaria. La media calcolata riguarda i siti selezionati e non tutte le posizioni del disco.'),
 step('Esportare selezione e sintesi','La tabella di appartenenza permette di ricostruire i tre calcoli, compresi i casi esattamente sulla distanza limite.','''
 dettagli <- data.frame(id=d$id,distanza_dal_centro_m=dist0,
   entro300=selezione[,1],entro600=selezione[,2],entro900=selezione[,3])
 write.csv(dettagli,percorso_risultati("appartenenza_buffer.csv"),row.names=FALSE)
 write.csv(risultato,percorso_risultati("sintesi_buffer.csv"),row.names=FALSE)
 risultato
 ''','La convenzione≤include il bordo. Dichiarare centro, metrica, raggio e predicato rende riproducibile il supporto della sintesi.')],
 step('Lo stesso raggio sul bordo della griglia','Spostare il centro nell’angolo(0,0), mantenendo600m.','''
 dist_angolo <- sqrt(d$x_m^2+d$y_m^2)
 s <- dist_angolo<=600
 data.frame(centro=c("750,750","0,0"),raggio_m=600,
   n=c(sum(dist0<=600),sum(s)),
   media=c(mean(d$concentrazione[dist0<=600]),mean(d$concentrazione[s])))
 ''','La numerosità disponibile e la configurazione cambiano al bordo. Confrontare i due numeri richiede riconoscere che i siti selezionati e la copertura sono diversi.'),
 'Confondere una media dei punti entro il raggio con una media areale del disco, oppure scegliere il raggio dopo aver cercato la media più favorevole.',
 'Il raggio definisce una scala di osservazione. I confronti devono conservare centro, unità, inclusione del bordo e numerosità; una selezione più ampia non garantisce automaticamente una sintesi più rappresentativa.')

nb('Come si trova un vicino diverso dal sito stesso quando esistono pareggi?',
 ['Escludere la diagonale dalla ricerca.','Riconoscere i pareggi nella griglia regolare.','Dichiarare la regola usata per sceglierne uno.'],DATA,[
 step('La distanza da sé non è un vicino','La matrice euclidea ha diagonale nulla. Per cercare un altro sito, la sostituiamo con infinito soltanto nella copia usata dalla ricerca.',LOAD+'''
 D <- as.matrix(dist(d[c("x_m","y_m")]))
 ricerca <- D;diag(ricerca) <- Inf
 j <- apply(ricerca,1,which.min)
 risultato <- data.frame(id=d$id,vicino=d$id[j],distanza_m=ricerca[cbind(seq_len(nrow(d)),j)])
 head(risultato,10)
 stopifnot(all(risultato$id!=risultato$vicino),all(risultato$distanza_m==250),all(diag(D)==0))
 ''','Il risultato dista sempre250m, perché la griglia ha quel passo. La matrice originale rimane disponibile con diagonale nulla per altre operazioni.'),
 step('Un minimo può avere più soluzioni','Contiamo tutti i siti alla distanza minima. which.min restituisce il primo secondo l’ordine delle righe, non un vicino geograficamente privilegiato.','''
 minimi <- apply(ricerca,1,min)
 numero_pareggi <- rowSums(abs(ricerca-minimi)<1e-9)
 data.frame(vicini_alla_distanza_minima=as.integer(names(table(numero_pareggi))),
   siti=as.integer(table(numero_pareggi)))
 d$id[which(abs(ricerca[1,]-minimi[1])<1e-9)]
 stopifnot(all(numero_pareggi>=2L))
 ''','Angoli, bordi e interni hanno due, tre e quattro vicini equidistanti. Un algoritmo che sceglie un solo indice rompe il pareggio con una convenzione.'),
 step('Il collegamento scelto è una relazione diretta','Disegniamo le frecce selezionate e salviamo anche il numero delle alternative equivalenti.','''
 stile_grafico()
 plot(d$x_m,d$y_m,type="n",asp=1,xlab="x locale (m)",ylab="y locale (m)",
   main="Un vicino scelto per ordine delle righe")
 arrows(d$x_m,d$y_m,d$x_m[j],d$y_m[j],length=.06,col="grey60")
 points(d$x_m,d$y_m,pch=19,col=palette_geo[1])
 risultato$numero_pareggi <- numero_pareggi
 write.csv(risultato,percorso_risultati("vicino_piu_prossimo.csv"),row.names=FALSE)
 ''','La relazione ottenuta scegliendo un solo minimo non è necessariamente reciproca. Il vicinato simmetrico entro una soglia è un oggetto diverso, costruito in N12.')],
 step('Cambiare l’ordine può cambiare il vincitore','Invertire le righe, rifare la ricerca e riallineare per ID.','''
 inverso <- d[nrow(d):1,]
 Di <- as.matrix(dist(inverso[c("x_m","y_m")]));diag(Di) <- Inf
 ji <- apply(Di,1,which.min)
 vicini_i <- setNames(inverso$id[ji],inverso$id)
 confronto <- data.frame(id=d$id,prima=risultato$vicino,dopo=unname(vicini_i[d$id]))
 data.frame(scelte_cambiate=sum(confronto$prima!=confronto$dopo),siti=nrow(d))
 head(confronto,6)
 ''','La distanza minima resta250m, mentre l’identità scelta può cambiare. Per un’applicazione serve una politica dei pareggi esplicita e coerente.'),
 'Lasciare la diagonale a zero, oppure interpretare il primo minimo come l’unico vicino possibile.',
 'La ricerca esclude il sito stesso e separa distanza minima da scelta dell’identità. Su una griglia regolare i pareggi sono la regola: conservarne il numero rende visibile la convenzione dell’algoritmo.')

nb('Che cosa cambia quando ogni sito distribuisce peso totale uno sui propri vicini?',
 ['Costruire A binaria con soglia260m.','Normalizzare per riga e verificare W.','Riconoscere bordi, asimmetria e siti isolati.'],DATA,[
 step('A conserva la relazione binaria','La soglia260m include i vicini ortogonali a250m ed esclude le diagonali a circa353.6m. La relazione fra due siti è simmetrica.',LOAD+'''
 ps <- pesi_spaziali(d,260)
 A <- ps$A;nv <- ps$n_vicini;W <- ps$W
 data.frame(siti=nrow(A),collegamenti_non_diretti=sum(A)/2,S0_binario=sum(A),
   isolati=sum(nv==0),simmetrica=all(A==t(A)))
 table(nv)
 stopifnot(sum(A)==224L,all(A==t(A)),all(diag(A)==0),all(nv>0))
 ''','Ci sono112 collegamenti non diretti, rappresentati due volte nella matrice. Gli angoli hanno due vicini, i bordi tre e gli interni quattro.'),
 step('W rende ciascun lag una media locale',r'La normalizzazione usa $w_{ij}=a_{ij}/\sum_j a_{ij}$. Ogni riga non isolata somma a uno; il peso del singolo vicino dipende dal numero di vicini del sito che riceve la media.','''
 risultato <- data.frame(id=d$id,n_vicini=nv,somma_riga=rowSums(W))
 head(risultato,10)
 data.frame(S0_normalizzato=sum(W),scarto_somma=max(abs(rowSums(W)-1)),
   asimmetria_massima=max(abs(W-t(W))))
 stopifnot(max(abs(rowSums(W)-1))<1e-12,abs(sum(W)-64)<1e-12)
 data.frame(direzione=c("S01 verso S02","S02 verso S01"),peso=c(W[1,2],W[2,1]))
 ''','La geometria binaria è simmetrica, mentre W non lo è: un angolo assegna1/2 a ciascun vicino, un bordo1/3. Questo modifica il prodotto quadratico usato da Moran.'),
 step('La rete e il registro documentano la scelta','Mostriamo una sola volta ogni collegamento binario e conserviamo entrambe le matrici con gli ID.','''
 ind <- which(upper.tri(A)&A>0,arr.ind=TRUE)
 stile_grafico()
 plot(d$x_m,d$y_m,type="n",asp=1,xlab="x locale (m)",ylab="y locale (m)",main="Vicinato entro 260 m")
 segments(d$x_m[ind[,1]],d$y_m[ind[,1]],d$x_m[ind[,2]],d$y_m[ind[,2]],col="grey70")
 points(d$x_m,d$y_m,pch=19,col=palette_geo[1])
 dimnames(A) <- dimnames(W) <- list(d$id,d$id)
 write.csv(A,percorso_risultati("A_binaria.csv"))
 write.csv(W,percorso_risultati("W_normalizzata.csv"))
 write.csv(risultato,percorso_risultati("audit_pesi.csv"),row.names=FALSE)
 ''','Il disegno rappresenta la relazione, mentre il CSV conserva i pesi numerici. È necessario nominare la matrice quando si riporta un indice spaziale.')],
 step('Una soglia troppo piccola produce isolati','Ridurre la soglia a200m e controllare la normalizzazione senza dividere per zero.','''
 piccoli <- pesi_spaziali(d,200)
 data.frame(soglia_m=200,isolati=length(piccoli$isolati),somma_pesi=sum(piccoli$W))
 stopifnot(length(piccoli$isolati)==64L,all(is.finite(piccoli$W)),sum(piccoli$W)==0)
 ''','Qui nessuna relazione resta disponibile e Moran non è definito. Il codice conserva righe nulle e obbliga a discutere la scelta del vicinato; non inventa vicini.'),
 'Dividere righe isolate per zero o presumere che una normalizzazione per riga conservi la simmetria.',
 'W distribuisce peso totale uno sui vicini di ciascun sito e consente una media locale. I bordi cambiano i pesi e possono rendere W asimmetrica: A e W devono restare oggetti distinti e dichiarati.')

nb('Quale indice di Moran si ottiene con pesi binari e quale con pesi normalizzati?',
 ['Calcolare esplicitamente I con A binaria.','Confrontare il risultato con W normalizzata.','Collegare la pendenza del diagramma a I_W.'],DATA,[
 step('La formula conserva la somma dei pesi',r'Per una matrice $M$, $I_M=(n/S_0)\sum_{i,j}m_{ij}v_i v_j/\sum_i v_i^2$, con $v_i=z_i-\bar z$ e $S_0=\sum_{i,j}m_{ij}$. Il laboratorio originale usa pesi binari.',LOAD+'''
 ps <- pesi_spaziali(d,260);A <- ps$A;W <- ps$W
 v <- d$concentrazione-mean(d$concentrazione);n <- length(v)
 I_A <- n/sum(A)*sum(A*outer(v,v))/sum(v^2)
 controllo <- as.numeric(n/sum(A)*crossprod(v,A%*%v)/crossprod(v))
 data.frame(matrice="A binaria",Moran_I=I_A,n=n,S0=sum(A),prodotto_quadratico=controllo)
 stopifnot(abs(I_A-controllo)<1e-12,abs(I_A-moran_I(d$concentrazione,A))<1e-12)
 ''','Il valore dell’indice dipende dal vicinato e dai pesi. La forma matriciale e la somma esplicita costituiscono due controlli del medesimo calcolo.'),
 step('La normalizzazione modifica l’indice','Calcoliamo anche I_W senza chiamarlo lo stesso risultato. In questo dataset W ha somma totale pari a n.','''
 I_W <- n/sum(W)*sum(W*outer(v,v))/sum(v^2)
 confronto <- data.frame(matrice=c("A binaria","W per riga"),S0=c(sum(A),sum(W)),
   Moran_I=c(I_A,I_W))
 confronto
 write.csv(confronto,percorso_risultati("Moran_due_matrici.csv"),row.names=FALSE)
 ''','Il trattamento dei bordi cambia il contributo relativo delle coppie. Una differenza fra i due indici non è un errore di calcolo: è una differenza fra statistiche.'),
 step('La pendenza riguarda il lag costruito con W','Nel diagramma ogni punto associa uno scarto alla media degli scarti dei suoi vicini. La pendenza OLS coincide qui con I_W, non con I_A.','''
 lag_W <- as.numeric(W%*%v)
 retta <- lm(lag_W~v)
 pendenza <- unname(coef(retta)["v"])
 data.frame(intercetta=coef(retta)[1],pendenza=pendenza,I_W=I_W,I_A=I_A)
 stopifnot(abs(pendenza-I_W)<1e-12)
 stile_grafico()
 plot(v,lag_W,pch=19,col=palette_geo[1],xlab="Scarto dalla media (u.a.)",
   ylab="Media degli scarti vicini con W (u.a.)",main="Diagramma di Moran: pendenza I_W")
 abline(h=0,v=0,lty=2,col="grey70");abline(retta,col=palette_geo[2],lwd=2)
 ''','La centratura di v e S0=n spiegano l’identità. Non trasferire la pendenza al valore binario: occorre conservare la stessa matrice nella formula e nel grafico.')],
 step('Moran è invariato da una trasformazione affine comune','Moltiplicare tutte le concentrazioni per10 e aggiungere7, conservando i pesi.','''
 z2 <- 10*d$concentrazione+7
 I2 <- moran_I(z2,A)
 data.frame(I_originale=I_A,I_trasformato=I2,scarto=I2-I_A)
 stopifnot(abs(I2-I_A)<1e-12)
 ''','L’indice è adimensionale e usa scarti normalizzati. La semivarianza, invece, conserva il quadrato dell’unità del dato e cambia sotto una moltiplicazione.'),
 'Riportare I senza descrivere i pesi, oppure sovrapporre il valore binario alla retta del diagramma costruito con W.',
 'Moran confronta prodotti fra scarti vicini rispetto alla dispersione totale. A e W generano due statistiche distinte. Nel diagramma con lag W la pendenza è I_W nelle condizioni verificate, mentre il laboratorio originale conserva I_A.')

nb('Quanto è insolita l’associazione positiva rispetto a etichette ricollocate sulle stesse posizioni?',
 ['Conservare le100 permutazioni originali dal file u.','Usare il conteggio con correzione+1.','Distinguere precisione Monte Carlo e ipotesi di scambiabilità.'],DATA+' Le permutazioni originali derivano dai primi6400 valori u di casuali_comuni_v3.csv, in100 blocchi consecutivi da64.',[
 step('Statistica e riferimento sono dichiarati prima del conteggio','L’alternativa è un’associazione positiva. Le posizioni e A rimangono fisse; si permutano i valori centrati della concentrazione.',LOAD+'''
 A <- pesi_spaziali(d,260)$A
 v <- d$concentrazione-mean(d$concentrazione)
 f <- function(a) length(a)/sum(A)*sum(A*outer(a,a))/sum(a^2)
 osservato <- f(v)
 u <- carica_dati("casuali_comuni_v3.csv")$u
 B <- 100L
 stopifnot(length(u)>=B*length(v))
 data.frame(I_osservato=osservato,B=B,uniformi_usati=B*length(v),alternativa="positiva")
 ''','Il riferimento richiede che la ricollocazione dei valori sulle posizioni sia una rappresentazione appropriata dell’ipotesi nulla. Non è una prova automatica di un meccanismo geologico.'),
 step('I blocchi u ricostruiscono le permutazioni originali','L’ordine dei64 uniformi in ogni blocco genera una permutazione completa. Manteniamo la sequenza originale del sito.','''
 nullo <- sapply(seq_len(B),function(b) {
   ind <- ((b-1L)*64L+1L):(b*64L)
   stopifnot(!anyDuplicated(u[ind]))
   permutazione <- order(u[ind])
   f(v[permutazione])
 })
 eccedenze <- sum(nullo>=osservato)
 p <- (1+eccedenze)/(B+1)
 risultato <- data.frame(I=osservato,eccedenze=eccedenze,B=B,p_unilaterale=p,
   risoluzione=1/(B+1),media_permutata=mean(nullo))
 risultato
 stopifnot(p>=1/101,p<=1)
 ''','La correzione+1 evita un valore zero quando nessuna delle100 permutazioni supera l’osservato. La risoluzione minima è1/101; un numero piccolo non elimina le ipotesi del riferimento.'),
 step('La figura include anche l’osservato','L’asse orizzontale contiene sia le statistiche permutate sia l’osservato, anche quando quest’ultimo è lontano dall’istogramma.','''
 stile_grafico()
 hist(nullo,breaks=15,xlim=range(c(nullo,osservato)),col="#CFE2E5",border="white",
   xlab="Moran I con A binaria",main="100 permutazioni originali: alternativa positiva")
 abline(v=osservato,col=palette_geo[2],lwd=2,lty=2)
 legend("topright","I osservato",lty=2,lwd=2,col=palette_geo[2],bty="n")
 write.csv(data.frame(permutazione=seq_len(B),I=nullo),percorso_risultati("permutazioni_originali.csv"),row.names=FALSE)
 write.csv(risultato,percorso_risultati("riferimento_Moran.csv"),row.names=FALSE)
 ''','Il risultato riguarda la disposizione osservata rispetto a questo riferimento condizionato. Dipendenza spaziale, trend e processo generatore richiedono ulteriore interpretazione.')],
 step('Una variante con999 nuove permutazioni','Usare un nuovo seme esplicito per999 permutazioni generate da R. Questa variante non ricicla né prolunga artificiosamente il file u originale.','''
 set.seed(20261114)
 B2 <- 999L
 nullo2 <- replicate(B2,f(v[sample.int(length(v))]))
 p2 <- (1+sum(nullo2>=osservato))/(B2+1)
 data.frame(protocollo=c("Originale: file u","Variante: seed 20261114"),
   B=c(B,B2),p=c(p,p2),risoluzione=c(1/(B+1),1/(B2+1)))
 write.csv(data.frame(permutazione=seq_len(B2),I=nullo2),percorso_risultati("permutazioni_variante999.csv"),row.names=FALSE)
 ''','Più simulazioni affinano la risoluzione Monte Carlo, ma non aggiungono siti né rendono vera l’ipotesi di scambiabilità. I due protocolli restano identificati separatamente.'),
 'Riportare p=0, scegliere la coda dopo aver visto l’esito o trattare le permutazioni come nuovi campioni del territorio.',
 'Il conteggio con+1 produce un riferimento Monte Carlo verificabile per l’alternativa positiva. Le100 permutazioni originali sono riproducibili dal file u; l’interpretazione resta condizionata a posizioni, pesi e scambiabilità dichiarati.')

nb('Che cosa rappresentano le2016 differenze fra coppie di64 siti?',
 ['Calcolare semivarianze per coppie non ordinate.','Aggregare nelle quattro classi originali.','Mostrare che molte coppie condividono gli stessi siti.'],DATA,[
 step('Ogni coppia entra una sola volta',r'La quantità per coppia è $\gamma_{ij}=\tfrac12(z_i-z_j)^2$. Se z è in u.a., la semivarianza è in(u.a.)².',LOAD+'''
 D <- as.matrix(dist(d[c("x_m","y_m")]))
 G <- .5*outer(d$concentrazione,d$concentrazione,"-")^2
 ind <- which(upper.tri(D),arr.ind=TRUE)
 coppie <- data.frame(i=ind[,1],j=ind[,2],h=D[ind],gamma=G[ind])
 data.frame(siti=nrow(d),coppie=nrow(coppie),attese=choose(nrow(d),2),
   distanza_massima_m=max(coppie$h))
 stopifnot(nrow(coppie)==2016L,all(coppie$i<coppie$j))
 ''','Le2016 righe sono combinazioni dei64 siti. Non corrispondono a2016 repliche indipendenti del processo.'),
 step('Le classi conservano numerosità e distanza media','Usiamo gli intervalli originali(0,300],(300,600],(600,1000],(1000,2500]metri. Il punto grafico è collocato alla distanza media delle coppie nella classe.','''
 coppie$classe <- cut(coppie$h,c(0,300,600,1000,2500))
 risultato <- aggregate(cbind(h,gamma)~classe,coppie,mean)
 risultato$n <- as.numeric(table(coppie$classe)[as.character(risultato$classe)])
 risultato
 stopifnot(sum(risultato$n)==2016L,!anyNA(coppie$classe))
 ''','Le classi hanno ampiezze e numerosità differenti. Il loro confronto riassume distanze, direzioni e possibili trend: non dimostra da solo stazionarietà o un modello di variogramma.'),
 step('La curva è una sintesi empirica','Disegniamo le medie senza barre di errore basate sull’ipotesi infondata di coppie indipendenti.','''
 stile_grafico()
 plot(risultato$h,risultato$gamma,type="b",pch=19,col=palette_geo[1],
   ylim=c(0,max(risultato$gamma)*1.15),
   xlab="Distanza media della classe (m)",ylab="Semivarianza media (u.a.^2)",
   main="Semivariogramma empirico per quattro classi")
 text(risultato$h,risultato$gamma,labels=paste0("n=",risultato$n),pos=3,cex=.8)
 write.csv(risultato,percorso_risultati("semivarianza_classi.csv"),row.names=FALSE)
 write.csv(coppie,percorso_risultati("coppie_spaziali.csv"),row.names=FALSE)
 ''','Il numero n aiuta a leggere quanto materiale entra in ogni media. Non autorizza a trattare queste righe come osservazioni indipendenti per una stima ingenua dell’errore standard.')],
 step('Un solo sito compare in63 coppie','Rimuovere le coppie che coinvolgono S01 e contarne la distribuzione fra le classi.','''
 coinvolte <- coppie$i==1L | coppie$j==1L
 data.frame(coppie_con_S01=sum(coinvolte),coppie_restanti=sum(!coinvolte),
   attese_dopo_rimozione=choose(63,2))
 table(coppie$classe[coinvolte])
 stopifnot(sum(coinvolte)==63L,sum(!coinvolte)==choose(63,2))
 ''','Una sola misura influenza63 differenze. Questa condivisione è una ragione concreta per non chiamare indipendenti tutte le coppie.'),
 'Usare entrambe le metà della matrice o costruire intervalli con2016 gradi di libertà come se le coppie fossero indipendenti.',
 'La semivarianza riassume differenze quadratiche fra siti a distanza simile. Le coppie condividono misure e la curva dipende dalle classi: numerosità elevate non eliminano dipendenza, trend o incertezza sul modello spaziale.')

nb('Una media calcolata sui siti accessibili lungo una strada rappresenta tutta la griglia?',
 ['Confrontare i16 siti con y≤250 con i64 di riferimento.','Descrivere copertura e distanza dai siti selezionati.','Distinguere campionamento di convenienza e disegno probabilistico.'],DATA,[
 step('La selezione cambia la popolazione osservata','La strada del caso didattico è rappresentata dalla fascia y≤250m. La media della griglia è un riferimento finito noto nel dataset sintetico.',LOAD+'''
 strada <- d$y_m<=250
 confronto <- data.frame(campione=c("Griglia di riferimento","Fascia strada"),
   n=c(nrow(d),sum(strada)),media=c(mean(d$concentrazione),mean(d$concentrazione[strada])))
 confronto
 stopifnot(sum(strada)==16L)
 ''','La differenza fra medie riguarda questa griglia sintetica. Non viene interpretata come una stima di bias universale o come un test fra campioni indipendenti.'),
 step('La mappa rende visibile la copertura','La fascia contiene due righe della griglia. Le altre posizioni sono note nell’archivio, ma vengono escluse dal campione di convenienza.','''
 stile_grafico()
 plot(d$x_m,d$y_m,pch=19,col=ifelse(strada,palette_geo[2],"grey65"),asp=1,ylim=c(0,2150),
   xlab="x locale (m)",ylab="y locale (m)",main="Campionare vicino alla strada")
 abline(h=250,lty=2,col="grey50")
 legend("topleft",c("Siti selezionati","Altri siti della griglia"),pch=19,
   col=c(palette_geo[2],"grey65"),bty="n")
 ''','La disponibilità di molte misure vicine alla strada non crea informazione sulle aree lontane. Un disegno spaziale si valuta anche dalla disposizione delle posizioni.'),
 step('La distanza quantifica una parte della copertura','Calcoliamo per ciascuno dei64 siti di riferimento la distanza dal sito selezionato più vicino.','''
 distanze <- distanze_incrociate(d[c("x_m","y_m")],d[strada,c("x_m","y_m")])
 copertura <- apply(distanze,1,min)
 data.frame(distanza_media_m=mean(copertura),distanza_massima_m=max(copertura),
   siti_oltre500m=sum(copertura>500))
 write.csv(confronto,percorso_risultati("confronto_strada.csv"),row.names=FALSE)
 write.csv(data.frame(id=d$id,selezionato=strada,distanza_piu_vicino_m=copertura),
   percorso_risultati("copertura_strada.csv"),row.names=FALSE)
 ''','È una misura di copertura rispetto a64 posizioni di riferimento. Non è un errore di previsione e non misura da sola la rappresentatività dell’intero territorio continuo.')],
 step('Allargare la fascia cambia ancora il campione','Usare y≤500m e confrontare numerosità e media.','''
 piu_ampia <- d$y_m<=500
 data.frame(fascia=c("y<=250","y<=500"),n=c(sum(strada),sum(piu_ampia)),
   media=c(mean(d$concentrazione[strada]),mean(d$concentrazione[piu_ampia])))
 stopifnot(sum(piu_ampia)==24L)
 ''','Aggiungere siti può cambiare la sintesi senza trasformare la selezione in un campionamento probabilistico. Non conosciamo probabilità di inclusione che giustifichino correzioni automatiche.'),
 'Presentare la media della fascia come media territoriale o pensare che una numerosità maggiore compensi sempre una copertura concentrata.',
 'Accessibilità e posizione possono cambiare ciò che il campione rappresenta. Media, numerosità e copertura vanno discusse insieme; qui il confronto è descrittivo rispetto a una griglia sintetica interamente disponibile.')

nb('Quando la media delle medie coincide con la media delle singole osservazioni?',
 ['Costruire quattro blocchi con16 siti ciascuno.','Verificare la media pesata per numerosità.','Distinguere uguale peso ai blocchi e uguale peso ai siti.'],DATA,[
 step('La partizione bilanciata ha quattro gruppi','Le soglie1000m per x e y producono quattro blocchi da16 siti. Le etichette indicano la posizione relativa nella griglia locale.',LOAD+'''
 d$blocco <- paste0(ifelse(d$y_m>=1000,"N","S"),ifelse(d$x_m>=1000,"E","O"))
 sintesi <- aggregate(concentrazione~blocco,d,mean)
 numerosita <- table(d$blocco)
 sintesi$n <- as.numeric(numerosita[sintesi$blocco])
 sintesi
 stopifnot(all(sintesi$n==16L),sum(sintesi$n)==64L)
 ''','Il bilanciamento deriva dalla griglia e dalle soglie scelte. Non è una proprietà generale delle partizioni territoriali.'),
 step('Due formule coincidono nel caso bilanciato',r'La media dei siti è $\bar z=\sum_b n_b\bar z_b/\sum_b n_b$. La media semplice delle medie coincide con questa formula solo quando le numerosità sono uguali, salvo coincidenze numeriche.','''
 media_siti <- mean(d$concentrazione)
 media_blocchi <- mean(sintesi$concentrazione)
 media_pesata <- weighted.mean(sintesi$concentrazione,sintesi$n)
 data.frame(calcolo=c("Tutti i siti","Blocchi con peso uguale","Blocchi pesati per n"),
   valore=c(media_siti,media_blocchi,media_pesata))
 stopifnot(abs(media_siti-media_blocchi)<1e-12,abs(media_siti-media_pesata)<1e-12)
 ''','L’uguaglianza è un’identità delle medie su questi gruppi. Non dimostra che le medie puntuali siano medie areali dei blocchi.'),
 step('La consegna conserva i pesi','Mostriamo le medie per blocco e salviamo la numerosità insieme a ogni valore.','''
 stile_grafico()
 barplot(sintesi$concentrazione,names.arg=sintesi$blocco,col=palette_geo[1:4],
   ylab="Concentrazione media dei siti (u.a.)",main="Quattro blocchi: 16 siti ciascuno")
 write.csv(sintesi,percorso_risultati("medie_blocchi.csv"),row.names=FALSE)
 ''','Una tabella di medie priva di numerosità può impedire la ricostruzione della media dei siti. Per una media areale servono invece supporti e pesi coerenti con quella domanda.')],
 step('Due blocchi sbilanciati','Costruire l’esempio con2 valori pari a10 e8 valori pari a20.','''
 piccolo <- c(10,10);grande <- rep(20,8)
 medie <- c(mean(piccolo),mean(grande));n <- c(length(piccolo),length(grande))
 data.frame(peso=c("Uguale ai blocchi","Uguale ai siti"),
   media=c(mean(medie),weighted.mean(medie,n)))
 stopifnot(mean(medie)==15,weighted.mean(medie,n)==18,mean(c(piccolo,grande))==18)
 ''','15 e18 rispondono a domande diverse: uguale peso ai due blocchi oppure ai dieci siti. Il peso corretto dipende dall’oggetto da stimare, non dal desiderio di ottenere una media particolare.'),
 'Calcolare una media semplice di medie con numerosità diverse senza dichiarare che si sta dando uguale peso ai gruppi.',
 'La media dei siti si ricostruisce pesando le medie di gruppo per le rispettive numerosità. Nel caso bilanciato le formule coincidono; cambiando supporto o obiettivo, i pesi devono essere nuovamente giustificati.')

nb('Come si costruisce una previsione IDW e quali limiti impongono i suoi pesi?',
 ['Calcolare le tre potenze originali nel punto(900,900).','Verificare normalizzazione e limite all’intervallo osservato.','Dichiarare il comportamento con siti coincidenti.'],DATA,[
 step('Il punto richiesto non coincide con un sito','Manteniamo la posizione(900,900)m e le potenze1,2,3 dello script originale. Non c’è un valore osservato in quella posizione da usare per scegliere la potenza.',LOAD+'''
 posizione <- c(900,900);xy <- as.matrix(d[c("x_m","y_m")])
 r <- sqrt((d$x_m-posizione[1])^2+(d$y_m-posizione[2])^2)
 stopifnot(all(r>0))
 data.frame(x_m=posizione[1],y_m=posizione[2],distanza_minima_m=min(r),distanza_massima_m=max(r))
 ''','La richiesta è una previsione puntuale nel piano locale. La posizione e l’esponente vanno dichiarati prima di interpretare il numero restituito.'),
 step('I pesi sono positivi e sommano a uno',r'Per distanze positive, $w_i=r_i^{-p}/\sum_jr_j^{-p}$ e $\hat z=\sum_iw_i z_i$. L’esponente maggiore concentra più peso sui siti vicini.','''
 potenze <- 1:3
 pesi <- sapply(potenze,function(p) {w<-r^-p;w/sum(w)})
 q <- as.numeric(crossprod(d$concentrazione,pesi))
 risultato <- data.frame(potenza=potenze,previsione=q,somma_pesi=colSums(pesi),
   peso_massimo=apply(pesi,2,max))
 risultato
 stopifnot(max(abs(colSums(pesi)-1))<1e-12,all(pesi>=0),
   all(q>=min(d$concentrazione)&q<=max(d$concentrazione)))
 ''','La previsione è una combinazione convessa dei valori usati. Non può oltrepassarne l’intervallo e non possiede automaticamente un intervallo d’incertezza statistica.'),
 step('Il registro rende esplicita l’influenza dei siti','Confrontiamo i pesi in funzione della distanza e salviamo ogni contributo.','''
 ordine <- order(r)
 stile_grafico()
 matplot(r[ordine],pesi[ordine,],type="l",lty=1,col=palette_geo[1:3],lwd=2,
   xlab="Distanza dal punto richiesto (m)",ylab="Peso normalizzato",main="IDW: sensibilita alla potenza")
 legend("topright",paste("p=",potenze),col=palette_geo[1:3],lty=1,lwd=2,bty="n")
 write.csv(risultato,percorso_risultati("IDW_potenze.csv"),row.names=FALSE)
 write.csv(data.frame(id=d$id,distanza_m=r,p1=pesi[,1],p2=pesi[,2],p3=pesi[,3]),
   percorso_risultati("IDW_pesi.csv"),row.names=FALSE)
 stopifnot(abs(idw_pred(xy,d$concentrazione,matrix(posizione,nrow=1),2)-q[2])<1e-12)
 ''','Una sensibilità alla potenza non dice quale previsione sia più accurata. La verifica richiede bersagli esclusi e un protocollo separato, come in N19.')],
 step('Coincidenza e duplicati hanno una regola esplicita','La funzione assegna tutto il peso ai siti coincidenti entro10⁻¹⁰m e, se sono più di uno, usa la loro media.','''
 esatto <- idw_pred(xy,d$concentrazione,xy[1,,drop=FALSE],2)
 duplicati <- matrix(c(0,0,0,0,100,0),ncol=2,byrow=TRUE)
 esempio <- idw_pred(duplicati,c(10,14,100),matrix(c(0,0),nrow=1),2)
 data.frame(caso=c("S01 osservato","Due valori coincidenti 10 e 14"),previsione=c(esatto,esempio))
 stopifnot(abs(esatto-d$concentrazione[1])<1e-12,esempio==12)
 ''','La media dei coincidenti è una politica computazionale dichiarata. Prima di applicarla a dati reali si deve capire se si tratta di repliche, duplicati o errori di posizione.'),
 'Calcolare0 elevato a una potenza negativa, scegliere p usando un bersaglio non osservato o interpretare la superficie IDW come una misura.',
 'IDW media valori con pesi espliciti legati alla distanza. La potenza controlla la località e la previsione resta nell’intervallo dei dati usati. Coincidenze, unità e scelta dei parametri vanno dichiarate; la precisione richiede una verifica indipendente.')

nb('Quanto funziona una previsione quando l’intero settore Est viene escluso dall’adattamento?',
 ['Fissare train40 e test24 con soglia1250m.','Confrontare IDW p2, media del train e vicino più prossimo.','Leggere gli errori senza ottimizzare sul test.'],DATA,[
 step('Il test è un settore geografico escluso','Il train usa x<1250m: cinque colonne,40 siti. Il test usa x≥1250m: tre colonne,24 siti. Tutti i bersagli sono a Est del massimo x del train, quindi questo è un trasferimento fuori dalla sua copertura geografica.',LOAD+'''
 tr <- d$x_m<1250;te <- !tr
 stopifnot(sum(tr)==40L,sum(te)==24L,!any(tr&te),all(tr|te))
 data.frame(ruolo=c("Train","Test"),n=c(sum(tr),sum(te)),
   minimo_x=c(min(d$x_m[tr]),min(d$x_m[te])),massimo_x=c(max(d$x_m[tr]),max(d$x_m[te])))
 table(area_del_CSV=d$area,ruolo=ifelse(tr,"Train","Test"))
 ''','La colonna area usa la diversa soglia1000m e non può sostituire questo split. Nel train entrano anche gli8 siti che il CSV chiama Est a x=1000.'),
 step('Tutte le previsioni usano soltanto il train','Fissiamo p=2 come nel laboratorio. I due riferimenti condividono gli stessi40 siti: media del train e valore del sito più vicino, con pareggi risolti per ordine delle righe.','''
 xy_tr <- d[tr,c("x_m","y_m")];xy_te <- d[te,c("x_m","y_m")]
 pred_idw <- idw_pred(xy_tr,d$concentrazione[tr],xy_te,p=2)
 pred_media <- rep(mean(d$concentrazione[tr]),sum(te))
 dist_te <- distanze_incrociate(xy_te,xy_tr)
 vicino <- apply(dist_te,1,which.min)
 pred_vicino <- d$concentrazione[tr][vicino]
 previsioni <- data.frame(id=d$id[te],x_m=d$x_m[te],y_m=d$y_m[te],
   IDW_p2=pred_idw,Media_train=pred_media,Vicino=pred_vicino)
 head(previsioni,6)
 stopifnot(all(is.finite(as.matrix(previsioni[,4:6]))))
 ''','I valori della concentrazione nel test non entrano né nei pesi né nei riferimenti. Le posizioni dei bersagli sono note perché definiscono dove si vuole prevedere.'),
 step('Il test viene aperto per misurare gli errori','La convenzione è osservato−previsto. Il confronto mantiene gli stessi24 bersagli per ogni metodo e non viene usato qui per cambiare p.','''
 osservato <- d$concentrazione[te]
 metriche_test <- as.data.frame(do.call(rbind,lapply(previsioni[,4:6],function(pr) metriche(osservato,pr))))
 metriche_test$metodo <- rownames(metriche_test);rownames(metriche_test) <- NULL
 metriche_test
 previsioni$osservato <- osservato;previsioni$errore_IDW <- osservato-pred_idw
 stile_grafico()
 plot(previsioni$x_m,previsioni$errore_IDW,pch=19,col=palette_geo[1],
   xlab="x del bersaglio escluso (m)",ylab="Osservato - IDW p2 (u.a.)",main="Errori nel settore Est escluso")
 abline(h=0,lty=2,col="grey50")
 write.csv(metriche_test,percorso_risultati("metriche_test_spaziale.csv"),row.names=FALSE)
 write.csv(previsioni,percorso_risultati("previsioni_test_spaziale.csv"),row.names=FALSE)
 ''','La prestazione riguarda questa separazione geografica. IDW è una regola di media pesata anche fuori dal dominio del train, ma l’uso qui comporta extrapolazione geografica e non garantisce di seguire un trend verso Est.')],
 step('Conservare la distanza dal train nella lettura','Riassumere gli errori IDW per colonna esclusa, senza scegliere un altro parametro dopo il confronto.','''
 previsioni$distanza_train_m <- apply(dist_te,1,min)
 per_colonna <- do.call(rbind,lapply(split(previsioni,previsioni$x_m),function(a)
   data.frame(x_m=a$x_m[1],n=nrow(a),distanza_minima_train_m=mean(a$distanza_train_m),
     MAE=mean(abs(a$errore_IDW)),bias=mean(a$errore_IDW))))
 rownames(per_colonna) <- NULL
 per_colonna
 write.csv(per_colonna,percorso_risultati("errori_per_colonna.csv"),row.names=FALSE)
 ''','Le tre colonne condividono un solo split e valori spazialmente dipendenti. Una lettura per distanza è descrittiva; non fornisce tre verifiche indipendenti del modello.'),
 'Confondere la partizione x<1000 con il train x<1250, includere dati del test nei pesi o scegliere la potenza che minimizza il test finale.',
 'La verifica geografica misura un compito dichiarato: prevedere24 siti orientali usando solo40 siti più a Ovest. Metodi e riferimenti vanno fissati prima di aprire i valori del test; gli errori vanno interpretati rispetto alla copertura e al trasferimento richiesto.')

nb('Come si consegna un GeoJSON mantenendo geometria, ID e attributi verificabili?',
 ['Scrivere e rileggere un GeoJSON reale con sf.','Controllare coordinate, identità e attributi per ID.','Conservare una scheda che distingua geometria geografica e coordinate locali.'],GEO,[
 step('La geometria della consegna è geografica','L’input sf usa OGC:CRS84 con ordine lon,lat. Manteniamo tutte le colonne originali come attributi: x_m/y_m restano un piano locale senza EPSG.',SF+'''
 p <- sf::st_as_sf(d,coords=c("lon","lat"),crs="OGC:CRS84",remove=FALSE)
 stopifnot(sf::st_is_longlat(p),!anyDuplicated(p$id))
 data.frame(siti=nrow(p),geometria=as.character(unique(sf::st_geometry_type(p))),
   CRS_ingresso=sf::st_crs(p)$input,attributi=ncol(sf::st_drop_geometry(p)))
 ''','Il GeoJSON non viene costruito usando x_m/y_m come se fossero longitudine e latitudine. Il georiferimento è sintetico e questa natura accompagna la consegna.'),
 step('Il file viene scritto e riletto davvero','Il driver GeoJSON usa l’opzione RFC7946 e conserva dieci cifre decimali nelle coordinate. Questa precisione di serializzazione non è accuratezza di rilievo. La rilettura attraverso sf verifica che il file possa essere interpretato come oggetto geografico.','''
 file <- percorso_risultati("campioni.geojson")
 sf::st_write(p,file,driver="GeoJSON",
   layer_options=c("RFC7946=YES","COORDINATE_PRECISION=10"),delete_dsn=TRUE,quiet=TRUE)
 q <- sf::st_read(file,quiet=TRUE,stringsAsFactors=FALSE)
 data.frame(siti_scritti=nrow(p),siti_riletti=nrow(q),
   ID_uguali=setequal(p$id,q$id),longlat_riletta=sf::st_is_longlat(q),bytes=file.info(file)$size)
 stopifnot(nrow(q)==64L,!anyDuplicated(q$id),setequal(p$id,q$id),sf::st_is_longlat(q))
 ''','Contare64 righe è necessario ma non sufficiente. Una consegna può conservare il numero di oggetti perdendo attributi, identità o coordinate.'),
 step('I controlli si allineano per ID','Riallineiamo la rilettura al dataset originale. Confrontiamo coordinate con tolleranza10⁻⁷gradi e attributi numerici con tolleranza10⁻⁸nelle rispettive unità.','''
 q <- q[match(d$id,q$id),]
 attributi <- sf::st_drop_geometry(q)
 coordinate <- sf::st_coordinates(sf::st_transform(q,"OGC:CRS84"))
 numeriche <- names(d)[vapply(d,is.numeric,logical(1))]
 differenze <- vapply(numeriche,function(n) max(abs(attributi[[n]]-d[[n]])),numeric(1))
 audit <- data.frame(colonna=numeriche,massimo_scarto=unname(differenze),tolleranza=1e-8)
 audit
 audit_geometria <- data.frame(asse=c("longitudine","latitudine"),
   massimo_scarto_gradi=c(max(abs(coordinate[,1]-d$lon)),max(abs(coordinate[,2]-d$lat))),
   tolleranza_gradi=1e-7)
 audit_geometria
 write.csv(audit_geometria,percorso_risultati("audit_geometria_GeoJSON.csv"),row.names=FALSE)
 stopifnot(identical(as.character(q$id),d$id),identical(as.character(q$area),d$area),
   all(differenze<1e-8),max(abs(coordinate[,1]-d$lon))<1e-7,
   max(abs(coordinate[,2]-d$lat))<1e-7,all(sf::st_geometry_type(q)=="POINT"))
 write.csv(audit,percorso_risultati("audit_GeoJSON.csv"),row.names=FALSE)
 scheda <- c("64 siti SINTETICI; concentrazione in unita arbitrarie.",
   "GeoJSON RFC7946: geometria geografica WGS84, ordine longitudine-latitudine.",
   "Coordinate serializzate con dieci decimali; la precisione non e accuratezza di rilievo.",
   "Attributi x_m/y_m: piano locale metrico senza EPSG; non sono offset UTM.",
   "Attributi lon/lat: georiferimento sintetico approssimato del corso.",
   "Verifica per ID: geometrie POINT, coordinate, numerosita e attributi.",
   paste("sf",packageVersion("sf")),capture.output(sf::sf_extSoftVersion()))
 writeLines(scheda,percorso_risultati("scheda_consegna.txt"),useBytes=TRUE)
 stile_grafico()
 plot(sf::st_geometry(q),axes=TRUE,pch=19,col=palette_geo[1],
   main="GeoJSON riletto: georiferimento sintetico",xlab="Longitudine",ylab="Latitudine")
 ''','Le tolleranze riguardano serializzazione e calcolo, non accuratezza di rilievo. Il controllo completo collega geometria e attributi alla stessa identità del sito.')],
 step('L’ordine delle righe non è l’identità','Invertire le righe rilette e mostrare che il confronto per ID ricostruisce l’associazione corretta.','''
 invertito <- q[nrow(q):1,]
 riallineato <- invertito[match(d$id,invertito$id),]
 stopifnot(identical(as.character(riallineato$id),d$id),
   max(abs(riallineato$concentrazione-d$concentrazione))<1e-8)
 data.frame(ordine_invertito_identico=identical(as.character(invertito$id),d$id),
   ID_riallineati_identici=identical(as.character(riallineato$id),d$id))
 ''','Una differenza nell’ordine non implica perdita di dati. Un confronto per posizione di riga potrebbe invece collegare misure e geometrie di siti diversi.'),
 'Esportare coordinate locali come GeoJSON geografico, verificare soltanto il numero di righe o presumere che l’ordine delle righe sia un identificatore.',
 'La consegna conserva un GeoJSON WGS84 effettivamente scritto e riletto, con verifica per ID di geometrie, coordinate e attributi. Una scheda dichiara natura sintetica, unità e distinzione fra piano locale e georiferimento; il file geografico da solo non sostituisce questi metadati.')

PREP='''# Trova il modulo dal progetto autonomo o dal progetto generale dei notebook.
.gs_cerca <- normalizePath(getwd(),winslash="/",mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca,file.path(.gs_cerca,"M11_Locus"),
    file.path(.gs_cerca,"03_Notebook_svolti","M11_Locus"),
    file.path(.gs_cerca,"M11","03_Notebook_svolti","M11_Locus"))
  .gs_ok <- file.exists(file.path(.gs_candidati,"M11_N01.Rmd")) &
    file.exists(file.path(.gs_candidati,"R","funzioni_notebook.R"))
  if(any(.gs_ok)) { .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]];break }
  .gs_padre <- dirname(.gs_cerca)
  if(.gs_padre==.gs_cerca) stop("Aprire il progetto M11_Locus o quello generale dei notebook.")
  .gs_cerca <- .gs_padre
}
source(file.path(.gs_modulo,"R","funzioni_notebook.R"),local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo,"{ID}")
carica_dati <- .gs_funzioni$carica_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88,digits=6)
if(requireNamespace("knitr",quietly=TRUE)) {
  knitr::opts_chunk$set(echo=TRUE,error=FALSE,warning=TRUE,message=TRUE,
    fig.width=8,fig.height=5,dpi=150,fig.align="center")
}
set.seed({SEED})
'''

SLIDE={1:'5–16',2:'18',3:'19–21',4:'22–24',5:'25–28 e 30',6:'29–31',7:'7 e 32–33',8:'34–36',9:'37–38',10:'39–40',11:'46',12:'44–55',13:'56–62',14:'63–70',15:'71–81',16:'82–84',17:'85–91',18:'92–95',19:'96–99 e 105',20:'106–108'}
def spazi(s):
 pattern=r'\b(?:M\d{2}(?:_N\d{2})?|N\d{2}|S\d{2}|CRS84|WGS84|EPSG:\d+|UTM\d+[NS]|RFC7946|[A-Za-z_]+_v\d+\.csv)\b'
 parts=re.split('('+pattern+')',s)
 for i in range(0,len(parts),2):
  t=parts[i]
  t=re.sub(r'(?<=[^\W\d_])(?=\d)',' ',t)
  t=re.sub(r'(?<=\d)(?=[^\W\d_])',' ',t)
  t=re.sub(r'(?<=[^\W\d_])(?=\(\d)',' ',t)
  t=re.sub(r'(?<=[^\W\d_])(?=[+]\d)',' ',t)
  t=re.sub(r'(?<=\w)([≤≥])',r' \1',t)
  t=re.sub(r'([≤≥])(?=\w)',r'\1 ',t)
  t=t.replace('⁻⁷gradi','⁻⁷ gradi').replace('⁻⁸nelle','⁻⁸ nelle').replace('⁻¹⁰m','⁻¹⁰ m')
  parts[i]=t
 return ''.join(parts)
def make():
 assert len(N)==20
 for n in N:
  for key in ['question','data','error','answer']:n[key]=spazi(n[key])
  n['objectives']=[spazi(x) for x in n['objectives']]
  for st in n['steps']+[n['variant']]:
   for key in ['title','text','reading']:st[key]=spazi(st[key])
 records=[]
 for i,n in enumerate(N,1):
  ident=f'M11_N{i:02d}'
  yaml='---\ntitle: '+json.dumps(n['title'],ensure_ascii=False)+'\nsubtitle: "'+ident+' · Locus"\nlang: it-IT\noutput:\n  html_document:\n    toc: true\n    self_contained: true\n    theme: null\n    highlight: tango\n    mathjax: null\n    pandoc_args: ["--mathml"]\n    css: "R/stile_notebook.css"\n---\n'
  sf_note=' Questo notebook richiede il pacchetto sf installato prima dell’analisi e usa le sue funzioni effettive.' if i in [5,6,20] else ' I calcoli usano R base e i pacchetti standard.'
  s=yaml+'\n# La domanda\n\n'+n['question']+'\n\n## Obiettivi\n\n'+'\n'.join('- '+x for x in n['objectives'])
  s+='\n\n**Prima di iniziare.** Sono richiesti vettori, tabelle, coordinate e funzioni R di base. I blocchi vanno eseguiti in ordine; il notebook è autonomo rispetto agli altri.'+sf_note
  s+='\n\n**Dati e unità.** '+n['data']
  s+='\n\n## Preparazione\n\nAprire il progetto autonomo di Locus o quello generale dei notebook. I CSV locali restano invariati. Gli output vanno in `Risultati/'+ident+'/`. Nessun download o installazione viene eseguito nei blocchi.\n\n```{r preparazione}\n'+PREP.replace('{ID}',ident).replace('{SEED}',str(11000+i))+'```\n'
  chunks=[dict(name='preparazione',code=PREP.replace('{ID}',ident).replace('{SEED}',str(11000+i)))]
  for j,st in enumerate(n['steps'],1):
   s+=f'\n## {j}. {st["title"]}\n\n{st["text"]}\n\n```{{r passo_{j:02d}}}\n{st["code"]}\n```\n\n**Lettura del risultato.** {st["reading"]}\n'
   chunks.append(dict(name=f'passo_{j:02d}',code=st['code']))
  v=n['variant'];s+=f'\n## Variante svolta\n\n**{v["title"]}.** {v["text"]}\n\n```{{r variante}}\n{v["code"]}\n```\n\n{v["reading"]}\n'
  chunks.append(dict(name='variante',code=v['code']))
  s+='\n## Errore da riconoscere\n\n'+n['error']+'\n\n## Risposta alla domanda\n\n'+n['answer']
  s+='\n\n## Raccordo con le slide\n\n[Slide '+SLIDE[i]+' della lezione Locus](../../02_PDF/M11_Locus/Locus_M11_statistica_spaziale.pdf#page='+str(int(re.match(r'\d+',SLIDE[i])[0]))+'). Il notebook conserva il tema del laboratorio originale e aggiunge verifiche e una variante svolta.\n'
  s+='\n\n## Riferimenti e provenienza\n\nQuesto svolgimento sviluppa `'+ident+'` del [modulo M11 del corso](https://marzione00.github.io/Lab_Geo/#modulo-M11). Il [codice originale](https://github.com/marzione00/Lab_Geo/blob/649f7cc577b96bd1044d81e78a2f530813e4f96b/materiali/laboratori/M11/'+ident+'.R) è conservato immutato in `R/Originali_corso/`; la mappa allegata documenta gli ampliamenti. Dati e originali hanno impronte SHA-256 e SHA-1 Git verificate.\n'
  if i in [5,6,20]:
   s+='\nDocumentazione primaria: [sf, trasformazione](https://r-spatial.github.io/sf/reference/st_transform.html), [sf, CRS](https://r-spatial.github.io/sf/reference/st_crs.html), [sf, scrittura](https://r-spatial.github.io/sf/reference/st_write.html), [GeoJSON RFC7946](https://www.rfc-editor.org/rfc/rfc7946).\n'
  else:
   s+='\nDocumentazione primaria delle operazioni: [R, dist](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/dist.html), [R, aggregate](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/aggregate.html), [R, sample](https://stat.ethz.ch/R-manual/R-devel/library/base/html/sample.html). Le definizioni spaziali e il riferimento inferenziale seguono il laboratorio originale, con le distinzioni esplicitate nel testo.\n'
  (BASE/f'{ident}.Rmd').write_text(s,encoding='utf-8')
  folder=BASE/'Verifiche'/ident;folder.mkdir(parents=True,exist_ok=True)
  for c in chunks:(folder/(c['name']+'.R')).write_text(c['code']+'\n',encoding='utf-8')
  records.append(dict(id=ident,titolo=n['title'],html=f'{ident}.html',rmd=f'{ident}.Rmd',blocchi=len(chunks),sha256_Rmd=hashlib.sha256(s.encode()).hexdigest(),chunks=[c['name'] for c in chunks]))
 (BASE/'Sorgenti_generazione/notebook_contenuti.json').write_text(json.dumps(N,ensure_ascii=False,indent=2),encoding='utf-8')
 (BASE/'Verifiche/piano_esecuzione.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
 with (BASE/'INDICE_NOTEBOOK.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=['id','titolo','html','rmd','blocchi']);w.writeheader()
  for row in records:w.writerow({k:row[k] for k in w.fieldnames})
 dst=BASE/'Sorgenti_generazione/genera_notebook.py'
 if Path(__file__).resolve()!=dst.resolve():shutil.copy2(__file__,dst)
 print('Creati20 Rmd e100 blocchi.')
if __name__=='__main__':make()
