# Pelago - Probabilita, variabilita e simulazione
# Eseguire dalla cartella di Pelago_M05.Rproj.
# Per mostrare il codice: source("Lezione_Pelago.R", echo = TRUE)
source("setup.R", encoding = "UTF-8")
dir.create("Risultati", showWarnings = FALSE)
pdf("Risultati/Figure_lezione.pdf", width = 9, height = 5.5)


# ======================================================
# 003_avvio.R
# ======================================================
# Aprire Pelago_M05.Rproj.
source("setup.R", encoding="UTF-8")
# Dati sintetici del corso
head(fossili)
head(provini)
# Argomenti e documentazione
args(mean)
help("sample")


# ======================================================
# 004_popolazione.R
# ======================================================
# Popolazione finita costruita
U04 <- data.frame(
  id=1:12,
  valore=seq(2.1,3.2,by=.1))
set.seed(17)
i04 <- sample(U04$id, size=4)
U04[i04, ]        # un campione
mean(U04$valore)  # media nota qui


# ======================================================
# 005_unita.R
# ======================================================
# Tre stazioni con quattro misure
d05 <- data.frame(
 stazione=rep(c("A","B","C"),each=4),
 misura=c(2.3,2.4,2.5,2.4,
          2.6,2.7,2.6,2.5,
          2.8,2.9,2.7,2.8))
G05 <- length(unique(d05$stazione))
c(righe=nrow(d05),stazioni=G05)


# ======================================================
# 006_stimatore.R
# ======================================================
# Modello didattico con media nota
mu06 <- 10
set.seed(17)
x06 <- rnorm(6,mean=mu06,sd=2)
mean(x06)  # stima ottenuta dai dati
# La regola vale per ogni campione.
stimatore06 <- function(x) mean(x)
stimatore06(x06)


# ======================================================
# 007_bersagli.R
# ======================================================
# Diametri costruiti, in micrometri
x07 <- c(4.2,5.1,6.4,7.0,7.3)
mean(x07)        # diametro medio
mean(x07 > 6)    # quota sopra 6
# Contrasto con ordine dichiarato
r07 <- c(4.8,5.2,5.6)
s07 <- c(6.1,6.5,7.2)
mean(s07)-mean(r07) # Spiky-Rounded


# ======================================================
# 008_pesi.R
# ======================================================
# Medie costruite di tre stazioni
m08 <- c(A=5,B=6,C=12)
w08 <- c(A=.2,B=.3,C=.5)
sum(w08)           # somma: 1
sum(w08*m08)       # media pesata
weighted.mean(m08,w08)
# Ogni stazione conta 1/3.
mean(m08)


# ======================================================
# 009_due_medie.R
# ======================================================
# Densita: g/cm^3, dati costruiti
n09 <- c(2,8)
m09 <- c(2.4,2.8)
weighted.mean(m09,n09) # 2.72
mean(m09)             # 2.60
c(peso_misure=n09[1]/sum(n09),
  peso_stazioni=1/length(n09))


# ======================================================
# 010_bilanciato.R
# ======================================================
# Riprendiamo i gruppi di slide 5.
m10 <- tapply(d05$misura,
  d05$stazione,mean)
c(righe=mean(d05$misura),
  stazioni=mean(m10))
table(d05$stazione)  # 4,4,4
# L'uguaglianza deriva dai pesi.


# ======================================================
# 011_densita.R
# ======================================================
# Due provini costruiti
m11 <- c(96,168)   # massa: g
v11 <- c(40,60)    # volume: cm^3
rho11 <- m11/v11
mean(rho11)       # 2.60 g/cm^3
sum(m11)/sum(v11) # 2.64 g/cm^3
weighted.mean(rho11,v11)


# ======================================================
# 012_casuale_semplice.R
# ======================================================
# Tutti i campioni di 2 fra 6 unita
u12 <- c(2,4,5,7,8,10)
ind12 <- combn(seq_along(u12),2)
medie12 <- apply(ind12,2,
  function(i) mean(u12[i]))
length(medie12)       # 15 campioni
c(pop=mean(u12),
  attesa=mean(medie12))


# ======================================================
# 013_strati.R
# ======================================================
# Quote note della popolazione
W13 <- c(.3,.7)
m13 <- c(5.2,8.4) # medie campionarie
n13 <- c(20,20)   # allocazione
sum(W13*m13)      # 7.44
weighted.mean(m13,n13) # 6.80
# I pesi W descrivono la popolazione.


