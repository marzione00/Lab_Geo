# Annula M07: frammenti eseguibili nell’ordine della presentazione.
# Aprire Annula_M07.Rproj e lanciare source("Lezione_Annula.R", echo=TRUE).
source("setup.R", encoding="UTF-8")
dir.create("Risultati", showWarnings=FALSE)
pdf("Risultati/Figure_lezione.pdf", width=9, height=5.5)

# 003_dati.R
# Avvio dalla cartella Annula_M07.
source("setup.R", encoding = "UTF-8")
# Una riga corrisponde a un fossile.
head(f[, c("id", "diametro_tot_um",
           "diametro_int_um")])
stopifnot(!anyDuplicated(f$id))

# 004_geometria.R
# La relazione deriva dalla costruzione
# geometrica delle tre misure.
scarto <- with(f, diametro_tot_um -
  diametro_int_um - 2 * spessore_um)
max(abs(scarto))
# Circa 1e-8: arrotondamento del CSV.

# 005_nuvola.R
# Colore secondo il morfotipo.
col <- c("#1D7890", "#C57E42")
plot(diametro_int_um ~ diametro_tot_um,
  data = f, col = col[f$morfotipo],
  pch = 16, xlab = "Totale (um)",
  ylab = "Interno (um)")

# 007_dominio.R
# Campo realmente osservato nel file.
range(f$diametro_tot_um)
# Un nuovo valore deve essere esaminato.
x0 <- 9
x0 >= min(f$diametro_tot_um) &&
  x0 <= max(f$diametro_tot_um)

# 009_correlazione.R
x <- f$diametro_tot_um
y <- f$diametro_int_um
cor(x, y, method = "pearson")
# Cambio di unita positivo: stesso r.
cor(x / 1000, y / 1000)
# L'inversione del segno cambia r.
cor(x, -y)

# 010_ranghi.R
# Spearman applica Pearson ai ranghi.
cor(x, y, method = "spearman")
cor(rank(x), rank(y))
# In caso di pareggi R usa ranghi medi.

# 011_curvatura.R
# Esempio costruito, senza rumore.
u <- seq(-2, 2, length.out = 101)
v <- u^2
cor(u, v)  # Praticamente zero.
plot(u, v, pch = 16)

# 012_campo.R
# Stessa legge, due campi del predittore.
set.seed(17)
u <- runif(1000, -4, 4)
v <- 2 * u + rnorm(1000)
centrali <- abs(u) < 1
c(intero = cor(u, v),
  ristretto = cor(u[centrali],
                 v[centrali]))

# 017_scarti.R
# Retta proposta, prima dell'ottimizzazione.
a <- -0.5
b <- 0.9
e_proposti <- y - (a + b * x)
sum(e_proposti^2)
# Confronto con il minimo trovato da lm.
sum(residuals(m0)^2)

# 022_minimi_mano.R
# Scarti dalle rispettive medie.
xc <- x - mean(x)
yc <- y - mean(y)
b1 <- sum(xc * yc) / sum(xc^2)
b0 <- mean(y) - b1 * mean(x)
c(intercetta = b0, pendenza = b1)
# Le due procedure devono coincidere.
all.equal(unname(coef(m0)), c(b0, b1))

# 023_lm.R
# La risposta compare a sinistra di ~.
m0 <- lm(diametro_int_um ~
           diametro_tot_um, data = f)
coef(m0)      # Intercetta e pendenza.
fitted(m0)    # Valori medi stimati.
residuals(m0) # Osservato - stimato.
summary(m0)

# 024_pendenza.R
# Incremento medio per +0.5 um in X.
delta_x <- 0.5
coef(m0)[2] * delta_x
# Previsione media a diametro totale 7.
predict(m0, newdata = data.frame(
  diametro_tot_um = 7))

# 026_matrice.R
# X contiene una colonna di 1 e il predittore.
X <- model.matrix(m0)
head(X)
dim(X)       # 160 righe, 2 colonne.
qr(X)$rank   # Rango della matrice.

