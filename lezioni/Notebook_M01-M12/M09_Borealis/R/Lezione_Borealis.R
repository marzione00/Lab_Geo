# BOREALIS M09 - Esercitazioni svolte in R
# Aprire il progetto del modulo o il progetto generale dei notebook.
# Ogni sezione corrisponde al notebook indicato.


# M09_N01 - Date, valori e provenienza dell’archivio CO₂
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M09_Borealis"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M09_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M09_Borealis o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M09_N01")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(9001)


# Leggere il tempo insieme alla misura
w <- carica_dati("co2_settimanale_storica.csv")
w$data <- as.Date(w$data)
w <- w[order(w$data), ]
stopifnot(!anyNA(w$data), !anyDuplicated(w$data))
head(w, 4)
data.frame(prima=min(w$data), ultima=max(w$data),
 righe=nrow(w), osservate=sum(!is.na(w$co2)), mancanti=sum(is.na(w$co2)))


# Controllare la distanza fra le date
passi_giorni <- as.integer(diff(w$data))
table(passi_giorni)
stopifnot(all(passi_giorni==7L))
head(w[is.na(w$co2), ], 6)


# Disegnare anche le interruzioni
plot(w$data, w$co2, type="l", col="#087C74",
 xlab="Data", ylab="CO2 (ppm)", main="Archivio settimanale storico")
metadati <- data.frame(fonte="Copia statsmodels, Keeling-Whorf/CDIAC",
 prima=as.character(min(w$data)), ultima=as.character(max(w$data)),
 unita="ppm", passo_giorni=7, aggregazione="Media settimanale storica")
write.csv(metadati, percorso_risultati("metadati_CO2.csv"), row.names=FALSE)
metadati


# Variante svolta
assenze <- aggregate(is.na(w$co2), list(anno=format(w$data,"%Y")), sum)
names(assenze)[2] <- "settimane_mancanti"
head(assenze[order(-assenze$settimane_mancanti), ], 6)


# M09_N02 - Medie mensili e numero di osservazioni
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M09_Borealis"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M09_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M09_Borealis o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M09_N02")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(9002)


# Definire l’aggregazione
w <- carica_dati("co2_settimanale_storica.csv")
w$data <- as.Date(w$data)
w <- w[order(w$data), ]
# La data di riferimento assegna ciascuna settimana a un mese.
gruppi <- split(w$co2, format(w$data, "%Y-%m"))
m <- do.call(rbind, lapply(names(gruppi), function(k) {
  z <- gruppi[[k]]
  n <- sum(!is.na(z))
  data.frame(data=as.Date(paste0(k, "-01")),
    co2_ppm=if (n > 0) mean(z, na.rm=TRUE) else NA_real_,
    n_settimane=n)
}))
rownames(m) <- NULL
head(m, 8)
table(m$n_settimane)


# Mostrare copertura e concentrazione
par(mfrow=c(2,1), mar=c(4.1,4.5,1.8,1.2))
plot(m$data, m$co2_ppm, type="l", col="#087C74",
 xlab="", ylab="CO2 (ppm)")
plot(m$data, m$n_settimane, type="h", col="#C57E42",
 xlab="Data", ylab="Valori disponibili")
sum(m$n_settimane==0L)


# Conservare una regola esplicita
m$almeno_tre <- m$n_settimane>=3L
m$co2_con_soglia <- ifelse(m$almeno_tre, m$co2_ppm, NA_real_)
table(m$almeno_tre)
write.csv(m, percorso_risultati("co2_mensile_con_copertura.csv"), row.names=FALSE)
head(m[!m$almeno_tre, ], 8)


# Variante svolta
medie <- c(10,20); conteggi <- c(2,8)
c(media_osservazioni=weighted.mean(medie,conteggi),
 media_periodi=mean(medie))


# M09_N03 - Verificare una ricostruzione mensile
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M09_Borealis"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M09_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M09_Borealis o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M09_N03")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(9003)


# Ricostruire senza copiare il risultato
w <- carica_dati("co2_settimanale_storica.csv")
w$data <- as.Date(w$data)
w <- w[order(w$data), ]
# La data di riferimento assegna ciascuna settimana a un mese.
gruppi <- split(w$co2, format(w$data, "%Y-%m"))
m <- do.call(rbind, lapply(names(gruppi), function(k) {
  z <- gruppi[[k]]
  n <- sum(!is.na(z))
  data.frame(data=as.Date(paste0(k, "-01")),
    co2_ppm=if (n > 0) mean(z, na.rm=TRUE) else NA_real_,
    n_settimane=n)
}))
rownames(m) <- NULL
riferimento <- carica_dati("co2_mensile_derivata.csv")
riferimento$data <- as.Date(riferimento$data)
c(mesi_calcolo=nrow(m), mesi_riferimento=nrow(riferimento))