# ======================================================
# 014_selezione_stazioni.R
# ======================================================
# Prima stazioni, poi le loro righe
ids14 <- unique(d05$stazione)
set.seed(17)
scelte14 <- sample(ids14,size=2)
d05[d05$stazione %in% scelte14, ]
# Le righe della stessa stazione
# restano insieme nella selezione.


# ======================================================
# 015_lab_estimandi.R
# ======================================================
# Stesso seme, diversa numerosita C
a15 <- lab_estimandi(nHigh=40)
b15 <- lab_estimandi(nHigh=10)
a15$indicatori
b15$indicatori
# Medie teoriche: A=5, B=6, C=12.


# ======================================================
# 016_lista_incompleta.R
# ======================================================
# Lista incompleta: esempio costruito
u16 <- data.frame(
 valore=c(4,5,5,6,8,9,10,11),
 accessibile=c(rep(TRUE,4),
               rep(FALSE,4)))
mean(u16$valore)
mean(u16$valore[u16$accessibile])


# ======================================================
# 017_bias.R
# ======================================================
# Simulazione diretta delle stime
n17 <- 60
set.seed(17)
t17 <- rnorm(200,mean=9,
             sd=2/sqrt(n17))
mean(t17)-10 # bias simulato
9-10         # bias del modello


# ======================================================
# 018_mse.R
# ======================================================
# Modello della slide precedente
n18 <- 60
bias18 <- -1
var18 <- 4/n18
mse18 <- var18+bias18^2
c(varianza=var18,bias=bias18,
  mse=mse18,rmse=sqrt(mse18))


# ======================================================
# 019_piu_osservazioni.R
# ======================================================
# Confronto teorico
n19 <- c(60,300)
data.frame(
 n=n19,
 se=2/sqrt(n19),
 bias=rep(-1,2),
 mse=4/n19+1)


# ======================================================
# 020_confronto_procedure.R
# ======================================================
# Bersaglio comune theta=10
v20 <- c(casuale=4/60,
         selettiva=4/300)
b20 <- c(casuale=0,selettiva=-1)
data.frame(se=sqrt(v20),
 bias=b20,mse=v20+b20^2)


# ======================================================
# 021_dati_mancanti.R
# ======================================================
# Registrare ogni esito del prelievo
d21 <- data.frame(
 id=1:6,
 misura=c(2.4,NA,2.7,2.5,NA,2.8),
 esito=c("ok","perso","ok","ok",
         "non accessibile","ok"))
table(d21$esito)
mean(d21$misura,na.rm=TRUE)


# ======================================================
# 022_registro.R
# ======================================================
# Metadati: esempio costruito
registro22 <- data.frame(
 id=c("P01","P02","P03"),
 stazione=c("A","A","B"),
 strato=c("Nord","Nord","Sud"),
 ordine=c(1,2,3),
 protocollo=rep("casuale",3))
registro22


# ======================================================
# 023_lab_selezione.R
# ======================================================
# Il sito genera direttamente stime.
a23 <- lab_selezione(n=60,bias=1)
b23 <- lab_selezione(n=300,bias=1)
a23$indicatori
b23$indicatori
c23 <- lab_selezione(n=60,bias=0)
c23$indicatori


# ======================================================
# 024_numerosita.R
# ======================================================
# Conteggi con significati diversi
G24 <- 6       # stazioni
m24 <- 4       # misure per stazione
n24 <- G24*m24 # osservazioni
B24 <- 2000    # repliche al computer
c(stazioni=G24,osservazioni=n24,
  repliche=B24)


# ======================================================
# 025_ripetizioni.R
# ======================================================
# Ogni colonna e' un nuovo campione.
set.seed(17)
X25 <- replicate(5,
  rnorm(4,mean=10,sd=2))
round(X25,2)
colMeans(X25) # una stima per campione
dim(X25)     # 4 misure x 5 campioni


# ======================================================
# 026_campioni.R
# ======================================================
set.seed(17)
# Ogni colonna e' un campione.
c26 <- replicate(4, rexp(6))
round(c26, 2)
m26 <- colMeans(c26)
round(m26, 2)  # Quattro medie


