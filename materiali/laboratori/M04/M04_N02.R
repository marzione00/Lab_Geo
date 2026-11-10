# Eventi complementari e soglie
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
ctx <- inizia_notebook("M04_N02")
set.seed(1007)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Preparazione: Evento e probabilità: una regola dichiarata
set.seed(407)
p <- .30
estrazioni <- rbinom(n = 20, size = 1, prob = p)
estrazioni
c(successi = sum(estrazioni), prove = length(estrazioni),
  frequenza_relativa = mean(estrazioni), probabilita_modello = p)


# Analisi principale: Eventi complementari e soglie
conteggi_demo <- c(0,1,2,3,4,5)
data.frame(conteggio = conteggi_demo,
           almeno_3 = conteggi_demo >= 3,
           piu_di_3 = conteggi_demo > 3,
           al_massimo_3 = conteggi_demo <= 3,
           esattamente_3 = conteggi_demo == 3)
1 - p
