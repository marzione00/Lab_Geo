# Aurea - Probabilita, variabilita e simulazione
# Eseguire dalla cartella di Aurea_M04.Rproj.
# Per mostrare il codice: source("Lezione_Aurea.R", echo = TRUE)
source("setup.R", encoding = "UTF-8")
dir.create("Risultati", showWarnings = FALSE)
pdf("Risultati/Figure_lezione.pdf", width = 9, height = 5.5)


# ======================================================
# 03_avvio.R
# ======================================================
# Aprire Aurea_M04.Rproj.
source("setup.R", encoding = "UTF-8")
# Parametri del caso fisico finale
parametri_densita
# Guida alle distribuzioni in R
help("Distributions")


# ======================================================
# 05_eventi.R
# ======================================================
# Un prelievo uniforme fra 6 provini
m05 <- c(104,106,108,110,112,114)
tipo05 <- c("F","M","F","M","F","M")
A05 <- m05 >= 110   # massa in g
B05 <- tipo05 == "M"
mean(A05)           # P(A) = 3/6
which(A05)          # provini 4,5,6


# ======================================================
# 06_operazioni.R
# ======================================================
# A: massa >=110 g; B: tipo M
mean(A05 & B05)  # entrambi: 2/6
mean(A05 | B05)  # almeno uno: 4/6
mean(!A05)       # complemento: 3/6
# Controllo della formula dell'unione
mean(A05) + mean(B05) -
  mean(A05 & B05)


# ======================================================
# 07_frequenza.R
# ======================================================
set.seed(17)  # sequenza riproducibile
x07 <- rbinom(200, 1, prob = .3)
k07 <- seq_along(x07)
f07 <- cumsum(x07) / k07
plot(k07, f07, type = "l",
  ylim = c(0, 1), xlab = "Prove",
  ylab = "Frequenza cumulativa")
abline(h = .3, lty = 2)


# ======================================================
# 08_atteso.R
# ======================================================
# Modello costruito per un conteggio
k08 <- 0:2
p08 <- c(.2, .5, .3)
sum(p08)           # normalizzazione
sum(k08 * p08)     # E(K) = 1.1
set.seed(17)
x08 <- sample(k08, 1000,
  replace = TRUE, prob = p08)
mean(x08)          # media simulata


# ======================================================
# 09_lab_eventi.R
# ======================================================
a09 <- lab_eventi(prob=.3, n=200)
b09 <- lab_eventi(prob=.3, n=800)
a09$indicatori
b09$indicatori
# Cambia la sequenza, lascia fisso p
c09 <- lab_eventi(prob=.3,
  n=800, seed=21)
c09$indicatori


# ======================================================
# 10_condizionata.R
# ======================================================
# Numeri attesi per 100 casi
t10 <- matrix(c(32,12,8,48), nrow=2,
  dimnames=list(c("B","nonB"),
                c("A","nonA")))
t10
t10["B","A"] / sum(t10["B",])
# Fra tutti i casi: P(A)=44/100
sum(t10[,"A"]) / sum(t10)


# ======================================================
# 11_totale.R
# ======================================================
prior11 <- .4    # P(B)
pa11 <- .8       # P(A dato B)
pb11 <- .2       # P(A dato nonB)
joint11 <- c(prior11 * pa11,
  (1-prior11) * pb11)
joint11         # .32 e .12
sum(joint11)    # P(A) = .44


# ======================================================
# 12_indipendenza.R
# ======================================================
# Esempio indipendente
pA12 <- .4; pB12 <- .5
pAB12 <- .2
pAB12 / pB12       # .4 = P(A)
isTRUE(all.equal(pAB12, pA12*pB12))
# Incompatibili: P(A e B)=0
0 == pA12*pB12     # FALSE


# ======================================================
# 13_bayes.R
# ======================================================
prior13 <- .4
pa13 <- .8; pb13 <- .2
pA13 <- pa13*prior13 +
  pb13*(1-prior13)
post13 <- pa13*prior13 / pA13
c(P_A = pA13, P_B_dato_A = post13)
# .44 e circa .72727


# ======================================================
# 14_prevalenza.R
# ======================================================
prior14 <- c(.1, .4, .8)
pa14 <- .8; pb14 <- .2
pA14 <- pa14*prior14 +
  pb14*(1-prior14)
post14 <- pa14*prior14/pA14
data.frame(prior14, post14)