# ======================================================
# 027_popolazioni.R
# ======================================================
# Due modelli con media e varianza 1
set.seed(17)
a27 <- rnorm(200, mean = 1, sd = 1)
b27 <- rexp(200, rate = 1)
c(mean(a27), var(a27))
c(mean(b27), var(b27))


# ======================================================
# 028_valore_atteso.R
# ======================================================
# Medie note, anche differenti
mu28 <- c(2, 4, 9)
mean(mu28)  # E della media: 5
# Se tutte le medie valgono mu
mu28 <- rep(5, 3)
sum(mu28) / length(mu28)


# ======================================================
# 029_media_normale.R
# ======================================================
# Media di n osservazioni N(1,1)
n29 <- 60
se29 <- 1 / sqrt(n29)
# Probabilita' di media fra .8 e 1.2
pnorm(1.2, 1, se29) -
  pnorm(.8, 1, se29)


# ======================================================
# 030_medie_esponenziali.R
# ======================================================
set.seed(17)
# Una nuova media a ogni replica
m30 <- replicate(200,
  mean(rexp(60, rate = 1)))
hist(m30, main = "200 medie",
     xlab = "Media campionaria")
sd(m30)
1 / sqrt(60)  # SE teorico


# ======================================================
# 031_chebyshev.R
# ======================================================
n31 <- c(25, 100, 400)
eps31 <- .2  # Tolleranza
# Varianza della popolazione = 1
lim31 <- pmin(1, 1/(n31*eps31^2))
data.frame(n = n31, limite = lim31)


# ======================================================
# 032_media_cumulativa.R
# ======================================================
set.seed(17)
x32 <- rexp(200)
n32 <- seq_along(x32)
mc32 <- cumsum(x32) / n32
plot(n32, mc32, type = "l",
  xlab = "n", ylab = "Media")
abline(h = 1, lty = 2)


# ======================================================
# 033_standardizzazione.R
# ======================================================
set.seed(17)
n33 <- 60
m33 <- replicate(1000,
  mean(rexp(n33)))
z33 <- sqrt(n33) * (m33 - 1)
c(media = mean(z33), sd = sd(z33))


# ======================================================
# 034_dipendenza_totale.R
# ======================================================
set.seed(17)
z34 <- rnorm(1)
x34 <- rep(z34, 100)
mean(x34)  # Identico a z34
# Aggiungere copie lascia la media
# uguale alla stessa osservazione.


# ======================================================
# 035_lab_distribuzioni.R
# ======================================================
# n: osservazioni; B: campioni
a35 <- lab_distribuzioni(
  n = 12, B = 1000,
  population = "exp", seed = 17)
b35 <- lab_distribuzioni(
  n = 60, B = 1000,
  population = "exp", seed = 17)
a35$indicatori
b35$indicatori


# ======================================================
# 036_varianza.R
# ======================================================
x36 <- c(4, 5, 6, 9)
sc36 <- x36 - mean(x36)
sum(sc36)  # Scarti vincolati
sum(sc36^2)/(length(x36)-1)
var(x36)   # Stesso denominatore
sd(x36)^2


# ======================================================
# 037_sd_se.R
# ======================================================
f37 <- read.csv(
  "Dati/fossili_simulati.csv")
p37 <- subset(f37,
              morfotipo == "Rounded")
x37 <- p37$diametro_tot_um
n37 <- length(x37)
s37 <- sd(x37)
c(SD = s37, SE = s37/sqrt(n37))


# ======================================================
# 038_covarianze.R
# ======================================================
# Quattro osservazioni, varianza 1
S38 <- matrix(.2, 4, 4)
diag(S38) <- 1
w38 <- rep(1/4, 4)
# Varianza della loro media
drop(t(w38) %*% S38 %*% w38)
sum(S38) / 4^2


# ======================================================
# 039_equicorrelazione.R
# ======================================================
n39 <- 60
rho39 <- .2
deff39 <- 1 + (n39-1)*rho39
c(SE = sqrt(deff39/n39),
  n_eff = n39/deff39)
# Varianza marginale fissata a 1


# ======================================================
# 040_lab_dipendenza.R
# ======================================================
a40 <- lab_dipendenza(
  n = 60, B = 200,
  rho = 0, seed = 17)
