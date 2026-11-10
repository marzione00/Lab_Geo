# Decomposizione e ricostruzione
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Questo blocco prepara soltanto percorsi, funzioni di servizio e riproducibilità.
# Non scarica dati, non installa pacchetti, non elimina oggetti e non modifica i CSV.
trova_radice <- function() {
  p <- normalizePath(getwd(), winslash = "/", mustWork = TRUE)
  repeat {
    if (file.exists(file.path(p, "Notebook_R_Geologia.Rproj"))) return(p)
    genitore <- dirname(p)
    if (identical(p, genitore)) stop("Aprire Notebook_R_Geologia.Rproj e riprovare.")
    p <- genitore
  }
}
root <- trova_radice()
source(file.path(root, "R", "funzioni_comuni.R"), local = TRUE)
ctx <- inizia_notebook("M09_N09")
set.seed(1017)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Preparazione: Dati storici, non una misura aggiornata
w <- leggi_dati("co2_settimanale_storica.csv")
w$data <- as.Date(w$data)
stopifnot(!anyNA(w$data),!anyDuplicated(w$data))
w <- w[order(w$data),]
data.frame(prima=min(w$data),ultima=max(w$data),
           righe=nrow(w),osservate=sum(!is.na(w$co2)),
           mancanti=sum(is.na(w$co2)))
# Guardare gli intervalli PRIMA di dichiarare che la serie è regolare.
table(as.integer(diff(w$data)))


# Preparazione: Aggregare e conservare un indicatore di copertura
mese <- format(w$data,"%Y-%m")
gruppi <- split(seq_len(nrow(w)),mese)
m <- do.call(rbind,lapply(names(gruppi),function(k) {
  valori <- w$co2[gruppi[[k]]]
  n <- sum(!is.na(valori))
  data.frame(data=as.Date(paste0(k,"-01")),
             co2_ppm=if(n>0) mean(valori,na.rm=TRUE) else NA_real_,
             n_settimane=n)
}))
rownames(m) <- NULL
head(m)
table(m$n_settimane)


# Preparazione: Confrontare la ricostruzione con il file fornito
riferimento <- leggi_dati("co2_mensile_derivata.csv")
riferimento$data <- as.Date(riferimento$data)
c <- merge(m,riferimento,by="data",suffixes=c("_calcolo","_corso"),all=TRUE)
stopifnot(nrow(c)==nrow(m),nrow(c)==nrow(riferimento))
stopifnot(identical(is.na(c$co2_ppm_calcolo),is.na(c$co2_ppm_corso)))
scarto <- abs(c$co2_ppm_calcolo-c$co2_ppm_corso)
stopifnot(max(scarto,na.rm=TRUE)<1e-5)
stopifnot(all(c$n_settimane_calcolo==c$n_settimane_corso))
max(scarto,na.rm=TRUE)


# Preparazione: Un calendario completo prima di creare un oggetto ts
d <- leggi_dati("co2_1985_2001.csv")
d$data <- as.Date(d$data)
attese <- seq(as.Date("1985-01-01"),as.Date("2001-12-01"),by="month")
stopifnot(identical(d$data,attese),!anyNA(d$co2_ppm),all(d$n_settimane>=3))
y <- ts(d$co2_ppm,start=c(1985,1),frequency=12)
stile_grafico()
plot(d$data,d$co2_ppm,type="l",col=palette_geo[1],
     xlab="Data",ylab="CO2 (ppm)",main="Estratto storico: dati osservati")
start(y); end(y); frequency(y)


# Preparazione: Vedere il ciclo entro gli anni
d$mese <- as.integer(format(d$data,"%m"))
d$anno <- as.integer(format(d$data,"%Y"))
medie_mensili <- aggregate(co2_ppm~mese,data=d,FUN=mean)
stile_grafico()
boxplot(co2_ppm~mese,data=d,xlab="Mese",ylab="CO2 (ppm)",
        main="Distribuzioni mensili: includono anche il trend storico")
lines(medie_mensili$mese,medie_mensili$co2_ppm,type="b",col=palette_geo[2],pch=19)
# Sottrarre la media di ciascun anno per una vista DESCRITTIVA del ciclo.
d$scarto_media_anno <- d$co2_ppm-ave(d$co2_ppm,d$anno,FUN=mean)
aggregate(scarto_media_anno~mese,data=d,FUN=mean)


# Preparazione: Media mobile centrata e causale
centrata <- stats::filter(y,rep(1/13,13),sides=2)
passata <- stats::filter(y,rep(1/13,13),sides=1)
stile_grafico()
plot(y,col="grey65",ylab="CO2 (ppm)",xlab="Anno",main="Due finestre, informazioni diverse")
lines(centrata,col=palette_geo[1],lwd=2)
lines(passata,col=palette_geo[2],lwd=2,lty=2)
legend("topleft",c("Osservazioni","Centrata 13 mesi","Solo passato 13 mesi"),
       col=c("grey65",palette_geo[1:2]),lty=c(1,1,2),bty="n")
c(NA_centrata=sum(is.na(centrata)),NA_passata=sum(is.na(passata)))


# Preparazione: LOESS e significato dello span
tempo <- seq_len(nrow(d))
loess_corto <- loess(d$co2_ppm~tempo,span=.15)
loess_lungo <- loess(d$co2_ppm~tempo,span=.45)
stile_grafico()
plot(d$data,d$co2_ppm,type="l",col="grey65",xlab="Data",ylab="CO2 (ppm)")
lines(d$data,fitted(loess_corto),col=palette_geo[1],lwd=2)
lines(d$data,fitted(loess_lungo),col=palette_geo[2],lwd=2,lty=2)
legend("topleft",c("Span 0.15","Span 0.45"),col=palette_geo[1:2],lty=1:2,bty="n")


# Preparazione: Anomalie rispetto a una base esplicita
t <- leggi_dati("temperatura_simulata.csv")
t$data <- as.Date(t$data)
t$mese <- as.integer(format(t$data,"%m"))
base <- t[seq_len(120),]
clima <- tapply(base$temperatura_C,base$mese,mean)
t$anomalia_C <- t$temperatura_C-as.numeric(clima[as.character(t$mese)])
stopifnot(!anyNA(t$anomalia_C))
stile_grafico()
plot(t$data,t$anomalia_C,type="l",col=palette_geo[1],
     xlab="Data",ylab="Anomalia (gradi C)",main="Simulazione: base primi 120 mesi")
abline(h=0,lty=2)
range(base$data)


# Analisi principale: Decomposizione e ricostruzione
temp_ts <- ts(t$temperatura_C,frequency=12)
dec <- stl(temp_ts,s.window="periodic",robust=TRUE)
plot(dec)
ricostruita <- rowSums(dec$time.series)
stopifnot(max(abs(as.numeric(temp_ts)-ricostruita))<1e-8)
salva_tabella(m,"co2_mensile_ricalcolata.csv",ctx$out)
salva_tabella(t[c("data","temperatura_C","anomalia_C")],"anomalie_simulate.csv",ctx$out)
salva_tabella(data.frame(data=t$data,dec$time.series),"decomposizione_simulata.csv",ctx$out)
