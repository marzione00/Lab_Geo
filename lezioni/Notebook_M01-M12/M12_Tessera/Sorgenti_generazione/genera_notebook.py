from pathlib import Path
import csv,hashlib,json,re,shutil,textwrap
HERE=Path(__file__).resolve().parent
BASE=HERE.parent if HERE.name=='Sorgenti_generazione' else HERE.parent/'M12/03_Notebook_svolti/M12_Tessera'
N=[]
T=[(BASE/'R/Originali_corso'/f'M12_N{i:02d}.R').read_text().splitlines()[0].lstrip('# ') for i in range(1,21)]
def step(title,text,code,reading):return dict(title=title,text=text,code=textwrap.dedent(code).strip(),reading=reading)
def nb(question,objectives,data,steps,variant,error,answer):N.append(dict(title=T[len(N)],question=question,objectives=objectives,data=data,steps=steps,variant=variant,error=error,answer=answer))
DATA='Il raster è interamente sintetico: 24 righe × 30 colonne, 720 celle quadrate di lato 30 m. Nel CSV riga e colonna partono da zero; x_m = 30 × colonna e y_m = 30 × riga indicano i centri nel piano locale. La riga 0 è a Sud; la riga 23 è a Nord. Le quote sono in metri sintetici. I dati non descrivono un rilievo reale.'
GEO=DATA+' Il GeoTIFF originale porta EPSG:32632, UTM zona 32 Nord, con georeferenziazione fittizia: corner Nord-Ovest E=500000, N=5000000; passo 30 m, PixelIsArea. I centri corrispondono a E=x_m+500015 e N=y_m+4999295. Le righe del TIFF procedono da Nord a Sud, al contrario della matrice locale.'
LOAD='d <- carica_dati("raster_v3.csv")\naudit_raster(d)\nd <- d[order(d$riga,d$colonna),]\nZ <- matrice_quote(d)'
TERRA=LOAD+'\nrichiedi_terra()\nr <- terra::rast(percorso_dati("raster_v3.tif"))'

nb('Quali controlli distinguono una griglia completa da una tabella con lo stesso numero di righe?',
 ['Verificare unicità delle celle e indici da zero.','Controllare entrambi i passi e la completezza della griglia.','Distinguere centri, estensione e numerosità.'],DATA,[
 step('Una riga identifica una cella', 'L’audit originale controlla 720 celle e unicità della coppia riga-colonna. Aggiungiamo intervalli, coordinate e completezza.',LOAD+'''
 controlli <- data.frame(controllo=c("720 celle","Coppie uniche","24 righe","30 colonne",
   "x coerente","y coerente"),esito=c(nrow(d)==720L,!anyDuplicated(d[c("riga","colonna")]),
   setequal(d$riga,0:23),setequal(d$colonna,0:29),all(d$x_m==30*d$colonna),all(d$y_m==30*d$riga)))
 controlli
 stopifnot(all(controlli$esito))
 ''','Contare le righe non basta: un duplicato e una cella mancante possono compensarsi. La chiave della cella è la coppia di indici.'),
 step('Il passo si controlla su due assi','Una griglia regolare richiede passi coerenti in x e in y. I limiti dei centri differiscono dai bordi esterni delle celle.','''
 dx <- unique(diff(sort(unique(d$x_m))));dy <- unique(diff(sort(unique(d$y_m))))
 risultato <- data.frame(asse=c("x","y"),centro_min=c(min(d$x_m),min(d$y_m)),
   centro_max=c(max(d$x_m),max(d$y_m)),passo_m=c(dx,dy),
   bordo_min=c(min(d$x_m)-dx/2,min(d$y_m)-dy/2),
   bordo_max=c(max(d$x_m)+dx/2,max(d$y_m)+dy/2))
 risultato
 stopifnot(length(dx)==1L,length(dy)==1L,dx==30,dy==30)
 ''','Il dominio delle celle misura 900 × 720 m, anche se la distanza fra i centri estremi è 870 × 690 m. Non confondiamo queste due estensioni.'),
 step('La carta accompagna il controllo tabellare','Mostriamo le quote sulla griglia e conserviamo le verifiche. La mappa usa le coordinate dei centri.','''
 mappa_matrice(Z,titolo="720 celle: centri su una griglia regolare")
 write.csv(controlli,percorso_risultati("audit_griglia.csv"),row.names=FALSE)
 write.csv(risultato,percorso_risultati("geometria_locale.csv"),row.names=FALSE)
 ''','Il disegno è una rappresentazione del campo sintetico. La regolarità apparente non sostituisce l’audit degli indici e delle unità.')],
 step('Stesso numero di righe, griglia incompleta','Sostituire l’ultima riga con una copia della prima senza cambiare il CSV.','''
 errata <- d;errata[nrow(errata),] <- errata[1,]
 esito <- data.frame(righe=nrow(errata),celle_distinte=nrow(unique(errata[c("riga","colonna")])),
   occorrenze_duplicate=sum(duplicated(errata[c("riga","colonna")])|
     duplicated(errata[c("riga","colonna")],fromLast=TRUE)))
 esito
 stopifnot(esito$righe==720L,esito$celle_distinte==719L)
 ''','La tabella conserva 720 righe ma perde una cella distinta. L’identità precede qualsiasi sintesi.'),
 'Usare il numero di righe come unico controllo oppure trattare il range dei centri come estensione delle celle.',
 'Una griglia verificabile conserva chiave, completezza, passo, unità e convenzione dei centri. Qui 720 celle coprono 900 × 720 m nel piano metrico sintetico.')

nb('Quale elemento della matrice corrisponde all’angolo Sud-Ovest?',
 ['Ricostruire la matrice dopo un ordinamento esplicito.','Collegare indici R e indici originali da zero.','Riconoscere un ribaltamento Nord-Sud.'],DATA,[
 step('Gli indici del CSV e quelli di R differiscono di uno','La prima riga della matrice rappresenta y=0; image riceve la trasposta perché il suo primo indice corrisponde all’asse x.',LOAD+'''
 angoli <- data.frame(angolo=c("SO","SE","NO","NE"),riga_csv=c(0,0,23,23),
   colonna_csv=c(0,29,0,29),quota_m=c(Z[1,1],Z[1,30],Z[24,1],Z[24,30]))
 angoli
 stopifnot(Z[1,1]==d$quota_m[d$riga==0&d$colonna==0],
   Z[24,30]==d$quota_m[d$riga==23&d$colonna==29])
 ''','Riga 1 in R e riga 0 nel CSV descrivono la stessa fascia meridionale. La corrispondenza deriva dalle coordinate, non dal solo modo di stampare la matrice.'),
 step('La mappa usa x e y dichiarati','La carta mantiene il Sud in basso e il Nord in alto. Il raster viene disegnato usando centri crescenti su entrambi gli assi.','''
 mappa_matrice(Z,titolo="Matrice locale: prima riga a Sud")
 data.frame(riga_R=c(1,24),riga_CSV=c(0,23),y_m=c(0,690))
 ''','La matrice stampata a schermo ha la prima riga in alto; questo non stabilisce il Nord. L’orientamento della carta è definito dal legame fra indici e coordinate.'),
 step('Un ribaltamento conserva le statistiche marginali','Confrontiamo la stessa matrice con le righe invertite. Media e massimo da soli non riconoscono l’errore.','''
 invertita <- Z[nrow(Z):1,]
 confronto <- data.frame(matrice=c("Corretta","Righe invertite"),
   media=c(mean(Z),mean(invertita)),massimo=c(max(Z),max(invertita)),
   quota_SO=c(Z[1,1],invertita[1,1]))
 confronto
 stopifnot(mean(Z)==mean(invertita),max(abs(Z-invertita))>0)
 write.csv(angoli,percorso_risultati("angoli.csv"),row.names=FALSE)
 write.csv(confronto,percorso_risultati("controllo_orientamento.csv"),row.names=FALSE)
 ''','Un istogramma può restare identico mentre ogni quota cambia posizione. L’audit deve associare i valori alle celle.')],
 step('Riordinare le righe del file non cambia la geometria','Rovesciare l’ordine delle righe della tabella e ricostruire la matrice ordinando gli indici.','''
 mescolata <- d[nrow(d):1,]
 ricostruita <- matrice_quote(mescolata)
 data.frame(massimo_scarto=max(abs(ricostruita-Z)),
   errore_senza_ordine=max(abs(matrix(mescolata$quota_m,24,byrow=TRUE)-Z)))
 stopifnot(identical(ricostruita,Z))
 ''','La posizione delle righe nella tabella non è la chiave spaziale. L’ordinamento esplicito rende l’operazione riproducibile.'),
 'Confondere la prima riga stampata della matrice con il Nord oppure verificare l’orientamento usando soltanto media e istogramma.',
 'Nel CSV la riga zero è a Sud; nella matrice locale è la riga R numero uno. La trasposta nell’immagine e il ribaltamento necessario per terra risolvono problemi diversi e devono essere espliciti.')

nb('Il GeoTIFF contiene soltanto quote o anche una geometria da verificare?',
 ['Leggere il GeoTIFF reale con terra.','Controllare risoluzione, estensione, CRS e centri.','Verificare l’orientamento confrontando tutte le quote con il CSV.'],GEO,[
 step('Lettura effettiva del file','Apriamo il TIFF originale immutato. L’etichetta EPSG appartiene al caso sintetico e non certifica un rilievo reale.',TERRA+'''
 geometria <- data.frame(righe=nrow(r),colonne=ncol(r),celle=terra::ncell(r),
   dx=terra::res(r)[1],dy=terra::res(r)[2],
   xmin=terra::xmin(r),xmax=terra::xmax(r),ymin=terra::ymin(r),ymax=terra::ymax(r))
 geometria
 terra::crs(r,describe=TRUE)[,c("name","authority","code")]
 stopifnot(terra::ncell(r)==720L,all(terra::res(r)==30),
   max(abs(as.vector(terra::ext(r))-c(500000,500900,4999280,5000000)))<1e-9)
 ''','La griglia è 24 × 30, con celle di 30 m. Il corner Nord-Ovest non coincide con il centro della prima cella.'),
 step('I centri verificano il mezzo pixel','Le prime celle nel TIFF stanno sul bordo settentrionale. Confrontiamo i loro centri con la trasformazione dichiarata del piano locale.','''
 celle <- c(1,30,691,720)
 centri <- terra::xyFromCell(r,celle)
 risultato <- data.frame(cella_TIFF=celle,E=centri[,1],N=centri[,2],
   x_locale=centri[,1]-500015,y_locale=centri[,2]-4999295)
 risultato
 stopifnot(identical(as.numeric(centri[1,]),c(500015,4999985)))
 ''','Il centro della prima cella TIFF è E=500015, N=4999985 e corrisponde al centro locale x=0, y=690. Il mezzo pixel conta su entrambi gli assi.'),
 step('Tutte le quote tornano nelle celle corrette','terra restituisce le righe dall’alto verso il basso. Le invertiamo per ricostruire la matrice locale dal Sud verso il Nord.','''
 letto <- matrice_locale(r)
 errore <- max(abs(letto-Z))
 data.frame(massimo_scarto_m=errore,terra=as.character(packageVersion("terra")))
 stopifnot(errore<1e-10)
 mappa_matrice(letto,titolo="GeoTIFF riletto: orientamento locale verificato")
 write.csv(geometria,percorso_risultati("geometria_GeoTIFF.csv"),row.names=FALSE)
 write.csv(risultato,percorso_risultati("centri_GeoTIFF.csv"),row.names=FALSE)
 writeLines(terra::crs(r),percorso_risultati("CRS_fittizio.wkt"))
 ''','La verifica cella per cella è più forte del confronto della media. I valori FLOAT64 del TIFF e quelli del CSV risultano confrontabili senza trasformare il CRS.')],
 step('Omettere il ribaltamento','Confrontare direttamente la matrice Nord-Sud di terra con quella locale Sud-Nord.','''
 nord_sud <- terra::as.matrix(r,wide=TRUE)
 data.frame(scarto_errato_m=max(abs(nord_sud-Z)),
   scarto_corretto_m=max(abs(nord_sud[24:1,]-Z)),
   media_invariata=abs(mean(nord_sud)-mean(Z))<1e-10)
 stopifnot(max(abs(nord_sud-Z))>0)
 ''','Il controllo sbagliato può conservare la media. L’identità delle celle va verificata insieme alla georeferenziazione.'),
 'Interpretare il corner come centro oppure attribuire al raster una collocazione reale perché possiede EPSG:32632.',
 'Un GeoTIFF unisce valori, numero di celle, risoluzione, origine, CRS e convenzione di orientamento. Qui la georeferenziazione è fittizia; il confronto con il CSV verifica la costruzione del file, non la sua corrispondenza a un territorio reale.')