# 028_qr.R
X <- model.matrix(m0)
# QR evita di formare esplicitamente
# l'inversa di t(X) %*% X.
b_qr <- qr.coef(qr(X), y)
max(abs(b_qr - coef(m0)))
# Equazioni normali: quasi zero.
max(abs(crossprod(X, residuals(m0))))

# 029_identita.R
# Deviazioni standard con lo stesso denominatore.
b_da_r <- cor(x, y) * sd(y) / sd(x)
c(formula = b_da_r,
  lm = unname(coef(m0)[2]))
# R2 = r^2: solo regressione semplice
# OLS con intercetta, sugli stessi casi.
c(r2 = cor(x, y)^2,
  R2 = summary(m0)$r.squared)

# 030_scomposizione.R
SST <- sum((y - mean(y))^2)
SSE <- sum(residuals(m0)^2)
SSR <- sum((fitted(m0) - mean(y))^2)
c(totale = SST, modello = SSR,
  residua = SSE)
all.equal(SST, SSR + SSE)

# 033_sigma.R
e <- residuals(m0)
n <- nobs(m0)
p <- m0$rank
s <- sqrt(sum(e^2) / (n - p))
c(calcolo = s, R = sigma(m0))
# RMSE in campione usa invece n.
sqrt(mean(e^2))

# 035_ci_coef.R
# Intervalli t sotto le ipotesi classiche.
confint(m0, level = 0.95)
# La tabella riporta anche gli errori standard.
coef(summary(m0))

# 039_predict.R
nuovo <- data.frame(diametro_tot_um = 7)
# Incertezza della media condizionata.
predict(m0, newdata = nuovo,
        interval = "confidence")
# Variabilita di un nuovo individuo.
predict(m0, newdata = nuovo,
        interval = "prediction")

# 040_estrapolazione.R
# Lo stesso comando produce numeri
# anche fuori dal campo osservato.
fuori <- data.frame(diametro_tot_um = 11)
predict(m0, newdata = fuori,
        interval = "prediction")
range(f$diametro_tot_um)

# 042_residui.R
# m0 descrive il diametro interno.
e42 <- residuals(m0)
yhat42 <- fitted(m0)
plot(yhat42, e42, pch = 19,
     xlab = "Valore stimato (um)",
     ylab = "Residuo (um)")
abline(h = 0, lty = 2)
# La curva locale aiuta la lettura.
lines(lowess(yhat42, e42), col = 2)

# 043_vincoli.R
# Con intercetta e minimi quadrati:
e43 <- residuals(m0)
c(somma = sum(e43),
  media = mean(e43))
# Anche X trasposta per e e' quasi 0.
X43 <- model.matrix(m0)
drop(crossprod(X43, e43))

# 044_curvatura.R
# Aggiungiamo un termine quadratico.
m_quad <- lm(diametro_int_um ~
  diametro_tot_um +
  I(diametro_tot_um^2), data = f)
plot(fitted(m_quad), resid(m_quad),
     pch = 19, xlab = "Stima (um)",
     ylab = "Residuo (um)")
abline(h = 0, lty = 2)

# 045_dispersione.R
# Scala dei residui standardizzati.
rs45 <- rstandard(m0)
plot(fitted(m0), sqrt(abs(rs45)),
     pch = 19, xlab = "Stima (um)",
     ylab = "Radice di |residuo std| ")
lines(lowess(fitted(m0),
             sqrt(abs(rs45))), col = 2)

# 046_ordine.R
# Esempio simulato: errori correlati.
set.seed(746)
e46 <- as.numeric(arima.sim(
  model = list(ar = 0.75), n = 80))
plot(e46, type = "b",
     xlab = "Ordine temporale",
     ylab = "Errore simulato")
abline(h = 0, lty = 2)
acf(e46, main = "Autocorrelazione")

# 048_qqplot.R
# Quantili dei residui standardizzati.
rs48 <- rstandard(m0)
qqnorm(rs48, pch = 19,
       xlab = "Quantile normale",
       ylab = "Residuo standardizzato")
qqline(rs48, col = 2)

# 049_leva.R
# La leva dipende dalla matrice X.
h49 <- hatvalues(m0)
plot(f$diametro_tot_um, h49,
     pch = 19, xlab = "Diametro (um)",
     ylab = "Leva")