# ======================================================
# 15_mille_casi.R
# ======================================================
# Nuovo esempio: tipo T e segnale S
N15 <- 1000
nT15 <- N15 * .10
segnali15 <- c(T = nT15*.90,
  altri = (N15-nT15)*.05)
segnali15           # 90 e 45
segnali15["T"] / sum(segnali15)
# Due terzi dei segnali attesi


# ======================================================
# 16_lab_condizionamento.R
# ======================================================
a16 <- lab_condizionamento(
  prior=.4, pa=.8, pb=.2)
b16 <- lab_condizionamento(
  prior=.1, pa=.8, pb=.2)
a16$indicatori
b16$indicatori
# Uguale probabilita' nei due gruppi
c16 <- lab_condizionamento(
  prior=.4, pa=.2, pb=.2)
c16$indicatori


# ======================================================
# 17_dominio.R
# ======================================================
# Formula esplicita e denominatore
bayes17 <- function(prior, pa, pb) {
  pA <- pa*prior + pb*(1-prior)
  if (pA == 0) return(NA_real_)
  pa*prior/pA
}
bayes17(.4, .8, .2)
bayes17(.4, 0, 0)  # condizione nulla


# ======================================================
# 18_variabile.R
# ======================================================
# Due prove indipendenti, p=.3
esiti18 <- c("00","01","10","11")
x18 <- c(0, 1, 1, 2)  # successi
p18 <- c(.49, .21, .21, .09)
# Somma i pesi per lo stesso X
tapply(p18, x18, sum)


# ======================================================
# 19_massa.R
# ======================================================
k19 <- 0:2
p19 <- c(.49, .42, .09)
sum(p19)             # 1
sum(p19[k19 >= 1])    # .51
sum(k19 * p19)        # atteso .6
barplot(p19, names.arg=k19,
  xlab="Successi", ylab="Probabilita'")


# ======================================================
# 20_densita.R
# ======================================================
# Modello uniforme fra 0 e 2
dunif(.75, min=0, max=2)   # .5
# Probabilita' tra .5 e 1
punif(1, 0, 2) - punif(.5, 0, 2)
# .25: altezza .5 per larghezza .5


# ======================================================
# 21_altezza.R
# ======================================================
# X uniforme [0, .2], adimensionale
dunif(.1, 0, .2)        # densita' 5
punif(.15, 0, .2) -
  punif(.05, 0, .2)     # area .5
# Il punto singolo ha area zero
punif(.1, 0, .2) - punif(.1, 0, .2)


# ======================================================
# 22_cumulativa.R
# ======================================================
k22 <- 0:2
p22 <- c(.49, .42, .09)
cumsum(p22)           # .49,.91,1
# Caso continuo: uniforme [0,2]
punif(c(0,.5,1,2), 0, 2)
# .00, .25, .50, 1.00


# ======================================================
# 23_momenti.R
# ======================================================
k23 <- 0:2
p23 <- c(.49, .42, .09)
mu23 <- sum(k23*p23)
v23 <- sum((k23-mu23)^2*p23)
c(media=mu23, varianza=v23,
  sd=sqrt(v23))
# .6, .42, circa .6481


# ======================================================
# 24_quantile.R
# ======================================================
# Uniforme [0,2]: F(q)=.75
qunif(.75, min=0, max=2)  # 1.5
# Caso discreto delle pagine 18-23
k24 <- 0:2
F24 <- cumsum(c(.49,.42,.09))
k24[which(F24 >= .75)[1]] # 1
# F(1)=.91: il salto supera .75


# ======================================================
# 25_lab_distribuzione.R
# ======================================================
a25 <- lab_distribuzione(cut=1)
a25$indicatori
# Probabilita' esatte della normale
pnorm(1)              # circa .8413
pnorm(1, lower.tail=FALSE)
b25 <- lab_distribuzione(cut=0)
b25$indicatori        # .5 e .5


# ======================================================
# 26_bernoulli.R
# ======================================================
# Una prova: evento presente = 1
set.seed(17)
x26 <- rbinom(12, size = 1,
             prob = .3)
x26
mean(x26)  # Frequenza osservata
# Media e varianza del modello
c(media = .3, varianza = .3*.7)


# ======================================================
# 27_somma_prove.R
# ======================================================
# Una sequenza costruita di 20 prove
x27 <- c(1,0,0,1,0, 0,1,0,0,0,
         1,0,0,0,1, 0,0,1,0,0)
