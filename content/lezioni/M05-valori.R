# Pelago M05 · valori citati nelle spiegazioni estese delle tappe.
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

# Dati e funzioni del progetto per le tappe successive.
source("setup.R", encoding = "UTF-8")
sk <- function(x) mean((x-mean(x))^3)/sd(x)^3

# ---- tappe 3-15
v("3 fossili righe colonne", dim(fossili)); v("3 provini righe colonne", dim(provini))
v("3 morfotipi", names(table(fossili$morfotipo))); v("3 morfotipi n", as.integer(table(fossili$morfotipo)))
v("3 affioramenti", length(unique(provini$affioramento))); v("3 stazioni", length(unique(provini$stazione)))
v("3 densita min max", range(provini$densita))
U04 <- data.frame(id=1:12, valore=seq(2.1,3.2,by=.1)); set.seed(17); i04 <- sample(U04$id, 4)
v("4 ids", i04); v("4 media campione", mean(U04$valore[i04])); v("4 media pop", mean(U04$valore)); v("4 campioni possibili", choose(12,4))
d05 <- data.frame(stazione=rep(c("A","B","C"),each=4), misura=c(2.3,2.4,2.5,2.4,2.6,2.7,2.6,2.5,2.8,2.9,2.7,2.8))
v("5 medie stazioni", tapply(d05$misura, d05$stazione, mean)); v("5 sd entro", tapply(d05$misura, d05$stazione, sd)); v("5 sd medie", sd(tapply(d05$misura, d05$stazione, mean)))
set.seed(17); x06 <- rnorm(6, 10, 2); v("6 x06", x06); v("6 errore, se, z", c(mean(x06)-10, 2/sqrt(6), (mean(x06)-10)/(2/sqrt(6))))
x07 <- c(4.2,5.1,6.4,7.0,7.3); v("7 quota >7, >=7", c(mean(x07>7), mean(x07>=7))); v("7 medie r s", c(mean(c(4.8,5.2,5.6)), mean(c(6.1,6.5,7.2)))); v("7 mediana", median(x07))
m08 <- c(5,6,12); v("8 pesi invertiti", sum(c(.5,.3,.2)*m08)); v("8 diff pesata-uguale", 8.8-mean(m08))
v("9 diff", 2.72-2.6); v("9 n uguali", weighted.mean(c(2.4,2.8), c(5,5)))
u12 <- c(2,4,5,7,8,10); me <- combn(u12, 2, mean); v("12 min max medie", range(me)); N<-6;n<-2
v("12 var medie, formula", c(mean((me-mean(me))^2), (1-n/N)*var(u12)/n)); v("12 S2", var(u12))
v("13 diff", 7.44-6.8)
ids14 <- unique(d05$stazione); set.seed(17); sc <- sample(ids14, 2); v("14 scelte", sc); v("14 media sel", mean(d05$misura[d05$stazione %in% sc]))
for (h in c(40,10)) { r <- lab_estimandi(nHigh=h); v(paste("15 nHigh", h, "osservate"), r$indicatori); v(paste("15 medie stazioni", h), r$medie_stazioni$valore); v(paste("15 teoriche", h), c((50+60+12*h)/(20+h), 23/3)) }

# ---- tappe 26-35
sk <- function(x) mean((x-mean(x))^3)/sd(x)^3
set.seed(17); c26 <- replicate(4, rexp(6)); m26 <- colMeans(c26); v("26 medie", m26); v("26 media delle 4, se teorico", c(mean(m26), 1/sqrt(6))); v("26 min max valori", range(c26))
set.seed(17); a27 <- rnorm(200,1,1); b27 <- rexp(200,1)
v("27 quota negativi a27, teorica", c(mean(a27<0), pnorm(0,1,1))); v("27 asimmetria a27 b27", c(sk(a27), sk(b27))); v("27 mediana b27, teorica", c(median(b27), log(2))); v("27 max b27", max(b27))
v("29 prob n=60,12,240", sapply(c(60,12,240), function(n) pnorm(1.2,1,1/sqrt(n))-pnorm(.8,1,1/sqrt(n))))
set.seed(17); m30 <- replicate(200, mean(rexp(60))); v("30 sd, se, diff", c(sd(m30), 1/sqrt(60), sd(m30)-1/sqrt(60))); v("30 err MC sd", (1/sqrt(60))/sqrt(2*200)); v("30 asimmetria teorica n=12,60", 2/sqrt(c(12,60))); v("30 asimmetria m30", sk(m30)); v("30 range m30", range(m30))
v("31 normale esatta n=25,100,400", 2*pnorm(-0.2*sqrt(c(25,100,400))))
v("31 esponenziale esatta", sapply(c(25,100,400), function(n) pgamma(.8, n, n) + pgamma(1.2, n, n, lower.tail=FALSE)))
v("31 n per limite .05", 1/(.05*.2^2))
set.seed(17); x32 <- rexp(200); mc <- cumsum(x32)/seq_along(x32); v("32 mc a 1,10,50,100,200", mc[c(1,10,50,100,200)]); v("32 max |mc-1| dopo 50", max(abs(mc[50:200]-1))); v("32 min max mc", range(mc))
set.seed(17); m33 <- replicate(1000, mean(rexp(60))); z33 <- sqrt(60)*(m33-1); v("33 asimmetria z", sk(z33)); v("33 quota |z|>1.96, z>1.96, z<-1.96", c(mean(abs(z33)>1.96), mean(z33>1.96), mean(z33< -1.96)))
v("34 z34", {set.seed(17); rnorm(1)}); v("34 var media rho=.1 n=100, n eff", c((1+99*.1)/100, 100/(1+99*.1)))
for (n in c(12,60)) { r <- lab_distribuzioni(n=n,B=1000,population="exp",seed=17); v(paste("35 n",n), r$indicatori); v(paste("35 errMC media",n), c(r$indicatori[3]/sqrt(1000), (r$indicatori[1]-1)/(r$indicatori[3]/sqrt(1000)))) }
r <- lab_distribuzioni(n=12,B=1000,population="normal",seed=17); v("35 normale n=12", r$indicatori)

