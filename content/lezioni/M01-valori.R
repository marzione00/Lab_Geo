# Terra M01 · valori citati nelle spiegazioni estese delle tappe.
# Eseguire dalla radice del repository: Rscript content/lezioni/M01-valori.R
# Codice: PolyForm Noncommercial 1.0.0, https://polyformproject.org/licenses/noncommercial/1.0.0
# Required Notice: Copyright 2026 Marzio De Corato (https://github.com/marzione00/Lab_Geo)
RNGkind("Mersenne-Twister", "Inversion", "Rejection")
setwd("lezioni/M01_Terra")
source("setup.R", encoding = "UTF-8")
v <- function(nome, x) cat(sprintf("%-38s %s\n", nome, paste(format(x, digits = 7), collapse = "  ")))
skew <- function(x) mean((x - mean(x))^3) / sd(x)^3
ciampino <- read.csv("Dati/meteostat_ciampino_2024.csv")
storica <- read.csv("Dati/meteostat_16239_2019_2024_originale.csv")

# 3-16 · primi passi, tabelle, indicatori
v("3 media con quarto valore 20", mean(c(3, 7, 10, 20)))
v("4 Fahrenheit, media K, media C", c(c(12, 14, 13) * 9/5 + 32, mean(c(12, 14, 13) + 273.15), mean(c(12, 14, 13))))
v("8 media delle medie di stazione", (3.05 + 7.1) / 2)
v("8 medie terra per stazione", tapply(terra$valore, terra$stazione, mean))
v("9 summary terra", summary(terra$valore))
g <- factor(c("A", "A", "B", "C"))
v("13 codici e loro media", c(as.integer(g), mean(as.integer(g))))
v("15 con 90: media, mediana", c(mean(c(2, 3, 3, 4, 90)), median(c(2, 3, 3, 4, 90))))
v("16 con 7: media, mediana", c(mean(c(10, 3, 2, 5, 7)), median(c(10, 3, 2, 5, 7))))
v("16 con 50: media, mediana", c(mean(c(10, 3, 2, 50)), median(c(10, 3, 2, 50))))

# 17-28 · Terra 01
v("17 pesi misure, stazione", c(as.vector(prop.table(table(terra$stazione))), 1/3))
v("20 media misure, stazioni (modello)", c((20 * 3 + 10 * 7 + 10 * 10) / 40, 20/3))
nA <- c(10, 20, 50, 100, 1000)
v("21 attesa media misure", (3 * nA + 170) / (nA + 20))
v("21 peso di A", nA / (nA + 20))
v("22 SE A, SE B", 0.4 / sqrt(c(20, 10)))
set.seed(17); a <- rnorm(20, 3, 0.4)
v("22 seme 17: media, sd", c(mean(a), sd(a)))
for (s in 1:3) { set.seed(s); a <- rnorm(20, 3, 0.4); v(paste("22 seme", s, "media, sd"), c(mean(a), sd(a))) }
set.seed(17); sim <- c(rnorm(20, 3, 0.4), rnorm(10, 7, 0.4), rnorm(10, 10, 0.4))
v("23 scarto massimo dal CSV", max(abs(sim - terra$valore)))
for (g in c("A", "B", "C")) {
  x <- terra$valore[terra$stazione == g]
  v(paste("25", g, "boxplot, fuori"), c(boxplot.stats(x)$stats, boxplot.stats(x)$out))
}
v("25 mediane", tapply(terra$valore, terra$stazione, median))

