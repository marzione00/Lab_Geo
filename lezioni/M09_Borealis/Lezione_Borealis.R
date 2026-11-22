# Borealis M09: frammenti eseguibili nell’ordine della presentazione.
# Aprire Borealis_M09.Rproj e lanciare source("Lezione_Borealis.R", echo=TRUE).
source("setup.R", encoding="UTF-8")
dir.create("Risultati", showWarnings=FALSE)
pdf("Risultati/Figure_lezione.pdf", width=9, height=5.5)

# 004_date.R
# ISO 8601: anno-mese-giorno.
date_es <- as.Date(c("2001-01-01",
                    "2001-02-01",
                    "2001-03-01"))
class(date_es)
diff(date_es)
# Febbraio e gennaio hanno durate diverse.

# 007_archivio.R
source("setup.R", encoding = "UTF-8")
range(wk$data)
nrow(wk)
sum(is.na(wk$co2))
# 2284 date, di cui 59 prive di valore.
c(osservati = sum(!is.na(wk$co2)),
  mancanti = sum(is.na(wk$co2)))

# 008_tabella.R
head(d, 5)
str(d)
# Tre ruoli: data, concentrazione, copertura.
stopifnot(inherits(d$data, "Date"),
  is.numeric(d$co2_ppm),
  all(d$n_settimane >= 0))

# 009_ordinare.R
# L'ordinamento coinvolge l'intera tabella.
wk <- wk[order(wk$data), ]
stopifnot(!anyNA(wk$data))
anyDuplicated(wk$data)
table(as.integer(diff(wk$data)))
# Una differenza in Date restituisce giorni.

# 010_assenze.R
cal_es <- data.frame(
  data = seq(as.Date("2001-01-01"),
             by = "month", length.out = 8),
  valore = c(5, 7, 6, NA, 9, 7, 6, 4))
cal_es[is.na(cal_es$valore), ]
# Il NA mantiene la posizione di aprile.

# 011_duplicati.R
duplicati <- wk[
  duplicated(wk$data) |
    duplicated(wk$data, fromLast = TRUE), ]
nrow(duplicati)
# Qui il risultato e' zero.
# Con piu' sensori, controllare data + sensore.

# 012_griglia.R
griglia_es <- data.frame(
  data = seq(min(cal_es$data), max(cal_es$data),
             by = "month"))
osservati_es <- cal_es[-4, ]
completo_es <- merge(griglia_es, osservati_es,
                    by = "data", all.x = TRUE)
completo_es

# 013_ts.R
y <- ts(d$co2_ppm,
        start = c(1985, 1), frequency = 12)
start(y)
end(y)
frequency(y)
head(time(y))
# Il tempo interno e' espresso in anni.

# 014_controllo_ts.R
griglia <- seq(as.Date("1985-01-01"),
               as.Date("2001-12-01"), by = "month")
stopifnot(identical(d$data, griglia),
          nrow(d) == 204L,
          !anyNA(d$co2_ppm),
          !anyDuplicated(d$data))
# Solo ora la frequenza descrive il file.

# 016_aggregare.R
mese_w <- format(wk$data, "%Y-%m")
gruppi_w <- split(wk$co2, mese_w)
media_m <- vapply(gruppi_w, function(v) {
  if (all(is.na(v))) NA_real_
  else mean(v, na.rm = TRUE)
}, numeric(1))
n_m <- vapply(gruppi_w, function(v)
  sum(!is.na(v)), integer(1))
head(cbind(media_m, n_m))

# 017_confronto.R
pos <- match(format(mon$data, "%Y-%m"),
             names(media_m))
ricostruita <- unname(media_m[pos])
stopifnot(identical(is.na(ricostruita),
                    is.na(mon$co2_ppm)))
scarto <- max(abs(ricostruita - mon$co2_ppm),
              na.rm = TRUE)
stopifnot(scarto < 1e-6)
scarto

# 019_pesi.R
medie_es <- c(10, 20)
conteggi_es <- c(2, 8)
mean(medie_es)
weighted.mean(medie_es, conteggi_es)
mean(rep(medie_es, conteggi_es))
# Gli ultimi due risultati coincidono.

# 020_durate.R
valori_es <- c(10, 20)
durate_es <- c(1, 3) # ore
weighted.mean(valori_es, durate_es)
# Ipotesi: ogni valore rappresenta
# l'intero intervallo indicato.

# 021_operatori.R
pioggia_es <- c(0, 5, 12, NA, 3)
c(totale_osservato = sum(pioggia_es, na.rm = TRUE),
  media_osservata = mean(pioggia_es, na.rm = TRUE),
  massimo_osservato = max(pioggia_es, na.rm = TRUE),
  giorni_osservati = sum(!is.na(pioggia_es)))