nb('Che cosa cambia quando una quota mancante viene sostituita da zero?',
 ['Costruire la maschera originale di 24 celle.','Separare copertura e media dei dati disponibili.','Quantificare l’effetto della sostituzione con zero.'],DATA,[
 step('La maschera è dichiarata con indici R','Conserviamo esattamente la maschera del laboratorio originale: righe R 5:8 e colonne R 10:15, cioè indici CSV 4:7 e 9:14.',LOAD+'''
 mascherata <- Z;mascherata[5:8,10:15] <- NA_real_
 errata <- mascherata;errata[is.na(errata)] <- 0
 risultato <- data.frame(celle_totali=length(Z),celle_mancanti=sum(is.na(mascherata)),
   copertura=mean(!is.na(mascherata)),media_disponibili=mean(mascherata,na.rm=TRUE),
   media_zero=mean(errata))
 risultato
 stopifnot(sum(is.na(mascherata))==24L)
 ''','NA significa quota non disponibile. Zero è invece una quota numerica e partecipa alla media.'),
 step('Il denominatore della media cambia','La media degli osservati usa 696 celle. La versione con zero divide la stessa somma per tutte le 720 celle.','''
 osservati <- sum(!is.na(mascherata))
 data.frame(n_disponibili=osservati,n_totale=length(Z),
   rapporto_medie=mean(errata)/mean(mascherata,na.rm=TRUE),
   copertura=osservati/length(Z),
   differenza_dalla_media_completa=mean(mascherata,na.rm=TRUE)-mean(Z))
 stopifnot(abs(mean(errata)-mean(mascherata,na.rm=TRUE)*osservati/length(Z))<1e-10)
 ''','Il rapporto fra le due medie coincide qui con la copertura, perché i valori mancanti sono stati sostituiti tutti con zero. La media disponibile può comunque differire da quella dell’intero dominio.'),
 step('Il bianco indica assenza, non quota bassa','Disegniamo la maschera conservando la scala delle quote originali.','''
 mappa_matrice(mascherata,titolo="24 celle senza dato: il bianco resta assenza",limiti=range(Z))
 write.csv(risultato,percorso_risultati("effetto_NoData.csv"),row.names=FALSE)
 write.csv(data.frame(riga=rep(0:23,each=30),colonna=rep(0:29,24),
   disponibile=as.vector(t(!is.na(mascherata)))),percorso_risultati("maschera.csv"),row.names=FALSE)
 ''','Una palette che usa un colore esplicito per NA rende visibile la copertura. La maschera deve viaggiare con il risultato.')],
 step('Una perdita concentrata in quota cambia la media disponibile','Rimuovere in memoria il decile superiore e confrontare copertura e media.','''
 selettiva <- Z;selettiva[Z>quantile(Z,.9)] <- NA_real_
 data.frame(caso=c("Completo","Maschera rettangolare","Decile alto escluso"),
   copertura=c(1,mean(!is.na(mascherata)),mean(!is.na(selettiva))),
   media=c(mean(Z),mean(mascherata,na.rm=TRUE),mean(selettiva,na.rm=TRUE)))
 ''','Una copertura elevata non garantisce una media rappresentativa se le celle mancanti seguono un meccanismo legato ai valori.'),
 'Ricodificare NA come zero o riportare una media senza indicare quante celle contribuiscono.',
 'NoData descrive un’assenza. La media dei disponibili, la copertura e il meccanismo della maschera rispondono a domande diverse e vanno riportati insieme.')

nb('La media di una finestra risponde alla stessa domanda della media dell’intero raster?',
 ['Applicare il ritaglio originale ai centri.','Contare celle e area del nuovo dominio.','Esplicitare l’inclusione dei bordi.'],DATA,[
 step('La finestra è una regola sui centri','Selezioniamo x fra 300 e 600 m e y fra 180 e 510 m, estremi inclusi.',LOAD+'''
 dentro <- d$x_m>=300 & d$x_m<=600 & d$y_m>=180 & d$y_m<=510
 risultato <- data.frame(dominio=c("Intero","Finestra"),n=c(nrow(d),sum(dentro)),
   media=c(mean(d$quota_m),mean(d$quota_m[dentro])),
   area_ha=c(nrow(d),sum(dentro))*900/10000)
 risultato
 stopifnot(sum(dentro)==132L)
 ''','La finestra contiene 11 colonne e 12 righe di centri. La sintesi riguarda quelle 132 celle, non l’intero dominio.'),
 step('I bordi delle celle superano i centri estremi','Se includiamo interamente le celle selezionate, la loro unione ha limiti spostati di mezzo pixel rispetto al rettangolo dei centri.','''
 x <- range(d$x_m[dentro]);y <- range(d$y_m[dentro])
 data.frame(asse=c("x","y"),centro_min=c(x[1],y[1]),centro_max=c(x[2],y[2]),
   bordo_min=c(x[1],y[1])-15,bordo_max=c(x[2],y[2])+15)
 stopifnot((diff(x)+30)*(diff(y)+30)==sum(dentro)*900)
 ''','Qui la selezione è per centro e attribuisce l’intera cella. Un ritaglio geometrico con frazioni di cella sarebbe un’altra operazione.'),
 step('Il dominio escluso rimane riconoscibile','Mostriamo soltanto i valori selezionati sulla geometria originale.','''
 vista <- Z;vista[!matrix(dentro,24,byrow=TRUE)] <- NA_real_
 mappa_matrice(vista,titolo="Finestra: 132 celle selezionate per centro",limiti=range(Z))
 write.csv(risultato,percorso_risultati("confronto_domini.csv"),row.names=FALSE)
 write.csv(d[dentro,],percorso_risultati("celle_finestra.csv"),row.names=FALSE)
 ''','Le celle bianche sono fuori dalla selezione, non quote uguali a zero. La media della finestra non corregge né sostituisce quella del dominio completo.')],
 step('Cambiare le disuguaglianze cambia la popolazione di celle','Usare estremi strettamente interni e confrontare numerosità e media.','''
 stretto <- d$x_m>300 & d$x_m<600 & d$y_m>180 & d$y_m<510
 data.frame(regola=c("Inclusiva","Stretta"),n=c(sum(dentro),sum(stretto)),
   media=c(mean(d$quota_m[dentro]),mean(d$quota_m[stretto])))
 stopifnot(sum(stretto)==90L)
 ''','Le celle sui bordi sono una parte concreta del risultato. La regola di inclusione deve essere riproducibile.'),
 'Confrontare medie di domini diversi senza dichiarare selezione, bordi e denominatore.',
 'Ritagliare cambia il dominio della domanda. Numero di celle, area, regola di inclusione e coordinate della finestra rendono interpretabile la nuova media.')

nb('Quando un conteggio di celle può diventare un’area in ettari?',
 ['Usare area proiettata di 30 × 30 m.','Collegare classi, conteggi e area totale.','Distinguere area planimetrica e superficie inclinata.'],DATA,[
 step('Ogni cella rappresenta 900 metri quadrati nel piano','Le classi sintetiche A e B partizionano le 720 celle. La conversione in ettari usa 10000 m² per ettaro.',LOAD+'''
 n <- table(d$unita)
 risultato <- data.frame(unita=names(n),celle=as.numeric(n),
   area_m2=as.numeric(n)*30*30,area_ha=as.numeric(n)*30*30/10000)
 risultato
 stopifnot(sum(risultato$celle)==720L,abs(sum(risultato$area_ha)-64.8)<1e-10)
 ''','Le aree si riferiscono al piano della griglia metrica sintetica. Non sono superfici topografiche corrette per l’inclinazione.'),
 step('Il controllo globale chiude il conteggio','La somma per classi deve coincidere con l’area del rettangolo esterno delle celle.','''
 controllo <- data.frame(area_conteggio_m2=sum(risultato$area_m2),
   area_estensione_m2=(870-0+30)*(690-0+30),
   quota_area=sum(risultato$area_ha))
 controllo
 stopifnot(controllo$area_conteggio_m2==controllo$area_estensione_m2)
 ''','Il controllo funziona perché non ci sono celle sovrapposte o mancanti nella partizione. Una mappa con frazioni di cella richiederebbe pesi di area.'),
 step('Confrontare le aree delle classi','L’asse verticale riporta ettari, non numero di osservazioni indipendenti.','''
 stile_grafico()
 bp <- barplot(risultato$area_ha,names.arg=risultato$unita,col=palette_geo[1:2],
   ylim=c(0,max(risultato$area_ha)*1.2),xlab="Unita sintetica",ylab="Area planimetrica (ha)",
   main="Dal conteggio delle celle all'area")
 text(bp,risultato$area_ha,labels=round(risultato$area_ha,2),pos=3)
 write.csv(risultato,percorso_risultati("aree_classi.csv"),row.names=FALSE)
 ''','Una classe più estesa comprende più area, ma non dimostra maggiore variabilità o maggiore informazione indipendente.')],
 step('Stesso conteggio, passo differente','Calcolare l’area di 720 celle con lato 15, 30 e 60 m; poi conservare il dominio riducendo il conteggio a 180 celle da 60 m.','''
 data.frame(lato_m=c(15,30,60),celle=720,area_ha=720*c(15,30,60)^2/10000)
 data.frame(griglia=c("30 m","60 m aggregata"),celle=c(720,180),
   area_ha=c(720*30^2,180*60^2)/10000)
 ''','Il conteggio da solo non è un’area. Quando si aggrega 2 × 2 conservando il dominio, il numero di celle cala ma l’area totale rimane costante.'),
 'Moltiplicare un conteggio per 900 senza verificare passo e unità, oppure chiamare superficie del terreno l’area proiettata.',
 'Il conteggio diventa area quando conosciamo la geometria e la copertura delle celle. In questa griglia regolare completa, 720 × 900 m² corrispondono a 64,8 ettari planimetrici.')

