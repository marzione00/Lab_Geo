# Gemina - Confrontare gruppi e valutare ipotesi
# Eseguire dalla cartella di Gemina_M06.Rproj.
# Per mostrare il codice: source("Lezione_Gemina.R", echo = TRUE)
source("setup.R", encoding = "UTF-8")
dir.create("Risultati", showWarnings = FALSE)
pdf("Risultati/Figure_lezione.pdf", width = 9, height = 5.5)


# ======================================================
# 003_avvio.R
# ======================================================
# Aprire Gemina_M06.Rproj.
source("setup.R", encoding="UTF-8")
# Dati sintetici del corso
f03 <- read.csv(
  "Dati/fossili_simulati.csv")
head(f03)
# Documentazione del test per medie
help("t.test")


# ======================================================
# 004_domanda.R
# ======================================================
# Una riga = un fossile sintetico.
f04 <- read.csv(
  "Dati/fossili_simulati.csv")
stopifnot(!anyDuplicated(f04$id))
table(f04$morfotipo)
summary(f04$diametro_tot_um)
# um nel nome indica micrometri.


# ======================================================
# 005_contrasto.R
# ======================================================
# Ordine dichiarato: Spiky-Rounded.
f05 <- read.csv(
  "Dati/fossili_simulati.csv")
g05 <- split(f05$diametro_tot_um,
             f05$morfotipo)
d05 <- mean(g05$Spiky) -
       mean(g05$Rounded)
d05  # micrometri


# ======================================================
# 006_segno.R
# ======================================================
# Dati costruiti, in micrometri
a06 <- c(4, 5, 6)
b06 <- c(6, 7, 8)
mean(b06)-mean(a06)  # +2 um
mean(a06)-mean(b06)  # -2 um
# Cambio di unita: um -> mm
(mean(b06)-mean(a06))/1000


# ======================================================
# 007_disegno.R
# ======================================================
# Esempio di misure ripetute
d07 <- data.frame(
  provino=rep(1:4, each=2),
  tempo=rep(c("prima","dopo"),4))
nrow(d07)                  # 8 righe
length(unique(d07$provino)) # 4 coppie
table(d07$provino, d07$tempo)


# ======================================================
# 008_punti.R
# ======================================================
f08 <- read.csv(
  "Dati/fossili_simulati.csv")
stripchart(diametro_tot_um ~ morfotipo,
 data=f08, method="stack", pch=16,
 col=c("#1D7890","#C57E42"),
 xlab="Diametro totale (um)")
tapply(f08$diametro_tot_um,
       f08$morfotipo, mean)


# ======================================================
# 009_medie_individui.R
# ======================================================
f09 <- read.csv(
  "Dati/fossili_simulati.csv")
g09 <- split(f09$diametro_tot_um,
             f09$morfotipo)
mean(g09$Spiky)-mean(g09$Rounded)
# Tutti i confronti fra individui
mean(outer(g09$Spiky,
           g09$Rounded, ">"))


# ======================================================
# 010_intervallo.R
# ======================================================
f10 <- read.csv(
  "Dati/fossili_simulati.csv")
g10 <- split(f10$diametro_tot_um,
             f10$morfotipo)
tt10 <- t.test(g10$Spiky,
 g10$Rounded, var.equal=FALSE)
tt10$conf.int  # IC bilaterale 95%
tt10$stderr    # errore standard


# ======================================================
# 011_ipotesi.R
# ======================================================
# Domanda fissata prima dei dati:
# H0: media_B-media_A = 0.
a11 <- c(3, 4, 6, 7, 9)
b11 <- c(4, 6, 7, 8, 10)
t.test(b11, a11, mu=0,
       alternative="two.sided")
# "greater" richiede H1: Delta>0.


# ======================================================
# 012_etichette.R
# ======================================================
# Valori fissi, etichette mobili
x12 <- c(1, 2, 4, 7)
g12 <- c("A","A","B","B")
set.seed(17)
gp12 <- sample(g12)
data.frame(valore=x12,
 originale=g12, permutato=gp12)
table(gp12) # 2 per gruppo