# 022_risoluzione.R
mese_es <- 1:48
segnale_es <- sin(2*pi*mese_es/12) +
              0.35*sin(2*pi*mese_es/3)
blocco3 <- (mese_es - 1) %/% 3
blocco12 <- (mese_es - 1) %/% 12
tapply(segnale_es, blocco3, mean)
tapply(segnale_es, blocco12, mean)

# 025_registro.R
registro <- data.frame(
  data = d$data,
  co2_ppm = d$co2_ppm,
  n_settimane = d$n_settimane)
attr(registro, "definizione") <-
  "Media delle settimane assegnate al mese"
head(registro, 3)
# Le colonne derivate verranno aggiunte dopo.

# 027_componenti.R
ricostruita_T <- with(temp,
  trend_simulato + stagione_simulata +
    residuo_simulato)
err_T <- max(abs(temp$temperatura_C -
                 ricostruita_T))
stopifnot(err_T < 2e-8)

# 028_stagione.R
# Una linea per ogni anno del segmento.
yr <- as.integer(format(d$data, "%Y"))
mo <- as.integer(format(d$data, "%m"))
matplot(1:12, sapply(c(1985, 1992, 2001),
  function(a) d$co2_ppm[yr == a]),
  type = "l", lty = 1, xlab = "Mese",
  ylab = "CO2 (ppm)")

# 030_media_mobile.R
ma3 <- stats::filter(z, rep(1/3, 3),
                     sides = 2)
ma13 <- stats::filter(z, rep(1/13, 13),
                      sides = 2)
plot(z, col = "grey60")
lines(ma3, col = "#C57E42")
lines(ma13, col = "#7363AA", lwd = 2)

# 031_bordi.R
c(NA_media3 = sum(is.na(ma3)),
  NA_media13 = sum(is.na(ma13)))
which(is.na(ma13))
# Con 240 dati completi: 2 NA e 12 NA.
stopifnot(sum(is.na(ma3)) == 2L,
          sum(is.na(ma13)) == 12L)

# 032_filtro_causale.R
passato13 <- stats::filter(z,
  rep(1/13, 13), sides = 1)
# Ogni valore usa presente e 12 mesi precedenti.
head(cbind(z, ma13, passato13), 15)

# 035_loess.R
tempo_T <- seq_along(z)
lo20 <- loess(as.numeric(z) ~ tempo_T,
              span = 0.20)
lo60 <- loess(as.numeric(z) ~ tempo_T,
              span = 0.60)
head(cbind(predict(lo20), predict(lo60)))
# Stesse osservazioni, diverso intorno.

# 036_mediana.R
v_es <- c(0, .2, -.1, .1, 6, -.1, .2, 0, .1)
med_es <- runmed(v_es, k = 3, endrule = "keep")
avg_es <- stats::filter(v_es, rep(1/3, 3))
cbind(v_es, med_es, avg_es)
# Una finestra di tre valori.

# 037_anomalia.R
mese_T <- as.integer(format(temp$data, "%m"))
base_T <- temp$data >= as.Date("2000-01-01") &
          temp$data <= as.Date("2004-12-01")
clima_T <- tapply(temp$temperatura_C[base_T],
                 mese_T[base_T], mean)
riferimento_T <- unname(clima_T[mese_T])
anomalia_T <- temp$temperatura_C - riferimento_T

# 038_stl.R
stl_T <- stl(z, s.window = "periodic",
             robust = TRUE)
componenti_T <- stl_T$time.series
err_stl <- max(abs(rowSums(componenti_T) -
                   as.numeric(z)))
stopifnot(err_stl < 1e-10)
plot(stl_T)

# 039_registro_componenti.R
tab_T <- data.frame(
  data = temp$data,
  osservata = temp$temperatura_C,
  riferimento = riferimento_T,
  anomalia = anomalia_T,
  resto_STL = componenti_T[, "remainder"])
head(tab_T, 3)

# 040_lag1.R
x40 <- proc$ar1
coppie1 <- data.frame(
  passato = head(x40, -1),
  presente = tail(x40, -1))
head(coppie1)
nrow(coppie1)
# 300 valori generano 299 coppie al ritardo 1.

# 041_lag12.R
n41 <- nrow(d)
coppie12 <- data.frame(
  data = d$data[13:n41],
  passato = head(d$co2_ppm, -12),
  presente = tail(d$co2_ppm, -12))
head(coppie12, 3)
stopifnot(nrow(coppie12) == 192L)