# Unire mediante la data
confronto <- merge(m, riferimento, by="data", all=TRUE,
 suffixes=c("_calcolo","_corso"))
stopifnot(nrow(confronto)==nrow(m), nrow(confronto)==nrow(riferimento),
 identical(is.na(confronto$co2_ppm_calcolo),is.na(confronto$co2_ppm_corso)),
 all(confronto$n_settimane_calcolo==confronto$n_settimane_corso))
head(confronto, 4)


# Ammettere soltanto l’arrotondamento atteso
confronto$scarto <- confronto$co2_ppm_calcolo-confronto$co2_ppm_corso
massimo <- max(abs(confronto$scarto), na.rm=TRUE)
stopifnot(massimo<1e-5)
massimo
plot(confronto$data, confronto$scarto, type="h", col="#087C74",
 xlab="Data", ylab="Scarto (ppm)")
abline(h=0, col="grey60")


# Variante svolta
rovesciato <- riferimento[nrow(riferimento):1, ]
controllo <- merge(m, rovesciato, by="data", suffixes=c("_a","_b"))
max(abs(controllo$co2_ppm_a-controllo$co2_ppm_b),na.rm=TRUE)


# M09_N04 - Il calendario prima di ts
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M09_Borealis"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M09_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M09_Borealis o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M09_N04")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(9004)


# Verificare tutte le date attese
d <- carica_dati("co2_1985_2001.csv")
d$data <- as.Date(d$data)
d <- d[order(d$data), ]
attese <- seq(as.Date("1985-01-01"), as.Date("2001-12-01"), by="month")
stopifnot(identical(d$data, attese), !anyNA(d$co2_ppm))
y <- ts(d$co2_ppm, start=c(1985,1), frequency=12)
c(n=nrow(d), copertura_minima=min(d$n_settimane))
stopifnot(nrow(d)==204L, all(d$n_settimane>=3L))
head(data.frame(data=d$data, co2=as.numeric(y)), 3)


# Leggere gli attributi temporali
list(inizio=start(y), fine=end(y), frequenza=frequency(y),
 primi_tempi=head(time(y)), primi_mesi=head(cycle(y)))
plot(d$data, as.numeric(y), type="l", col="#087C74",
 xlab="Data", ylab="CO2 (ppm)")


# Rendere visibile un mese mancante
senza <- d[-5, c("data","co2_ppm")]
completa <- merge(data.frame(data=attese), senza, by="data", all.x=TRUE)
completa[3:7, ]
stopifnot(nrow(completa)==204L, sum(is.na(completa$co2_ppm))==1L)
con_buco <- ts(completa$co2_ppm, start=c(1985,1), frequency=12)
end(con_buco)


# Variante svolta
c(valori_assenti=sum(is.na(con_buco)),
 valori_zero=sum(con_buco==0,na.rm=TRUE),
 posizioni_totali=length(con_buco))


# M09_N05 - Il ciclo stagionale dentro gli anni
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M09_Borealis"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M09_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M09_Borealis o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M09_N05")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(9005)


# Confrontare i mesi
d <- carica_dati("co2_1985_2001.csv")
d$data <- as.Date(d$data)
d <- d[order(d$data), ]
attese <- seq(as.Date("1985-01-01"), as.Date("2001-12-01"), by="month")
stopifnot(identical(d$data, attese), !anyNA(d$co2_ppm))
y <- ts(d$co2_ppm, start=c(1985,1), frequency=12)
d$mese <- as.integer(format(d$data,"%m"))
d$anno <- format(d$data,"%Y")
boxplot(co2_ppm~mese, data=d, col="#D9ECE8", border="#087C74",
 xlab="Mese", ylab="CO2 (ppm)")
aggregate(co2_ppm~mese, data=d, mean)


# Centrare ogni anno per descrivere il ciclo
d$scarto_media_anno <- d$co2_ppm-ave(d$co2_ppm,d$anno,FUN=mean)
ciclo <- aggregate(scarto_media_anno~mese,data=d,mean)
plot(ciclo$mese,ciclo$scarto_media_anno,type="b",pch=19,col="#087C74",
 xlab="Mese",ylab="Scarto dalla media annua (ppm)")
abline(h=0,lty=3)
ciclo


# Conservare le differenze fra anni
mat <- matrix(d$scarto_media_anno,nrow=12)
matplot(1:12,mat,type="l",lty=1,col=adjustcolor("grey45",.35),
 xlab="Mese",ylab="Scarto dalla media annua (ppm)")
