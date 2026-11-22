# Polychroma M08 · valori citati nelle spiegazioni estese delle tappe.
# Eseguire dalla radice del repository: Rscript content/lezioni/M08-valori.R
# Codice: PolyForm Noncommercial 1.0.0, https://polyformproject.org/licenses/noncommercial/1.0.0
# Required Notice: Copyright 2026 Marzio De Corato (https://github.com/marzione00/Lab_Geo)
RNGkind("Mersenne-Twister", "Inversion", "Rejection")
setwd("lezioni/M08_Polychroma")
invisible(capture.output(source("setup.R", encoding = "UTF-8")))
vars <- v
v <- function(nome, x) cat(sprintf("%-38s %s\n", nome, paste(format(x, digits = 7), collapse = "  ")))
# 2-7 · dati e scale
v("2 quote varianza PC1, PC2", summary(pc)$importance[2, 1:2])
v("3 n per litologia", table(d$litologia_generatrice))
v("5 sd delle otto variabili", apply(X, 2, sd))
v("5 range SiO2, CaO, densita, grana", c(range(d$SiO2), range(d$CaO), range(d$densita), range(d$grana_mm)))
v("3 max |somma ossidi + resto - 100|", max(abs(rowSums(d[c("SiO2", "CaO", "MgO", "FeO", "resto_wt")]) - 100)))
print(d[c(1, 31, 61), c("id", "litologia_generatrice")])
# 8-14 · scale e distanze
dd <- X[1, ] - X[2, ]
v("8 scarti SiO2 e grana (mm) fra R001 e R002", dd[c("SiO2", "grana_mm")])
v("9 quote scarti^2 sulla distanza", round(dd^2 / sum(dd^2), 4))
v("9 distanza standardizzata R001-R002", sqrt(sum((Z[1, ] - Z[2, ])^2)))
v("10 medie", attr(Z, "scaled:center"))
# 15-21 · ridondanza e composizioni
v("15 scarto standardizzato SiO2 R001-R002 e quadrato", c(Z[1, "SiO2"] - Z[2, "SiO2"], (Z[1, "SiO2"] - Z[2, "SiO2"])^2))
fo <- read.csv("Dati/fossili_simulati.csv"); M <- as.matrix(fo[c("diametro_tot_um", "diametro_int_um", "spessore_um")])
v("18 quote varianza PCA fossili", prcomp(M, scale. = TRUE)$sdev^2 / 3)
comp <- as.matrix(d[c("SiO2", "CaO", "MgO", "FeO", "resto_wt")]); clr <- log(comp) - rowMeans(log(comp))
pcc <- prcomp(clr)
v("24 quote varianza CLR", pcc$sdev^2 / sum(pcc$sdev^2))
v("23 media geometrica R001", exp(mean(log(comp[1, ]))))
v("25 min delle cinque parti; min colore e fossili", c(min(comp), min(d$colore), min(d$fossili)))
# 36-42 · autovalori
lam <- pc$sdev^2
v("39 quote varianza, cumulata 2 e 3", c(lam / 8, sum(lam[1:2]) / 8, sum(lam[1:3]) / 8))
v("37 score PC1 R001 da formula", sum(Z[1, ] * pc$rotation[, 1]))
# 50-57 · ricostruzione
Z2 <- pc$x[, 1:2] %*% t(pc$rotation[, 1:2]); X2 <- sweep(sweep(Z2, 2, pc$scale, "*"), 2, pc$center, "+")
v("55 RMSE originali per variabile", sqrt(colMeans((X - X2)^2)))
v("55 minimi ricostruiti", apply(X2, 2, min))
v("55 n negativi per variabile", colSums(X2 < 0))
# 58-64 · k-means
v("60 scomposizione con c=(1,2): 8 + 3*|c-mu|^2", 8 + 3 * sum((c(1, 2) - c(1, 1))^2))
set.seed(818); W64 <- replicate(20, kmeans(Z, centers = 3, nstart = 1, iter.max = 100)$tot.withinss)
v("64 avvii al minimo su 20, valori distinti", c(sum(abs(W64 - min(W64)) < 1e-6), length(unique(round(W64, 3)))))
print(table(round(W64, 3)))
# 65-72 · k-means sulle rocce
set.seed(816); km <- kmeans(Z, 3, nstart = 50, iter.max = 100)
v("67 quota W e B su T", c(km$tot.withinss, km$betweenss) / km$totss)
print(table(km$cluster, d$litologia_generatrice))
v("65 WSS per gruppo", km$withinss)
# 86-88 · Ward
D <- dist(Z); h <- hclust(D, method = "ward.D2")
v("86 ultime altezze, Delta W = h^2/2", c(tail(h$height, 3), tail(h$height, 3)^2 / 2))
v("86 somma Delta W, WSS Ward k=3", c(sum(h$height^2 / 2), 712 - sum(tail(h$height, 2)^2 / 2)))
# 91-96 · coappartenenze e stabilità
v("91 coppie", choose(90, 2))
set.seed(818); Wa <- replicate(30, kmeans(Z, 3, nstart = 1, iter.max = 100)$tot.withinss)
v("95 avvii al minimo su 30", sum(abs(Wa - min(Wa)) < 1e-6))
# 100 · campioni distanti
d2c <- rowSums((Z - km$centers[km$cluster, ])^2)
v("100 soglia 95%, d2 dei segnalati, mediana d2", c(quantile(d2c, .95), sort(d2c[d2c > quantile(d2c, .95)]), median(d2c)))
v("100 n con grana 0.03, n FeO 0.05, max CaO, max fossili", c(sum(d$grana_mm == 0.03), sum(d$FeO == 0.05), max(d$CaO), max(d$fossili)))
# 96 · accordo medio della figura (calcolato dal progetto)
print(read.csv("Calcoli/perturbations_mean.csv"))