# 042_scatter_lag.R
plot(coppie1$passato, coppie1$presente,
     pch = 16, col = "#1D789080",
     xlab = "Valore precedente",
     ylab = "Valore presente")
cor(coppie1$passato, coppie1$presente)

# 043_cor_vs_acf.R
x43 <- c(1, 2, 3, 5, 4)
cor(head(x43, -1), tail(x43, -1))
as.numeric(acf(x43, lag.max = 1,
               plot = FALSE)$acf[2])
# cor() ricentra separatamente le due colonne.
# acf() usa la media dell'intera serie.

# 044_acf_manuale.R
xc44 <- x43 - mean(x43)
rho44 <- sum(head(xc44, -1) *
               tail(xc44, -1)) / sum(xc44^2)
rho_R <- as.numeric(acf(x43, plot = FALSE)$acf[2])
stopifnot(abs(rho44 - rho_R) < 1e-12)
rho44 # 0.4

# 046_scala_acf.R
a46 <- as.numeric(acf(proc$ar1,
  lag.max = 24, plot = FALSE)$acf)
b46 <- as.numeric(acf(10*proc$ar1 + 5,
  lag.max = 24, plot = FALSE)$acf)
stopifnot(max(abs(a46 - b46)) < 1e-12)

# 047_leggere_acf.R
acf(proc$ar1, lag.max = 24,
    main = "AR(1): ritardi in passi")
acf(y, lag.max = 24,
    main = "CO2: ritardi espressi in anni")
# Per y mensile, il ritardo 1 del grafico
# corrisponde a 12 osservazioni.

# 049_bande.R
a49 <- as.numeric(acf(proc$rumore_bianco,
  lag.max = 24, plot = FALSE)$acf)[-1]
banda49 <- 1.96 / sqrt(nrow(proc))
which(abs(a49) > banda49)
# Confronti puntuali, fra loro dipendenti.

# 050_na_acf.R
# Controllo prima di calcolare l'ACF.
stopifnot(!anyNA(y))
# Esempio: un mese rimane NA.
y50 <- y
y50[30] <- NA
sum(complete.cases(head(y50, -1),
                   tail(y50, -1)))

# 051_pacf.R
pacf(proc$ar1, lag.max = 24,
     main = "Autocorrelazione parziale")
# R stima modelli autoregressivi
# di ordine via via maggiore.

# 052_acf_pacf_teoria.R
# Valori teorici per AR(1), phi = 0.65.
ARMAacf(ar = 0.65, lag.max = 12)
ARMAacf(ar = 0.65, lag.max = 12, pacf = TRUE)

# 053_tre_acf.R
for (nome in c("rumore_bianco", "ar1",
               "random_walk")) {
  acf(proc[[nome]], lag.max = 24, main = nome)
}

# 056_rumore.R
set.seed(19056)
# Rumore gaussiano IID.
e56 <- rnorm(300)
acf(e56, lag.max = 24,
    main = "Rumore bianco simulato")
# L'ACF campionaria oscilla attorno a zero.
mean(e56)
var(e56)

# 057_dipendenza.R
set.seed(19057)
u57 <- rnorm(10001)
e57 <- head(u57, -1) * tail(u57, -1)
# Stessa coppia di tempi, due confronti.
cor(head(e57, -1), tail(e57, -1))
cor(head(e57^2, -1), tail(e57^2, -1))

# 058_ar1.R
set.seed(19058)
# arima.sim gestisce il tratto iniziale.
a58 <- arima.sim(
  model = list(ar = 0.65), n = 300)
plot(a58, ylab = "Valore",
     main = "AR(1), phi = 0.65")
acf(a58, lag.max = 24)

# 059_impulso.R
# Risposta teorica a un impulso unitario.
k59 <- 0:12
effetto59 <- 0.65^k59
data.frame(ritardo = k59,
           effetto = round(effetto59, 4))

# 060_varianza_ar.R
phi60 <- c(0, 0.3, 0.65, 0.9)
# Innovazioni con varianza unitaria.
data.frame(phi = phi60,
  varianza = 1 / (1 - phi60^2))

# 061_acf_ar.R
k61 <- 0:12
# Curve teoriche, senza errore campionario.
rho61 <- sapply(c(0.65, -0.65, 0.9),
               function(p) p^k61)
matplot(k61, rho61, type = "b",
        xlab = "Ritardo", ylab = "ACF")
abline(h = 0, col = "grey70")

# 062_inizializzazione.R
# Il CSV fornito parte da un valore fissato.
head(proc[, c("passo", "ar1")])
stopifnot(proc$ar1[1] == 0)
h62 <- 0:10
v62 <- (1 - 0.65^(2 * h62)) /
       (1 - 0.65^2)