lines(1:12,rowMeans(mat),col="#087C74",lwd=3)
range(apply(mat,2,function(z)diff(range(z))))


# Variante svolta
d$periodo <- ifelse(d$anno<="1992","1985-1992","1993-2001")
aggregate(scarto_media_anno~mese+periodo,data=d,mean)


# M09_N06 - Media mobile centrata e rivolta al passato
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M09_Borealis"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M09_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M09_Borealis o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M09_N06")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(9006)


# Due finestre della stessa larghezza
d <- carica_dati("co2_1985_2001.csv")
d$data <- as.Date(d$data)
d <- d[order(d$data), ]
attese <- seq(as.Date("1985-01-01"), as.Date("2001-12-01"), by="month")
stopifnot(identical(d$data, attese), !anyNA(d$co2_ppm))
y <- ts(d$co2_ppm, start=c(1985,1), frequency=12)
centrata <- stats::filter(y, rep(1/13,13), sides=2)
passata <- stats::filter(y, rep(1/13,13), sides=1)
c(NA_centrata=sum(is.na(centrata)),NA_passata=sum(is.na(passata)))
head(data.frame(data=d$data,centrata=as.numeric(centrata),
 passata=as.numeric(passata)),15)


# Osservare il ritardo
plot(d$data,as.numeric(y),type="l",col="grey70",
 xlab="Data",ylab="CO2 (ppm)")
lines(d$data,as.numeric(centrata),col="#087C74",lwd=2)
lines(d$data,as.numeric(passata),col="#C57E42",lwd=2)
legend("topleft",c("Osservazioni","Centrata","Solo presente e passato"),
 col=c("grey70","#087C74","#C57E42"),lty=1,bty="n",cex=.8)


# Verificare a mano una posizione
i <- 50L
c(centrata_R=centrata[i],centrata_manual=mean(y[(i-6):(i+6)]),
 passata_R=passata[i],passata_manual=mean(y[(i-12):i]))
data.frame(finestra=c("centrata","passata"),
 prima=c(as.character(d$data[i-6]),as.character(d$data[i-12])),
 ultima=c(as.character(d$data[i+6]),as.character(d$data[i])))


# Variante svolta
corta <- stats::filter(y,rep(1/3,3),sides=2)
plot(d$data,as.numeric(corta),type="l",col="#7363AA",
 xlab="Data",ylab="CO2 (ppm)")
lines(d$data,as.numeric(centrata),col="#087C74",lwd=2)


# M09_N07 - LOESS: il ruolo dello span
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M09_Borealis"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M09_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M09_Borealis o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M09_N07")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(9007)


# Due estensioni locali
d <- carica_dati("co2_1985_2001.csv")
d$data <- as.Date(d$data)
d <- d[order(d$data), ]
attese <- seq(as.Date("1985-01-01"), as.Date("2001-12-01"), by="month")
stopifnot(identical(d$data, attese), !anyNA(d$co2_ppm))
y <- ts(d$co2_ppm, start=c(1985,1), frequency=12)
tempo <- seq_along(y)
corto <- loess(as.numeric(y)~tempo,span=.15)
lungo <- loess(as.numeric(y)~tempo,span=.45)
c(n=length(y),vicini_indicativi_corto=.15*length(y),
 vicini_indicativi_lungo=.45*length(y))


# Confrontare la forma
plot(d$data,as.numeric(y),type="l",col="grey70",
 xlab="Data",ylab="CO2 (ppm)")
lines(d$data,fitted(corto),col="#087C74",lwd=2)
lines(d$data,fitted(lungo),col="#C57E42",lwd=2)
legend("topleft",c("span 0.15","span 0.45"),
 col=c("#087C74","#C57E42"),lty=1,bty="n")


# Controllare il resto
resto <- as.numeric(y)-fitted(lungo)
acf(resto,lag.max=36,main="Resto dopo LOESS, span 0.45")
c(SD_osservata=sd(y),SD_resto=sd(resto),
 ACF12=as.numeric(acf(resto,plot=FALSE,lag.max=12)$acf[13]))


# Variante svolta
primi <- 1:150
parziale <- loess(as.numeric(y)[primi]~tempo[primi],span=.45)
data.frame(data=tail(d$data[primi],6),
 stima_solo_passato=tail(fitted(parziale),6),
 stima_intero_archivio=fitted(lungo)[145:150])


# M09_N08 - Anomalie e periodo di riferimento
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M09_Borealis"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M09_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M09_Borealis o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M09_N08")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(9008)


