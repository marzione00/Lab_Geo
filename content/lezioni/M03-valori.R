# Iride M03 · valori citati nelle spiegazioni estese delle tappe.
# Eseguire dalla radice del repository: Rscript content/lezioni/M03-valori.R
# Codice: PolyForm Noncommercial 1.0.0, https://polyformproject.org/licenses/noncommercial/1.0.0
# Required Notice: Copyright 2026 Marzio De Corato (https://github.com/marzione00/Lab_Geo)
RNGkind("Mersenne-Twister", "Inversion", "Rejection")
setwd("lezioni/M03_Iride")
invisible(capture.output(source("setup.R", encoding = "UTF-8")))
v <- function(nome, x) cat(sprintf("%-38s %s\n", nome, paste(format(x, digits = 7), collapse = "  ")))
diam <- fossili$diametro_tot_um

# 7 · varianze dei due campioni costruiti
v("7 varianze A, B", c(var(c(4, 5, 6)), var(c(1, 5, 9))))
# 12-13 · quote condizionate e copertura
v("12 quota in A, quota da A", c(10 / 50, 10 / 30))
v("13 quota con ignoti come zeri", 2 / 6)
# 23 · laboratorio della posizione
a <- lab_posizione(outlier = 15)$indicatori; b <- lab_posizione(outlier = 100)$indicatori
v("23 differenza delle medie, mediane", c(b[["media"]] - a[["media"]], a[["mediana"]], b[["mediana"]]))
v("23 media meno mediana con 15", a[["media"]] - a[["mediana"]])
# 28 · quartili di tipo 7
xq <- c(1, 2, 4, 7, 8, 9, 10, 12)
v("28 quartili tipo 7, tipo 6", c(quantile(xq, c(.25, .75), type = 7), quantile(xq, c(.25, .75), type = 6)))
# 30 · diametro dei 160 fossili
v("30 media, sd, sd/media", c(mean(diam), sd(diam), sd(diam) / mean(diam)))
v("30 IQR", IQR(diam))
# 43 · soglie del boxplot nel caso della tappa 42
v("43 B, L, U", c(7 - 3, 3 - 1.5 * 4, 7 + 1.5 * 4))
# 49 · differenze fra morfotipi
g <- split(diam, fossili$morfotipo)
v("49 diff medie, diff mediane", c(mean(g$Spiky) - mean(g$Rounded), median(g$Spiky) - median(g$Rounded)))
v("49 rapporto sd S/R", sd(g$Spiky) / sd(g$Rounded))
# 54 · correlazione diametro-diaframma
r <- cor(fossili$diametro_tot_um, fossili$diaframma_um)
v("54 r, r^2", c(r, r^2))
# 66 · mappa con gradiente 4 e senza gradiente
v("66 aumento atteso della media", 4 * mean(1:20) / 20)
v("66 sd attesa con gradiente", sqrt((4 / 20)^2 * var(rep(1:20, 20)) + 0.3^2))