b40 <- lab_dipendenza(
  n = 60, B = 200,
  rho = .2, seed = 17)
a40$indicatori
b40$indicatori


# ======================================================
# 041_stazioni.R
# ======================================================
G41 <- 6   # Stazioni indipendenti
m41 <- 4   # Provini per stazione
rho41 <- .6
deff41 <- 1 + (m41-1)*rho41
n41 <- G41*m41
c(DEFF = deff41, n_eff = n41/deff41)


# ======================================================
# 042_radice_n.R
# ======================================================
n42 <- c(4, 25, 100)
se42 <- 1/sqrt(n42)
data.frame(n = n42, SE = se42)
# Rapporto: da 25 a 100
sqrt(25/100)


# ======================================================
# 043_proporzione.R
# ======================================================
evento43 <- c(rep(1, 18), rep(0, 42))
n43 <- length(evento43)
p43 <- mean(evento43)
sqrt(p43*(1-p43)/n43)
# Con zero eventi la stima e' zero:
# non implica certezza su p.


# ======================================================
# 044_popolazione_finita.R
# ======================================================
pop44 <- c(2, 4, 6, 8, 10)
m44 <- colMeans(combn(pop44, 2))
# Varianza esatta sui 10 campioni
mean((m44-mean(pop44))^2)
# Formula senza reinserimento
(1-2/length(pop44))*var(pop44)/2


# ======================================================
# 045_strati.R
# ======================================================
f45 <- read.csv(
  "Dati/fossili_simulati.csv")
g45 <- split(f45$diametro_tot_um,
             f45$morfotipo)
w45 <- c(Rounded = .5, Spiky = .5)
se45 <- sqrt(sum(w45^2 *
  sapply(g45, var)/lengths(g45)))
se45


# ======================================================
# 046_pianificazione.R
# ======================================================
sigma46 <- 1  # SD pilota, micrometri
E46 <- .1     # Semiampiezza voluta
z46 <- qnorm(.975)
n46 <- ceiling((z46*sigma46/E46)^2)
n46
z46*sigma46/sqrt(n46)


# ======================================================
# 047_barre.R
# ======================================================
f47 <- read.csv(
  "Dati/fossili_simulati.csv")
p47 <- subset(f47,
              morfotipo == "Rounded")
x47 <- p47$diametro_tot_um
s47 <- sd(x47); n47 <- length(x47)
c(SD = s47, SE = s47/sqrt(n47),
  IC95 = qt(.975,n47-1)*s47/sqrt(n47))


# ======================================================
# 048_student.R
# ======================================================
n48 <- 20
q48 <- qt(.975, df = n48-1)
q48  # Circa 2.093
# Area centrale della Student
pt(q48, n48-1) - pt(-q48, n48-1)


# ======================================================
# 049_intervallo_t.R
# ======================================================
# Esempio costruito, n = 6
x49 <- c(4.2, 5.1, 5.4, 6, 6.3, 7)
n49 <- length(x49)
se49 <- sd(x49)/sqrt(n49)
q49 <- qt(.975, n49-1)
mean(x49) + c(-1,1)*q49*se49


# ======================================================
# 050_livelli.R
# ======================================================
liv50 <- c(.80, .90, .95, .99)
q50 <- qt((1+liv50)/2, df = 19)
data.frame(livello = liv50,
           quantile = q50)
# La semiampiezza e' quantile * SE.


# ======================================================
# 051_ic_fossili.R
# ======================================================
f51 <- read.csv(
  "Dati/fossili_simulati.csv")
p51 <- subset(f51,
              morfotipo == "Rounded")
x51 <- p51$diametro_tot_um
n51 <- length(x51)
q51 <- qt(.975, n51-1)
se51 <- sd(x51)/sqrt(n51)
mean(x51) + c(-1,1)*q51*se51
t.test(x51)$conf.int


# ======================================================
# 052_copertura.R
# ======================================================
a52 <- lab_intervalli(
  n = 30, B = 200, rho = 0,
  level = .95, seed = 17)
sum(a52$dati$copre)  # 187 su 200
mean(a52$dati$copre)
a52$indicatori


# ======================================================
# 053_lab_intervalli.R
# ======================================================
b53 <- lab_intervalli(
  n = 30, B = 200, rho = .2,
  level = .95, seed = 17)