# ======================================================
# 013_sei_assegnazioni.R
# ======================================================
x13 <- c(1, 2, 4, 7)
# Scegliere 2 dei 4 indici per A.
i13 <- combn(4, 2)
t13 <- apply(i13, 2, function(i) {
  mean(x13[-i])-mean(x13[i])
})
t13
mean(abs(t13) >= 4) # 2/6 esatto


# ======================================================
# 014_una_permutazione.R
# ======================================================
x14 <- c(1, 2, 4, 7)
g14 <- c("A","A","B","B")
# Una riassegnazione ammessa
gp14 <- g14[c(1, 4, 2, 3)]
diff(tapply(x14, g14, mean))  # 4
diff(tapply(x14, gp14, mean)) # 2
# Per un riordino casuale:
sample(g14)


# ======================================================
# 015_molte_permutazioni.R
# ======================================================
set.seed(17)
x15 <- c(rnorm(20),rnorm(20,.6))
g15 <- rep(0:1, each=20)
obs15 <- diff(tapply(x15,g15,mean))
B15 <- 200
t15 <- replicate(B15, {
 gp <- sample(g15)
 diff(tapply(x15,gp,mean))
})


# ======================================================
# 016_estremita.R
# ======================================================
# Oggetti della slide 15
soglia16 <- abs(obs15)
estremi16 <- abs(t15) >= soglia16
K16 <- sum(estremi16)
K16  # 66 dei 200 contrasti
sum(t15 <= -soglia16) +
  sum(t15 >= soglia16)


# ======================================================
# 017_p_monte_carlo.R
# ======================================================
# Correzione per permutazioni estratte
p17 <- (1+K16)/(B15+1)
p17
# Risoluzione: caso di zero estremi
1/(B15+1)
data.frame(B=c(200,1000),
 minimo=1/(c(200,1000)+1))


# ======================================================
# 018_bootstrap_permutazione.R
# ======================================================
a18 <- c(1,2,4,5)
b18 <- c(3,5,6,8)
set.seed(17)
# Bootstrap entro ciascun gruppo
mean(sample(b18,4,replace=TRUE)) -
 mean(sample(a18,4,replace=TRUE))
# Permutazione: valori fissi
sample(rep(c("A","B"), each=4))


# ======================================================
# 019_vincoli.R
# ======================================================
# Quattro differenze appaiate
d19 <- c(.4, -.2, .7, .5)
set.seed(17)
# Scambio delle due etichette
# soltanto entro ciascuna coppia.
s19 <- sample(c(-1,1), 4,
              replace=TRUE)
mean(s19*d19)


# ======================================================
# 020_p_bilaterale.R
# ======================================================
# Riferimento t con 20 gradi di liberta'
t20 <- 2
nu20 <- 20
p20 <- 2 * pt(-abs(t20), df = nu20)
p20  # Circa 0.0593


# ======================================================
# 021_gradi_liberta.R
# ======================================================
# Stessa statistica, riferimenti diversi
2 * pt(-2, df = 5)
2 * pt(-2, df = 20)
2 * pnorm(-2)
# La scelta del riferimento va motivata.


# ======================================================
# 022_direzione.R
# ======================================================
t22 <- 2
nu22 <- 20
# Alternativa: Delta > 0, scelta prima
pt(t22, nu22, lower.tail = FALSE)
# Alternativa: Delta diverso da zero
2 * pt(-abs(t22), nu22)


# ======================================================
# 024_soglie_vicine.R
# ======================================================
p24 <- c(0.049, 0.051)
t24 <- qt(1 - p24 / 2, df = 20)
data.frame(p = p24, t = t24,
  rifiuto = p24 <= 0.05)


# ======================================================
# 025_effetto_precisione.R
# ======================================================
# Intervalli illustrativi: stima e SE
d25 <- c(0.2, 0.2, 1.0, 1.0)
se25 <- c(0.05, 0.4, 0.2, 0.8)
data.frame(stima = d25,
  minimo = d25 - 1.96 * se25,
  massimo = d25 + 1.96 * se25)


# ======================================================
# 026_margine_scientifico.R
# ======================================================
# Margine stabilito prima dei risultati
delta_min26 <- 0.5
ic26 <- c(0.10, 0.30)
# Tutto l'IC illustrativo e' nel margine?
all(ic26 > -delta_min26 &
    ic26 < delta_min26)