nb('Perché una media aggregata 2 × 2 può conservare la media globale ma perdere estremi?',
 ['Aggregare blocchi completi di quattro celle.','Verificare media, range e nuovo passo.','Mostrare il ruolo delle numerosità con NoData.'],DATA,[
 step('Il nuovo supporto contiene quattro celle originali','Ogni valore aggregato è la media di un blocco 2 × 2. I centri dei nuovi blocchi partono da 15 m.',LOAD+'''
 ag <- aggrega_blocchi(Z,2,2);A <- ag$media
 risultato <- data.frame(griglia=c("30 m","60 m"),celle=c(length(Z),length(A)),
   media=c(mean(Z),mean(A)),minimo=c(min(Z),min(A)),massimo=c(max(Z),max(A)))
 risultato
 stopifnot(identical(dim(A),c(12L,15L)),all(ag$numero==4L),
   abs(mean(Z)-mean(A))<1e-10,min(A)>=min(Z),max(A)<=max(Z))
 ''','La media globale si conserva perché tutti i blocchi hanno lo stesso numero di celle della stessa area. Gli estremi locali vengono attenuati dalla media.'),
 step('Il dominio resta lo stesso, il supporto cambia','Confrontiamo coordinate dei centri e bordi dell’aggregato.','''
 xa <- seq(15,855,60);ya <- seq(15,675,60)
 data.frame(asse=c("x","y"),primo_centro=c(xa[1],ya[1]),
   ultimo_centro=c(tail(xa,1),tail(ya,1)),bordo_min=c(xa[1],ya[1])-30,
   bordo_max=c(tail(xa,1),tail(ya,1))+30)
 stopifnot(length(A)*60^2==length(Z)*30^2)
 ''','Aggregazione e interpolazione non sono sinonimi. Il nuovo valore riassume un supporto più ampio, pur coprendo lo stesso dominio.'),
 step('La carta aggregata usa la scala originale','Conserviamo la stessa legenda per mostrare la perdita di dettaglio.','''
 mappa_matrice(A,xa,ya,titolo="Aggregazione 2 x 2: 180 celle da 60 m",limiti=range(Z))
 write.csv(risultato,percorso_risultati("confronto_aggregazione.csv"),row.names=FALSE)
 write.csv(data.frame(x_m=rep(xa,12),y_m=rep(ya,each=15),quota_media_m=as.vector(t(A))),
   percorso_risultati("celle_60m.csv"),row.names=FALSE)
 ''','Più o meno pixel sullo schermo non cambiano questo supporto. Il confronto conserva unità e scala cromatica.')],
 step('Un blocco con tre celle disponibili pesa quanto gli altri?','Rimuovere una sola quota dal primo blocco e confrontare media semplice e media pesata dei blocchi.','''
 incompleta <- Z;incompleta[1,1] <- NA_real_
 a_na <- aggrega_blocchi(incompleta,2,2)
 confronto <- data.frame(media_celle=mean(incompleta,na.rm=TRUE),
   media_blocchi=mean(a_na$media),media_pesata=weighted.mean(a_na$media,a_na$numero))
 confronto
 stopifnot(abs(confronto$media_celle-confronto$media_pesata)<1e-10)
 ''','Con numerosità diverse, la media semplice dei blocchi assegna lo stesso peso a blocchi con quantità di dati diverse. I pesi ripristinano la media delle celle disponibili, non necessariamente quella dell’intero territorio.'),
 'Generalizzare la conservazione della media a blocchi incompleti senza pesi o interpretare l’aggregato come nuova misura al centro.',
 'L’aggregazione 2 × 2 conserva la media qui perché i blocchi sono completi ed equiponderati. Cambia il supporto dei valori e attenua gli estremi; NoData e aree differenti richiedono una regola di ponderazione esplicita.')

nb('Perché una quota continua e un codice di classe non si ricampionano con la stessa regola?',
 ['Riprodurre l’esempio monodimensionale originale.','Eseguire resample di terra su classi e quote.','Controllare codici ammissibili e geometria del bersaglio.'],GEO,[
 step('Il codice di classe non è una misura continua','Conserviamo l’esempio originale con codici 1,1,2,2. L’interpolazione lineare può produrre 1,5, che non è una classe.',LOAD+'''
 x <- c(0,30,60,90);classe <- c(1,1,2,2);q <- seq(0,90,15)
 lineare <- approx(x,classe,xout=q)$y
 vicino <- vapply(q,function(v) classe[which.min(abs(x-v))],numeric(1))
 risultato <- data.frame(x=q,lineare_ERRATO=lineare,vicino=vicino)
 risultato
 stopifnot(any(!lineare %in% c(1,2)),all(vicino %in% c(1,2)))
 ''','Nel piccolo esempio which.min risolve gli eventuali pareggi con la prima posizione. Il numero 1,5 non acquisisce significato soltanto perché è fra due codici.'),
 step('Ricampionamento reale con terra','Trasliamo di mezzo pixel il bersaglio in x. Confrontiamo bilinear e near su un raster di classi, e bilinear sulle quote continue.','''
 richiedi_terra();r <- terra::rast(percorso_dati("raster_v3.tif"))
 codici <- as.numeric(factor(d$unita,levels=sort(unique(d$unita))))
 rc <- raster_da_matrice(matrix(codici,24,byrow=TRUE),r)
 bersaglio <- terra::shift(terra::rast(r),dx=15,dy=0)
 cl_lin <- terra::resample(rc,bersaglio,method="bilinear")
 cl_near <- terra::resample(rc,bersaglio,method="near")
 quote_lin <- terra::resample(r,bersaglio,method="bilinear")
 a <- as.numeric(terra::values(cl_lin));b <- as.numeric(terra::values(cl_near))
 prova <- data.frame(metodo=c("Classi bilinear","Classi near","Quote bilinear"),
   celle_valide=c(sum(is.finite(a)),sum(is.finite(b)),sum(is.finite(terra::values(quote_lin)))),
   codici_non_ammessi=c(sum(is.finite(a)&!a %in% c(1,2)),sum(is.finite(b)&!b %in% c(1,2)),NA))
 prova
 stopifnot(any(is.finite(a)&!a %in% c(1,2)),all(b[is.finite(b)] %in% c(1,2)))
 ''','terra esegue davvero entrambi i metodi. I codici near restano ammissibili, ma ciò non garantisce conservazione delle aree delle classi. Il bersaglio traslato può anche cambiare la copertura.'),
 step('Il grafico rende visibile il valore inesistente','L’esempio monodimensionale permette di leggere i numeri senza confonderli con una nuova classe.','''
 stile_grafico()
 plot(q,lineare,type="b",pch=19,col=palette_geo[2],ylim=c(.8,2.2),
   xlab="Posizione (m)",ylab="Codice numerico della classe",main="Interpolare un codice crea categorie inesistenti")
 lines(q,vicino,type="b",pch=17,col=palette_geo[1]);abline(h=c(1,2),col="grey75",lty=3)
 legend("topleft",c("Lineare: errato per classi","Vicino: codici validi"),
   col=palette_geo[c(2,1)],pch=c(19,17),lty=1,bty="n",cex=.8)
 write.csv(risultato,percorso_risultati("esempio_1D.csv"),row.names=FALSE)
 write.csv(prova,percorso_risultati("resample_terra.csv"),row.names=FALSE)
 ''','Per un valore continuo l’interpolazione è una regola numerica da giustificare; per un’etichetta discreta può violare perfino l’insieme dei valori consentiti.')],
 step('Ricampionare sulla griglia identica','Usare near sulle quote con bersaglio uguale all’originale e confrontare tutte le celle. Dichiarare una tolleranza di 10⁻⁴ m per il percorso numerico di ricampionamento.','''
 identico <- terra::resample(r,r,method="near")
 errore <- max(abs(terra::values(identico)-terra::values(r)),na.rm=TRUE)
 tolleranza <- 1e-4
 data.frame(stessa_geometria=terra::compareGeom(identico,r,stopOnError=FALSE),
   errore_m=errore,tolleranza_m=tolleranza)
 stopifnot(errore<tolleranza)
 ''','Nel runtime distribuito il percorso di ricampionamento introduce un piccolo arrotondamento coerente con precisione interna float32. La geometria identica non garantisce identità bit per bit. Un successivo file FLOAT64 non recupererebbe precisione già persa; questo controllo non valida metodi su griglie differenti.'),
 'Usare bilinear sui codici di una classe oppure chiamare informazione nuova i pixel prodotti dal ricampionamento.',
 'Il metodo dipende dal significato della variabile. Near conserva i codici discreti; bilinear può essere una scelta per campi continui, ma modifica valori e supporto. Geometria del bersaglio, copertura e scopo restano parte del risultato.')

nb('Come si verifica una derivata numerica usando un piano di cui conosciamo il risultato?',
 ['Costruire il piano analitico originale.','Verificare gx e gy su 616 celle interne.','Controllare denominatore e unità.'],DATA,[
 step('Un caso con risposta nota','Il piano sintetico è z(x,y)=900+0,12x+0,08y. Le pendenze parziali attese sono note prima del calcolo.',LOAD+'''
 P <- outer((0:23)*30,(0:29)*30,function(y,x) 900+.12*x+.08*y)
 gx <- (P[2:23,3:30]-P[2:23,1:28])/60
 gy <- (P[3:24,2:29]-P[1:22,2:29])/60
 risultato <- data.frame(componente=c("gx","gy"),atteso=c(.12,.08),
   media=c(mean(gx),mean(gy)),errore_max=c(max(abs(gx-.12)),max(abs(gy-.08))))
 risultato
 stopifnot(all(risultato$errore_max<1e-12),length(gx)==616L)
 ''','La differenza usa i centri a destra e a sinistra, separati da 60 m. Il bordo viene escluso perché manca uno dei due vicini.'),
 step('Confrontare la funzione di servizio con la formula','La funzione usata negli altri notebook deve riprodurre il calcolo esplicito del piano.','''
 prova <- gradienti_centrali(P)
 data.frame(celle_interne=length(prova$gx),bordo_escluso=length(P)-length(prova$gx),
   errore_gx=max(abs(prova$gx-gx)),errore_gy=max(abs(prova$gy-gy)))
 stopifnot(max(abs(prova$gx-gx))<1e-12,max(abs(prova$gy-gy))<1e-12)
 ''','Un test analitico rivela errori di segno, assi o denominatore. Non dimostra che i dati reali siano privi di errore o che un modello di superficie sia adeguato.'),
 step('Il piano mantiene gradienti costanti','Disegniamo il caso sintetico e salviamo gli scarti rispetto ai valori attesi.','''
 mappa_matrice(P,titolo="Piano noto: gx=0.12, gy=0.08")
 write.csv(risultato,percorso_risultati("prova_derivate.csv"),row.names=FALSE)
 ''','La superficie cresce verso Est e verso Nord. Le due componenti della derivata sono rapporti fra metri verticali e metri orizzontali.')],
 step('Sbagliare la distanza fra i vicini raddoppia il risultato','Usare 30 m nel denominatore al posto di 60 m e riconoscere l’errore.','''
 errata <- (P[2:23,3:30]-P[2:23,1:28])/30
 data.frame(gx_corretto=mean(gx),gx_errato=mean(errata),rapporto=mean(errata)/mean(gx))
 stopifnot(abs(mean(errata)-.24)<1e-12)
 ''','La distanza della differenza centrale è due volte il passo. La forma regolare della mappa non rende visibile da sola un errore di scala.'),
 'Dividere per un solo passo, scambiare gx e gy o attribuire derivata ai bordi senza una regola specifica.',
 'Un piano noto fornisce un controllo indipendente: le 616 celle interne devono restituire 0,12 e 0,08 entro la tolleranza numerica dichiarata. Derivate e unità si verificano prima dell’interpretazione geomorfologica.')