data.frame(passi = h62, varianza = v62)

# 063_rumore_comune.R
set.seed(19063)
e63 <- rnorm(150)
ar63 <- function(phi) {
  x <- numeric(length(e63))
  for (t in 2:length(x))
    x[t] <- phi * x[t-1] + e63[t]
  x
}
# Le due traiettorie usano lo stesso e63.
matplot(cbind(ar63(0.3), ar63(0.9)),
        type = "l", ylab = "Valore")

# 064_random_walk.R
set.seed(19064)
e64 <- rnorm(150)
# X0 = 0. cumsum conserva gli shock.
rw64 <- c(0, cumsum(e64))
plot(0:150, rw64, type = "l",
     xlab = "Tempo", ylab = "X")
stopifnot(isTRUE(all.equal(
  diff(rw64), e64)))

# 065_varianza_rw.R
t65 <- c(1, 4, 25, 100)
# X0 fissato, varianza innovazioni = 1.
data.frame(tempo = t65,
           varianza = t65,
           deviazione = sqrt(t65))

# 066_repliche.R
set.seed(19066)
B66 <- 2000
# Ogni colonna usa innovazioni nuove.
rw66 <- replicate(B66, cumsum(rnorm(100)))
# Varianza tra repliche, a tempo fissato.
v66 <- apply(rw66, 1, var)
round(v66[c(1, 25, 100)], 1)

# 069_detrending.R
# Temperatura sintetica: una retta da verificare.
t69 <- seq_along(z)
fit69 <- lm(as.numeric(z) ~ t69)
res69 <- residuals(fit69)
plot(t69, res69, type = "l",
     xlab = "Mese", ylab = "Residuo")
acf(res69, lag.max = 36)

# 070_incrementi.R
x70 <- c(10, 13, 12, 16)
diff(x70)
# Il secondo incremento e' negativo.
stopifnot(identical(diff(x70),
                    c(3, -1, 4)))

# 071_date_differenze.R
dy71 <- diff(y)
# Ogni differenza assume la data finale.
tab71 <- data.frame(
  data = tail(d$data, -1),
  incremento_ppm = as.numeric(dy71))
head(tab71)
c(n = length(dy71), start(dy71))

# 073_stagionale.R
ds73 <- diff(y, lag = 12)
# Il primo valore confronta due gennaio.
data.frame(
  data = tail(d$data, -12),
  variazione_annua = as.numeric(ds73))[1:4, ]
c(start(ds73), end(ds73))
length(ds73)

# 074_operatore.R
# Identita' su un vettore numerico.
v74 <- as.numeric(y)
manuale74 <- v74[-1] - head(v74, -1)
stopifnot(isTRUE(all.equal(
  manuale74, as.numeric(diff(y)))))

# 075_combinata.R
dc75 <- diff(diff(y, lag = 12))
# Cambiare l'ordine produce lo stesso filtro.
alt75 <- diff(diff(y), lag = 12)
stopifnot(isTRUE(all.equal(dc75, alt75)))
plot(dc75, ylab = "Differenza combinata")
acf(dc75, lag.max = 36)

# 076_numerosita.R
# Confronto sul segmento completo.
forme76 <- list(livelli = y,
  ordinaria = diff(y),
  stagionale = diff(y, lag = 12),
  combinata = diff(diff(y, lag = 12)))
sapply(forme76, length)
sapply(forme76, start)

# 077_ricostruzione.R
v77 <- as.numeric(y)
ric77 <- c(v77[1],
           v77[1] + cumsum(diff(v77)))
# Tolleranza dovuta all'aritmetica numerica.
max(abs(ric77 - v77))
stopifnot(max(abs(ric77 - v77)) < 1e-10)

# 080_sovradifferenza.R
set.seed(19080)
e80 <- rnorm(10000)
de80 <- diff(e80)
r80 <- acf(de80, lag.max = 10,
           plot = FALSE)$acf
round(c(varianza = var(de80),
        acf1 = r80[2]), 3)
acf(de80, lag.max = 10)

# 081_alternative.R
# Due ACF teoriche con lo stesso primo lag.
lag81 <- 0:8
acf_diff81 <- c(1, -0.5, rep(0, 7))
acf_ar81 <- (-0.5)^lag81
data.frame(lag = lag81,
  rumore_differenziato = acf_diff81,
  ar_negativo = acf_ar81)

# 082_due_trasformazioni.R
set.seed(19082)
t82 <- 1:200
x82 <- 10 + 0.04 * t82 + rnorm(200)
r82 <- residuals(lm(x82 ~ t82))
d82 <- diff(x82)
# Lo stesso input, due resti differenti.
c(detrend = acf(r82, plot = FALSE)$acf[2],
  differenza = acf(d82, plot = FALSE)$acf[2])