# ======================================================
# 029_calibrazione.R
# ======================================================
set.seed(6029)
# Z standard normale sotto H0
z29 <- rnorm(5000)
p29 <- 2 * pnorm(-abs(z29))
mean(p29 <= 0.05)
# Frequenza Monte Carlo, non identita'


# ======================================================
# 030_potenza_normale.R
# ======================================================
# Due gruppi, sigma noto = 1
se30 <- sqrt(2 / 30)
eta30 <- 0.5 / se30
c30 <- qnorm(0.975)
pnorm(-c30, mean = eta30) +
  pnorm(c30, eta30, lower.tail = FALSE)


# ======================================================
# 031_potenza_t.R
# ======================================================
# n indica la numerosita' di ogni gruppo
pt31 <- power.t.test(n = 30,
  delta = 0.5, sd = 1, sig.level = 0.05,
  type = "two.sample",
  alternative = "two.sided",
  strict = TRUE)
pt31$power


# ======================================================
# 032_effetti_potenza.R
# ======================================================
# Sensibilita' a tre effetti prefissati
sapply(c(0.2, 0.5, 0.8), function(d) {
  power.t.test(n = 60, delta = d,
    sd = 1, sig.level = 0.05,
    type = "two.sample",
    strict = TRUE)$power
})


# ======================================================
# 033_n_approssimato.R
# ======================================================
alpha33 <- 0.05
pot33 <- 0.80
sigma33 <- 1
delta33 <- 0.5
n33 <- 2 * sigma33^2 *
  (qnorm(1 - alpha33 / 2) +
   qnorm(pot33))^2 / delta33^2
ceiling(n33)  # 63 per gruppo


# ======================================================
# 034_n_test_t.R
# ======================================================
# Livello predefinito: 0.05
r34 <- power.t.test(delta = 0.5,
  sd = 1, power = 0.8,
  type = "two.sample", strict = TRUE)
ceiling(r34$n)  # 64 per gruppo


# ======================================================
# 035_regola_arresto.R
# ======================================================
set.seed(6035)
x35 <- rnorm(100)  # H0: media zero
n35 <- seq(10, 100, 10)
z35 <- cumsum(x35)[n35] / sqrt(n35)
any(abs(z35) > qnorm(0.975))
# Un percorso; la figura ne ripete 5000.


# ======================================================
# 036_piano_analisi.R
# ======================================================
# Schema da completare prima dei dati
piano36 <- list(contrasto = "B - A",
  alternativa = "two.sided",
  alpha = 0.05, effetto_minimo = 0.5,
  n_per_gruppo = 64,
  analisi = "una volta, a n fissato")
str(piano36)


# ======================================================
# 037_dati_fossili.R
# ======================================================
f37 <- read.csv("Dati/fossili_simulati.csv")
a37 <- f37$diametro_tot_um[
  f37$morfotipo == "Rounded"]
b37 <- f37$diametro_tot_um[
  f37$morfotipo == "Spiky"]
c(A = length(a37), B = length(b37))


# ======================================================
# 038_errore_standard.R
# ======================================================
# Contributi delle due varianze stimate
va38 <- var(a37) / length(a37)
vb38 <- var(b37) / length(b37)
se38 <- sqrt(va38 + vb38)
c(A = va38, B = vb38, SE = se38)


# ======================================================
# 039_statistica_welch.R
# ======================================================
d39 <- mean(b37) - mean(a37)
d0_39 <- 0  # Contrasto sotto H0
t39 <- (d39 - d0_39) / se38
c(stima = d39, SE = se38, t = t39)


# ======================================================
# 040_gradi_welch.R
# ======================================================
na40 <- length(a37)
nb40 <- length(b37)
nu40 <- (va38 + vb38)^2 /
  (va38^2 / (na40 - 1) +
   vb38^2 / (nb40 - 1))
nu40  # Circa 156.89; puo' non essere intero


# ======================================================
# 041_intervallo_welch.R
# ======================================================
q41 <- qt(0.975, df = nu40)
ic41 <- d39 + c(-1, 1) * q41 * se38
p41 <- 2 * pt(-abs(t39), df = nu40)
c(minimo = ic41[1], massimo = ic41[2],
  p = p41)