# ---- tappe 36-47
x <- c(4,5,6,9); v("36 media, scarti", c(mean(x), x-mean(x))); v("36 dev n, n-1", c(sum((x-6)^2)/4, sum((x-6)^2)/3))
set.seed(36); s2n <- replicate(20000, {y <- rnorm(4); c(var(y), var(y)*3/4)}); v("36 E S2 n-1, n (sim n=4)", rowMeans(s2n))
f <- read.csv("Dati/fossili_simulati.csv"); r <- f$diametro_tot_um[f$morfotipo=="Rounded"]; s <- f$diametro_tot_um[f$morfotipo=="Spiky"]
v("37 media sd se Rounded", c(mean(r), sd(r), sd(r)/sqrt(80))); v("37 n", length(r))
v("37 Spiky media sd", c(mean(s), sd(s)))
v("38 var media cov0, cov.2", c(1/4, (4+12*.2)/16))
v("39 SE rho 0,.05,.2,.5 n=60", sqrt((1+59*c(0,.05,.2,.5))/60)); v("39 neff", 60/(1+59*c(0,.05,.2,.5)))
v("39 limite sqrt(rho)", sqrt(.2)); v("39 SE n=600 rho=.2", sqrt((1+599*.2)/600))
for (rho in c(0,.2)) { z <- lab_dipendenza(n=60,B=200,rho=rho,seed=17); v(paste("40 rho", rho), z$indicatori); v(paste("40 errMC sd", rho), z$indicatori[2]/sqrt(2*200)) }
z <- lab_dipendenza(n=60,B=200,rho=.2,seed=17); m <- z$dati$media; v("40 quota medie fuori 1.96 se ind", mean(abs(m) > 1.96*z$indicatori[1]))
v("41 DEFF rho 0 .3 .6 .9", 1+3*c(0,.3,.6,.9)); v("41 neff", 24/(1+3*c(0,.3,.6,.9)))
v("41 G=12 m=2 rho=.6 neff, G=3 m=8", c(24/(1+1*.6), 24/(1+7*.6)))
v("42 SE n 4 25 100 400", 1/sqrt(c(4,25,100,400)))
v("43 p, se", c(18/60, sqrt(.3*.7/60))); v("43 se p=.5 n=60", sqrt(.25/60)); v("43 n=240 se", sqrt(.3*.7/240))
v("43 zero eventi: regola del tre, esatto 95", c(3/60, 1-0.05^(1/60)))
pop <- c(2,4,6,8,10); v("44 S2, fpc, var con reins", c(var(pop), 1-2/5, mean((pop-6)^2)/2)); v("44 medie", colMeans(combn(pop,2)))
g <- split(f$diametro_tot_um, f$morfotipo); v("45 var gruppi, n", c(sapply(g,var), lengths(g)))
v("45 se pesi .3 .7", sqrt(sum(c(.3,.7)^2*sapply(g,var)/lengths(g)))); v("45 media strat .5", sum(.5*sapply(g,mean)))
v("46 n per E .2, .05", ceiling((qnorm(.975)/c(.2,.05))^2)); v("46 z", qnorm(.975)); v("46 sigma 1.2 -> n", ceiling((qnorm(.975)*1.2/.1)^2))
v("47 qt, qnorm", c(qt(.975,79), qnorm(.975))); v("47 IC", mean(r)+c(-1,1)*qt(.975,79)*sd(r)/sqrt(80)); v("47 quota entro +-sd", mean(abs(r-mean(r))<=sd(r)))