# 29-41 · campionamento e statistica
set.seed(1); v("29 siti con seme 1", c(sample(1:6, 2), sample(7:12, 2), sample(13:18, 2)))
d <- data.frame(stazione = c("A", "A", "B", "B"), valore = c(3.1, NA, 7, 7))
v("30 media disponibili, senza duplicato", c(mean(d$valore, na.rm = TRUE), mean(unique(d)$valore, na.rm = TRUE)))
x <- c(0, 0, 0, 1, 2, 8, 24)
v("32 senza 24: media, mediana; piovosi", c(mean(x[x < 24]), median(x[x < 24]), mean(x[x > 0])))
v("34 RMSE con 18, MAE", c(sqrt(mean((c(10, 12, 15) - c(9, 13, 18))^2)), mean(abs(c(10, 12, 15) - c(9, 13, 18)))))
x <- rbind(c(1, 2), c(2, 1), c(2, 2), c(8, 9), c(9, 8), c(9, 9)); z <- scale(x)
v("35 media, sd colonne", c(attr(z, "scaled:center"), attr(z, "scaled:scale")))
set.seed(17); v("35 centri", kmeans(z, centers = 2, nstart = 20)$centers)
v("36 acf", acf(c(1, 2, 3, 4, 4, 3, 2, 1, 1, 2, 3, 4), lag.max = 5, plot = FALSE)$acf[2:4])
set.seed(17); t <- 1:30; x <- 2 + 0.1 * t + rnorm(30, sd = 0.6)
v("37 retta stimata", coef(lm(x ~ t)))
v("38 scarto, sd, SE", c(mean(c(20.2, 20.3, 20.4)) - 20, sd(c(20.2, 20.3, 20.4)), 0.1 / sqrt(3)))
x <- c(3, 4, 5, 6, 7, 8, 16)
v("41 mediana senza massimo", median(x[x < 16]))

# 42-53
x <- 1:8; y <- c(1, 4, 8, 16, 24, 36, 49, 65); fit <- lm(y ~ x)
v("42 coefficienti, R2", c(coef(fit), summary(fit)$r.squared))
v("42 residui", resid(fit))
v("42 residui quadratica", range(resid(lm(y ~ x + I(x^2)))))
x <- c(3.1, 3.4, 2.8, 3, 3.2)
v("43 IP 95%, IC 90%", c(mean(x) + c(-1, 1) * qt(.975, 4) * sd(x) * sqrt(1.2), mean(x) + c(-1, 1) * qt(.95, 4) * sd(x) / sqrt(5)))
set.seed(17); x <- rexp(1000); m <- cumsum(x) / seq_along(x)
v("45 medie cumulative 1, 10, 100, 1000", m[c(1, 10, 100, 1000)])
v("45 fuori banda da n=10", sum(abs(m[10:1000] - 1) > 2 / sqrt(10:1000)))
for (n in c(1, 5, 30)) {
  set.seed(17); z <- sqrt(n) * (replicate(3000, mean(rexp(n))) - 1)
  v(paste("47 n", n, "media, sd, asimm., code"), c(mean(z), sd(z), skew(z), mean(abs(z) > 1.96), sum(z > 1.96), sum(z < -1.96)))
}
v("52 senza 100: media, mediana", c(mean(c(3, 4, 5)), median(c(3, 4, 5))))

# 54-62 · statistica descrittiva
x <- c(1, 2, 2, 3, 7)
v("54 varianza; con 70: ampiezza, sd, IQR", c(var(x), diff(range(c(1, 2, 2, 3, 70))), sd(c(1, 2, 2, 3, 70)), IQR(c(1, 2, 2, 3, 70))))
p <- demo$pioggia; mese <- format(demo$data, "%m")
v("56 media, quota asciutti, intensita", c(mean(p), mean(p == 0), mean(p[p > 0]), sum(p > 0)))
v("56 quota piovosi per mese", tapply(p > 0, mese, mean))
v("56 intensita per mese", tapply(p[p > 0], mese[p > 0], mean))
v("56 Ciampino: giorni, quota asciutti", c(sum(!is.na(ciampino$pioggia)), mean(ciampino$pioggia == 0, na.rm = TRUE)))
v("56 Ciampino mediane mensili", tapply(ciampino$pioggia, substr(ciampino$data, 6, 7), median, na.rm = TRUE))
ok <- complete.cases(ciampino[c("sole", "tmax", "nubi_ottavi")])
v("58 n, r sole-tmax, r sole-nubi", c(sum(ok), cor(ciampino$sole[ok], ciampino$tmax[ok]), cor(ciampino$sole[ok], ciampino$nubi_ottavi[ok])))
x <- -3:3; y <- x^2
v("59 r senza ultimo, senza centro", c(cor(x[-7], y[-7]), cor(x[-4], y[-4])))
mod <- lm(tmax ~ tmin, data = demo)
v("60 IC pendenza, R2, range tmin", c(confint(mod)[2, ], summary(mod)$r.squared, range(demo$tmin)))
v("61 acf residui ritardo 1", acf(residuals(mod), plot = FALSE)$acf[2])
v("62 Ciampino retta, R2", c(coef(lm(tmax ~ tmin, ciampino)), summary(lm(tmax ~ tmin, ciampino))$r.squared))