# ======================================================
# 042_t_test.R
# ======================================================
# Il primo argomento definisce B - A.
tt42 <- t.test(b37, a37,
  mu = 0, alternative = "two.sided",
  var.equal = FALSE, conf.level = 0.95)
tt42$estimate
tt42$conf.int
tt42$p.value


# ======================================================
# 043_osservare_gruppi.R
# ======================================================
# Controllo descrittivo prima del test
by(f37$diametro_tot_um, f37$morfotipo,
  function(x) c(n = length(x),
    media = mean(x), sd = sd(x),
    minimo = min(x), massimo = max(x)))


# ======================================================
# 044_varianze_separate.R
# ======================================================
# Nessun obbligo di pretest delle varianze
t.test(b37, a37, var.equal = FALSE)
# Confronto descrittivo delle dispersioni
c(sdA = sd(a37), sdB = sd(b37))


# ======================================================
# 045_effetto_standardizzato.R
# ======================================================
# na40 e nb40: numerosita' gia' calcolate
sp45 <- sqrt(((na40 - 1) * var(a37) +
  (nb40 - 1) * var(b37)) /
  (na40 + nb40 - 2))
d45 <- d39 / sp45
glass45 <- d39 / sd(a37)
c(d_pooled = d45, rispetto_A = glass45)


# ======================================================
# 046_browser_welch.R
# ======================================================
set.seed(17)
a46 <- rnorm(30)
b46 <- rnorm(30, mean = 0.5, sd = 2)
tt46 <- t.test(b46, a46)
mean(b46) - mean(a46)
tt46$conf.int
tt46$p.value


# ======================================================
# 048_allineare_coppie.R
# ======================================================
# Esempio: righe in ordine diverso
p48 <- data.frame(id=c(1,2,3),
                  prima=c(10,14,8))
d48 <- data.frame(id=c(3,1,2),
                 dopo=c(7,11,16))
j48 <- merge(p48,d48,by="id")
stopifnot(!anyDuplicated(j48$id))
j48$D <- j48$dopo-j48$prima
j48  # Differenze: 1, 2, -1


# ======================================================
# 049_osservare_coppie.R
# ======================================================
d49 <- read.csv(
  "Dati/misure_appaiate_simulate.csv")
stopifnot(!anyDuplicated(d49$id))
D49 <- d49$dopo-d49$prima
# Una differenza per provino
c(n=length(D49), media=mean(D49))
plot(D49, ylab="Dopo - prima (u.c.)",
     xlab="Indice del provino")
abline(h=0, lty=2)
qqnorm(D49); qqline(D49)


# ======================================================
# 050_covarianza.R
# ======================================================
d50 <- read.csv(
  "Dati/misure_appaiate_simulate.csv")
a50 <- d50$prima; b50 <- d50$dopo
v50 <- var(b50)+var(a50)-
       2*cov(b50,a50)
stopifnot(isTRUE(all.equal(
  v50,var(b50-a50))))
c(var_D=v50,cor=cor(a50,b50))


# ======================================================
# 051_se_appaiato.R
# ======================================================
# Generatore del laboratorio, tau=3
set.seed(17); n51 <- 30
u51 <- rnorm(n51,0,3)
a51 <- 10+u51+rnorm(n51)
b51 <- 10+u51+.6+rnorm(n51)
c(appaiato=sd(b51-a51)/sqrt(n51),
  indipendente=sqrt(var(a51)/n51+
                    var(b51)/n51))


# ======================================================
# 052_t_differenze.R
# ======================================================
d52 <- read.csv(
  "Dati/misure_appaiate_simulate.csv")
D52 <- d52$dopo-d52$prima
n52 <- length(D52)
se52 <- sd(D52)/sqrt(n52)
t52 <- mean(D52)/se52  # H0: Delta=0
p52 <- 2*pt(-abs(t52),df=n52-1)
c(t=t52,p=p52)


# ======================================================
# 053_due_chiamate.R
# ======================================================
d53 <- read.csv(
  "Dati/misure_appaiate_simulate.csv")
a53 <- t.test(d53$dopo-d53$prima)
b53 <- t.test(d53$dopo,d53$prima,
              paired=TRUE)