c(somma = sum(h49),
  parametri = m0$rank)

# 051_cook.R
# Una misura del cambiamento globale.
D51 <- cooks.distance(m0)
plot(D51, type = "h",
     xlab = "Indice del fossile",
     ylab = "Distanza di Cook")
j51 <- which.max(D51)
f[j51, c("id", "morfotipo")]

# 052_sensibilita.R
# Confronto, senza modificare f.
j52 <- which.max(cooks.distance(m0))
m_sens <- update(m0, data = f[-j52, ])
rbind(completo = coef(m0),
      senza_caso = coef(m_sens))
# Conserviamo l'identita' del caso.
f[j52, ]

# 053_errore_misura.R
# Esempio classico, tutto simulato.
set.seed(753)
x53 <- rnorm(1000)
y53 <- 2 + 1.5*x53 + rnorm(1000)
w53 <- x53 + rnorm(1000, sd = 0.8)
c(latente = coef(lm(y53 ~ x53))[2],
  misurato = coef(lm(y53 ~ w53))[2])
# Pendenza limite attesa:
1.5 / (1 + 0.8^2)

# 054_loglog.R
# I logaritmi richiedono valori > 0.
stopifnot(all(f$diametro_int_um > 0),
          all(f$diametro_tot_um > 0))
m_loglog <- lm(log(diametro_int_um) ~
  log(diametro_tot_um), data = f)
coef(m_loglog)
plot(m_loglog, which = 1)

# 055_ritrasformazione.R
# Profilo dentro il dominio osservato.
nuovo55 <- data.frame(
  diametro_tot_um = 7)
eta55 <- predict(m_loglog, nuovo55)
mediana55 <- exp(eta55)
# Media con errori log-normali omogenei.
media55 <- exp(eta55 +
  sigma(m_loglog)^2 / 2)
c(mediana = mediana55, media = media55)

# 056_multiplo.R
# Un predittore quantitativo e un gruppo.
m_add <- lm(diametro_int_um ~
  diametro_tot_um + morfotipo,
  data = f)
coef(m_add)
summary(m_add)$sigma

# 058_riferimento.R
# Scegliamo il gruppo di riferimento.
f$morfotipo <- relevel(
  factor(f$morfotipo), ref = "Rounded")
levels(f$morfotipo)
contrasts(f$morfotipo)
# La scelta entra nella parametrizzazione.
m_add <- lm(diametro_int_um ~
  diametro_tot_um + morfotipo, data = f)

# 059_matrice.R
# Colonne usate realmente dal modello.
X59 <- model.matrix(m_add)
colnames(X59)
head(X59, 6)
# La colonna iniziale vale sempre 1.
stopifnot(all(X59[, 1] == 1))

# 060_additivo.R
# Contrasto a diametro totale fissato.
nuovi60 <- data.frame(
  diametro_tot_um = c(7, 7),
  morfotipo = c("Rounded", "Spiky"))
mu60 <- predict(m_add, nuovi60)
diff(mu60)
# Coincide con il coefficiente di gruppo.
coef(m_add)["morfotipoSpiky"]

# 061_interazione.R
# * include effetti principali e prodotto.
m_int <- lm(diametro_int_um ~
  diametro_tot_um * morfotipo,
  data = f)
coef(m_int)
# Le colonne rendono visibile il prodotto.
colnames(model.matrix(m_int))

# 062_contrasto.R
# Confrontiamo tre diametri scelti.
x62 <- c(6, 7, 8)
a62 <- data.frame(diametro_tot_um = x62,
                   morfotipo = "Rounded")
b62 <- a62; b62$morfotipo <- "Spiky"
delta62 <- predict(m_int, b62) -
           predict(m_int, a62)
data.frame(diametro = x62, delta = delta62)

# 063_centrare.R
# Il valore 7 um ha significato nel dominio.
f$x_c <- f$diametro_tot_um - 7
m_c <- lm(diametro_int_um ~
  x_c * morfotipo, data = f)
coef(m_c)
# Le previsioni restano uguali.
max(abs(fitted(m_c) - fitted(m_int)))