# 083_registro.R
registro83 <- data.frame(
  serie = c("livelli", "diff1", "diff12", "combinata"),
  n = sapply(forme76, length),
  prima_data = as.character(d$data[c(1,2,13,14)]),
  ultima_data = as.character(tail(d$data, 1)))
registro83

# 087_ritardi_adf.R
# Analisi di sensibilita', non ricerca del p minimo.
ks87 <- c(1, 4, 8)
stat87 <- sapply(ks87, function(k) {
  tseries::adf.test(as.numeric(y),
                    k = k)$statistic
})
data.frame(k = ks87, statistica = stat87)

# 088_adf.R
# Pacchetto richiesto dal progetto.
stopifnot(requireNamespace("tseries",
                          quietly = TRUE))
adf88 <- tseries::adf.test(
  as.numeric(y), k = 4)
adf88
# Campi da riportare nel resoconto.
adf88[c("statistic", "parameter",
        "p.value", "alternative")]

# 089_somme_parziali.R
# Versione Level: si sottrae la media.
e89 <- as.numeric(y) - mean(y)
S89 <- cumsum(e89)
plot(S89, type = "l", ylab = "Somma residui",
     xlab = "Mese")
abline(h = 0, col = "grey70")

# 091_kpss.R
kL91 <- tseries::kpss.test(as.numeric(y),
  null = "Level", lshort = TRUE)
kT91 <- tseries::kpss.test(as.numeric(y),
  null = "Trend", lshort = TRUE)
kL91
kT91

# 093_avvisi.R
w93 <- character()
a93 <- withCallingHandlers(
  tseries::adf.test(as.numeric(y), k = 4),
  warning = function(w) {
    w93 <<- c(w93, conditionMessage(w))
  })
# Gli avvisi sono registrati e restano visibili.
list(test = a93, avvisi = w93)

# 095_cambio_livello.R
set.seed(19095)
x95 <- c(rep(0, 80), rep(2, 80)) + rnorm(160)
plot(x95, type = "l", ylab = "Valore")
abline(v = 80.5, col = "darkorange")
# Consultare i metadati prima dei test.
c(media_prima = mean(x95[1:80]),
  media_dopo = mean(x95[81:160]))

# 096_resoconto.R
resoconto96 <- list(
  serie = "CO2 mensile storica, livelli",
  periodo = range(d$data),
  osservazioni = length(y),
  adf = adf88,
  kpss_livello = kL91,
  kpss_trend = kT91)
resoconto96$periodo

# 098_co2_diff1.R
delta1 <- diff(y)
plot(delta1, ylab = "Differenza (ppm)")
acf(as.numeric(delta1), lag.max = 24,
    main = "Differenza mensile")
length(delta1) # 203 valori

# 099_co2_diff12.R
delta12 <- diff(y, lag = 12)
plot(delta12,
     ylab = "Differenza rispetto a 12 mesi (ppm)")
length(delta12) # 192 valori
acf(as.numeric(delta12), lag.max = 24)

# 100_co2_combinata.R
deltaC <- diff(diff(y, lag = 12))
alternativaC <- diff(diff(y), lag = 12)
stopifnot(max(abs(deltaC - alternativaC)) < 1e-10)
length(deltaC) # 191 valori
plot(deltaC, ylab = "Differenza combinata (ppm)")

# 101_allineare_trasformazioni.R
confronto <- data.frame(
  data = d$data,
  livello = as.numeric(y),
  diff1 = c(NA, as.numeric(delta1)),
  diff12 = c(rep(NA, 12), as.numeric(delta12)),
  combinata = c(rep(NA, 13), as.numeric(deltaC)))
head(confronto, 15)

# 103_diagnosi_residua.R
varianti <- list(diff1 = delta1,
                 diff12 = delta12,
                 combinata = deltaC)
sapply(varianti, function(v) {
  a <- as.numeric(acf(as.numeric(v),
    lag.max = 12, plot = FALSE)$acf)
  c(lag1 = a[2], lag12 = a[13])
})

# 104_esportare.R
dir.create("Risultati", showWarnings = FALSE)
write.csv(confronto,
  "Risultati/CO2_trasformazioni.csv",
  row.names = FALSE)
scelte <- list(periodo = range(d$data),
  frequenza = 12, ritardi = c(1, 12),
  ADF_k = 4, KPSS_lshort = TRUE)
saveRDS(scelte, "Risultati/scelte.rds")

dev.off()
