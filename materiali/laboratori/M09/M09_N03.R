# Confrontare la ricostruzione con il file fornito
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
ctx <- inizia_notebook("M09_N03")
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


# Analisi principale: Confrontare la ricostruzione con il file fornito
riferimento <- leggi_dati("co2_mensile_derivata.csv")
riferimento$data <- as.Date(riferimento$data)
c <- merge(m,riferimento,by="data",suffixes=c("_calcolo","_corso"),all=TRUE)
stopifnot(nrow(c)==nrow(m),nrow(c)==nrow(riferimento))
stopifnot(identical(is.na(c$co2_ppm_calcolo),is.na(c$co2_ppm_corso)))
scarto <- abs(c$co2_ppm_calcolo-c$co2_ppm_corso)
stopifnot(max(scarto,na.rm=TRUE)<1e-5)
stopifnot(all(c$n_settimane_calcolo==c$n_settimane_corso))
max(scarto,na.rm=TRUE)