b53$indicatori
c53 <- mean(b53$dati$copre)
# SE Monte Carlo della copertura
sqrt(c53*(1-c53)/200)


# ======================================================
# 054_previsione.R
# ======================================================
# x51: diametri Rounded
n54 <- length(x51)
q54 <- qt(.975, n54-1)
mean(x51) + c(-1,1)*q54 *
  sd(x51)*sqrt(1+1/n54)
# Include la variabilita' futura.


# ======================================================
# 055_contrasto.R
# ======================================================
f55 <- read.csv(
  "Dati/fossili_simulati.csv")
g55 <- split(f55$diametro_tot_um,
             f55$morfotipo)
S55 <- g55$Spiky; R55 <- g55$Rounded
mean(S55) - mean(R55)
t.test(S55, R55,
       var.equal = FALSE)$conf.int


# ======================================================
# 056_differenze.R
# ======================================================
# Tre coppie costruite, micrometri
tot56 <- c(7.2, 5.8, 6.4)
int56 <- c(6.3, 5.0, 5.3)
d56 <- tot56 - int56
d56
sd(d56)/sqrt(length(d56))
# Il numero di coppie e' 3.


# ======================================================
# 057_ic_appaiato.R
# ======================================================
f57 <- read.csv(
  "Dati/fossili_simulati.csv")
p57 <- subset(f57,
              morfotipo == "Rounded")
d57 <- p57$diametro_tot_um -
       p57$diametro_int_um
c(media = mean(d57), n = length(d57))
t.test(d57)$conf.int


# ======================================================
# 058_sensibilita.R
# ======================================================
# Esempio costruito
x58 <- c(4.1,4.7,5,5.2,5.4,5.6,5.8,6)
z58 <- x58
z58[8] <- 12  # Un valore cambiato
rbind(prima = c(mean(x58), sd(x58)),
      dopo = c(mean(z58), sd(z58)))
rbind(t.test(x58)$conf.int,
      t.test(z58)$conf.int)


# ======================================================
# 060_distribuzione_empirica.R
# ======================================================
# Quattro osservazioni adimensionali
x60 <- c(4, 5, 7, 8)
F60 <- ecdf(x60)  # Frazione <= t
F60(c(4, 6, 8))  # .25, .50, 1
plot(F60, main = "CDF empirica",
     xlab = "t", ylab = "F_n(t)")


# ======================================================
# 061_masse.R
# ======================================================
x61 <- c(4, 5, 7, 8)
p61 <- rep(1/4, 4)
sum(p61)       # Probabilita totale
sum(x61*p61)   # Media empirica: 6
# Ogni posizione ha probabilita 1/4
data.frame(valore = x61, p = p61)


# ======================================================
# 062_indici.R
# ======================================================
x62 <- c(4, 5, 7, 8)
# Replica scelta per il diagramma
j62 <- c(3, 3, 1, 4)
x62[j62]        # 7, 7, 4, 8
mean(x62[j62])  # 6.5
# Una replica estratta casualmente
set.seed(17)
sample.int(4, 4, replace = TRUE)


# ======================================================
# 063_molteplicita.R
# ======================================================
x63 <- c(4, 5, 7, 8)
j63 <- c(3, 3, 1, 4)
N63 <- tabulate(j63, nbins = 4)
N63              # 1, 0, 2, 1
sum(N63)         # 4 estrazioni
sum(N63*x63)/4   # Media: 6.5
mean(x63[j63])   # Stesso valore


# ======================================================
# 064_enumerazione.R
# ======================================================
x64 <- c(4, 5, 7, 8)
# Tutte le 4^4 sequenze ordinate
j64 <- as.matrix(expand.grid(
  rep(list(1:4), 4)))
m64 <- apply(j64, 1,
  function(j) mean(x64[j]))
length(m64)               # 256
mean(m64)                 # 6
mean((m64-mean(m64))^2)    # .625


# ======================================================
# 065_varianza_condizionata.R
# ======================================================
x65 <- c(4, 5, 7, 8)
n65 <- length(x65)
s265 <- var(x65)        # 10/3
v65 <- (n65-1)/n65^2*s265
v65                    # .625
sqrt(v65)              # SE esatto
# Varianza di una sola estrazione
mean((x65-mean(x65))^2)  # 2.5