nb('Una pendenza di 45 gradi coincide con il 45 per cento?',
 ['Calcolare il modulo del gradiente interno.','Distinguere angolo in gradi e rapporto percentuale.','Conservare le coordinate delle 616 celle valide.'],DATA,[
 step('Dal gradiente a due unità di pendenza','Le differenze centrali producono due rapporti adimensionali. Angolo e percentuale derivano dallo stesso modulo g, con trasformazioni diverse.',LOAD+'''
 g <- gradienti_centrali(Z)
 risultato <- data.frame(x_m=rep((1:28)*30,22),y_m=rep((1:22)*30,each=28),
   gradi=as.vector(t(g$gradi)),percento=as.vector(t(g$percento)))
 summary(risultato[c("gradi","percento")])
 stopifnot(nrow(risultato)==616L,all(risultato$gradi>=0&risultato$gradi<90))
 ''','La relazione è angolo = arctan(g) e percentuale = 100g. Le due colonne non sono intercambiabili.'),
 step('Tre valori di riferimento controllano la conversione','Usiamo angoli noti e verifichiamo il percorso inverso.','''
 angoli <- c(0,10,45)
 conversione <- data.frame(gradi=angoli,percento=100*tan(angoli*pi/180))
 conversione
 errore <- max(abs(atan(risultato$percento/100)*180/pi-risultato$gradi))
 data.frame(errore_ritorno_gradi=errore)
 stopifnot(abs(conversione$percento[3]-100)<1e-10,errore<1e-10)
 ''','45 gradi corrispondono al 100 per cento. La percentuale può superare 100; non è una probabilità.'),
 step('L’istogramma dichiara l’unità','Il grafico riguarda le sole celle interne su cui la derivata centrale è definita.','''
 stile_grafico()
 hist(risultato$gradi,breaks=20,col=palette_geo[1],border="white",
   xlab="Pendenza (gradi)",ylab="Numero di celle interne",main="Pendenza sintetica: 616 celle interne")
 write.csv(risultato,percorso_risultati("pendenze_interne.csv"),row.names=FALSE)
 write.csv(conversione,percorso_risultati("conversione_unita.csv"),row.names=FALSE)
 ''','Le celle sono spazialmente dipendenti. Le barre descrivono una distribuzione di valori, non 616 repliche indipendenti.')],
 step('Conservare le unità del piano analitico','Verificare la pendenza di un piano con gradiente (0,12; 0,08).','''
 modulo <- sqrt(.12^2+.08^2)
 data.frame(modulo=modulo,gradi=atan(modulo)*180/pi,percento=100*modulo)
 ''','Un caso analitico aiuta a riconoscere valori impossibili o conversioni mancanti, ma non quantifica da solo l’errore del DEM.'),
 'Confondere gradi e percentuale, dimenticare radianti o trattare tutte le celle interne come repliche indipendenti.',
 'La pendenza in gradi è un angolo; quella percentuale è cento volte il dislivello per unità di distanza orizzontale. Entrambe richiedono unità coerenti e una regola esplicita per i bordi.')

nb('Come si media una direzione vicina al passaggio fra 359 e 0 gradi?',
 ['Riprodurre il caso originale 359° e 1°.','Usare seno, coseno e lunghezza della risultante.','Riconoscere quando una direzione media è indefinita.'],DATA,[
 step('La media aritmetica perde la circolarità','Due direzioni quasi settentrionali non hanno come direzione media il Sud.',LOAD+'''
 a <- c(359,1);radiani <- a*pi/180
 media <- media_circolare(a)
 risultato <- data.frame(arimetica=mean(a),circolare=unname(media["media_gradi"]),
   risultante=unname(media["risultante"]))
 risultato
 stopifnot(abs(risultato$circolare)<1e-8,risultato$risultante>.99)
 ''','La media circolare somma vettori unitari e ne legge la direzione. Il nome arimetica nella tabella originale è conservato; il valore è la media aritmetica.'),
 step('L’esposizione del terreno richiede anche una pendenza','Calcoliamo l’azimut di discesa dal gradiente. Usiamo Nord=0° e senso orario; le celle quasi piatte non hanno una direzione affidabile.','''
 g <- gradienti_centrali(Z)
 soglia <- 1e-8
 esposizione <- g$azimut_discesa;esposizione[g$modulo<=soglia] <- NA_real_
 data.frame(celle_interne=length(esposizione),direzioni_valide=sum(is.finite(esposizione)),
   minimo= min(esposizione,na.rm=TRUE),massimo=max(esposizione,na.rm=TRUE),
   soglia_gradiente=soglia)
 stopifnot(all(esposizione[is.finite(esposizione)]>=0 & esposizione[is.finite(esposizione)]<360))
 ''','L’esposizione è l’azimut della discesa, calcolato con atan2(-gx,-gy). La convenzione e il trattamento delle celle piatte devono accompagnare i valori.'),
 step('Leggere le due medie sul cerchio','Il grafico mostra la differenza geometrica tra media lineare e media circolare.','''
 stile_grafico();par(mar=c(2,2,3,2))
 theta <- seq(0,2*pi,length.out=361)
 plot(sin(theta),cos(theta),type="l",asp=1,axes=FALSE,xlim=c(-1.3,1.3),ylim=c(-1.3,1.3),
   xlab="",ylab="",col="grey70",main="359 e 1 gradi: due direzioni vicine al Nord")
 points(sin(radiani),cos(radiani),pch=19,col=palette_geo[1])
 arrows(0,0,0,.9,length=.12,lwd=2,col=palette_geo[1])
 arrows(0,0,0,-.9,length=.12,lwd=2,col=palette_geo[2])
 text(c(-.42,.42),c(1.05,1.05),c("359 gradi","1 grado"),cex=.85)
 text(.05,.52,"Circolare: 0",pos=4,col=palette_geo[1],cex=.85)
 text(.05,-.52,"Aritmetica: 180",pos=4,col=palette_geo[2],cex=.85)
 text(c(0,1.15,0,-1.15),c(1.25,0,-1.2,0),c("N","E","S","O"))
 write.csv(risultato,percorso_risultati("media_angoli.csv"),row.names=FALSE)
 ''','Le due osservazioni sono quasi coincidenti a Nord. Il valore aritmetico 180° indica invece una direzione opposta.')],
 step('Due direzioni opposte non definiscono una media stabile','Usare 0° e 180° e controllare la lunghezza della risultante.','''
 opposte <- media_circolare(c(0,180))
 opposte
 stopifnot(is.na(opposte["media_gradi"]),opposte["risultante"]<1e-8)
 ''','Quando la risultante è quasi zero, l’angolo numerico ottenuto da atan2 è instabile. La convenzione qui restituisce NA, evitando una direzione senza sostegno geometrico.'),
 'Mediare direttamente gli angoli o interpretare l’esposizione di una cella piatta come una direzione fisica ben definita.',
 'Le direzioni si sintetizzano sul cerchio. Occorre dichiarare Nord, senso di rotazione, risultante e regola per valori piatti o angoli che si compensano.')

nb('Cambiare la luce modifica il rilievo o soltanto la sua rappresentazione?',
 ['Conservare pendenza e esposizione del terreno.','Calcolare due illuminazioni con azimut opposti.','Verificare la formula con il prodotto fra normale e luce.'],DATA,[
 step('La superficie rimane fissa','Usiamo le 616 celle interne e altezza solare di 45°. Cambia soltanto l’azimut della sorgente luminosa.',LOAD+'''
 g <- gradienti_centrali(Z)
 h1 <- hillshade_esplicito(g$gx,g$gy,315,45)
 h2 <- hillshade_esplicito(g$gx,g$gy,135,45)
 risultato <- data.frame(azimut=c(315,135),altezza=45,media=c(mean(h1),mean(h2)),
   minimo=c(min(h1),min(h2)),massimo=c(max(h1),max(h2)))
 risultato
 stopifnot(identical(dim(h1),c(22L,28L)),all(h1>=0&h1<=1),all(h2>=0&h2<=1))
 ''','L’intensità modellata va da 0 a 1. Non è una nuova quota e non è una misura radiometrica osservata.'),
 step('Una seconda formulazione verifica segni e assi','Il prodotto della normale unitaria con il vettore della luce deve coincidere con la formula basata su pendenza ed esposizione.','''
 errori <- vapply(c(315,135),function(az) {
   luce <- c(sin(az*pi/180)*cos(pi/4),cos(az*pi/180)*cos(pi/4),sin(pi/4))
   attesa <- (-g$gx*luce[1]-g$gy*luce[2]+luce[3])/sqrt(1+g$gx^2+g$gy^2)
   attesa[attesa<0] <- 0
   max(abs(hillshade_esplicito(g$gx,g$gy,az,45)-attesa))
 },numeric(1))
 data.frame(azimut=c(315,135),errore_massimo=errori)
 stopifnot(all(errori<1e-12))
 ''','Questo controllo protegge la convenzione dell’azimut. Il modello considera illuminazione locale; non calcola ombre portate da rilievi lontani.'),
 step('Due luci, una scala di intensità comune','Le due carte usano la stessa scala 0–1, così la differenza dipende dall’illuminazione dichiarata.','''
 op <- par(no.readonly=TRUE);layout(matrix(1:3,nrow=1),widths=c(4,4,.7))
 for(k in 1:2) {
   stile_grafico();par(mar=c(4.2,4,3,.4),cex=.8)
   image((1:28)*30,(1:22)*30,t(list(h1,h2)[[k]]),asp=1,col=gray.colors(40,start=0,end=1),
     zlim=c(0,1),xlab="x locale (m)",ylab="y locale (m)",main=paste("Azimut",c(315,135)[k]),useRaster=TRUE)
 }
 par(mar=c(4.2,0,3,2.7));plot.new();plot.window(xlim=c(0,1),ylim=c(0,1))
 br <- seq(0,1,length.out=41)
 rect(0,head(br,-1),.5,tail(br,-1),col=gray.colors(40,start=0,end=1),border=NA)
 axis(4,at=c(0,.5,1),las=1);mtext("I",side=3,line=.5)
 layout(1);par(op)
 write.csv(risultato,percorso_risultati("illuminazioni.csv"),row.names=FALSE)
 ''','Il contrasto visivo può cambiare molto senza che il DEM cambi. Un hillshade non sostituisce legenda delle quote, orientamento o controlli del terreno.')],
 step('Cambiare anche l’altezza della luce','Confrontare 20° e 70° mantenendo azimut 315° e verificare la stessa formulazione vettoriale.','''
 verifica <- lapply(c(20,70),function(alt) {
   h <- hillshade_esplicito(g$gx,g$gy,315,alt)
   luce <- c(sin(315*pi/180)*cos(alt*pi/180),cos(315*pi/180)*cos(alt*pi/180),sin(alt*pi/180))
   attesa <- (-g$gx*luce[1]-g$gy*luce[2]+luce[3])/sqrt(1+g$gx^2+g$gy^2)
   attesa[attesa<0] <- 0
   data.frame(altezza=alt,media=mean(h),errore=max(abs(h-attesa)))
 })
 verifica <- do.call(rbind,verifica);verifica
 stopifnot(all(verifica$errore<1e-12))
 ''','La prova con altezze diverse da 45° distingue correttamente seno e coseno dell’altezza luminosa.'),
 'Interpretare i chiari e gli scuri come variazioni di quota o come una misura della riflettanza del terreno.',
 'L’hillshade è una rappresentazione condizionata a luce, convenzioni e modello di illuminazione. La topografia resta fissa; l’intensità cambia con azimut e altezza solare.')