# Costruire dodici riferimenti
t <- carica_dati("temperatura_simulata.csv")
t$data <- as.Date(t$data)
t$mese <- as.integer(format(t$data, "%m"))
u <- t$temperatura_C
base <- t$data>=as.Date("2000-01-01") & t$data<=as.Date("2004-12-01")
clima <- tapply(u[base],t$mese[base],mean)
data.frame(mese=1:12,riferimento_C=as.numeric(clima),
 valori_per_mese=as.integer(table(t$mese[base])))


# Sottrarre il mese corrispondente
t$riferimento_C <- as.numeric(clima[as.character(t$mese)])
t$anomalia_C <- u-t$riferimento_C
stopifnot(!anyNA(t$anomalia_C))
plot(t$data,t$anomalia_C,type="l",col="#087C74",
 xlab="Data",ylab="Anomalia (gradi C)")
abline(h=0,lty=3)
tapply(t$anomalia_C[base],t$mese[base],mean)


# Conservare dato, riferimento e scarto
uscita <- data.frame(data=t$data,temperatura_C=u,
 riferimento_C=t$riferimento_C,anomalia_C=t$anomalia_C,
 base="2000-2004: cinque anni simulati")
stopifnot(max(abs(uscita$temperatura_C-uscita$riferimento_C-uscita$anomalia_C))<1e-12)
write.csv(uscita,percorso_risultati("anomalie_con_riferimento.csv"),row.names=FALSE)
head(uscita,4)


# Variante svolta
base10 <- t$data<as.Date("2010-01-01")
clima10 <- tapply(u[base10],t$mese[base10],mean)
anomalia10 <- u-as.numeric(clima10[as.character(t$mese)])
data.frame(mese=1:12,base5=as.numeric(clima),base10=as.numeric(clima10),
 differenza_riferimenti=as.numeric(clima10-clima))


# M09_N09 - Decomposizione STL e ricostruzione
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M09_Borealis"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M09_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M09_Borealis o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M09_N09")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(9009)


# Verificare le componenti note
t <- carica_dati("temperatura_simulata.csv")
t$data <- as.Date(t$data)
t$mese <- as.integer(format(t$data, "%m"))
u <- t$temperatura_C
scarto <- u-t$trend_simulato-t$stagione_simulata-t$residuo_simulato
max(abs(scarto))
stopifnot(max(abs(scarto))<2e-8)
head(t[c("data","temperatura_C","trend_simulato","stagione_simulata","residuo_simulato")],3)


# Stimare una decomposizione
temp_ts <- ts(u,start=c(2000,1),frequency=12)
dec <- stl(temp_ts,s.window="periodic")
par(las=0) # STL usa etichette verticali per le componenti.
plot(dec)
ricostruita <- rowSums(dec$time.series)
max(abs(ricostruita-u))
stopifnot(max(abs(ricostruita-u))<1e-10)


# Confrontare stima e verità simulata
c(RMSE_trend=sqrt(mean((dec$time.series[,"trend"]-t$trend_simulato)^2)),
 RMSE_stagione=sqrt(mean((dec$time.series[,"seasonal"]-t$stagione_simulata)^2)))
acf(dec$time.series[,"remainder"],lag.max=24,main="ACF del resto STL")
write.csv(data.frame(data=t$data,dec$time.series),
 percorso_risultati("decomposizione_STL.csv"),row.names=FALSE)


# Variante svolta
robusta <- stl(temp_ts,s.window="periodic",robust=TRUE)
c(scarto_trend_max=max(abs(robusta$time.series[,"trend"]-dec$time.series[,"trend"])),
 pesi_ridotti=sum(robusta$weights<.9))


# M09_N10 - Rumore bianco, AR(1) e random walk
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M09_Borealis"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M09_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M09_Borealis o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M09_N10")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(9010)


# Leggere le realizzazioni
p <- carica_dati("processi_simulati.csv")
stopifnot(nrow(p)==300L, !anyNA(p))
nomi <- c("rumore_bianco", "ar1", "random_walk")
head(p[c("passo",nomi)],4)
par(mfrow=c(3,1),mar=c(3.8,4.5,1.7,1.2))
for(n in nomi) plot(p$passo,p[[n]],type="l",col="#087C74",
 xlab="Passo",ylab=n)


# Controllare le equazioni
eps <- p$rumore_bianco[-1]
c(errore_AR=max(abs(tail(p$ar1,-1)-.65*head(p$ar1,-1)-eps)),
 scarto_incrementi_RW_da_eps=max(abs(diff(p$random_walk)-eps)),
 iniziale_AR=p$ar1[1],iniziale_RW=p$random_walk[1])