stopifnot(isTRUE(all.equal(
  a53$p.value,b53$p.value)))
a53$conf.int  # Intervallo al 95%


# ======================================================
# 054_confronti_ranghi.R
# ======================================================
# Esempio con un pareggio: valore 3
a54 <- c(1,3,5); b54 <- c(2,3,6)
M54 <- outer(b54,a54,">")+
       .5*outer(b54,a54,"==")
M54  # Righe B, colonne A
c(U=sum(M54),theta=mean(M54))


# ======================================================
# 056_rank_sum.R
# ======================================================
f56 <- read.csv(
  "Dati/fossili_simulati.csv")
g56 <- split(f56$diametro_tot_um,
             f56$morfotipo)
x56 <- g56$Spiky; y56 <- g56$Rounded
wilcox.test(x56,y56,exact=FALSE,
            correct=TRUE)
mean(outer(x56,y56,">")+
     .5*outer(x56,y56,"=="))


# ======================================================
# 057_stessa_mediana.R
# ======================================================
# Normali teoriche: mediana comune
x57 <- seq(-6,6,length.out=241)
matplot(x57,cbind(dnorm(x57),
        dnorm(x57,0,2)),type="l",
        xlab="Valore",ylab="Densita")
pnorm(0/sqrt(1^2+2^2))  # P(B>A)=.5


# ======================================================
# 058_signed_rank.R
# ======================================================
D58 <- c(1,-2,3,-4) # Esempio
z58 <- D58[D58!=0]  # Escludere zeri
r58 <- rank(abs(z58))
sum(r58[z58>0])     # W+ = 4
wilcox.test(D58,mu=0,
            exact=FALSE,correct=TRUE)
# Ipotesi: simmetria attorno a zero


# ======================================================
# 059_test_segni.R
# ======================================================
D59 <- c(1,-2,3,-4,2,0,1)
z59 <- D59[D59!=0]
k59 <- sum(z59>0); n59 <- length(z59)
# Tra i cambiamenti non nulli
binom.test(k59,n59,p=.5)
# Si usano soltanto i segni;
# le ampiezze non entrano nel test.


# ======================================================
# 060_conteggi_quote.R
# ======================================================
# Esempio costruito: 30 unita per sito
T60 <- matrix(c(18,12,9,21),2,
              byrow=TRUE)
dimnames(T60) <- list(
  sito=c("A","B"),
  esito=c("Presenza","Assenza"))
T60
prop.table(T60,1) # Quote per riga


# ======================================================
# 061_attesi.R
# ======================================================
O61 <- matrix(c(18,12,9,21),2,
              byrow=TRUE)
E61 <- outer(rowSums(O61),
             colSums(O61))/sum(O61)
E61  # 13.5 e 16.5 per riga
chisq.test(O61,correct=FALSE)$expected


# ======================================================
# 062_chi_quadrato.R
# ======================================================
O62 <- matrix(c(18,12,9,21),2,
              byrow=TRUE)
q62 <- chisq.test(O62,correct=FALSE)
C62 <- (O62-q62$expected)^2/
        q62$expected
C62  # Contributi delle quattro celle
c(X2=sum(C62),p=q62$p.value)


# ======================================================
# 063_fisher.R
# ======================================================
# Margini: 27 presenze, 33 assenze
a63 <- 0:27
pr63 <- dhyper(a63,27,33,30)
pobs63 <- dhyper(18,27,33,30)
# Bilaterale: includere tabelle
# non piu probabili dell'osservata
sum(pr63[pr63<=pobs63*(1+1e-7)])
T63 <- matrix(c(18,12,9,21),2,
              byrow=TRUE)
fisher.test(T63)$p.value


# ======================================================
# 064_categorie_browser.R
# ======================================================
# Impostazione iniziale del browser
T64 <- matrix(c(15,35,25,35),2,
              byrow=TRUE)
q64 <- chisq.test(T64,correct=FALSE)
prop.table(T64,1)
c(atteso_min=min(q64$expected),
  p_chi=q64$p.value,
  p_fisher=fisher.test(T64)$p.value)


# ======================================================
# 065_quattro_gruppi.R
# ======================================================
# Generatore iniziale: quattro gruppi
set.seed(17); n65 <- 30
g65 <- factor(rep(LETTERS[1:4],
                  each=n65))