nb('Che cosa misura un indice normalizzato costruito da due bande sintetiche?',
 ['Riprodurre le due bande del laboratorio.','Controllare denominatore, intervallo e geometria.','Separare formula e interpretazione fisica.'],DATA,[
 step('Le bande sono dichiarate e sintetiche','Il rosso varia con y e il NIR con x, secondo le formule originali. Non sono bande acquisite da un sensore.',LOAD+'''
 rosso <- .2+.05*cos(d$y_m/150)
 nir <- .4+.1*sin(d$x_m/180)
 indice <- (nir-rosso)/(nir+rosso)
 risultato <- data.frame(riga=d$riga,colonna=d$colonna,rosso=rosso,NIR=nir,indice=indice)
 head(risultato,6)
 data.frame(minimo=min(indice),massimo=max(indice),denominatore_min=min(nir+rosso))
 stopifnot(all(nir+rosso>0),all(abs(indice)<=1))
 ''','Con bande non negative e somma positiva, la formula restituisce valori fra −1 e 1. Questa proprietà algebrica non identifica da sola vegetazione, litologia o qualità ambientale.'),
 step('Il rapporto normalizza una differenza','Confrontiamo differenza, somma e indice su alcune celle esplicite.','''
 ii <- c(1,30,361,720)
 data.frame(riga=d$riga[ii],colonna=d$colonna[ii],differenza=nir[ii]-rosso[ii],
   somma=nir[ii]+rosso[ii],indice=indice[ii])
 stopifnot(max(abs(indice*(nir+rosso)-(nir-rosso)))<1e-12)
 ''','Un indice è una trasformazione deterministica delle bande. I suoi valori non sono osservazioni indipendenti aggiuntive.'),
 step('La mappa conserva la geometria delle bande','Le due bande sono allineate per costruzione. L’indice mantiene le stesse celle e la stessa maschera.','''
 mappa_matrice(matrix(indice,24,byrow=TRUE),titolo="Indice da bande sintetiche allineate",
   unita="Indice",limiti=c(-1,1),colori=colorRampPalette(c("#985052","#F3F0DF","#1D7890"))(40))
 write.csv(risultato,percorso_risultati("bande_e_indice.csv"),row.names=FALSE)
 ''','La scala −1–1 esplicita l’intervallo algebrico. Il nome di una formula non basta per attribuire ai dati una calibrazione fisica.')],
 step('Un fattore comune si cancella, un offset comune no','Moltiplicare entrambe le bande per 100 e poi aggiungere 0,1 a entrambe; confrontare gli indici.','''
 scalato <- (100*nir-100*rosso)/(100*nir+100*rosso)
 offset <- ((nir+.1)-(rosso+.1))/((nir+.1)+(rosso+.1))
 data.frame(errore_fattore_comune=max(abs(scalato-indice)),
   variazione_offset=max(abs(offset-indice)))
 stopifnot(max(abs(scalato-indice))<1e-12,max(abs(offset-indice))>0)
 ''','L’invarianza a un fattore comune non rende irrilevante la calibrazione. Offset, scale differenti, maschere e disallineamento possono modificare il risultato.'),
 'Interpretare l’indice sintetico come una diagnosi ambientale reale o combinare bande senza controllare allineamento e calibrazione.',
 'Il rapporto normalizzato sintetizza due bande definite sulle stesse celle. Le proprietà algebriche sono verificabili; il significato fisico richiede informazioni sul sensore, sulle bande, sulla calibrazione e sulla maschera.')

nb('Quando il denominatore è troppo piccolo, qual è la regola del calcolo?',
 ['Conservare la soglia originale di 10⁻⁶.','Distinguere zero esatto e denominatore piccolo.','Verificare la sensibilità e documentare la maschera.'],DATA,[
 step('Una regola prima del rapporto','Usiamo i quattro casi originali. L’indice è calcolato solo se la somma supera 10⁻⁶ nelle unità delle bande.',LOAD+'''
 rosso <- c(.2,0,1e-10,.3);nir <- c(.4,0,2e-10,.2)
 den <- nir+rosso;soglia <- 1e-6;ok <- den>soglia
 indice <- rep(NA_real_,4);indice[ok] <- (nir[ok]-rosso[ok])/den[ok]
 risultato <- data.frame(caso=1:4,rosso=rosso,NIR=nir,denominatore=den,
   usato=ok,indice=indice)
 risultato
 stopifnot(sum(is.na(indice))==2L)
 ''','Il terzo caso avrebbe un rapporto finito, ma la sua scala assoluta è troppo piccola rispetto alla soglia dichiarata. La maschera non riguarda soltanto le divisioni per zero.'),
 step('Un piccolo errore assoluto può diventare grande nel rapporto','Nel caso piccolo aggiungiamo 10⁻¹⁰ alla sola banda rossa e confrontiamo gli indici non mascherati.','''
 originale_piccolo <- (nir[3]-rosso[3])/(nir[3]+rosso[3])
 perturbato <- (nir[3]-(rosso[3]+1e-10))/(nir[3]+rosso[3]+1e-10)
 data.frame(indice_non_mascherato=originale_piccolo,indice_perturbato=perturbato,
   variazione=perturbato-originale_piccolo,perturbazione_assoluta=1e-10)
 ''','Il calcolo è algebricamente definito ma sensibile. Una soglia ha senso rispetto alle unità, alla precisione e alla qualità delle bande.'),
 step('NA resta riconoscibile nella rappresentazione','La figura distingue valori calcolati e casi esclusi. Nessun valore mancante è sostituito da zero.','''
 stile_grafico()
 plot(1:4,rep(NA_real_,4),type="n",xlim=c(.5,4.5),ylim=c(-.4,.6),xaxt="n",
   xlab="Caso originale",ylab="Indice normalizzato",main="Maschera del denominatore: due casi esclusi")
 rect(c(1.7,2.7),-.4,c(2.3,3.3),.6,col="#EDF0F1",border=NA)
 axis(1,at=1:4);abline(h=0,col="grey70",lty=3)
 points(which(ok),indice[ok],pch=19,cex=1.3,col=palette_geo[1])
 text(which(!ok),rep(.1,sum(!ok)),"NA",col=palette_geo[2])
 write.csv(risultato,percorso_risultati("maschera_denominatore.csv"),row.names=FALSE,na="")
 ''','NA indica la decisione della maschera. Il simbolo non rappresenta un indice pari a zero.')],
 step('Cambiare soglia cambia la copertura','Ripetere la regola con tre soglie e contare i casi ammessi, senza scegliere la soglia dal risultato più favorevole.','''
 soglie <- c(1e-12,1e-6,.1)
 data.frame(soglia=soglie,ammessi=vapply(soglie,function(t) sum(den>t),integer(1)))
 ''','La soglia più piccola ammette il caso numericamente sensibile. La scelta va motivata con unità e qualità del dato, non con l’aspetto della carta.'),
 'Dividere sempre e correggere dopo i risultati oppure usare una soglia senza dichiararne unità e conseguenza sulla copertura.',
 'La regola del denominatore fa parte della definizione operativa dell’indice. Valori, soglia e maschera devono essere conservati insieme; la presenza di un numero finito non garantisce stabilità.')

nb('Dopo una statistica zonale, che cosa rappresenta una riga della tabella?',
 ['Conservare media, dispersione e numero di celle per unità.','Verificare la media globale con i pesi corretti.','Distinguere dispersione e incertezza della media.'],DATA,[
 step('Le celle vengono riassunte per unità','Ogni riga della nuova tabella descrive la classe A o B, non una cella.',LOAD+'''
 gruppi <- split(d$quota_m,d$unita)
 risultato <- do.call(rbind,lapply(names(gruppi),function(u) data.frame(unita=u,
   media=mean(gruppi[[u]]),sd=sd(gruppi[[u]]),n=length(gruppi[[u]]))))
 rownames(risultato) <- NULL
 risultato
 stopifnot(sum(risultato$n)==720L)
 ''','La deviazione standard descrive la dispersione delle quote nelle celle della zona. Non è un errore standard della media e non presume indipendenza spaziale.'),
 step('Ricostruire la media delle celle richiede i conteggi','La media delle medie zonali può differire dalla media delle 720 celle se le zone hanno estensione diversa.','''
 controllo <- data.frame(media_celle=mean(d$quota_m),media_zone=mean(risultato$media),
   media_zone_pesata=weighted.mean(risultato$media,risultato$n))
 controllo
 stopifnot(abs(controllo$media_celle-controllo$media_zone_pesata)<1e-10)
 ''','Con celle della stessa area, il numero di celle è il peso planimetrico. La media semplice delle zone risponde invece a una domanda che attribuisce lo stesso peso a ogni zona.'),
 step('Mostrare la distribuzione prima di ridurla a una media','Il boxplot descrive mediana e dispersione; il rombo indica la media zonale calcolata.','''
 stile_grafico()
 boxplot(quota_m~unita,data=d,col=palette_geo[1:2],xlab="Unita sintetica",ylab="Quota (m)",
   main="Distribuzione delle quote per zona")
 points(seq_len(nrow(risultato)),risultato$media,pch=18,cex=1.3,col="#15283E")
 legend("topleft","Rombo: media zonale",pch=18,col="#15283E",bty="n",cex=.8)
 write.csv(risultato,percorso_risultati("statistiche_zonali.csv"),row.names=FALSE)
 write.csv(controllo,percorso_risultati("controllo_pesi_zonali.csv"),row.names=FALSE)
 ''','Questa figura non è un test tra campioni indipendenti. Le distribuzioni riguardano due porzioni del campo sintetico.')],
 step('La copertura si controlla per zona','Mascherare le prime 20 celle di A in memoria e riportare la copertura delle due zone.','''
 copia <- d;ii <- which(copia$unita=="A")[1:20];copia$quota_m[ii] <- NA_real_
 do.call(rbind,lapply(split(copia$quota_m,copia$unita),function(v)
   data.frame(totali=length(v),disponibili=sum(is.finite(v)),copertura=mean(is.finite(v)),
     media_disponibili=mean(v,na.rm=TRUE))))
 ''','Una copertura globale può nascondere perdite concentrate in una zona. Il numero di celle disponibili deve accompagnare ogni statistica.'),
 'Mescolare righe di celle e righe di zone, omettere i conteggi o usare sd/√n senza un modello della dipendenza.',
 'Una sintesi zonale cambia il livello della tabella. Unità, numero di celle, copertura e dispersione consentono di interpretare la media e scegliere pesi coerenti con la domanda.')

nb('Le differenze fra celle a 30 e 300 metri hanno la stessa distribuzione?',
 ['Conservare le coppie orizzontali originali.','Contare le coppie e descrivere le differenze assolute.','Riconoscere trend, direzione e riuso delle celle.'],DATA,[
 step('Due distanze, stessa direzione','Costruiamo le differenze orizzontali: una colonna e dieci colonne di distanza.',LOAD+'''
 breve <- as.vector(Z[,2:30]-Z[,1:29])
 lunga <- as.vector(Z[,11:30]-Z[,1:20])
 risultato <- data.frame(distanza_m=c(30,300),direzione="Est-Ovest",coppie=c(length(breve),length(lunga)),
   media_abs=c(mean(abs(breve)),mean(abs(lunga))),mediana_abs=c(median(abs(breve)),median(abs(lunga))))
 risultato
 stopifnot(length(breve)==696L,length(lunga)==480L)
 ''','Le due distanze usano numerosità e porzioni di griglia diverse. Molte coppie condividono una cella e non sono repliche indipendenti.'),
 step('Separare differenza firmata e dissimilarità','La media firmata può riflettere un gradiente verso Est; la media assoluta riassume una dissimilarità.','''
 data.frame(distanza_m=c(30,300),media_firmata=c(mean(breve),mean(lunga)),
   sd_differenze=c(sd(breve),sd(lunga)),media_quadratica=c(mean(breve^2),mean(lunga^2)))
 ''','Differenze più grandi a distanza maggiore non dimostrano da sole una legge di covarianza: trend e orientamento possono contribuire.'),
 step('La figura mantiene conteggi e unità','Le barre rappresentano metri di differenza assoluta media, senza barre di errore che fingano indipendenza delle coppie.','''
 stile_grafico()
 bp <- barplot(risultato$media_abs,names.arg=paste(risultato$distanza_m,"m"),col=palette_geo[1:2],
   ylim=c(0,max(risultato$media_abs)*1.22),xlab="Separazione Est-Ovest",ylab="Differenza assoluta media (m)",
   main="Distanza e differenze fra celle")
 text(bp,risultato$media_abs,labels=paste0("n=",risultato$coppie),pos=3,cex=.8)
 write.csv(risultato,percorso_risultati("differenze_spaziali.csv"),row.names=FALSE)
 ''','La carta e le direzioni del rilievo completano il confronto; il conteggio delle coppie non misura il numero di informazioni indipendenti.')],
 step('Cambiare direzione mantenendo le distanze','Ripetere il confronto lungo Nord-Sud.','''
 nord30 <- as.vector(Z[2:24,]-Z[1:23,])
 nord300 <- as.vector(Z[11:24,]-Z[1:14,])
 data.frame(distanza_m=c(30,300),direzione="Nord-Sud",coppie=c(length(nord30),length(nord300)),
   media_abs=c(mean(abs(nord30)),mean(abs(nord300))))
 stopifnot(length(nord30)==690L,length(nord300)==420L)
 ''','Una differenza fra direzioni è descrittiva. Prima di attribuirla ad anisotropia della componente residua occorre discutere il trend e il dominio.'),
 'Interpretare tutte le differenze come indipendenti oppure dedurre una covarianza stazionaria dal solo confronto di due distanze.',
 'La distanza entra nella dissimilarità, ma la sintesi dipende anche da direzione, dominio e trend. Le coppie sono costruite riusando le stesse celle e richiedono un’interpretazione coerente.')