# Processo e singola traiettoria
data.frame(serie=nomi,
 media=vapply(p[nomi],mean,numeric(1)),
 SD=vapply(p[nomi],sd,numeric(1)))
phi <- .65
c(varianza_equilibrio_innovazioni_unitarie=1/(1-phi^2),
 quota_transitorio_dopo_10=phi^(2*10))


# Variante svolta
set.seed(1910)
z <- simula_ar1(300,phi=.7)
c(media=mean(z),varianza=var(z),ACF1=as.numeric(acf(z,plot=FALSE,lag.max=1)$acf[2]))


# M09_N11 - Ritardo uno: coppie e autocorrelazione
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M09_Borealis"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M09_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M09_Borealis o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M09_N11")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(9011)


# Costruire le coppie giuste
p <- carica_dati("processi_simulati.csv")
stopifnot(nrow(p)==300L, !anyNA(p))
nomi <- c("rumore_bianco", "ar1", "random_walk")
x <- p$ar1
passato <- head(x,-1)
presente <- tail(x,-1)
c(coppie=length(passato),correlazione=cor(passato,presente))
plot(passato,presente,pch=19,col=adjustcolor("#087C74",.6),
 xlab="X al passo t-1",ylab="X al passo t")
abline(lm(presente~passato),col="#C57E42",lwd=2)


# Riprodurre il calcolo di acf
centrata <- x-mean(x)
man <- sum(tail(centrata,-1)*head(centrata,-1))/sum(centrata^2)
r_acf <- as.numeric(acf(x,plot=FALSE,lag.max=1)$acf[2])
c(cor_coppie=cor(passato,presente),acf_R=r_acf,acf_manuale=man)
stopifnot(abs(man-r_acf)<1e-12)


# Cambiare il ritardo
confronto <- do.call(rbind,lapply(c(1,2,6,12),function(k) {
 data.frame(ritardo=k,coppie=length(x)-k,
 cor_coppie=cor(head(x,-k),tail(x,-k)),
 acf_R=as.numeric(acf(x,plot=FALSE,lag.max=k)$acf[k+1]))
}))
confronto


# Variante svolta
as.numeric(acf(x,plot=FALSE,lag.max=0)$acf)
sum(centrata*centrata)/sum(centrata^2)


# M09_N12 - Leggere ACF e PACF di processi diversi
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M09_Borealis"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M09_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M09_Borealis o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M09_N12")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(9012)


# Confrontare le autocorrelazioni
p <- carica_dati("processi_simulati.csv")
stopifnot(nrow(p)==300L, !anyNA(p))
nomi <- c("rumore_bianco", "ar1", "random_walk")
par(mfrow=c(3,1),mar=c(4.1,4.5,3.3,1.2))
for(n in nomi) acf(p[[n]],lag.max=24,main=n)
data.frame(serie=nomi,ACF1=vapply(p[nomi],function(z)
 as.numeric(acf(z,plot=FALSE,lag.max=1)$acf[2]),numeric(1)))


# La dipendenza lineare al netto dei ritardi intermedi
par(mfrow=c(1,2),mar=c(4.1,4.5,3.3,1.2))
acf(p$ar1,lag.max=24,main="AR(1): ACF")
pacf(p$ar1,lag.max=24,main="AR(1): PACF")
head(as.numeric(pacf(p$ar1,plot=FALSE,lag.max=6)$acf))


# Interpretare le bande
n <- nrow(p)
banda <- 1.96/sqrt(n)
a <- as.numeric(acf(p$rumore_bianco,plot=FALSE,lag.max=24)$acf)[-1]
c(limite=banda,lag_fuori_banda=sum(abs(a)>banda),lag_esaminati=length(a))
# Due metà della stessa traiettoria: controllo descrittivo.
data.frame(serie=nomi,media1=sapply(p[nomi],function(z)mean(z[1:150])),
 media2=sapply(p[nomi],function(z)mean(z[151:300])))


# Variante svolta
set.seed(1912)
uscite <- replicate(200,{
 z<-rnorm(300)
 any(abs(as.numeric(acf(z,plot=FALSE,lag.max=24)$acf)[-1])>1.96/sqrt(300))
})
mean(uscite)


# M09_N13 - Differenziare e ricostruire un random walk
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M09_Borealis"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M09_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M09_Borealis o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M09_N13")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(9013)


# Calcolare gli incrementi
p <- carica_dati("processi_simulati.csv")
stopifnot(nrow(p)==300L, !anyNA(p))
nomi <- c("rumore_bianco", "ar1", "random_walk")
x <- p$random_walk
delta <- diff(x)
data.frame(passo=p$passo[-1],incremento=delta)[1:6,]
c(livelli=length(x),incrementi=length(delta))


