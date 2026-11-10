# Propagare l’incertezza con molte estrazioni
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
ctx <- inizia_notebook("M04_N14")
set.seed(1008)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Preparazione: Un modello continuo non assegna probabilità ai singoli punti
mu <- 2.65
sigma <- 0.06
p_intervallo <- pnorm(2.75, mu, sigma) - pnorm(2.55, mu, sigma)
c(densita_al_centro = dnorm(mu, mu, sigma),
  probabilita_tra_2_55_e_2_75 = p_intervallo)
stile_grafico()
curve(dnorm(x, mean = mu, sd = sigma), from = 2.4, to = 2.9,
      xlab = "Densità modellata (g/cm^3)", ylab = "Densità di probabilità",
      main = "Distribuzione teorica, non dati di campo", col = palette_geo[1], lwd = 2)


# Preparazione: Standardizzare e ritrovare le probabilità
limiti <- c(2.55, 2.75)
z <- (limiti - mu) / sigma
p_standard <- pnorm(z[2]) - pnorm(z[1])
z
stopifnot(abs(p_standard - p_intervallo) < 1e-12)
# Quantili centrali teorici al 95%.
qnorm(c(.025, .975), mean = mu, sd = sigma)


# Preparazione: Dati positivi e asimmetria
set.seed(411)
meanlog <- log(0.5)
sdlog <- .7
granuli <- rlnorm(5000, meanlog = meanlog, sdlog = sdlog)
c(media_simulata = mean(granuli), mediana_simulata = median(granuli),
  media_teorica = exp(meanlog + sdlog^2/2),
  mediana_teorica = exp(meanlog))
stile_grafico()
hist(granuli, breaks = 40, col = palette_geo[1],
     xlab = "Dimensione simulata (mm)", ylab = "Frequenza",
     main = "Distribuzione positiva e asimmetrica")


# Preparazione: Disegnare l’esperimento di incertezza
m0 <- 106
V0 <- 40
u_m <- 1
u_V <- 0.6
rho_nominale <- m0 / V0
parametri <- data.frame(quantita = c("massa", "volume"),
                        valore = c(m0, V0),
                        incertezza_standard = c(u_m, u_V),
                        unita = c("g", "cm^3"))
parametri
rho_nominale


# Analisi principale: Propagare l’incertezza con molte estrazioni
set.seed(412)
B <- 20000L
massa <- rnorm(B, mean = m0, sd = u_m)
volume <- rnorm(B, mean = V0, sd = u_V)
stopifnot(all(massa > 0), all(volume > 0))
rho <- massa / volume
q_rho <- quantile(rho, c(.025, .5, .975))
riassunto <- data.frame(
  quantita = c("nominale", "media_MC", "sd_MC", "q025", "mediana", "q975"),
  valore = c(rho_nominale, mean(rho), sd(rho), as.numeric(q_rho)))
riassunto