length(x27)  # Numero di prove n
sum(x27)     # Numero di successi K
mean(x27)    # Proporzione K/n


# ======================================================
# 28_probabilita_binomiale.R
# ======================================================
# Esattamente 2 successi su 3
p28 <- .3
choose(3, 2) * p28^2 * (1-p28)
dbinom(2, size = 3, prob = p28)
# Esattamente 8 su 20
dbinom(8, size = 20, prob = .3)


# ======================================================
# 29_centro_dispersione.R
# ======================================================
# Parametri del modello
n29 <- 20
p29 <- .3
c(media = n29*p29,
  varianza = n29*p29*(1-p29))
k29 <- 0:n29
sum(k29 * dbinom(k29, n29, p29))
sqrt(n29*p29*(1-p29))  # SD


# ======================================================
# 30_coda_binomiale.R
# ======================================================
# Almeno 8: sommare k = 8,...,20
sum(dbinom(8:20, 20, .3))
# lower.tail=FALSE calcola P(K>q)
pbinom(7, size = 20, prob = .3,
       lower.tail = FALSE)
# P(K=8) e' una sola probabilita
dbinom(8, 20, .3)


# ======================================================
# 31_quattro_funzioni.R
# ======================================================
# d: probabilita del valore
dbinom(8, 20, .3)
# p: probabilita cumulata
pbinom(8, 20, .3)
# q: primo k con F(k) >= .95
qbinom(.95, 20, .3)
# r: cinque conteggi simulati
set.seed(17)
rbinom(5, size = 20, prob = .3)


# ======================================================
# 32_teoria_simulazione.R
# ======================================================
# 400 repliche, 20 prove ciascuna
set.seed(17)
s32 <- rbinom(400, size=20, prob=.3)
f32 <- tabulate(s32+1, nbins=21)/400
plot(0:20, dbinom(0:20,20,.3),
     type="h", xlab="k", ylab="P")
points(0:20, f32, col="orange",pch=16)
mean(s32)  # 5.9375; teoria: 6


# ======================================================
# 33_lab_binomiale.R
# ======================================================
# Esperimento m04-binomiale
a33 <- lab_binomiale(n=20, prob=.3)
b33 <- lab_binomiale(n=40, prob=.3)
a33$indicatori
b33$indicatori
# Il sito usa 400 repliche
length(a33$simulazioni)


# ======================================================
# 34_tasso_esposizione.R
# ======================================================
# Esempio: fratture lungo una linea
rate34 <- 2  # Eventi per metro
L34 <- 3     # Metri osservati
mu34 <- rate34 * L34
mu34         # Conteggio atteso: 6
dpois(0, lambda = mu34)


# ======================================================
# 35_poisson_distribuzione.R
# ======================================================
# Media del conteggio: 6
k35 <- 0:qpois(.999, lambda=6)
pr35 <- dpois(k35, lambda=6)
sum(pr35)  # Quasi 1: coda esclusa
c(media=6, varianza=6, sd=sqrt(6))


# ======================================================
# 36_esposizioni.R
# ======================================================
# Stesso tasso: esposizione doppia
L36 <- c(3, 6)
mu36 <- 2 * L36
data.frame(esposizione=L36,
           media=mu36,
           sd=sqrt(mu36),
           cv=1/sqrt(mu36))


# ======================================================
# 37_coda_poisson.R
# ======================================================
# Almeno 10 eventi, media 6
ppois(9, lambda=6,
      lower.tail=FALSE)
# Primo conteggio con cumulata >= .95
qpois(.95, lambda=6)
ppois(10, lambda=6)


# ======================================================
# 38_eventi_rari.R
# ======================================================
# Molte prove, p piccolo: n*p=6
k38 <- 0:25
b38 <- dbinom(k38, 200, .03)
p38 <- dpois(k38, 6)
max(abs(b38-p38))
c(var_bin=200*.03*.97, var_pois=6)


# ======================================================
# 39_somma_poisson.R
# ======================================================
# Due conteggi indipendenti
set.seed(17)
a39 <- rpois(10000, lambda=2)
b39 <- rpois(10000, lambda=4)
s39 <- a39 + b39
c(media=mean(s39), varianza=var(s39))
# La distribuzione esatta e' Pois(6)


# ======================================================
# 40_eterogeneita.R
# ======================================================
# Due regimi con uguale probabilita
set.seed(17)
mu40 <- sample(c(2,10), 10000,
               replace=TRUE)
