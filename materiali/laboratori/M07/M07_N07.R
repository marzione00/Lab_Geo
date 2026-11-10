# Residui contro valori stimati
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
ctx <- inizia_notebook("M07_N07")
set.seed(1013)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Preparazione: Definire risposta e predittore
f <- leggi_dati("fossili_simulati.csv")
x <- f$diametro_tot_um
y <- f$diametro_int_um
stopifnot(all(is.finite(x)),all(is.finite(y)),all(y<=x))
stile_grafico()
plot(x,y,pch=19,col=adjustcolor(palette_geo[1],alpha.f=.6),
     xlab="Diametro totale (micrometri)",ylab="Diametro interno (micrometri)",
     main="Due misure dello stesso individuo")
abline(0,1,lty=2)


# Preparazione: Pearson e Spearman: quale relazione riassumono?
correlazioni <- data.frame(
  metodo=c("Pearson","Spearman"),
  coefficiente=c(cor(x,y,method="pearson"),cor(x,y,method="spearman")))
correlazioni
# Invertire x e y non cambia il coefficiente di correlazione.
stopifnot(abs(cor(x,y)-cor(y,x))<1e-12)
# Cambiare soltanto l'unità di x non cambia Pearson.
cor(x*1000,y)


# Preparazione: La retta dei minimi quadrati a mano
b1 <- cov(x,y)/var(x)
b0 <- mean(y)-b1*mean(x)
y_hat_manuale <- b0+b1*x
residui_manuali <- y-y_hat_manuale
c(intercetta=b0,pendenza=b1)
c(somma_residui=sum(residui_manuali),SSE=sum(residui_manuali^2))


# Preparazione: Stimare con lm e leggere i coefficienti
modello <- lm(diametro_int_um ~ diametro_tot_um,data=f)
coef(modello)
summary(modello)
stopifnot(isTRUE(all.equal(unname(coef(modello)),c(b0,b1))))
stopifnot(max(abs(fitted(modello)-y_hat_manuale))<1e-10)
confint(modello)


# Preparazione: R² ed errore residuo non sono la stessa cosa
e <- residuals(modello)
SSE <- sum(e^2)
SST <- sum((y-mean(y))^2)
R2_manuale <- 1-SSE/SST
sigma_residua <- sqrt(SSE/df.residual(modello))
data.frame(R2=R2_manuale,SD_residua_um=sigma_residua,
           RMSE_sul_train=sqrt(mean(e^2)))
stopifnot(abs(R2_manuale-summary(modello)$r.squared)<1e-10)


# Preparazione: Media prevista e nuovo individuo
griglia <- data.frame(diametro_tot_um=seq(min(x),max(x),length.out=100))
IC <- predict(modello,newdata=griglia,interval="confidence",level=.95)
IP <- predict(modello,newdata=griglia,interval="prediction",level=.95)
stopifnot(all((IP[,"upr"]-IP[,"lwr"]) >= (IC[,"upr"]-IC[,"lwr"])))
stile_grafico()
plot(x,y,pch=19,col="grey65",xlab="Diametro totale (micrometri)",
     ylab="Diametro interno (micrometri)",main="Media stimata e previsione individuale")
lines(griglia$diametro_tot_um,IC[,"fit"],col=palette_geo[1],lwd=2)
lines(griglia$diametro_tot_um,IC[,"lwr"],col=palette_geo[1],lty=2)
lines(griglia$diametro_tot_um,IC[,"upr"],col=palette_geo[1],lty=2)
lines(griglia$diametro_tot_um,IP[,"lwr"],col=palette_geo[2],lty=3)
lines(griglia$diametro_tot_um,IP[,"upr"],col=palette_geo[2],lty=3)
legend("topleft",c("Media stimata / IC","IP nuovo individuo"),
       col=palette_geo[1:2],lty=c(2,3),bty="n")


# Analisi principale: Residui contro valori stimati
stile_grafico()
plot(fitted(modello),e,pch=19,col=adjustcolor(palette_geo[1],alpha.f=.65),
     xlab="Diametro interno stimato (micrometri)",ylab="Residuo (micrometri)",
     main="Residui contro valori stimati")
abline(h=0,lty=2)
# Una curva descrittiva aiuta a vedere un eventuale andamento residuo.
lines(lowess(fitted(modello),e),col=palette_geo[2],lwd=2)