# Controllare la struttura degli incrementi
par(mfrow=c(2,1),mar=c(4.1,4.5,3.3,1.2))
plot(p$passo[-1],delta,type="l",col="#087C74",
 xlab="Passo",ylab="Incremento")
acf(delta,lag.max=24,main="ACF degli incrementi")
c(incrementi=length(delta),media=mean(delta),SD=sd(delta))


# Ricostruire con il valore iniziale
ricostruita <- c(x[1],x[1]+cumsum(delta))
max(abs(ricostruita-x))
stopifnot(max(abs(ricostruita-x))<1e-8)
write.csv(data.frame(passo=p$passo,livello=x,ricostruito=ricostruita),
 percorso_risultati("ricostruzione_random_walk.csv"),row.names=FALSE)


# Variante svolta
c(scarto_differenze=max(abs(diff(x+100)-delta)),
 scarto_livelli=mean((x+100)-x))


# M09_N14 - Differenziare troppo introduce dipendenza
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M09_Borealis"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M09_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M09_Borealis o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M09_N14")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(9014)


# Una trasformazione superflua
set.seed(1805)
e <- rnorm(3000)
delta <- diff(e)
data.frame(serie=c("Bianco","Differenza del bianco"),
 varianza=c(var(e),var(delta)),
 ACF1=c(as.numeric(acf(e,plot=FALSE,lag.max=1)$acf[2]),
 as.numeric(acf(delta,plot=FALSE,lag.max=1)$acf[2])))


# Derivare il riferimento
teoria <- data.frame(lag=0:8,rho=c(1,-.5,rep(0,7)))
campione <- as.numeric(acf(delta,plot=FALSE,lag.max=8)$acf)
data.frame(teoria,stima=campione)
acf(delta,lag.max=24,main="Differenza di rumore bianco")


# Osservare il termine comune
data.frame(t=2:6,precedente=e[1:5],corrente=e[2:6],
 differenza=delta[1:5])
# Ogni differenza e' una combinazione di due innovazioni.
stopifnot(max(abs(delta-(tail(e,-1)-head(e,-1))))<1e-12)


# Variante svolta
doppia <- diff(e,differences=2)
c(varianza=var(doppia),ACF1=as.numeric(acf(doppia,plot=FALSE,lag.max=1)$acf[2]))
acf(doppia,lag.max=12,main="Seconda differenza del bianco")


# M09_N15 - Rimuovere un trend e differenziare
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M09_Borealis"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M09_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M09_Borealis o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M09_N15")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(9015)


# Un trend deterministico con resto dipendente
p <- carica_dati("processi_simulati.csv")
stopifnot(nrow(p)==300L, !anyNA(p))
nomi <- c("rumore_bianco", "ar1", "random_walk")
tempo <- p$passo
x <- .03*tempo+p$ar1
fit <- lm(x~tempo)
coef(fit)
plot(tempo,x,type="l",col="#087C74",xlab="Passo",ylab="Valore simulato")
abline(fit,col="#C57E42",lwd=2)


# Due risultati diversi
resto <- residuals(fit)
delta <- diff(x)
c(n_resto=length(resto),n_differenze=length(delta),
 media_resto=mean(resto),media_differenze=mean(delta))
par(mfrow=c(1,2),mar=c(4.1,4.5,3.3,1.2))
acf(resto,lag.max=20,main="Dopo la retta")
acf(delta,lag.max=20,main="Dopo la differenza")


# La differenza della componente di trend
trend_vero <- .03*tempo
range(diff(trend_vero))
c(scarto_equazione=max(abs(delta-(.03+diff(p$ar1)))),
 RMSE_retta=sqrt(mean((fitted(fit)-trend_vero)^2)))


# Variante svolta
resto_vero <- x-trend_vero
c(scarto_dal_generatore=max(abs(resto_vero-p$ar1)),
 scarto_residui=max(abs(resto_vero-resto)))


# M09_N16 - ADF e KPSS: ipotesi, specifiche e avvisi
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M09_Borealis"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M09_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M09_Borealis o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M09_N16")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(9016)


# Eseguire l’ADF dichiarando il modello
p <- carica_dati("processi_simulati.csv")
stopifnot(nrow(p)==300L, !anyNA(p))
nomi <- c("rumore_bianco", "ar1", "random_walk")
stopifnot(requireNamespace("tseries",quietly=TRUE))
packageVersion("tseries")
adf <- cattura_test(tseries::adf.test(p$ar1,k=4))
adf$test
adf$avvisi