mu65 <- rep((0:3)*.5,each=n65)
s65 <- rep(seq(1,2,length.out=4),
            each=n65)
y65 <- rnorm(4*n65,mu65,s65)
tapply(y65,g65,mean)


# ======================================================
# 067_anova_a_mano.R
# ======================================================
y67 <- c(1,3,4,6)
g67 <- factor(c("A","A","B","B"))
m67 <- ave(y67,g67,FUN=mean)
W67 <- sum((y67-m67)^2)  # Entro: 4
B67 <- sum((m67-mean(y67))^2) # 9
F67 <- (B67/1)/(W67/2)
F67
pf(F67,1,2,lower.tail=FALSE)
anova(lm(y67~g67))  # Stesso F


# ======================================================
# 068_welch_piu_gruppi.R
# ======================================================
r68 <- read.csv(
  "Dati/rocce_simulate.csv")
# Densita nelle litologie simulate
q68 <- oneway.test(
  densita~litologia_generatrice,
  data=r68,var.equal=FALSE)
q68
tapply(r68$densita,
       r68$litologia_generatrice,sd)


# ======================================================
# 069_contrasti_previsti.R
# ======================================================
# Famiglia prevista: tre confronti
set.seed(17)
g69 <- rep(LETTERS[1:4],each=30)
y69 <- rnorm(120,rep(0:3,each=30))
z69 <- split(y69,g69)
p69 <- sapply(z69[c("B","C","D")],
  function(z) t.test(z,z69$A)$p.value)
p.adjust(p69,method="holm")


# ======================================================
# 071_rischio_familiare.R
# ======================================================
# Nulle vere; test indipendenti
m71 <- c(1,6,10,20,50)
a71 <- .05
risk71 <- 1-(1-a71)^m71
cbind(test=m71,FWER=risk71)


# ======================================================
# 072_ripetere_famiglie.R
# ======================================================
set.seed(17)
v72 <- replicate(2000, {
  p72 <- runif(20) # Ipotesi nulle
  h72 <- p.adjust(p72,"holm")
  c(grezzi=any(p72<.05),
    Holm=any(h72<.05))
})
rowMeans(v72) # Quote di famiglie
# 2000 famiglie, 20 test per famiglia


# ======================================================
# 074_holm.R
# ======================================================
p74 <- c(.003,.018,.041,.2)
adj74 <- p.adjust(p74,method="holm")
# Calcolo sui p-value gia ordinati
manuale74 <- pmin(1,cummax(4:1*p74))
stopifnot(isTRUE(all.equal(
  adj74,manuale74)))
data.frame(p74,adj74,rifiuto=adj74<=.05)


# ======================================================
# 075_famiglia_completa.R
# ======================================================
p75 <- c(A_B=.003,A_C=.018,
          A_D=.041,B_C=.2)
# Correggere la famiglia dichiarata
adj75 <- p.adjust(p75,"holm")
data.frame(contrasto=names(p75),
           p=unname(p75),
           Holm=unname(adj75))


# ======================================================
# 077_risultato_appaiato.R
# ======================================================
d77 <- read.csv(
  "Dati/misure_appaiate_simulate.csv")
z77 <- d77$dopo-d77$prima
t77 <- t.test(z77)
data.frame(n=length(z77),
  stima=mean(z77),lo=t77$conf.int[1],
  hi=t77$conf.int[2],p=t77$p.value)


# ======================================================
# 078_lab_contrasto.R
# ======================================================
source("setup.R", encoding="UTF-8")
# Cambia solo la differenza vera.
z78 <- lab_contrasto(delta=1)
w78 <- lab_contrasto(delta=0)
rbind(delta1=z78$metrics,
      delta0=w78$metrics)


# ======================================================
# 079_lab_permutazione.R
# ======================================================
# Lo stesso campione, piu permutazioni
z79 <- lab_permutazione(B=200)
w79 <- lab_permutazione(B=1000)
rbind(B200=z79$metrics,
      B1000=w79$metrics)
# Nessun nuovo individuo aggiunto.


