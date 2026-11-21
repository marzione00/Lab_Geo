# Tellus M02 · valori citati nelle spiegazioni estese delle tappe.
# Eseguire dalla radice del repository: Rscript content/lezioni/M02-valori.R
# Codice: PolyForm Noncommercial 1.0.0, https://polyformproject.org/licenses/noncommercial/1.0.0
# Required Notice: Copyright 2026 Marzio De Corato (https://github.com/marzione00/Lab_Geo)
RNGkind("Mersenne-Twister", "Inversion", "Rejection")
setwd("lezioni/M02_Tellus")
invisible(capture.output(source("setup.R", encoding = "UTF-8")))
v <- function(nome, x) cat(sprintf("%-38s %s\n", nome, paste(format(x, digits = 7), collapse = "  ")))

# 6-8 · trasformazione affine
v("6 media di 1:10", mean(1:10))
v("8 medie per tre scenari", 5.5 * c(1, 1.5, 1.5) + c(0, 0, -1))

# 15 · estremi della selezione sulla griglia
x <- seq(0, 10, by = 0.5)
v("15 [3,8] inclusi, esclusi", c(sum(x >= 3 & x <= 8), sum(!(x >= 3 & x <= 8))))
v("15 [4,7] inclusi, esclusi", c(sum(x >= 4 & x <= 7), sum(!(x >= 4 & x <= 7))))
v("15 (3,8) stretto inclusi", sum(x > 3 & x < 8))

# 25 · media con la virgola riconosciuta
v("25 media quattro valori", mean(c(1.2, 2.4, 3.1, 4.8)))

# 42 · media prima e dopo la duplicazione di B
v("42 media 3 righe, 4 righe", c(mean(c(2, 5, 9)), mean(c(2, 5, 5, 9))))

# 47 · imputazione con la media
v("47 varianze disponibili, imputati", c(var(c(4, 6)), var(c(4, 5, 6))))

# 49 · estremi della media con un dato censurato
v("49 estremi della media", c(sum(c(0.12, 0.08)) / 3, (sum(c(0.12, 0.08)) + 0.05) / 3))

# 50 · laboratorio dei mancanti, seme 17
set.seed(17); lx <- rlnorm(200, 1, 0.5)
cas <- runif(200) < 0.3; alt <- rank(lx) > 140
v("50 mancanti casuali, selettivi", c(sum(cas), sum(alt)))
v("50 media completa, casuale, selettiva", c(mean(lx), mean(lx[!cas]), mean(lx[!alt])))
v("50 calo relativo selettivo", 1 - mean(lx[!alt]) / mean(lx))

# 58 · temperature simulate con un valore fuori dominio
set.seed(17); t29 <- rnorm(29, 15, 3)
v("58 media con 250, senza, con 20", c(mean(c(t29, 250)), mean(t29), mean(c(t29, 20))))

# 63 · composizione dopo A = 80
v("63 percentuali dopo", 100 * c(80, 35, 25) / 140)