# Distinguere stazionarietà in livello e attorno a un trend
k_level <- cattura_test(tseries::kpss.test(p$ar1,null="Level"))
k_trend <- cattura_test(tseries::kpss.test(p$ar1,null="Trend"))
do.call(rbind,list(riga_test("AR1","KPSS Level",k_level),
 riga_test("AR1","KPSS Trend",k_trend)))


# Conservare i limiti tabulati
esiti <- do.call(rbind,lapply(nomi,function(n)tabella_test(n,p[[n]],k=4)))
esiti
write.csv(esiti,percorso_risultati("ADF_KPSS_con_avvisi.csv"),row.names=FALSE)


# Variante svolta
do.call(rbind,lapply(c(0L,4L,8L),function(k) {
 riga_test("AR1",paste("ADF k",k),cattura_test(tseries::adf.test(p$ar1,k=k)))
}))


# M09_N17 - CO₂: differenze ordinarie e stagionali
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M09_Borealis"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M09_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M09_Borealis o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M09_N17")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(9017)


# Allineare quattro rappresentazioni
d <- carica_dati("co2_1985_2001.csv")
d$data <- as.Date(d$data)
d <- d[order(d$data), ]
attese <- seq(as.Date("1985-01-01"), as.Date("2001-12-01"), by="month")
stopifnot(identical(d$data, attese), !anyNA(d$co2_ppm))
y <- ts(d$co2_ppm, start=c(1985,1), frequency=12)
d1 <- diff(y)
d12 <- diff(y,lag=12)
d1d12 <- diff(d12)
data.frame(serie=c("Livello","Diff1","Diff12","Combinata"),
 n=c(length(y),length(d1),length(d12),length(d1d12)),
 prima=c(as.character(d$data[1]),as.character(d$data[2]),
 as.character(d$data[13]),as.character(d$data[14])))


# Confrontare la dipendenza
serie <- list(livello=y,diff1=d1,diff12=d12,combinata=d1d12)
par(mfrow=c(2,2),mar=c(4.1,4.5,3.3,1.2))
for(n in names(serie)) acf(serie[[n]],lag.max=36,main=n)


# Verificare l’operatore combinato
x <- as.numeric(y); n <- length(x)
esplicita <- x[14:n]-x[13:(n-1)]-x[2:(n-12)]+x[1:(n-13)]
altra <- diff(diff(y),lag=12)
c(errore_formula=max(abs(esplicita-as.numeric(d1d12))),
 errore_commutazione=max(abs(as.numeric(altra-d1d12))))
stopifnot(max(abs(esplicita-as.numeric(d1d12)))<1e-10)


# Variante svolta
tab <- data.frame(data=d$data,livello=as.numeric(y),
 diff1=c(NA,as.numeric(d1)),diff12=c(rep(NA,12),as.numeric(d12)),
 combinata=c(rep(NA,13),as.numeric(d1d12)))
write.csv(tab,percorso_risultati("co2_trasformazioni_allineate.csv"),row.names=FALSE)
head(tab,15)


# M09_N18 - Una diagnosi completa prima del modello
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M09_Borealis"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M09_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M09_Borealis o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M09_N18")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(9018)


# Riunire calendario e trasformazioni
d <- carica_dati("co2_1985_2001.csv")
d$data <- as.Date(d$data)
d <- d[order(d$data), ]
attese <- seq(as.Date("1985-01-01"), as.Date("2001-12-01"), by="month")
stopifnot(identical(d$data, attese), !anyNA(d$co2_ppm))
y <- ts(d$co2_ppm, start=c(1985,1), frequency=12)
serie <- list(livello=as.numeric(y),diff1=as.numeric(diff(y)),
 diff12=as.numeric(diff(y,lag=12)),combinata=as.numeric(diff(diff(y,lag=12))))
sintesi <- data.frame(serie=names(serie),n=sapply(serie,length),
 media=sapply(serie,mean),SD=sapply(serie,sd),
 ACF1=sapply(serie,function(z)as.numeric(acf(z,plot=FALSE,lag.max=1)$acf[2])))
sintesi


# Affiancare test e grafici
esiti <- do.call(rbind,lapply(names(serie),function(n)tabella_test(n,serie[[n]],k=4)))
esiti
par(mfrow=c(2,1),mar=c(4.1,4.5,3.3,1.2))
plot(d$data[-(1:13)],serie$combinata,type="l",col="#087C74",
 xlab="Data",ylab="Differenza combinata (ppm)")
acf(serie$combinata,lag.max=36,main="ACF: lag in mesi")