# ======================================================
# 080_lab_pvalue.R
# ======================================================
# t e df sono assegnati direttamente.
z80 <- lab_pvalue(t=2,df=20)
w80 <- lab_pvalue(t=2,df=5)
rbind(df20=z80$metrics,
      df5=w80$metrics)
2*pt(-abs(2), df=20)


# ======================================================
# 081_lab_potenza.R
# ======================================================
# Calcolo teorico, sd comune = 1
z81 <- lab_potenza(n=30)
w81 <- lab_potenza(n=120)
rbind(n30=z81$metrics,
      n120=w81$metrics)
# Delta=.5 e alfa=.05 restano fissi.


# ======================================================
# 082_lab_welch.R
# ======================================================
# Rapporto fra SD: 2 -> 1
z82 <- lab_welch(ratio=2)
w82 <- lab_welch(ratio=1)
rbind(sd2=z82$metrics,
      sd1=w82$metrics)
z82$test$conf.int
w82$test$conf.int


# ======================================================
# 083_lab_appaiati.R
# ======================================================
# Varia la componente individuale.
z83 <- lab_appaiati(tau=3)
w83 <- lab_appaiati(tau=5)
rbind(tau3=z83$metrics,
      tau5=w83$metrics)
all.equal(z83$differenze,
          w83$differenze)


# ======================================================
# 084_lab_ranghi.R
# ======================================================
# SD di B: da 1 a 2
z84 <- lab_ranghi(ratio=1)
w84 <- lab_ranghi(ratio=2)
rbind(sd1=z84$metrics,
      sd2=w84$metrics)
# Delta=.5; 35 dati per gruppo.


# ======================================================
# 085_lab_categorie.R
# ======================================================
# A: 15 su 50; B: count su 60
z85 <- lab_categorie(count=25)
w85 <- lab_categorie(count=18)
z85$tabella
z85$attesi
rbind(B25=z85$metrics,
      B18=w85$metrics)


# ======================================================
# 086_lab_anova.R
# ======================================================
# Quattro gruppi, SD diverse
z86 <- lab_anova(ratio=2)
w86 <- lab_anova(ratio=1)
rbind(sd_diverse=z86$metrics,
      sd_uguali=w86$metrics)
# Ogni riga contiene due metodi.


# ======================================================
# 087_lab_multipli.R
# ======================================================
# Stesso seme, famiglia piu ampia
z87 <- lab_multipli(m=20)
w87 <- lab_multipli(m=100)
rbind(m20=z87$metrics,
      m100=w87$metrics)
# Conteggi di una singola famiglia.


# ======================================================
# 088_lab_relazione.R
# ======================================================
# L'effetto vero resta Delta=.3.
z88 <- lab_relazione(n=30)
w88 <- lab_relazione(n=120)
rbind(n30=z88$metrics,
      n120=w88$metrics)
z88$data[c("x","lo","hi")]


# ======================================================
# 090_rivedere_conclusioni.R
# ======================================================
z90 <- lab_relazione(n=30)
# Prima leggere l'effetto e l'IC.
z90$data[c("x","lo","hi")]
# Poi il p-value del riferimento.
z90$metrics
# Scrivere il limite dell'inferenza.


# ======================================================
# 091_differenze_a_mano.R
# ======================================================
# Cinque coppie costruite, unita u.c.
a91 <- c(10,12,9,11,13)
b91 <- c(10.4,12.1,9.7,10.8,13.5)
d91 <- b91-a91
c(media=mean(d91), SE=sd(d91)/sqrt(5))
all.equal(mean(d91),
          mean(b91)-mean(a91))


# ======================================================
# 092_relazione_fossili.R
# ======================================================
f92 <- read.csv(
 "Dati/fossili_simulati.csv")
g92 <- split(f92$diametro_tot_um,
             f92$morfotipo)
t92 <- t.test(g92$Spiky,g92$Rounded)
c(SE=t92$stderr,p=t92$p.value)
t92$conf.int


# ======================================================
# 093_verifica_finale.R
# ======================================================
# Due domande definite in anticipo
f93 <- read.csv(
 "Dati/fossili_simulati.csv")
variabili93 <- c("diametro_tot_um",
                 "diametro_int_um")
summary(f93[variabili93])
# Completare Esercizi/
# 12_verifica_finale.R


# Chiudere il documento delle figure.
dev.off()