k40 <- rpois(10000, lambda=mu40)
c(media=mean(k40), varianza=var(k40))
# Teoria: media 6, varianza 6+16=22


# ======================================================
# 41_lab_poisson.R
# ======================================================
# Stessa media, tassi differenti
a41 <- lab_poisson(rate=2,
                  exposure=3)
b41 <- lab_poisson(rate=1,
                  exposure=6)
a41$indicatori
b41$indicatori
all.equal(a41$dati, b41$dati)


# ======================================================
# 42_normale.R
# ======================================================
# Modello continuo: media 10, SD 2
x42 <- seq(2, 18, length.out=201)
d42 <- dnorm(x42, mean=10, sd=2)
plot(x42, d42, type="l",
     xlab="x", ylab="Densita")
# dnorm restituisce una densita
dnorm(10, mean=10, sd=2)


# ======================================================
# 43_posizione_scala.R
# ======================================================
# Stessa variabile, tre modelli
x43 <- seq(2, 20, length.out=201)
a43 <- dnorm(x43, 10, 1)
b43 <- dnorm(x43, 10, 2)
c43 <- dnorm(x43, 14, 2)
matplot(x43, cbind(a43,b43,c43),
        type="l", lty=1,
        xlab="x", ylab="Densita")


# ======================================================
# 44_standardizzare.R
# ======================================================
# Valore 14 nel modello N(10, 2^2)
z44 <- (14 - 10) / 2
z44  # Due deviazioni sopra la media
pnorm(14, mean=10, sd=2)
pnorm(z44)  # Stessa probabilita


# ======================================================
# 45_probabilita_intervallo.R
# ======================================================
# Probabilita fra 8 e 12
pnorm(12, mean=10, sd=2) -
  pnorm(8, mean=10, sd=2)
# Stesso intervallo: -1 < Z < 1
pnorm(1) - pnorm(-1)


# ======================================================
# 46_quantile_normale.R
# ======================================================
# Soglia con il 95% a sinistra
q46 <- qnorm(.95, mean=10, sd=2)
q46  # 13.28971
qnorm(.95)  # 1.644854
pnorm(q46, mean=10, sd=2)


# ======================================================
# 47_intervallo_centrale.R
# ======================================================
# Due code del 2.5% ciascuna
i47 <- qnorm(c(.025,.975), 10, 2)
i47  # 6.080072, 13.919928
diff(pnorm(i47, mean=10, sd=2))
# Quantile unilaterale: altra soglia
qnorm(.95, mean=10, sd=2)


# ======================================================
# 48_limite_normale.R
# ======================================================
# Concentrazione [mg/L], modello
# normale con media 1 e SD 0.8
pnorm(0, mean=1, sd=.8)
# Probabilita negativa: circa 10.6%
# Con media 10 e SD 2 e' molto minore
pnorm(0, mean=10, sd=2)


# ======================================================
# 49_lab_normale.R
# ======================================================
# Stesso livello, scale differenti
a49 <- lab_normale(mu=10, sd=2,
                  q=.95)
b49 <- lab_normale(mu=20, sd=4,
                  q=.95)
a49$indicatori
b49$indicatori


# ======================================================
# 50_prodotti.R
# ======================================================
# Fattori positivi adimensionali
f50 <- c(1.2, .8, 1.1)
prod(f50)       # Prodotto: 1.056
exp(sum(log(f50)))
# Stesso risultato entro precisione
all.equal(log(prod(f50)),
          sum(log(f50)))


# ======================================================
# 51_lognormale.R
# ======================================================
# X adimensionale, 500 estrazioni
set.seed(17)
x51 <- rlnorm(500, 0, .6)
range(x51)
hist(log(x51), probability = TRUE,
     main = "Logaritmo di X",
     xlab = "log(X)", col = "#E0ECEA")
curve(dnorm(x, 0, .6), add = TRUE,
      col = "#087C74", lwd = 2)


# ======================================================
# 52_media_mediana.R
# ======================================================
set.seed(17)
x52 <- rlnorm(500, 0, .6)
c(mediana_teoria = 1,
  mediana_sim = median(x52),
  media_teoria = exp(.6^2/2),
  media_sim = mean(x52))


# ======================================================
# 53_cv.R
# ======================================================
# X lognormale: formula esatta
s53 <- c(.1, .3, .6)
cv53 <- sqrt(expm1(s53^2))
data.frame(sdlog = s53, CV = cv53,
           percento = 100*cv53)