# Scrivere un registro delle decisioni
registro <- c(
 "CO2 storica 1985-2001: 204 mesi completi, aggregati locali da dati settimanali.",
 "Ogni mese ha almeno tre valori settimanali disponibili.",
 "Confrontate differenza ordinaria, stagionale a 12 mesi e combinata.",
 "La combinata conserva 191 osservazioni e cambia la risposta in incrementi stagionali.",
 "ADF: costante e trend, k=4. KPSS: Level e Trend. Avvisi salvati nella tabella.",
 "La dipendenza residua richiede un modello e una valutazione temporale separata.",
 "I livelli originali restano disponibili; nessuna previsione e' valutata qui.")
writeLines(registro,percorso_risultati("registro_diagnosi.txt"))
write.csv(esiti,percorso_risultati("test_con_specifiche.csv"),row.names=FALSE)
cat(paste(registro,collapse="
"))


# Variante svolta
riga_test("combinata","ADF k8",
 cattura_test(tseries::adf.test(serie$combinata,k=8)))


# M09_N19 - Quante osservazioni restano dopo le differenze?
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M09_Borealis"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M09_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M09_Borealis o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M09_N19")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(9019)


# Contare i valori utilizzabili
d <- carica_dati("co2_1985_2001.csv")
d$data <- as.Date(d$data)
d <- d[order(d$data), ]
attese <- seq(as.Date("1985-01-01"), as.Date("2001-12-01"), by="month")
stopifnot(identical(d$data, attese), !anyNA(d$co2_ppm))
y <- ts(d$co2_ppm, start=c(1985,1), frequency=12)
n <- length(y); s <- 12L
stagionale <- diff(y,lag=s)
combinata <- diff(stagionale)
c(n=n,n_stagionale=length(stagionale),n_combinata=length(combinata),
 formula=n-s-1L)
stopifnot(length(combinata)==191L)


# Contare attraverso il calendario
data.frame(serie=c("livello","stagionale","combinata"),
 prima=c(as.character(d$data[1]),as.character(d$data[13]),as.character(d$data[14])),
 ultima=rep(as.character(tail(d$data,1)),3),
 n=c(length(y),length(stagionale),length(combinata)))
list(inizio_combinata=start(combinata),fine_combinata=end(combinata))


# Un buco interno cambia il conteggio dei valori finiti
con_buco <- y; con_buco[80] <- NA_real_
diff_buco <- diff(diff(con_buco,lag=12))
c(posizioni=length(diff_buco),valori_finiti=sum(is.finite(diff_buco)),
 valori_NA=sum(is.na(diff_buco)))
which(is.na(diff_buco))


# Variante svolta
do.call(rbind,lapply(c(4L,6L,12L),function(s) {
 z<-diff(diff(y,lag=s))
 data.frame(lag=s,n_effettivo=length(z),n_formula=length(y)-s-1L)
}))


# M09_N20 - Il riferimento −1/2 e la variabilità campionaria
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M09_Borealis"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M09_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M09_Borealis o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M09_N20")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(9020)


# Riprodurre l’esperimento lungo
set.seed(1840)
x <- rnorm(10000)
z <- diff(x)
rho <- as.numeric(acf(z,plot=FALSE,lag.max=1)$acf[2])
c(ACF1=rho,teoria=-.5,scarto=rho+.5,n=length(z))


# Ripetere a due numerosità
set.seed(1920)
B <- 300L
stima <- function(n) as.numeric(acf(diff(rnorm(n)),plot=FALSE,lag.max=1)$acf[2])
brevi <- replicate(B,stima(100))
lunghe <- replicate(B,stima(1000))
data.frame(n=c(100,1000),media=c(mean(brevi),mean(lunghe)),
 SD=c(sd(brevi),sd(lunghe)),
 q025=c(quantile(brevi,.025),quantile(lunghe,.025)),
 q975=c(quantile(brevi,.975),quantile(lunghe,.975)))


# Visualizzare la dispersione
lim <- range(c(brevi,lunghe,-.5))
par(mfrow=c(1,2),mar=c(4.1,4.5,3.3,1.2))
hist(brevi,breaks=15,xlim=lim,col="#D9ECE8",border="white",
 main="n = 100",xlab="ACF al lag 1")
abline(v=-.5,col="#C57E42",lwd=2)
hist(lunghe,breaks=15,xlim=lim,col="#D9ECE8",border="white",
 main="n = 1000",xlab="ACF al lag 1")
abline(v=-.5,col="#C57E42",lwd=2)


# Variante svolta
set.seed(1840)
ampia <- 5*rnorm(10000)
c(ACF1=as.numeric(acf(diff(ampia),plot=FALSE,lag.max=1)$acf[2]),
 rapporto_varianze=var(diff(ampia))/var(z))
