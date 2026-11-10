# Laboratorio applicativo — Numero di osservazioni
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
ctx <- inizia_notebook("M09_N19")
set.seed(1018)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Preparazione: Tre processi, tre domande
p <- leggi_dati("processi_simulati.csv")
richiedi_colonne(p,c("passo","rumore_bianco","ar1","random_walk"))
stopifnot(nrow(p)==300,!anyNA(p))
stile_grafico()
matplot(p$passo,p[c("rumore_bianco","ar1","random_walk")],type="l",lty=1,
        col=palette_geo[1:3],xlab="Passo",ylab="Unità simulate",main="Realizzazioni simulate")
legend("topleft",c("Rumore bianco","AR(1)","Random walk"),col=palette_geo[1:3],lty=1,bty="n")


# Preparazione: La correlazione con il passato
x <- p$ar1
ritardo <- 1
x_passato <- head(x,-ritardo)
x_presente <- tail(x,-ritardo)
cor(x_passato,x_presente)
stile_grafico()
plot(x_passato,x_presente,pch=19,col=adjustcolor(palette_geo[1],.6),
     xlab="X al passo t-1",ylab="X al passo t",main="AR(1): diagramma al ritardo 1")
abline(lm(x_presente~x_passato),col=palette_geo[2],lwd=2)
acf(x,lag.max=24,main="AR(1): autocorrelazione campionaria")


# Preparazione: ACF di processi diversi
for(nome in c("rumore_bianco","ar1","random_walk")) {
  acf(p[[nome]],lag.max=30,main=paste("Simulazione:",nome))
}
# Confronto puramente descrittivo tra due metà della realizzazione.
confronto_meta <- do.call(rbind,lapply(c("rumore_bianco","ar1","random_walk"),function(n) {
  z <- p[[n]]
  data.frame(serie=n,media1=mean(z[1:150]),media2=mean(z[151:300]),
             sd1=sd(z[1:150]),sd2=sd(z[151:300]))
}))
confronto_meta


# Preparazione: Differenziare una volta
delta_rw <- diff(p$random_walk)
stopifnot(length(delta_rw)==nrow(p)-1)
stile_grafico()
plot(p$passo[-1],delta_rw,type="l",col=palette_geo[1],
     xlab="Passo della variazione",ylab="Differenza",main="Incrementi del random walk")
acf(delta_rw,lag.max=24,main="ACF degli incrementi")
# Ricostruzione dei livelli, conoscendo il valore iniziale.
ricostruzione <- c(p$random_walk[1],p$random_walk[1]+cumsum(delta_rw))
stopifnot(max(abs(ricostruzione-p$random_walk))<1e-8)


# Preparazione: Differenziare troppo crea struttura
set.seed(1805)
bianco <- rnorm(3000)
eccesso <- diff(bianco)
a0 <- acf(bianco,plot=FALSE,lag.max=2)$acf[2]
a1 <- acf(eccesso,plot=FALSE,lag.max=2)$acf[2]
data.frame(serie=c("Bianco","Differenza del bianco"),acf_lag1=c(a0,a1))
acf(eccesso,lag.max=24,main="Differenziare il rumore bianco: dipendenza artificiale")


# Preparazione: Trend deterministico e differenza non sono sinonimi
tempo <- p$passo
serie_trend <- .03*tempo+p$ar1
fit_trend <- lm(serie_trend~tempo)
residuo_trend <- residuals(fit_trend)
serie_differenziata <- diff(serie_trend)
acf(residuo_trend,main="Dopo rimozione della retta")
acf(serie_differenziata,main="Dopo differenza prima")
coef(fit_trend)


# Preparazione: ADF e KPSS: due ipotesi diverse
esiti_test <- NULL
if(requireNamespace("tseries",quietly=TRUE)) {
  esegui_test <- function(nome,z) {
    # NON sopprimiamo i warning: spesso segnalano p-value fuori dalla tabella.
    adf <- tseries::adf.test(z,k=4)
    livello <- tseries::kpss.test(z,null="Level")
    trend <- tseries::kpss.test(z,null="Trend")
    data.frame(serie=nome,test=c("ADF, costante+trend; k=4","KPSS livello","KPSS trend"),
               statistica=c(unname(adf$statistic),unname(livello$statistic),unname(trend$statistic)),
               p_riportato=c(adf$p.value,livello$p.value,trend$p.value))
  }
  esiti_test <- do.call(rbind,lapply(c("rumore_bianco","ar1","random_walk"),
                          function(n) esegui_test(n,p[[n]])))
  print(esiti_test)
  salva_tabella(esiti_test,"test_stazionarieta_p_riportati.csv",ctx$out)
} else {
  message("Sezione ADF/KPSS non eseguita: installare tseries tramite R/00_installazione.R.")
}


# Preparazione: CO2: livello, differenza stagionale e differenza combinata
d <- leggi_dati("co2_1985_2001.csv")
y <- ts(d$co2_ppm,start=c(1985,1),frequency=12)
d1 <- diff(y,lag=1)
d12 <- diff(y,lag=12)
d1d12 <- diff(d12,lag=1)
data.frame(serie=c("Livello","Diff.1","Diff.12","Diff.12 poi1"),
           lunghezza=c(length(y),length(d1),length(d12),length(d1d12)))
acf(y,lag.max=36,main="CO2: livelli")
acf(d12,lag.max=36,main="CO2: differenza stagionale")
acf(d1d12,lag.max=36,main="CO2: differenza stagionale e prima")


# Preparazione: Una diagnosi, non soltanto un p-value
salva_tabella(confronto_meta,"confronto_meta_simulazioni.csv",ctx$out)
salva_testo(c(
  "Dati: processi simulati e CO2 storica del corso.",
  "ADF e KPSS, se disponibili, sono supporti alla diagnosi e non verdetti universali.",
  "La differenziazione cambia risposta e lunghezza della serie.",
  "Il modello del notebook 19 ricevera i LIVELLI originali, non differenze precomputate."
),"promemoria_diagnostica.txt",ctx$out)


# Analisi principale: Laboratorio applicativo — Numero di osservazioni
d <- leggi_dati("co2_1985_2001.csv")
length(diff(diff(d$co2_ppm,lag=12)))