# ======================================================
# 066_molte_repliche.R
# ======================================================
x66 <- c(4, 5, 7, 8)
n66 <- length(x66)
B66 <- 2000
set.seed(17)
b66 <- replicate(B66, {
  j <- sample.int(n66, n66,
                  replace = TRUE)
  mean(x66[j])
})
length(b66)  # Una media per replica


# ======================================================
# 067_errore_standard_boot.R
# ======================================================
# b66 contiene 2000 medie bootstrap
sd(b66)      # SE bootstrap: circa .783
# Errore MC della media delle repliche
sd(b66)/sqrt(length(b66))  # .0175
# Dispersione delle quattro misure
sd(x66)      # Circa 1.826


# ======================================================
# 068_bias_bootstrap.R
# ======================================================
# Media delle repliche meno stima
mean(b66) - mean(x66)  # .00225
# Il valore condizionato esatto e 0
sum(x66/length(x66)) - mean(x66)
# Una selezione distorta del campione
# richiede informazioni sul disegno.


# ======================================================
# 069_quantile_tipo7.R
# ======================================================
# Esempio di 20 statistiche ordinate
v69 <- seq(1, 2.9, by = .1)
p69 <- .975
h69 <- 1 + (length(v69)-1)*p69
j69 <- floor(h69)
g69 <- h69-j69
(1-g69)*v69[j69] + g69*v69[j69+1]
quantile(v69, p69, type = 7)


# ======================================================
# 070_bootstrap_mediana.R
# ======================================================
set.seed(17)
x70 <- rlnorm(30, 0, .6)
set.seed(17)
m70 <- replicate(2000,
  median(sample(x70, replace = TRUE)))
median(x70)
quantile(m70, c(.025, .975),
         type = 7)


# ======================================================
# 071_laboratorio_bootstrap.R
# ======================================================
r71 <- lab_bootstrap(
  n = 30, B = 200, seed = 17)
r71$indicatori
# La distribuzione e condizionata
# ai 30 valori del campione.
hist(r71$dati$media,
     xlab = "Media bootstrap",
     main = "Ricampionamento")


# ======================================================
# 072_struttura_dati.R
# ======================================================
# Dati sintetici letti da setup.R
table(fossili$morfotipo)
table(provini$stazione)
# Una riga del fossile contiene
# due misure della stessa unita.
head(fossili[c("id",
  "diametro_tot_um", "diametro_int_um")])


# ======================================================
# 073_quote_pooled.R
# ======================================================
# Indici del campione riunito
g73 <- fossili$morfotipo
set.seed(17)
j73 <- sample.int(length(g73),
  length(g73), replace = TRUE)
table(g73[j73])
# N_R varia fra repliche.
length(j73)  # Totale sempre 160


# ======================================================
# 074_stratificato.R
# ======================================================
g74 <- split(fossili$diametro_tot_um,
             fossili$morfotipo)
rb74 <- function(v)
  mean(sample(v, replace = TRUE))
set.seed(17)
b74 <- replicate(2000,
  .5*rb74(g74$Rounded) +
  .5*rb74(g74$Spiky))
sd(b74)


# ======================================================
# 075_pooled_stratificato.R
# ======================================================
z75 <- fossili$diametro_tot_um
set.seed(17)
bp75 <- replicate(2000,
  mean(sample(z75, replace = TRUE)))
# b74 usa quote fissate a 80 e 80
c(pooled = sd(bp75),
  stratificato = sd(b74))
mean(z75)  # Media osservata comune


# ======================================================
# 076_contrasto_gruppi.R
# ======================================================
# Contrasto Spiky meno Rounded
set.seed(17)
delta76 <- replicate(2000,
  rb74(g74$Spiky) - rb74(g74$Rounded))
mean(g74$Spiky) - mean(g74$Rounded)
quantile(delta76, c(.025, .975),
         type = 7)


# ======================================================
# 077_coppie.R
# ======================================================
r77 <- subset(fossili,
               morfotipo == "Rounded")
d77 <- with(r77,
  diametro_tot_um - diametro_int_um)
set.seed(17)
bd77 <- replicate(2000,
  mean(sample(d77, replace = TRUE)))
c(differenza = mean(d77),
  SE = sd(bd77))


# ======================================================
# 078_medie_stazione.R
# ======================================================
# Densita in g/cm^3, 4 provini/sito
st78 <- aggregate(densita ~ stazione,
                  provini, mean)
