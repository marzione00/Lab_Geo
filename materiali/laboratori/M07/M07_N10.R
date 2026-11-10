# Il protocollo prima di guardare gli errori
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
ctx <- inizia_notebook("M07_N10")
set.seed(1014)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Analisi principale: Il protocollo prima di guardare gli errori
f <- leggi_dati("fossili_simulati.csv")
f$morfotipo <- factor(f$morfotipo,levels=c("Rounded","Spiky"))
is_test <- seq_len(nrow(f))%%5L==0L
train <- f[!is_test,]
test <- f[is_test,]
stopifnot(nrow(train)==128L,nrow(test)==32L)
stopifnot(length(intersect(train$id,test$id))==0L)
table(insieme=ifelse(is_test,"test","train"),morfotipo=f$morfotipo)
