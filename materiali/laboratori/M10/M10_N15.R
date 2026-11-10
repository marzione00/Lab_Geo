# Stabilità e residui del sistema
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
ctx <- inizia_notebook("M10_N15")
set.seed(1020)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Preparazione: Percorso obbligatorio e approfondimento
f <- leggi_dati("fossili_simulati.csv")
richiedi_colonne(f,c("id","morfotipo","diametro_tot_um","diametro_int_um"))
audit <- data.frame(
  controllo=c("ID unici","Diametri completi","Totale positivo","Interno entro totale"),
  esito=c(!anyDuplicated(f$id),!anyNA(f[c("diametro_tot_um","diametro_int_um")]),
          all(f$diametro_tot_um>0),all(f$diametro_int_um>0 & f$diametro_int_um<=f$diametro_tot_um)))
audit
stopifnot(all(audit$esito))


# Preparazione: Dichiarare prima il confronto predittivo
test_idx <- seq(5,nrow(f),by=5)
tr <- f[-test_idx,]; te <- f[test_idx,]
stopifnot(nrow(tr)==128,nrow(te)==32,!any(tr$id %in% te$id))
mod <- lm(diametro_int_um~diametro_tot_um,data=tr)
prev <- as.numeric(predict(mod,newdata=te))
baseline <- rep(mean(tr$diametro_int_um),nrow(te))
rmse <- function(obs,pr) sqrt(mean((obs-pr)^2))
confronto <- data.frame(modello=c("Media del train","Regressione semplice"),
                       RMSE=c(rmse(te$diametro_int_um,baseline),rmse(te$diametro_int_um,prev)))
confronto


# Preparazione: Un grafico e una diagnostica utili alla domanda
stile_grafico()
plot(prev,te$diametro_int_um,pch=19,col=palette_geo[1],
     xlab="Previsto nel test (micrometri)",ylab="Osservato nel test (micrometri)",
     main="Progetto base: verifica su 32 individui non usati per stimare")
abline(0,1,lty=2)
stile_grafico()
plot(fitted(mod),residuals(mod),pch=19,col=palette_geo[2],
     xlab="Stimato nel train",ylab="Residuo nel train",main="Diagnostica distinta dalla verifica predittiva")
abline(h=0,lty=2)
coef(mod)


# Preparazione: Generare una relazione che riporti i risultati reali
rapporto <- c(
  "PROGETTO GUIDATO — dati morfometrici SIMULATI del corso",
  "Domanda: prevedere il diametro interno dal totale, senza attribuzione causale.",
  sprintf("Campioni: %d train, %d test; split ogni quinta riga.",nrow(tr),nrow(te)),
  sprintf("Pendenza nel train: %.4f; intercetta: %.4f.",coef(mod)[2],coef(mod)[1]),
  sprintf("RMSE baseline: %.4f micrometri.",confronto$RMSE[1]),
  sprintf("RMSE regressione: %.4f micrometri.",confronto$RMSE[2]),
  "Limiti: simulazione, misure geometricamente legate, un solo holdout.",
  "DA COMPLETARE: interpretare i grafici e indicare quali dati nuovi servirebbero."
)
salva_testo(rapporto,"relazione_progetto_base.txt",ctx$out)
salva_tabella(audit,"audit_progetto.csv",ctx$out)
salva_tabella(confronto,"metriche_progetto.csv",ctx$out)
salva_tabella(data.frame(id=te$id,osservato=te$diametro_int_um,previsto=prev),"test_progetto.csv",ctx$out)
saveRDS(mod,file.path(ctx$out,"modello_progetto.rds"))
cat(paste(rapporto,collapse="
"))


# Preparazione: Approfondimento: un VAR(1) come due regressioni
p <- leggi_dati("processi_simulati.csv")
v <- p[1:250,c("x_VAR","y_VAR")]
lagged <- data.frame(x=v$x_VAR[-1],y=v$y_VAR[-1],
                     x_lag=head(v$x_VAR,-1),y_lag=head(v$y_VAR,-1))
fit_x <- lm(x~x_lag+y_lag,data=lagged)
fit_y <- lm(y~x_lag+y_lag,data=lagged)
coef(fit_x); coef(fit_y)
A <- rbind(coef(fit_x)[c("x_lag","y_lag")],coef(fit_y)[c("x_lag","y_lag")])
intercetta <- c(coef(fit_x)[1],coef(fit_y)[1])
A


# Analisi principale: Stabilità e residui del sistema
autovalori <- eigen(A,only.values=TRUE)$values
moduli <- Mod(autovalori)
data.frame(parte_reale=Re(autovalori),parte_immaginaria=Im(autovalori),modulo=moduli)
stabile <- all(moduli<1)
if(!stabile) warning("Il VAR stimato non risulta stabile: discutere prima di interpretare.")
acf(residuals(fit_x),lag.max=20,main="VAR: residui equazione X")
acf(residuals(fit_y),lag.max=20,main="VAR: residui equazione Y")
cor(residuals(fit_x),residuals(fit_y))