st78
mean(provini$densita)
mean(st78$densita)  # Stesso valore
table(provini$stazione)


# ======================================================
# 079_stazioni_intere.R
# ======================================================
v79 <- split(provini$densita,
              provini$stazione)
# Sei indici illustrativi
j79 <- c(2, 2, 6, 4, 1, 3)
mean(unlist(v79[j79]))
mean(sapply(v79[j79], mean))
# Identici: 4 provini per stazione


# ======================================================
# 080_gruppi_diseguali.R
# ======================================================
# Due stazioni illustrative
n80 <- c(2, 8)
medie80 <- c(2.4, 2.8)  # g/cm^3
mean(medie80)           # 2.60
weighted.mean(medie80, n80) # 2.72
# L'aggregazione definisce i pesi.


# ======================================================
# 081_righe_stazioni.R
# ======================================================
set.seed(17)
br81 <- replicate(2000,
  mean(sample(provini$densita,
              replace = TRUE)))
set.seed(17)
bs81 <- replicate(2000,
  mean(sample(stazioni$densita,
              replace = TRUE)))
c(righe = sd(br81), siti = sd(bs81))


# ======================================================
# 082_affioramenti.R
# ======================================================
a82 <- split(stazioni$densita,
              stazioni$affioramento)
set.seed(17)
ab82 <- replicate(2000,
  rb74(a82$A) - rb74(a82$B))
mean(a82$A) - mean(a82$B)
quantile(ab82, c(.025, .975),
         type = 7)


# ======================================================
# 083_pochi_siti.R
# ======================================================
# Sei medie locali indipendenti
quantile(bs81, c(.025, .975),
         type = 7)
# Student assume normalita delle
# medie di stazione, oltre a iid.
t.test(stazioni$densita)$conf.int
length(stazioni$densita)  # 6


# ======================================================
# 084_modello_stazioni.R
# ======================================================
G84 <- 12
m84 <- 6
tau84 <- 2     # SD fra stazioni
rho84 <- tau84^2/(tau84^2+1)
se84 <- sqrt(tau84^2/G84 +
             1/(G84*m84))
c(rho_intra = rho84, SE = se84)


# ======================================================
# 085_laboratorio_stazioni.R
# ======================================================
r85 <- lab_ricampionamento(
  tau = 2, B = 200, seed = 17)
r85$indicatori
# Variante: componente comune nulla
r85b <- lab_ricampionamento(
  tau = 0, B = 200, seed = 17)
r85b$indicatori


# ======================================================
# 088_serie_temporale.R
# ======================================================
r88 <- lab_blocchi(length = 8,
  rho = .7, B = 200, seed = 17)
x88 <- r88$campione
plot(x88, type = "l",
     xlab = "Tempo",
     ylab = "Valore adimensionale")
abline(h = 0, lty = 2)


# ======================================================
# 089_varianza_ar1.R
# ======================================================
n89 <- 120
rho89 <- .7
h89 <- 1:(n89-1)
v89 <- (n89 + 2*sum(
  (n89-h89)*rho89^h89))/n89^2
sqrt(v89)      # SE teorico: .215
1/sqrt(n89)    # Ipotesi iid: .091


# ======================================================
# 090_indici_individuali.R
# ======================================================
set.seed(17)
j90 <- sample.int(length(x88),
  length(x88), replace = TRUE)
head(j90, 12)
# I valori adiacenti nella replica
# possono essere lontani nella serie.
head(diff(j90), 11)


# ======================================================
# 091_blocchi_esempio.R
# ======================================================
n91 <- 8
L91 <- 3
inizi91 <- c(7, 3, 5)
j91 <- unlist(lapply(inizi91,
  function(s)
    ((s-1+0:(L91-1)) %% n91)+1))
j91             # 9 indici
j91[1:n91]      # Troncamento a 8


# ======================================================
# 092_replica_blocchi.R
# ======================================================
n92 <- length(x88)
L92 <- 8
set.seed(17)
s92 <- sample.int(n92,
  ceiling(n92/L92), replace = TRUE)
j92 <- unlist(lapply(s92,
  function(s)
    ((s-1+0:(L92-1)) %% n92)+1))
mean(x88[j92[1:n92]])