nb('Che cosa assume un bootstrap che ricampiona dodici blocchi del raster?',
 ['Riprodurre i 12 blocchi originali di 6 × 10 celle.','Usare le 300 repliche determinate dal file u.','Interpretare i quantili come dimostrazione condizionata alle ipotesi.'],DATA,[
 step('La replica campiona blocchi, non singole celle','I blocchi sono disgiunti, completi e di uguale dimensione: 60 celle, cioè 5,4 ettari ciascuno.',LOAD+'''
 v <- numeric(12);k <- 1L
 for(i in 1:4) for(j in 1:3) {
   v[k] <- mean(Z[((i-1)*6+1):(i*6),((j-1)*10+1):(j*10)])
   k <- k+1L
 }
 data.frame(blocco=1:12,media=v,celle=60)
 stopifnot(abs(mean(v)-mean(Z))<1e-10)
 ''','L’uguaglianza delle medie deriva dal bilanciamento dei blocchi. La geometria del blocco definisce quanta dipendenza locale si conserva nel ricampionamento.'),
 step('Il protocollo originale usa uniformi salvate','Ogni replica seleziona 12 blocchi con reinserimento. I primi 3600 valori u determinano le 300 repliche.','''
 casuali <- carica_dati("casuali_comuni_v3.csv");u <- casuali$u
 stopifnot(length(u)>=3600L,all(u[1:3600]>=0 & u[1:3600]<1))
 ix <- matrix(floor(u[1:3600]*12)+1,300,byrow=TRUE)
 b <- apply(ix,1,function(i) mean(v[i]))
 q <- quantile(b,c(.025,.975),type=7)
 risultato <- data.frame(media=mean(v),basso=unname(q[1]),alto=unname(q[2]),
   repliche=length(b),blocchi=length(v),sd_repliche=sd(b))
 risultato
 stopifnot(length(b)==300L,all(ix>=1&ix<=12))
 ''','I quantili descrivono il meccanismo di ricampionamento scelto. Non garantiscono copertura del 95%: con soli 12 blocchi, trend e scambiabilità dubbia, l’interpretazione inferenziale richiede cautela motivata.'),
 step('La distribuzione è condizionata ai blocchi osservati','Il grafico distingue media della griglia e quantili bootstrap. Il titolo non li presenta come intervallo garantito.','''
 stile_grafico()
 hist(b,breaks=20,col=palette_geo[1],border="white",xlab="Media dei blocchi ricampionati (m)",
   ylab="Numero di repliche",main="Bootstrap a blocchi: distribuzione condizionata")
 abline(v=mean(v),col=palette_geo[2],lwd=2);abline(v=q,col=palette_geo[3],lty=2,lwd=2)
 legend("topright",c("Media della griglia","Quantili 2.5% e 97.5%"),
   col=palette_geo[c(2,3)],lty=c(1,2),bty="n",cex=.75)
 write.csv(risultato,percorso_risultati("bootstrap_blocchi.csv"),row.names=FALSE)
 write.csv(data.frame(replica=1:300,media=b),percorso_risultati("repliche_blocchi.csv"),row.names=FALSE)
 ''','Il campo finito di 720 celle è completamente noto in questo esercizio. L’uso del bootstrap è didattico: una vera inferenza deve prima specificare il parametro, il campionamento o il modello aleatorio.')],
 step('Cambiare l’unità di ricampionamento cambia la domanda','Con un nuovo seme esplicito, ricampionare singole celle come confronto di meccanismi, senza dichiararle indipendenti.','''
 set.seed(20261117)
 celle <- as.vector(Z)
 iid <- replicate(300,mean(celle[sample.int(length(celle),length(celle),replace=TRUE)]))
 confronto <- data.frame(schema=c("Blocchi originali","Singole celle: ipotesi iid"),
   sd_repliche=c(sd(b),sd(iid)),basso=c(unname(q[1]),unname(quantile(iid,.025))),
   alto=c(unname(q[2]),unname(quantile(iid,.975))))
 confronto
 write.csv(confronto,percorso_risultati("confronto_meccanismi_bootstrap.csv"),row.names=FALSE)
 ''','Lo schema iid distrugge la struttura spaziale. Una differenza fra gli intervalli non dimostra quale abbia copertura corretta; rende visibile la dipendenza dalle ipotesi.'),
 'Chiamare automaticamente intervallo di confidenza al 95% i quantili di 300 repliche o presumere che il ricampionamento a blocchi risolva qualsiasi trend.',
 'Il bootstrap a blocchi è un meccanismo esplicito che conserva la struttura entro i blocchi e ne ricampiona le medie. Le sue proprietà inferenziali dipendono da parametro, blocchi, dipendenza e scambiabilità; qui è una dimostrazione condizionata, non una garanzia di copertura.')

nb('Come si legge una finestra del GeoTIFF senza confondere indici e orientamento?',
 ['Eseguire readStart, readValues e readStop di terra.','Verificare le 48 celle originali contro la matrice completa.','Distinguere una prova su file piccolo da una strategia per grandi raster.'],GEO,[
 step('Una finestra usa gli indici del TIFF','Le righe R 5:10 e le colonne R 10:17 del TIFF individuano 6 × 8 celle. Le righe procedono da Nord a Sud.',TERRA+'''
 leggi_finestra <- function(r,row,nrows,col,ncols) {
   terra::readStart(r)
   on.exit(terra::readStop(r))
   terra::readValues(r,row=row,nrows=nrows,col=col,ncols=ncols,mat=FALSE)
 }
 win <- leggi_finestra(r,5,6,10,8)
 data.frame(valori=length(win),minimo=min(win),massimo=max(win),media=mean(win))
 stopifnot(length(win)==48L)
 ''','La lettura è effettiva sul file. on.exit garantisce la chiusura anche se una successiva operazione nella funzione fallisce.'),
 step('Il confronto con la matrice completa è un controllo','Per questo piccolo esercizio carichiamo anche l’intera matrice e verifichiamo ordinamento e valori.','''
 M <- terra::as.matrix(r,wide=TRUE)
 attesi <- as.vector(t(M[5:10,10:17]))
 risultato <- data.frame(n=length(win),errore=max(abs(win-attesi)),
   bytes_valori_finestra=as.numeric(object.size(win)),bytes_matrice=as.numeric(object.size(M)))
 risultato
 stopifnot(risultato$errore<1e-10)
 ''','La matrice completa serve qui per verificare il risultato. Queste misure di object.size non includono cache GDAL, processi o memoria totale e non sono un benchmark di I/O.'),
 step('La finestra torna nel piano locale','Per la carta invertiamo le sei righe della finestra. I suoi centri sono x=270…480 m e y=420…570 m.','''
 W <- matrix(win,nrow=6,ncol=8,byrow=TRUE)
 mappa_matrice(W[6:1,],seq(270,480,30),seq(420,570,30),
   titolo="Finestra letta dal GeoTIFF: 48 celle",limiti=range(Z))
 write.csv(risultato,percorso_risultati("audit_finestra.csv"),row.names=FALSE)
 write.csv(data.frame(ordine=seq_along(win),quota_m=win),percorso_risultati("valori_finestra.csv"),row.names=FALSE)
 ''','Una finestra di lettura seleziona un sottoinsieme senza cambiare i valori. Le coordinate restano necessarie per collegare quel sottoinsieme alla griglia.')],
 step('Due finestre coprono l’intero raster','Leggere separatamente le metà settentrionale e meridionale e ricostruire la media globale con i conteggi.','''
 nord <- leggi_finestra(r,1,12,1,30)
 sud <- leggi_finestra(r,13,12,1,30)
 media_finestre <- weighted.mean(c(mean(nord),mean(sud)),c(length(nord),length(sud)))
 data.frame(n_nord=length(nord),n_sud=length(sud),media_finestre=media_finestre,
   media_intera=mean(M),scarto=abs(media_finestre-mean(M)))
 stopifnot(length(nord)+length(sud)==720L,abs(media_finestre-mean(M))<1e-10)
 ''','L’elaborazione a finestre può accumulare somme e conteggi. Derivate e filtri richiederebbero anche un margine di vicini attorno a ciascuna finestra.'),
 'Scambiare le righe del CSV e del TIFF, chiamare prova di memoria un confronto di object.size o ignorare i margini necessari ai filtri.',
 'La lettura a finestre controlla quanti valori vengono materializzati per operazione. Una verifica corretta confronta celle e orientamento; il trattamento di filtri, bordi e NoData resta parte dell’algoritmo.')

