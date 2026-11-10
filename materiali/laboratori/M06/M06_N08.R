# Effetto nelle unità originali e standardizzato
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
ctx <- inizia_notebook("M06_N08")
set.seed(1011)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Preparazione: Una domanda e un contrasto con segno
f <- leggi_dati("fossili_simulati.csv")
x <- f$diametro_tot_um[f$morfotipo=="Spiky"]
y <- f$diametro_tot_um[f$morfotipo=="Rounded"]
stopifnot(length(x)==80L,length(y)==80L,all(is.finite(c(x,y))))
delta <- mean(x)-mean(y)
data.frame(gruppo=c("Spiky","Rounded"),n=c(length(x),length(y)),
           media=c(mean(x),mean(y)),sd=c(sd(x),sd(y)))
delta


# Preparazione: Guardare le distribuzioni prima del risultato numerico
stile_grafico()
boxplot(list(Rounded=y,Spiky=x),outline=FALSE,col=c("grey90","grey85"),
        xlab="Morfotipo",ylab="Diametro totale (micrometri)",
        main="Confronto di distribuzioni, non soltanto di medie")
set.seed(611)
stripchart(list(Rounded=y,Spiky=x),vertical=TRUE,method="jitter",
           add=TRUE,pch=19,cex=.5,col=palette_geo[1:2])


# Preparazione: Una singola permutazione delle etichette
set.seed(612)
z <- c(x,y)
nx <- length(x)
id_x <- sample(seq_along(z),size=nx,replace=FALSE)
delta_perm <- mean(z[id_x])-mean(z[-id_x])
c(osservata=delta,permutata=delta_perm)
# Ogni valore compare una volta nella partizione.
stopifnot(length(id_x)==nx,length(z[-id_x])==length(y))


# Preparazione: Molte permutazioni e p-value Monte Carlo
set.seed(613)
B <- 4000L
perm <- replicate(B,{
  id <- sample(seq_along(z),size=nx,replace=FALSE)
  mean(z[id])-mean(z[-id])
})
piu_estremi <- sum(abs(perm)>=abs(delta))
p_perm <- (1+piu_estremi)/(B+1)
data.frame(B=B,contrasto_osservato=delta,
           permutazioni_almeno_estreme=piu_estremi,p_MonteCarlo=p_perm,
           risoluzione_minima=1/(B+1))


# Preparazione: Il grafico della distribuzione nulla
stile_grafico()
hist(perm,breaks=40,col="grey90",border="white",
     xlim=range(c(perm,-abs(delta),abs(delta))),
     xlab="Differenza permutata (micrometri)",ylab="Permutazioni",
     main="Riferimento sotto scambiabilità delle etichette")
abline(v=c(-abs(delta),abs(delta)),col=palette_geo[3],lwd=2)
abline(v=0,lty=3)


# Preparazione: Welch: differenza tra medie senza imporre varianze uguali
w <- t.test(x,y,var.equal=FALSE,conf.level=.95)
risultato <- data.frame(
  contrasto="Spiky - Rounded",effetto_um=delta,
  basso95=w$conf.int[1],alto95=w$conf.int[2],
  t=unname(w$statistic),gradi_liberta=unname(w$parameter),p_value=w$p.value)
risultato
# Ricostruiamo il denominatore della statistica.
SE_delta <- sqrt(var(x)/length(x)+var(y)/length(y))
stopifnot(abs(delta/SE_delta-unname(w$statistic))<1e-10)


# Preparazione: Il numero di osservazioni cambia l’incertezza
set.seed(614)
n_grid <- c(10L,40L,160L)
esempio_n <- do.call(rbind,lapply(n_grid,function(nn){
  a <- rnorm(nn,.2,1)
  b <- rnorm(nn,0,1)
  test <- t.test(a,b)
  data.frame(n_per_gruppo=nn,effetto_vero=.2,effetto_osservato=mean(a)-mean(b),
             basso=test$conf.int[1],alto=test$conf.int[2],p=test$p.value)
}))
esempio_n


# Analisi principale: Effetto nelle unità originali e standardizzato
sd_pool <- sqrt(((length(x)-1)*var(x)+(length(y)-1)*var(y))/
                (length(x)+length(y)-2))
effetto_standardizzato <- delta/sd_pool
data.frame(effetto_um=delta,SD_pooled=sd_pool,
           differenza_in_SD_pooled=effetto_standardizzato)
# Nessuna soglia automatica piccolo/medio/grande viene imposta qui.