# ======================================================
# 54_miscela.R
# ======================================================
# Due popolazioni adimensionali
set.seed(17)
g54 <- rbinom(500, 1, .65)
mu54 <- ifelse(g54 == 1, 2, 6)
sd54 <- ifelse(g54 == 1, .7, 1)
x54 <- rnorm(500, mu54, sd54)
hist(x54, probability = TRUE,
     main = "Miscela di due gruppi",
     xlab = "X", col = "#E0ECEA")


# ======================================================
# 55_supporto_modello.R
# ======================================================
# Esempio adimensionale costruito
pnorm(0, mean = 1, sd = .6)
# Probabilita' circa 0.048
plnorm(0, meanlog = 0, sdlog = .6)
# Qui P(X <= 0) = 0


# ======================================================
# 56_lab_lognormale.R
# ======================================================
# Due esperimenti, ciascuno con B=500
a56 <- lab_moltiplicazione(
  sdlog = .3, seed = 17)
b56 <- lab_moltiplicazione(
  sdlog = .8, seed = 17)
a56$indicatori
b56$indicatori


# ======================================================
# 57_monte_carlo.R
# ======================================================
# E[X^2] per X normale standard
set.seed(17)
B57 <- 5000
x57 <- rnorm(B57)
y57 <- x57^2
c(stima = mean(y57), teoria = 1)


# ======================================================
# 58_replica_completa.R
# ======================================================
set.seed(17)
B58 <- 10000
k58 <- rbinom(B58, 20, .3)
i58 <- k58 >= 8
c(stima = mean(i58),
  esatta = pbinom(7, 20, .3,
    lower.tail = FALSE))


# ======================================================
# 59_errore_mc.R
# ======================================================
# p e' noto in questo esempio
B59 <- c(200, 800, 3200)
p59 <- .1
se59 <- sqrt(p59*(1-p59)/B59)
data.frame(B = B59, SE_MC = se59)


# ======================================================
# 60_convergenza.R
# ======================================================
set.seed(17)
B60 <- 2000
i60 <- rbinom(B60, 1, .1)
b60 <- seq_len(B60)
p60 <- cumsum(i60)/b60
plot(b60, p60, type = "l",
     xlab = "Repliche B",
     ylab = "Frequenza cumulativa")
abline(h = .1, col = "#C57E42")


# ======================================================
# 61_numero_repliche.R
# ======================================================
# Obiettivo: SE_MC <= 0.01
eps61 <- .01; p61 <- .1
B61 <- ceiling((p61/eps61) *
               ((1-p61)/eps61))
Bmax61 <- ceiling(1/(4*eps61^2))
c(con_p_noto = B61,
  limite_generale = Bmax61)


# ======================================================
# 62_seme.R
# ======================================================
set.seed(17)
a62 <- rnorm(5)
set.seed(17)
b62 <- rnorm(5)
identical(a62, b62)
RNGkind()
R.version.string


# ======================================================
# 63_due_errori.R
# ======================================================
set.seed(17)
B63 <- 2000
y63 <- rlnorm(B63, 0, .6)
s63 <- sd(y63)
c(SD_uscita = s63,
  SE_media_MC = s63/sqrt(B63))


# ======================================================
# 64_bias.R
# ======================================================
# V fissato; scostamento di 2 g noto
set.seed(17)
m64 <- rnorm(20000, 108, 1)
d64 <- m64/40
dc64 <- (m64-2)/40
c(senza_correzione = mean(d64),
  con_correzione = mean(dc64))


# ======================================================
# 65_lab_mc.R
# ======================================================
a65 <- lab_monte_carlo(
  B = 200, prob = .1, seed = 17)
b65 <- lab_monte_carlo(
  B = 800, prob = .1, seed = 17)
a65$indicatori
b65$indicatori
a65$indicatori["se_mc_teorico"] /
  b65$indicatori["se_mc_teorico"]


# ======================================================
# 66_densita.R
# ======================================================
# Unita': g, cm^3 e g/cm^3
m0 <- 106
V0 <- 40
um <- 1
uV <- .6
d0 <- m0/V0
c(densita = d0, CV_m = um/m0,
  CV_V = uV/V0)