nb('Due raster con la stessa forma e lo stesso passo sono necessariamente allineati?',
 ['Costruire due geometrie terra traslate di mezzo pixel.','Controllare estensione, centri e origine.','Eseguire un ricampionamento esplicito e verificarne il bersaglio.'],GEO,[
 step('La traslazione cambia la posizione delle celle','Usiamo il GeoTIFF originale e una copia spostata di 15 m verso Est. Quote e dimensioni restano uguali in memoria.',TERRA+'''
 spostato <- terra::shift(r,dx=15,dy=0)
 risultato <- data.frame(stessa_forma=nrow(r)==nrow(spostato)&ncol(r)==ncol(spostato),
   stesso_passo=all(terra::res(r)==terra::res(spostato)),
   stessa_geometria=terra::compareGeom(r,spostato,stopOnError=FALSE),
   shift_pixel=(terra::xmin(spostato)-terra::xmin(r))/terra::res(r)[1])
 risultato
 data.frame(raster=c("Originale","Spostato"),xmin=c(terra::xmin(r),terra::xmin(spostato)),
   xmax=c(terra::xmax(r),terra::xmax(spostato)))
 stopifnot(risultato$stessa_forma,risultato$stesso_passo,!risultato$stessa_geometria,
   risultato$shift_pixel==.5)
 ''','Dimensioni uguali permettono operazioni elemento per elemento che possono essere geograficamente sbagliate. La posizione dei centri è una parte del dato.'),
 step('Allineare significa scegliere una nuova regola numerica','Ricampioniamo realmente la copia traslata sulla griglia originale con bilinear. Il bersaglio torna uguale, i valori possono cambiare.','''
 riallineato <- terra::resample(spostato,r,method="bilinear")
 v0 <- as.numeric(terra::values(r));v1 <- as.numeric(terra::values(riallineato))
 validi <- is.finite(v0)&is.finite(v1)
 audit <- data.frame(geometria_target=terra::compareGeom(r,riallineato,stopOnError=FALSE),
   coppie_valide=sum(validi),media_scarto_m=mean(v1[validi]-v0[validi]),
   massimo_scarto_m=max(abs(v1[validi]-v0[validi])))
 audit
 stopifnot(audit$geometria_target,audit$coppie_valide>0)
 ''','Il ricampionamento corregge la compatibilità delle griglie secondo una regola dichiarata. Non recupera informazioni indipendenti che la traslazione abbia reso indisponibili.'),
 step('Il mezzo pixel diventa visibile nei centri','Mostriamo sei centri effettivi delle due geometrie in coordinate relative al corner del riquadro.','''
 celle <- c(1:3,31:33)
 a <- terra::xyFromCell(r,celle);b <- terra::xyFromCell(spostato,celle)
 a <- sweep(a,2,c(500000,4999940),"-");b <- sweep(b,2,c(500000,4999940),"-")
 stile_grafico()
 plot(a,type="n",asp=1,xlim=c(-5,115),ylim=c(-5,90),
   xlab="E relativo al corner (m)",ylab="N relativo al riquadro (m)",
   main="Stesse dimensioni: centri traslati di 15 m")
 for(x in seq(0,90,30)) segments(x,0,x,60,col="#B6CDD5")
 for(y in seq(0,60,30)) segments(0,y,90,y,col="#B6CDD5")
 arrows(a[,1],a[,2],b[,1],b[,2],length=.07,col="grey55")
 points(a,pch=19,col=palette_geo[1]);points(b,pch=17,col=palette_geo[2])
 legend("topleft",c("Originale","Traslato"),pch=c(19,17),col=palette_geo[1:2],bty="n",cex=.8)
 write.csv(risultato,percorso_risultati("disallineamento.csv"),row.names=FALSE)
 write.csv(audit,percorso_risultati("ricampionamento.csv"),row.names=FALSE)
 ''','Il disegno usa centri estratti da terra, non coordinate inventate per suggerire uno spostamento.')],
 step('Anche una traslazione intera cambia l’estensione','Spostare di 30 m e controllare che la forma e il passo non bastino ancora.','''
 intero <- terra::shift(r,dx=30,dy=0)
 data.frame(shift_pixel=(terra::xmin(intero)-terra::xmin(r))/30,
   stessa_geometria=terra::compareGeom(r,intero,stopOnError=FALSE),
   stesso_passo=all(terra::res(r)==terra::res(intero)))
 stopifnot(!terra::compareGeom(r,intero,stopOnError=FALSE))
 ''','La coincidenza della griglia periodica non implica uguaglianza del dominio. Prima di combinare raster servono anche estensione e corrispondenza delle celle.'),
 'Sommare raster perché hanno lo stesso numero di righe e colonne o chiamare allineamento la sola assegnazione di un CRS.',
 'La compatibilità richiede CRS, passo, origine, estensione e orientamento coerenti. Ricampionare è un’operazione esplicita sul valore, non una semplice modifica dell’etichetta.')

nb('Come si consegnano le 616 pendenze interne mantenendo geometria, orientamento e NoData?',
 ['Scrivere e rileggere il CSV originale delle celle interne.','Esportare GeoTIFF reali con terra.','Verificare valori, CRS, risoluzione, centri e maschera di bordo.'],GEO,[
 step('Il CSV mantiene le coordinate delle celle interne','La differenza centrale esclude una fascia di una cella su ciascun lato. I 616 valori sono ordinati da Sud a Nord nel CSV.',TERRA+'''
 g <- gradienti_centrali(Z);s <- g$gradi
 risultato <- data.frame(x_m=rep((1:28)*30,22),y_m=rep((1:22)*30,each=28),
   pendenza_gradi=as.vector(t(s)))
 file_csv <- percorso_risultati("pendenze.csv")
 write.csv(risultato,file_csv,row.names=FALSE)
 csv_letto <- read.csv(file_csv)
 data.frame(celle=nrow(csv_letto),minimo=min(csv_letto$pendenza_gradi),
   massimo=max(csv_letto$pendenza_gradi),errore_roundtrip=max(abs(csv_letto$pendenza_gradi-risultato$pendenza_gradi)))
 stopifnot(nrow(csv_letto)==616L,all(is.finite(csv_letto$pendenza_gradi)),
   max(abs(csv_letto$pendenza_gradi-risultato$pendenza_gradi))<1e-10)
 ''','Le coordinate interne sono x=30…840 m e y=30…660 m. Le quote originarie e le pendenze hanno unità differenti.'),
 step('Due GeoTIFF esplicitano il bordo','Il file principale è 22 × 28, ristretto alle celle interne. Il secondo conserva 24 × 30 celle, con 104 celle di bordo NoData. I valori sono materializzati prima della scrittura.','''
 completo <- matrix(NA_real_,24,30);completo[2:23,2:29] <- s
 r_completo <- raster_da_matrice(completo,r);names(r_completo) <- "pendenza_gradi"
 modello_interno <- terra::crop(terra::rast(r),terra::ext(500030,500870,4999310,4999970))
 r_interno <- raster_da_matrice(s,modello_interno);names(r_interno) <- "pendenza_gradi"
 file_interno <- percorso_risultati("pendenze_interne.tif")
 file_bordo <- percorso_risultati("pendenze_con_bordo_NoData.tif")
 terra::writeRaster(r_interno,file_interno,overwrite=TRUE,datatype="FLT8S",NAflag=-9999,gdal="COMPRESS=NONE")
 terra::writeRaster(r_completo,file_bordo,overwrite=TRUE,datatype="FLT8S",NAflag=-9999,gdal="COMPRESS=NONE")
 data.frame(file=c(basename(file_interno),basename(file_bordo)),
   righe=c(nrow(r_interno),nrow(r_completo)),colonne=c(ncol(r_interno),ncol(r_completo)),
   celle_valide=c(sum(is.finite(s)),sum(is.finite(completo))),
   celle_NoData=c(sum(is.na(s)),sum(is.na(completo))))
 ''','La georeferenziazione fittizia viene ereditata senza attribuirle realtà geografica. Nel TIFF le righe sono ribaltate rispetto al CSV; il valore NoData scritto è −9999, distinto da una pendenza nulla.'),
 step('Rilettura e verifica cella per cella','Riapriamo entrambi i file con terra. Il controllo riguarda geometria, centro di riferimento, orientamento, maschera e valori.','''
 letto <- terra::rast(file_interno);bordo <- terra::rast(file_bordo)
 valori <- matrice_locale(letto);valori_bordo <- matrice_locale(bordo)
 centri <- terra::xyFromCell(letto,c(1,terra::ncell(letto)))
 audit <- data.frame(controllo=c("Geometria interna","Geometria completa","Risoluzione 30m",
   "616 valori interni","104 NoData bordo","Maschera esatta","Valori interni","Valori completi",
   "Centro NW corretto","Centro SE corretto"),
   esito=c(terra::compareGeom(letto,r_interno,stopOnError=FALSE),
     terra::compareGeom(bordo,r,stopOnError=FALSE),all(terra::res(letto)==30),
     sum(is.finite(valori))==616L,sum(is.na(valori_bordo))==104L,
     identical(is.na(valori_bordo),is.na(completo)),max(abs(valori-s))<1e-10,
     max(abs(valori_bordo-completo),na.rm=TRUE)<1e-10,
     max(abs(centri[1,]-c(500045,4999955)))<1e-9,
     max(abs(centri[2,]-c(500855,4999325)))<1e-9))
 audit
 stopifnot(all(audit$esito))
 crs_letto <- terra::crs(letto,describe=TRUE)[,c("name","authority","code")]
 crs_letto
 info_interno <- terra::describe(file_interno,print=FALSE)
 info_bordo <- terra::describe(file_bordo,print=FALSE)
 tag_NoData <- data.frame(file=c(basename(file_interno),basename(file_bordo)),
   sentinel_meno9999=c(any(grepl("NoData Value=-9999",info_interno,fixed=TRUE)),
     any(grepl("NoData Value=-9999",info_bordo,fixed=TRUE))))
 tag_NoData
 stopifnot(all(as.character(crs_letto$code)=="32632"),all(tag_NoData$sentinel_meno9999))
 writeLines(info_interno,percorso_risultati("GDAL_pendenze_interne.txt"))
 writeLines(info_bordo,percorso_risultati("GDAL_pendenze_con_bordo.txt"))
 write.csv(tag_NoData,percorso_risultati("audit_tag_NoData.csv"),row.names=FALSE)
 write.csv(audit,percorso_risultati("audit_consegna.csv"),row.names=FALSE)
 writeLines(c("DATI SINTETICI; georeferenziazione UTM fittizia EPSG32632.",
   "CSV: 616 centri locali, righe da Sud a Nord, pendenza in gradi.",
   "GeoTIFF interno: 22x28, passo 30 m, corner NW 500030/4999970.",
   "GeoTIFF completo: 24x30, 104 celle di bordo NoData; NAflag=-9999, FLT8S.",
   "Centri: E=x_locale+500015, N=y_locale+4999295. TIFF da Nord a Sud.",
   paste("terra",packageVersion("terra"))),percorso_risultati("scheda_consegna.txt"))
 mappa_matrice(valori,(1:28)*30,(1:22)*30,titolo="Pendenze GeoTIFF rilette: 616 celle",unita="Gradi")
 ''','Un file che si apre non è necessariamente corretto. La verifica deve includere il CRS, non soltanto forma e valori; compareGeom controlla anche il riferimento geografico dei file prodotti.')],
 step('L’errore di orientamento conserva media e istogramma','Confrontare la matrice terra senza ribaltamento con la matrice locale e verificare che la media non lo riconosca.','''
 sbagliata <- terra::as.matrix(letto,wide=TRUE)
 data.frame(scarto_senza_ribaltamento=max(abs(sbagliata-s)),
   media_invariata=abs(mean(sbagliata)-mean(s))<1e-10,
   scarto_corretto=max(abs(sbagliata[nrow(sbagliata):1,]-s)))
 stopifnot(max(abs(sbagliata-s))>0)
 ''','La consegna corretta mantiene la corrispondenza cella per cella. I controlli del solo range, della media o del numero di celle non bastano.'),
 'Consegnare soltanto una matrice senza georeferenziazione, confondere bordo NoData con pendenza zero o dimenticare il ribaltamento Nord-Sud.',
 'La consegna comprende CSV, GeoTIFF interno, GeoTIFF con bordo NoData e una scheda. La rilettura reale con terra verifica 616 pendenze, 104 celle di bordo assenti, orientamento e geometria fittizia dichiarata.')

