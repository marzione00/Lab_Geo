# Un modello continuo non assegna probabilità ai singoli punti
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
ctx <- inizia_notebook("M04_N10")
set.seed(1008)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Analisi principale: Un modello continuo non assegna probabilità ai singoli punti
mu <- 2.65
sigma <- 0.06
p_intervallo <- pnorm(2.75, mu, sigma) - pnorm(2.55, mu, sigma)
c(densita_al_centro = dnorm(mu, mu, sigma),
  probabilita_tra_2_55_e_2_75 = p_intervallo)
stile_grafico()
curve(dnorm(x, mean = mu, sd = sigma), from = 2.4, to = 2.9,
      xlab = "Densità modellata (g/cm^3)", ylab = "Densità di probabilità",
      main = "Distribuzione teorica, non dati di campo", col = palette_geo[1], lwd = 2)
