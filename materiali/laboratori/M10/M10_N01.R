# Fissare l’origine della previsione
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
ctx <- inizia_notebook("M10_N01")
set.seed(1019)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Analisi principale: Fissare l’origine della previsione
d <- leggi_dati("co2_1985_2001.csv")
d$data <- as.Date(d$data)
stopifnot(identical(d$data,seq(as.Date("1985-01-01"),as.Date("2001-12-01"),by="month")))
y <- ts(d$co2_ppm,start=c(1985,1),frequency=12)
train <- window(y,end=c(1998,12))
test <- window(y,start=c(1999,1))
h <- length(test)
stopifnot(length(train)==168,h==36,!anyNA(y))
data.frame(insieme=c("Train","Test"),n=c(length(train),length(test)))