# 064_intervallo_contrasto.R
# m_c e' centrato a 7 um.
j64 <- match("morfotipoSpiky",
             names(coef(m_c)))
d64 <- coef(m_c)[j64]
se64 <- sqrt(vcov(m_c)[j64, j64])
t64 <- qt(0.975, df.residual(m_c))
c(stima = d64,
  basso = d64 - t64*se64,
  alto = d64 + t64*se64)

# 065_profilo.R
# Stessi nomi e livelli del modello.
nuovi65 <- data.frame(
  diametro_tot_um = c(6.5, 7.5),
  morfotipo = c("Rounded", "Spiky"))
predict(m_int, newdata = nuovi65,
        interval = "confidence")
# Nuovi individui: intervallo piu' ampio.
predict(m_int, newdata = nuovi65,
        interval = "prediction")

# 067_identita.R
# Identita' delle misure sintetiche.
scarto67 <- with(f, diametro_tot_um -
  diametro_int_um - 2*spessore_um)
max(abs(scarto67))
# Anche l'arrotondamento conta.
summary(scarto67)

# 068_rango.R
# Esempio con dipendenza esatta costruita.
x68 <- f$diametro_tot_um
s68 <- f$spessore_um
z68 <- x68 - 2*s68
X68 <- cbind(1, x68, z68, s68)
c(colonne = ncol(X68),
  rango = qr(X68)$rank)

# 069_modelli.R
# Formule motivate da ipotesi diverse.
formule69 <- list(
  comune = diametro_int_um ~
    diametro_tot_um,
  additivo = diametro_int_um ~
    diametro_tot_um + morfotipo,
  interazione = diametro_int_um ~
    diametro_tot_um * morfotipo)
# La valutazione seguira' un protocollo.
names(formule69)

# 071_risposta_binaria.R
# 1 indica Spiky, 0 indica Rounded.
f$spiky <- as.integer(
  f$morfotipo == "Spiky")
table(f$morfotipo, f$spiky)
stopifnot(all(f$spiky %in% c(0, 1)))

# 072_odds.R
# Tre scale per la stessa probabilita'.
p72 <- c(0.2, 0.5, 0.8)
data.frame(
  probabilita = p72,
  odds = p72 / (1 - p72),
  logit = qlogis(p72))
# La funzione inversa recupera p.
plogis(qlogis(p72))

# 073_curva_logistica.R
# Curva teorica: eta varia da -4 a 4.
eta73 <- seq(-4, 4, length.out = 101)
plot(eta73, plogis(eta73), type = "l",
     xlab = "Predittore lineare eta",
     ylab = "Probabilita'", ylim = c(0, 1))
abline(h = 0.5, v = 0, lty = 2)

# 074_glm.R
# Stima descrittiva sul campione.
m_log <- glm(spiky ~ diametro_tot_um,
  data = f, family = binomial())
summary(m_log)$coefficients
m_log$converged
# Probabilita' nella scala 0--1.
p_log <- predict(m_log,
                 type = "response")
range(p_log)

# 075_odds_ratio.R
# Effetto di +1 um sul rapporto degli odds.
b75 <- coef(m_log)["diametro_tot_um"]
c(per_1_um = exp(b75),
  per_0_5_um = exp(0.5*b75))
# Cambiare l'unita' cambia l'incremento.

# 076_effetto_probabilita.R
# Probabilita' per profili espliciti.
nuovi76 <- data.frame(
  diametro_tot_um = c(6, 7, 8))
p76 <- predict(m_log, nuovi76,
               type = "response")
data.frame(nuovi76, probabilita = p76)
# Differenze per incrementi di 1 um.
diff(p76)

# 077_soglia.R
# Probabilita' descrittive gia' calcolate.
soglia77 <- 0.5
classe77 <- as.integer(p_log >= soglia77)
head(data.frame(
  probabilita = p_log,
  classe = classe77,
  osservato = f$spiky))

# 078_classificazione.R
# Livelli espliciti anche se un conteggio e' 0.
tab78 <- table(
  osservato = factor(f$spiky, levels = 0:1),
  previsto = factor(classe77, levels = 0:1))