# 63-72 · gestione, grafici, trasformazioni
v("65 media senza 12", mean(c(1.2, 1.4)))
v("66 sole medio e massimo in ore", c(mean(demo$sole), max(demo$sole)) / 60)
h <- hist(terra$valore, plot = FALSE)
v("67 classi e conteggi", c(h$breaks, h$counts))
u <- log1p(demo$pioggia)
v("68 massimo, asimmetria prima e dopo", c(max(demo$pioggia), max(u), skew(demo$pioggia), skew(u)))
zt <- (demo$tmax - mean(demo$tmax)) / sd(demo$tmax)
v("68 media, sd tmax, range z", c(mean(demo$tmax), sd(demo$tmax), range(zt)))
pc <- ciampino$pioggia[!is.na(ciampino$pioggia)]
v("69 Ciampino massimo, log1p", c(max(pc), log1p(max(pc)), exp(1) - 1, exp(4) - exp(3)))
v("70 Ciampino tmax media, sd, range z", c(mean(ciampino$tmax), sd(ciampino$tmax), range((ciampino$tmax - mean(ciampino$tmax)) / sd(ciampino$tmax))))
ym <- format(demo$data, "%Y-%m")
sc <- stl(ts(tapply(demo$tmax, ym, mean), start = c(2022, 1), frequency = 12), s.window = "periodic")$time.series
v("71 stagione, tendenza, resto", c(range(sc[, 1]), range(sc[, 2]), range(sc[, 3])))
base <- demo$data < as.Date("2024-01-01"); rif <- tapply(demo$tmax[base], mese[base], mean)
v("72 riferimento gennaio, luglio; 2024", c(rif["01"], rif["07"], mean((demo$tmax - rif[mese])[!base])))

# 73-84 · serie temporali
v("73 giorni > 10 mm per mese", tapply(storica$prcp, sprintf("%02d", storica$month), function(x) sum(x > 10, na.rm = TRUE)))
x <- demo$tmax; m31 <- as.numeric(stats::filter(x, rep(1/31, 31), sides = 2))
md <- runmed(x, 31, endrule = "constant"); md[c(1:15, 1082:1096)] <- NA
v("76 NA, sd prima e dopo, scarto max", c(sum(is.na(m31)), sd(x), sd(m31, na.rm = TRUE), max(abs(m31 - md), na.rm = TRUE)))
demo$giorno <- seq_len(nrow(demo))
for (s in c(0.1, 0.2, 0.3)) v(paste("77-78 loess span", s, "range"), range(predict(loess(tmax ~ giorno, demo, span = s, degree = 1))))
v("77 sd attorno alla curva", sd(demo$tmax - predict(loess(tmax ~ giorno, demo, span = 0.2, degree = 1))))
lo <- predict(loess(storica$temp ~ seq_len(nrow(storica)), span = 0.2, degree = 2))
v("80 escursione annua loess", tapply(lo, storica$year, function(x) diff(range(x))))
v("80 escursione annua media 31 g", tapply(as.numeric(stats::filter(storica$temp, rep(1/31, 31), sides = 2)), storica$year, function(x) diff(range(x, na.rm = TRUE))))
an <- demo$tmax - tapply(demo$tmax, mese, mean)[mese]
v("81 range, sd, media per anno", c(range(an), sd(an), tapply(an, format(demo$data, "%Y"), mean)))
cs <- demo$tmax + 2 * (demo$data >= as.Date("2023-07-01")); yr <- format(demo$data, "%Y")
v("82 giorni dopo il salto, effetto annuo", c(sum(demo$data >= as.Date("2023-07-01")), tapply(cs, yr, mean) - tapply(demo$tmax, yr, mean)))
