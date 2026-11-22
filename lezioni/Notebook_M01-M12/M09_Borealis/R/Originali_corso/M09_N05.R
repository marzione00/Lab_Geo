# Vedere il ciclo entro gli anni
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
ctx <- inizia_notebook("M09_N05")
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


# Analisi principale: Vedere il ciclo entro gli anni
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