tab78
sum(diag(tab78)) / sum(tab78)

# 079_sensibilita_specificita.R
# tab78: righe osservate, colonne previste.
TP79 <- tab78["1", "1"]
FN79 <- tab78["1", "0"]
TN79 <- tab78["0", "0"]
FP79 <- tab78["0", "1"]
c(sensibilita = TP79/(TP79+FN79),
  specificita = TN79/(TN79+FP79))

# 080_brier.R
# Valutazione descrittiva sul campione.
brier80 <- mean((p_log - f$spiky)^2)
# Riferimento costante: frequenza osservata.
pbase80 <- mean(f$spiky)
base80 <- mean((pbase80 - f$spiky)^2)
c(modello = brier80, riferimento = base80)

# 081_calibrazione.R
# Intervalli fissi di probabilita'.
d81 <- data.frame(
  bin = cut(p_log, breaks = seq(0, 1, 0.2),
            include.lowest = TRUE),
  p = p_log, y = f$spiky)
aggregate(cbind(p, y) ~ bin,
          data = d81, FUN = mean)
table(d81$bin)

# 083_split.R
# Regola fissata prima della selezione.
is_test <- seq_len(nrow(f)) %% 5L == 0L
training <- f[!is_test, ]
test <- f[is_test, ]
c(training = nrow(training),
  test = nrow(test))
stopifnot(length(intersect(training$id,
                         test$id)) == 0L)

# 084_riferimento.R
# Il riferimento usa solo il training.
media_train <- mean(
  training$diametro_int_um)
prev_base <- rep(media_train,
                 nrow(test))
media_train

# 085_metriche.R
metriche <- function(osservato, previsto) {
  e <- osservato - previsto
  c(MAE = mean(abs(e)),
    RMSE = sqrt(mean(e^2)))
}
# Esempio con scarti noti.
metriche(c(0, 0, 0), c(1, 1, 4))

# 086_fold.R
# Cinque parti interne al solo training.
set.seed(714)
fold <- sample(rep(1:5,
  length.out = nrow(training)))
table(fold)
# Il test esterno non compare nei fold.

# 087_trasformazioni.R
# Parametri appresi soltanto nel training.
mu_x <- mean(training$diametro_tot_um)
sd_x <- sd(training$diametro_tot_um)
z_train <- (training$diametro_tot_um - mu_x) / sd_x
z_test <- (test$diametro_tot_um - mu_x) / sd_x
# Nei fold, mu_x e sd_x si ristimano
# ogni volta sui quattro fold di stima.

# 089_cv.R
# Formule definite nel progetto.
formule <- formule_annula()
# Stessi fold per tutti i modelli.
cv <- valida_annula(training, fold,
                   formule)
cv[order(cv$RMSE), ]
scelta <- cv$modello[
  which.min(cv$RMSE)]

# 090_test_finale.R
# Ristima sui 128 casi di training.
mod_finale <- lm(formule[[scelta]],
                 data = training)
prev_test <- predict(mod_finale, newdata = test)
metriche(test$diametro_int_um, prev_test)
metriche(test$diametro_int_um, prev_base)

# 092_simulazione.R
# Nuovi dati dalla stessa legge.
set.seed(17)
sim <- data.frame(
  x = seq(-1, 1, length.out = 24))
sim$y <- sin(3 * sim$x) + rnorm(24)
mp <- lm(y ~ poly(x, 3, raw = TRUE),
         data = sim)
nuovi <- data.frame(
  x = seq(-1, 1, length.out = 150))
nuovi$y <- sin(3 * nuovi$x) + rnorm(150)
metriche(nuovi$y,
  predict(mp, newdata = nuovi))

# 097_logistica_test.R
# Risposta: TRUE per i fossili Spiky.
g_train <- glm(
  I(morfotipo == "Spiky") ~
    diametro_tot_um +
    rapporto_int_tot,
  data = training,
  family = binomial())
p_test <- predict(g_train,
  newdata = test, type = "response")
y_test <- as.integer(
  test$morfotipo == "Spiky")
mean((p_test - y_test)^2) # Brier.
mean((p_test >= 0.5) == y_test)

dev.off()