# ======================================================
# 093_confronto_blocchi.R
# ======================================================
# Output del caso iniziale r88
r88$indicatori
split(r88$dati$media,
      r88$dati$metodo) |>
  lapply(sd)
# SE teorico: modello AR(1)
sqrt(v89)


# ======================================================
# 094_numero_blocchi.R
# ======================================================
n94 <- 120
L94 <- c(1, 8, 30)
data.frame(lunghezza = L94,
  blocchi = ceiling(n94/L94))
# L=1: 120 blocchi individuali
# L=8: 15 blocchi
# L=30: 4 blocchi


# ======================================================
# 095_laboratorio_blocchi.R
# ======================================================
r95 <- lab_blocchi(length = 8,
  rho = .7, B = 200, seed = 17)
r95$indicatori
r95b <- lab_blocchi(length = 1,
  rho = .7, B = 200, seed = 17)
r95b$indicatori
identical(r95$campione,
          r95b$campione) # TRUE


# ======================================================
# 096_tre_numeri.R
# ======================================================
n96 <- 30   # Osservazioni fissate
B96 <- 200  # Repliche per calcolo
R96 <- 30   # Ripetizioni del calcolo
c(osservazioni = n96,
  repliche = B96,
  ripetizioni = R96)
B96*R96     # 6000 medie calcolate


# ======================================================
# 097_stabilita_se.R
# ======================================================
set.seed(17)
x97 <- rlnorm(30, 0, .6)
se97 <- function(B)
  sd(replicate(B,
    mean(sample(x97, replace = TRUE))))
set.seed(717)
s97 <- sapply(c(50, 200, 1000),
  function(B) replicate(12, se97(B)))
s97


# ======================================================
# 098_limiti_ripetuti.R
# ======================================================
set.seed(17)
x98 <- rlnorm(30, 0, .6)
q98 <- replicate(30, {
  b <- replicate(200,
    mean(sample(x98, replace = TRUE)))
  quantile(b, .975, type = 7)
})
sd(q98)  # Variabilita numerica


# ======================================================
# 099_posizione_coda.R
# ======================================================
B99 <- c(40, 200, 1000)
p99 <- .975
h99 <- 1 + (B99-1)*p99
data.frame(B = B99, posizione = h99,
  repliche_coda_circa = B99*(1-p99))
# Il quantile dipende da pochi
# valori vicini alla coda superiore.


# ======================================================
# 100_confronto_B.R
# ======================================================
r100a <- lab_precisione(
  B = 200, seed = 17)
r100b <- lab_precisione(
  B = 1000, seed = 17)
c(B200 = sd(r100a$dati$y),
  B1000 = sd(r100b$dati$y))
identical(r100a$campione,
          r100b$campione)


# ======================================================
# 101_laboratorio_precisione.R
# ======================================================
r101 <- lab_precisione(
  B = 200, seed = 17)
r101$indicatori
plot(r101$dati$x, r101$dati$y,
  xlab = "Ripetizione",
  ylab = "Limite superiore")
mean(r101$campione) # Media fissata


# ======================================================
# 102_registro.R
# ======================================================
dir.create("Risultati",
           showWarnings = FALSE)
registro102 <- list(
  n = 30, B = 200, seed = 17,
  unita = "osservazione",
  statistica = "media",
  quantili = "type 7",
  ambiente = sessionInfo())
saveRDS(registro102,
        "Risultati/registro.rds")


# ======================================================
# 106_fossili.R
# ======================================================
# Diametri in micrometri, dati del corso
x106 <- fossili$diametro_tot_um
g106 <- split(x106,fossili$morfotipo)
set.seed(17)
b106 <- replicate(2000,
  mean(sample(x106,replace=TRUE)))
s106 <- replicate(2000,mean(vapply(
  g106,function(z)
    mean(sample(z,replace=TRUE)),0.0)))
c(pooled=sd(b106),strati=sd(s106))


# ======================================================
# 107_relazione.R
# ======================================================
# Registrare risultato e ambiente
r107 <- lab_ricampionamento(
  tau=2,B=1000,seed=17)
dir.create("Risultati",
           showWarnings=FALSE)
saveRDS(r107,"Risultati/stazioni.rds")
writeLines(capture.output(sessionInfo()),
  "Risultati/sessionInfo.txt")


# Chiudere il documento delle figure.
dev.off()