PREP='''# Trova il modulo dal progetto autonomo o da quello generale dei notebook.
.gs_cerca <- normalizePath(getwd(),winslash="/",mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca,file.path(.gs_cerca,"M12_Tessera"),
    file.path(.gs_cerca,"03_Notebook_svolti","M12_Tessera"),
    file.path(.gs_cerca,"M12","03_Notebook_svolti","M12_Tessera"))
  .gs_ok <- file.exists(file.path(.gs_candidati,"M12_N01.Rmd")) &
    file.exists(file.path(.gs_candidati,"R","funzioni_notebook.R"))
  if(any(.gs_ok)) { .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]];break }
  .gs_padre <- dirname(.gs_cerca)
  if(.gs_padre==.gs_cerca) stop("Aprire il progetto M12_Tessera o quello generale dei notebook.")
  .gs_cerca <- .gs_padre
}
source(file.path(.gs_modulo,"R","funzioni_notebook.R"),local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo,"{ID}")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88,digits=6)
if(requireNamespace("knitr",quietly=TRUE)) {
  knitr::opts_chunk$set(echo=TRUE,error=FALSE,warning=TRUE,message=TRUE,
    fig.width=8,fig.height=5,dpi=150,fig.align="center")
}
set.seed(20261104)
'''
FORMULE={
 1:r'$x_j=30j,\quad y_i=30i,\quad i=0,\ldots,23,\quad j=0,\ldots,29.$',
 3:r'$E=x_{\mathrm{locale}}+500015,\quad N=y_{\mathrm{locale}}+4999295.$',
 4:r'$\overline z_{\mathrm{disponibili}}=\frac{\sum_i m_i z_i}{\sum_i m_i},\quad m_i\in\{0,1\}.$ Qui il numeratore include soltanto le celle disponibili.',
 6:r'$A_{\mathrm{ha}}=n_{\mathrm{celle}}\,\Delta x\,\Delta y/10000.$',
 7:r'$\overline z=\frac{\sum_b n_b\overline z_b}{\sum_b n_b}.$ Con blocchi completi 2 × 2, tutti i pesi sono quattro.',
 9:r'$g_x(i,j)\simeq\frac{z_{i,j+1}-z_{i,j-1}}{2\Delta x},\qquad g_y(i,j)\simeq\frac{z_{i+1,j}-z_{i-1,j}}{2\Delta y}.$ Gli indici della matrice locale crescono verso Est e Nord.',
 10:r'$g=\sqrt{g_x^2+g_y^2},\quad \theta_{\mathrm{gradi}}=\frac{180}{\pi}\arctan(g),\quad p_{\%}=100g.$',
 11:r'$\overline a=\operatorname{atan2}(\overline{\sin a},\overline{\cos a}),\qquad \rho=\sqrt{\overline{\sin a}^{\,2}+\overline{\cos a}^{\,2}}.$ La media angolare è dichiarata indefinita quando la risultante è troppo piccola.',
 12:r'$I=\max(0,\mathbf n\cdot\mathbf l),\qquad \mathbf n=(-g_x,-g_y,1)/\sqrt{1+g_x^2+g_y^2}.$ La luce è un vettore unitario definito da azimut e altezza.',
 13:r'$v=(N-R)/(N+R).$ Le bande qui sono non negative e hanno somma strettamente positiva.',
 14:r'$v_i=(N_i-R_i)/(N_i+R_i)\quad\text{solo se}\quad N_i+R_i>10^{-6}.$ Negli altri casi il risultato è NA.',
 15:r'$\overline z_{\mathrm{celle}}=\sum_k n_k\overline z_k/\sum_k n_k.$',
 16:r'$d_h=\operatorname{media}\bigl(|z(x+h,y)-z(x,y)|\bigr).$ È una sintesi descrittiva sulla direzione e sulle coppie disponibili.',
 17:r'$\overline z^{\,*}=(1/12)\sum_{b=1}^{12}\overline z_{J_b},\qquad J_b\in\{1,\ldots,12\}.$ Il ricampionamento avviene con reinserimento.',
 20:r'$n_{\mathrm{interni}}=(24-2)(30-2)=616,\qquad n_{\mathrm{bordo}}=720-616=104.$'
}
ADATTAMENTI=[
 'Audit originale conservato; aggiunti passi sui due assi, centri/bordi e duplicato con numero di righe invariato.',
 'Matrice e angoli originali conservati; aggiunti ordinamento esplicito, inversione Nord-Sud e verifica per cella.',
 'Lettura terra effettiva; aggiunti CRS fittizio, corner/centri e confronto integrale CSV/TIFF.',
 'Maschera originale righe R5:8 colonne10:15 conservata; esplicitati indici CSV e meccanismo selettivo.',
 'Finestra inclusiva originale conservata; aggiunti 132 centri, bordi delle celle e variante stretta90celle.',
 'Conteggi e64.8ha originali conservati; aggiunto controllo planimetrico e cambio di passo.',
 'Aggregazione2x2 conservata; aggiunti centri60m e media pesata con NoData.',
 'Esempio1D originale conservato; ampliamento reale terra::resample bilinear/near su classi e quote.',
 'Piano0.12x+0.08y conservato; aggiunti prova helper,616celle e errore denominatore.',
 'Pendenza interna originale conservata; aggiunti coordinate, conversioni e prova45gradi=100percento.',
 'Caso359/1gradi conservato; aggiunti esposizione, risultante e direzioni opposte indefinite.',
 'Hillshade originale315/135 a45gradi conservato; verifica normale-luce e variante altezza20/70.',
 'Bande sintetiche originali conservate; aggiunti allineamento, scala e offset.',
 'Quattro casi e soglia1e-6 conservati; aggiunti sensibilità e maschera dichiarata.',
 'Media/sd/n zonali conservati; aggiunti pesi e copertura per zona.',
 'Differenze orizzontali30/300m conservate; aggiunta direzione Nord-Sud e avvertenza sulle coppie condivise.',
 'Dodici blocchi e300repliche dai primi3600u conservati; variante iid con seme20261117 e limiti inferenziali espliciti.',
 'Finestra originale6x8 e48valori letti realmente con terra; chiusura garantita, orientamento e due mezze finestre.',
 'Shift originale15m conservato ed eseguito con terra; resample reale e variante spostamento30m.',
 'CSV616celle originale conservato; aggiunti due GeoTIFF reali FLT8S/NoData−9999, rilettura, CRS e orientamento.'
]
PDF='../../02_PDF/M12_Tessera/Tessera_M12_raster_telerilevamento_morfometria.pdf'
def make():
 assert len(N)==20
 slides={}
 if (BASE/'MAPPA_SLIDE.csv').exists():
  slides={r['notebook']:r['slide'] for r in csv.DictReader((BASE/'MAPPA_SLIDE.csv').open())}
 records=[]
 for i,n in enumerate(N,1):
  ident=f'M12_N{i:02d}'
  yaml='---\ntitle: '+json.dumps(n['title'],ensure_ascii=False)+'\nsubtitle: "'+ident+' · Tessera"\nlang: it-IT\noutput:\n  html_document:\n    toc: true\n    self_contained: true\n    theme: null\n    highlight: tango\n    mathjax: null\n    pandoc_args: ["--mathml"]\n    css: "R/stile_notebook.css"\n---\n'
  terra_note=' Questo notebook richiede terra installato prima dell’analisi e usa le sue funzioni effettive.' if i in [3,8,18,19,20] else ' I calcoli usano R base e i pacchetti standard.'
  s=yaml+'\n# La domanda\n\n'+n['question']+'\n\n## Obiettivi\n\n'+'\n'.join('- '+x for x in n['objectives'])
  s+='\n\n**Prima di iniziare.** Sono richiesti vettori, matrici, tabelle e funzioni R di base. Eseguire i blocchi in ordine; ogni notebook è autonomo rispetto agli altri.'+terra_note
  s+='\n\n**Dati e unità.** '+n['data']
  if i in FORMULE:s+='\n\n**Relazione usata.** '+FORMULE[i]
  s+='\n\n## Preparazione\n\nAprire il progetto autonomo di Tessera o quello generale dei notebook. I file originali restano invariati. Gli output vanno in `Risultati/'+ident+'/`. Nessun download o installazione avviene nei blocchi.\n\n```{r preparazione}\n'+PREP.replace('{ID}',ident)+'```\n'
  chunks=[dict(name='preparazione',code=PREP.replace('{ID}',ident))]
  for j,st in enumerate(n['steps'],1):
   s+=f'\n## {j}. {st["title"]}\n\n{st["text"]}\n\n```{{r passo_{j:02d}}}\n{st["code"]}\n```\n\n**Lettura del risultato.** {st["reading"]}\n'
   chunks.append(dict(name=f'passo_{j:02d}',code=st['code']))
  v=n['variant'];s+=f'\n## Variante svolta\n\n**{v["title"]}.** {v["text"]}\n\n```{{r variante}}\n{v["code"]}\n```\n\n{v["reading"]}\n'
  chunks.append(dict(name='variante',code=v['code']))
  s+='\n## Errore da riconoscere\n\n'+n['error']+'\n\n## Risposta alla domanda\n\n'+n['answer']
  label='Lezione Tessera';url=PDF
  if ident in slides and re.match(r'\d+',slides[ident]):label='Slide '+slides[ident]+' della lezione Tessera';url+='#page='+re.match(r'\d+',slides[ident])[0]
  s+='\n\n## Raccordo con le slide\n\n['+label+']('+url+'). La [mappa dei notebook e delle slide](MAPPA_SLIDE.csv) conserva il raccordo puntuale con la lezione estesa.\n'
  s+='\n## Riferimenti e provenienza\n\nQuesto svolgimento sviluppa `'+ident+'` del [modulo M12 del corso](https://marzione00.github.io/Lab_Geo/#modulo-M12). Il [codice originale](https://github.com/marzione00/Lab_Geo/blob/649f7cc577b96bd1044d81e78a2f530813e4f96b/materiali/laboratori/M12/'+ident+'.R) è conservato immutato in `R/Originali_corso/`. Dati e originali hanno SHA-256 e SHA-1 Git verificati; gli ampliamenti sono dichiarati nella [mappa degli originali](MAPPA_ORIGINALI.csv).\n'
  if i in [3,8,18,19,20]:s+='\nDocumentazione primaria: [terra, rast](https://rspatial.github.io/terra/reference/rast.html), [terra, resample](https://rspatial.github.io/terra/reference/resample.html), [terra, readValues](https://rspatial.github.io/terra/reference/readValues.html), [terra, writeRaster](https://rspatial.github.io/terra/reference/writeRaster.html).\n'
  else:s+='\nDocumentazione primaria delle operazioni: [R, matrix](https://stat.ethz.ch/R-manual/R-devel/library/base/html/matrix.html), [R, image](https://stat.ethz.ch/R-manual/R-devel/library/graphics/html/image.html), [R, quantile](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/quantile.html). Le ipotesi e le convenzioni specifiche sono esplicitate nello svolgimento.\n'
  (BASE/f'{ident}.Rmd').write_text(s,encoding='utf-8')
  folder=BASE/'Verifiche'/ident;folder.mkdir(parents=True,exist_ok=True)
  for c in chunks:(folder/(c['name']+'.R')).write_text(c['code']+'\n',encoding='utf-8')
  records.append(dict(id=ident,titolo=n['title'],html=f'{ident}.html',rmd=f'{ident}.Rmd',blocchi=len(chunks),sha256_Rmd=hashlib.sha256(s.encode()).hexdigest(),chunks=[c['name'] for c in chunks]))
 (BASE/'Sorgenti_generazione/notebook_contenuti.json').write_text(json.dumps(N,ensure_ascii=False,indent=2))
 (BASE/'Verifiche/piano_esecuzione.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
 with (BASE/'INDICE_NOTEBOOK.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['id','titolo','html','rmd','blocchi']);w.writeheader()
  for r in records:w.writerow({k:r[k] for k in w.fieldnames})
 p=BASE/'R/Originali_corso/PROVENIENZA.json';j=json.loads(p.read_text())
 for i,r in enumerate(j['files']):r['sha256_svolgimento']=records[i]['sha256_Rmd'];r['adattamenti']=ADATTAMENTI[i]
 p.write_text(json.dumps(j,ensure_ascii=False,indent=2))
 with (BASE/'MAPPA_ORIGINALI.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(j['files'][0]));w.writeheader();w.writerows(j['files'])
 dst=BASE/'Sorgenti_generazione/genera_notebook.py'
 if Path(__file__).resolve()!=dst.resolve():shutil.copy2(__file__,dst)
 print('Creati 20 Rmd e 100 blocchi.')
if __name__=='__main__':make()
