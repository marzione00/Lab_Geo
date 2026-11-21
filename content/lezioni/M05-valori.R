# Pelago M05 · valori citati nelle spiegazioni estese (tappe 16-25).
# Eseguire dalla radice del repository: Rscript content/lezioni/M05-valori.R
# Codice: PolyForm Noncommercial 1.0.0, https://polyformproject.org/licenses/noncommercial/1.0.0
# Required Notice: Copyright 2026 Marzio De Corato (https://github.com/marzione00/Lab_Geo)
RNGkind("Mersenne-Twister", "Inversion", "Rejection")
setwd("lezioni/M05_Pelago")
source("Pelago_laboratori.R", encoding = "UTF-8")
v <- function(nome, x) cat(sprintf("%-34s %s\n", nome, paste(format(x, digits = 7), collapse = "  ")))

# 16 · lista incompleta
y <- c(4, 5, 5, 6, 8, 9, 10, 11); acc <- rep(c(TRUE, FALSE), each = 4)
v("16 media popolazione", mean(y))
v("16 media lista", mean(y[acc]))
v("16 scarto lista-popolazione", mean(y[acc]) - mean(y))
m2 <- combn(y[acc], 2, mean)
v("16 medie campioni n=2 dalla lista", m2)
v("16 attesa n=2, sd n=2", c(mean(m2), sqrt(mean((m2 - mean(m2))^2))))
m3 <- combn(y[acc], 3, mean)
v("16 attesa n=3, sd n=3", c(mean(m3), sqrt(mean((m3 - mean(m3))^2))))
v("16 lista alternata", mean(y[rep(c(TRUE, FALSE), 4)]))

# 17 · distorsione simulata
set.seed(17); t17 <- rnorm(200, 9, 2/sqrt(60))
v("17 bias simulato", mean(t17) - 10)
v("17 sd stime, errore MC", c(sd(t17), sd(t17)/sqrt(200)))
v("17 scarto in errori MC", (mean(t17) - 9)/(sd(t17)/sqrt(200)))
set.seed(17); t17b <- rnorm(2000, 9, 2/sqrt(60))
v("17 bias con 2000 stime", mean(t17b) - 10)
v("17 errore MC atteso B=200, B=2000", (2/sqrt(60))/sqrt(c(200, 2000)))
for (s in c(1, 2, 3)) { set.seed(s); v(paste("17 bias seme", s), mean(rnorm(200, 9, 2/sqrt(60))) - 10) }

# 18-20 · MSE
v("18 varianza, mse, rmse, se", c(4/60, 4/60 + 1, sqrt(4/60 + 1), 2/sqrt(60)))
v("19 se n=60,300", 2/sqrt(c(60, 300)))
v("19 mse n=60,300,6000", 4/c(60, 300, 6000) + 1)
v("19 n per dimezzare se da 60", 60 * 4)
v("20 rapporto mse selettiva/casuale", (4/300 + 1)/(4/60))
v("20 rapporto se selettiva/casuale", sqrt(4/300)/sqrt(4/60))
v("20 n casuale con mse 1.0133", 4/(4/300 + 1))

# 21 · mancanti
v("21 media disponibili", mean(c(2.4, 2.7, 2.5, 2.8)))
v("21 quota osservata", 4/6)

# 23 · laboratorio
for (cfg in list(c(60, 1), c(300, 1), c(60, 0))) {
  r <- lab_selezione(n = cfg[1], bias = cfg[2])
  a <- r$dati$valore[r$dati$disegno == "Casuale"]; b <- r$dati$valore[r$dati$disegno == "Selezionato"]
  v(sprintf("23 n=%d b=%g: mse sel, teorica", cfg[1], cfg[2]), c(mean((b - 10)^2), 4/cfg[1] + cfg[2]^2))
  v(sprintf("23 n=%d b=%g: media sel, sd sel", cfg[1], cfg[2]), c(mean(b), sd(b)))
  v(sprintf("23 n=%d b=%g: media cas, mse cas", cfg[1], cfg[2]), c(mean(a), mean((a - 10)^2)))
}
r <- lab_selezione(n = 60, bias = 1, B = 1000)
v("23 B=1000: mse sel", r$indicatori[["mse_simulato"]])

# 24 · conteggi
provini <- read.csv("Dati/campioni_modulo1.csv", stringsAsFactors = FALSE)
v("24 righe, stazioni, affioramenti", c(nrow(provini), length(unique(provini$stazione)), length(unique(provini$affioramento))))
v("24 misure per stazione", as.vector(table(provini$stazione)))

# 25 · campioni ripetuti
set.seed(17); X25 <- replicate(5, rnorm(4, 10, 2))
v("25 medie", colMeans(X25))
v("25 media e sd delle medie", c(mean(colMeans(X25)), sd(colMeans(X25))))
v("25 sd teorica della media", 2/sqrt(4))
v("25 sd entro campione", apply(X25, 2, sd))
set.seed(17); X25b <- replicate(2000, rnorm(4, 10, 2))
v("25 con 2000 campioni: media, sd", c(mean(colMeans(X25b)), sd(colMeans(X25b))))

# Valori delle proposte «Prova a modificare»
set.seed(17); v("17 bias con n17=600", mean(rnorm(200, 9, 2/sqrt(600))) - 10)
v("17 intervallo 3 sd", 9 + c(-3, 3) * 2/sqrt(60))
v("18 mse con bias -0.1, n=600", c(4/60 + 0.01, 4/600 + 1))
v("19 se n=60,240,960,3840", 2/sqrt(c(60, 240, 960, 3840)))
v("19 mse n=60,240,960,3840", 4/c(60, 240, 960, 3840) + 1)
v("19 bias -6/sqrt(n), mse 40/n", c(-6/sqrt(c(60, 300)), 40/c(60, 300)))
v("20 semiampiezza 95% selettiva", qnorm(0.975) * sqrt(4/300))
v("20 z di 10 per stima 9", (10 - 9 - qnorm(0.975) * sqrt(4/300))/sqrt(4/300))
v("20 mse selettiva b=-0.2", 4/300 + 0.04)
v("20 |b| con mse uguali", sqrt(4/60 - 4/300))
v("21 quota mancante", mean(is.na(c(2.4, NA, 2.7, 2.5, NA, 2.8))))
v("23 mse teorica n=300 b=0.5", 4/300 + 0.25)
set.seed(17); X <- replicate(2000, rnorm(16, 10, 2))
v("25 2000 campioni n=16: sd medie", sd(colMeans(X)))