# ======================================================
# 67_rpos.R
# ======================================================
# mu e s: media e SD originali
rpos <- function(n, mu, s) {
  v <- log1p((s/mu)^2)
  rlnorm(n, log(mu)-v/2, sqrt(v))
}
set.seed(17)
head(rpos(6, mu = 106, s = 1))


# ======================================================
# 68_simula_densita.R
# ======================================================
# Ingressi indipendenti, positivi
set.seed(17)
B68 <- 20000
m68 <- rpos(B68, 106, 1)
v68 <- rpos(B68, 40, .6)
d68 <- m68/v68
c(media = mean(d68), SD = sd(d68))
quantile(d68, c(.025, .975))


# ======================================================
# 69_sensibilita.R
# ======================================================
m0 <- 106; V0 <- 40
cm69 <- 1/V0
cV69 <- -m0/V0^2
c(sensibilita_massa = cm69,
  sensibilita_volume = cV69)
# Effetto di +1 g e di +0.6 cm^3
c(cm69*1, cV69*.6)


# ======================================================
# 70_contributi.R
# ======================================================
# Contributi in (g/cm^3)^2
q70 <- c(massa = (1/40)^2,
         volume = (106*.6/40^2)^2)
u70 <- sqrt(sum(q70))
c(SD_approssimata = u70)
100*q70/sum(q70)


# ======================================================
# 71_covarianza.R
# ======================================================
# c: correlazione sulla scala fisica
c71 <- c(-.7, 0, .7)
a71 <- 1/106
b71 <- .6/40
u71 <- 2.65*sqrt(a71^2+b71^2 -
                 2*c71*a71*b71)
data.frame(c = c71, SD = u71)


# ======================================================
# 72_ingressi_correlati.R
# ======================================================
set.seed(17)
s72 <- .1; c72 <- .7
z72 <- matrix(rnorm(4000), ncol = 2)
u72 <- z72[, 1]
v72 <- c72*u72 +
  sqrt(1-c72^2)*z72[, 2]
x72 <- exp(log(10)+s72*u72)
y72 <- exp(log(5)+s72*v72)
r72 <- x72/y72
sd(r72)


# ======================================================
# 73_rapporto_esatto.R
# ======================================================
s73 <- .1; c73 <- .7
t273 <- 2*s73^2*(1-c73)
c(mediana = 2,
  media = 2*exp(t273/2),
  SD = 2*sqrt(expm1(t273) *
                 exp(t273)))


# ======================================================
# 74_scale_parametri.R
# ======================================================
s74 <- .3; cl74 <- .7
CV74 <- sqrt(expm1(s74^2))
c74 <- expm1(cl74*s74^2) /
       expm1(s74^2)
c(SD_log = s74, CV_originale = CV74,
  cor_log = cl74, cor_originale = c74)


# ======================================================
# 75_confronto_approssimazione.R
# ======================================================
# Correlazione dei log uguale a 0
s75 <- c(.02, .1, .2, .3)
t275 <- 2*s75^2
a75 <- 2*sqrt(t275)
e75 <- 2*sqrt(expm1(t275)*exp(t275))
data.frame(sdlog = s75,
  approssimata = a75, esatta = e75,
  scarto_percento = 100*(e75-a75)/e75)


# ======================================================
# 76_lab_propagazione.R
# ======================================================
a76 <- lab_propagazione(
  rho = 0, cv = .1, seed = 17)
b76 <- lab_propagazione(
  rho = .7, cv = .1, seed = 17)
c76 <- lab_propagazione(
  rho = 0, cv = .3, seed = 17)
rbind(A = a76$indicatori,
      B = b76$indicatori,
      C = c76$indicatori)


# ======================================================
# 78_strumenti.R
# ======================================================
# Densita': 106 g / 40 cm^3
u78 <- function(um, uV) {
  2.65*sqrt((um/106)^2+(uV/40)^2)
}
u78(1, .6)    # situazione iniziale
u78(.5, .6)   # migliora la massa
u78(1, .3)    # migliora il volume
# Incertezze in g/cm^3; c=0


# ======================================================
# 80_consegna.R
# ======================================================
# Caso fisico: input indipendenti
set.seed(17)
B80 <- 20000
m80 <- rpos(B80, 106, 1)
v80 <- rpos(B80, 40, .6)
d80 <- m80/v80
dir.create("Risultati",
           showWarnings=FALSE)
write.csv(data.frame(densita=d80),
  "Risultati/densita.csv",
  row.names=FALSE)


# Chiudere il documento delle figure.
dev.off()
