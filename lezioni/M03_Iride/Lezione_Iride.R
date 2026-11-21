# Iride - Descrivere e visualizzare i dati
# Eseguire dalla cartella di Iride_M03.Rproj.
# Per mostrare il codice: source("Lezione_Iride.R", echo = TRUE)
source("setup.R", encoding = "UTF-8")
dir.create("Risultati", showWarnings = FALSE)
pdf("Risultati/Figure_lezione.pdf", width = 9, height = 5.5)


# ======================================================
# 03_avvio.R
# ======================================================
# Aprire Iride_M03.Rproj.
source("setup.R", encoding = "UTF-8")
# Tabelle lette dai CSV distribuiti
dim(fossili)       # 160 righe
dim(rocce)         # 90 righe
dim(campioni)      # 24 righe
names(fossili)


# ======================================================
# 04_campione.R
# ======================================================
# Un fossile per riga
head(fossili[, 1:3], 3)
table(fossili$morfotipo)
# Due gruppi di 80 individui
range(fossili$diametro_tot_um)


# ======================================================
# 05_controlli.R
# ======================================================
# Variabile e unita': diametro in um
x05 <- fossili$diametro_tot_um
c(n = length(x05),
  mancanti = sum(is.na(x05)))
stopifnot(!anyDuplicated(fossili$id))
stopifnot(all(is.finite(x05)))
stopifnot(all(x05 > 0))
summary(x05)


# ======================================================
# 06_supporto.R
# ======================================================
# Densita' dei 24 provini [g/cm^3]
c06 <- campioni
c06$rho <- c06$massa_g /
            c06$volume_cm3
# Una media per stazione: sei valori
st06 <- aggregate(rho ~ stazione,
  data = c06, FUN = mean)
nrow(c06)
nrow(st06)


# ======================================================
# 07_sintesi.R
# ======================================================
# Esempi costruiti, adimensionali
a07 <- c(4, 5, 6)
b07 <- c(1, 5, 9)
c(mean(a07), mean(b07))  # 5, 5
c(var(a07), var(b07))   # 1, 16


# ======================================================
# 09_lab_supporto.R
# ======================================================
# Stesso seme, rumore diverso
a09 <- lab_supporto(noise = 1)
b09 <- lab_supporto(noise = 3)
a09$indicatori
b09$indicatori
# Ogni stazione conserva 8 misure
table(a09$dati$gruppo)


# ======================================================
# 10_conteggi.R
# ======================================================
# Frequenze assolute per morfotipo
n10 <- table(fossili$morfotipo)
n10
sum(n10)  # 160 individui
barplot(n10, ylab = "N. di fossili",
        col = c("#1D7890", "#C57E42"))


# ======================================================
# 11_proporzioni.R
# ======================================================
# Stesso conteggio, denominatore noto
p11 <- prop.table(n10)
100 * p11  # Percentuali
stopifnot(abs(sum(p11) - 1) < 1e-12)


# ======================================================
# 12_doppia_entrata.R
# ======================================================
# Esempio costruito: gruppi A e B
t12 <- matrix(c(10, 40, 20, 80),
  nrow = 2, byrow = TRUE,
  dimnames = list(c("A", "B"),
    c("evento", "assenza")))
t12
prop.table(t12, margin = 1) # Per riga
prop.table(t12, margin = 2) # Colonne


# ======================================================
# 13_copertura.R
# ======================================================
# 1: evento; 0: assenza; NA: ignoto
x13 <- c(1, 0, 1, NA, 0, NA)
n13 <- length(x13)
v13 <- sum(!is.na(x13))
e13 <- sum(x13 == 1, na.rm = TRUE)
c(eventi = e13, validi = v13, n = n13)
c(quota_valida = e13 / v13,
  copertura = v13 / n13)


# ======================================================
# 14_pesi.R
# ======================================================
# Medie e numerosita' di due gruppi
m14 <- c(2, 8)
n14 <- c(2, 8)
mean(m14)                 # 5
weighted.mean(m14, n14)   # 6.8
sum(n14 * m14) / sum(n14)


# ======================================================
# 15_lab_denominatori.R
# ======================================================
# A: 10 eventi su 50 unita'
a15 <- lab_denominatori(nB = 100,
  scale = "count")
b15 <- lab_denominatori(nB = 200,
  scale = "rate")
a15$dati
b15$dati


# ======================================================
# 16_media.R
# ======================================================
# Esempio costruito, adimensionale
x16 <- c(2, 4, 6)
m16 <- mean(x16)
sum(x16)
length(x16) * m16  # Stesso totale
mean(fossili$diametro_tot_um)


# ======================================================
# 17_quadrati.R
# ======================================================
x17 <- c(2, 4, 6)
scarti2 <- function(a) {
  sum((x17 - a)^2)
}
sapply(c(3, 4, 5), scarti2)
# 11, 8, 11: minimo in a = 4


# ======================================================
# 18_mediana.R
# ======================================================
# Prima si ordinano i valori
x18 <- c(8, 2, 9, 4, 5)
sort(x18)
median(x18)       # 5
median(c(2, 4, 6, 9))  # 5


# ======================================================
# 19_assoluti.R
# ======================================================
x19 <- c(2, 4, 6)
scarti1 <- function(a) {
  sum(abs(x19 - a))
}
sapply(c(3, 4, 5), scarti1)
# 5, 4, 5: minimo in a = 4


# ======================================================
# 20_sensibilita.R
# ======================================================
# Si modifica soltanto l'ultimo valore
a20 <- c(4, 5, 6, 7)
b20 <- c(4, 5, 6, 27)
c(mean(a20), mean(b20))
c(median(a20), median(b20))
# La media cresce di (27 - 7) / 4


# ======================================================
# 21_densita.R
# ======================================================
# Due provini: volumi in cm^3
v21 <- c(1, 9)
rho21 <- c(2, 4)  # Densita' g/cm^3
m21 <- rho21 * v21  # Masse in g
mean(rho21)                  # 3
sum(m21) / sum(v21)          # 3.8
weighted.mean(rho21, v21)    # 3.8


# ======================================================
# 22_moda.R
# ======================================================
# Esempio discreto con ripetizioni
x22 <- c(1, 1, 2, 3, 4)
f22 <- table(x22)
names(f22)[f22 == max(f22)] # "1"
# mode() descrive il tipo, non la moda
mode(x22)                  # "numeric"


# ======================================================
# 23_lab_posizione.R
# ======================================================
# 29 valori comuni, uno modificato
a23 <- lab_posizione(outlier = 15)
b23 <- lab_posizione(outlier = 100)
rbind(a23$indicatori, b23$indicatori)
# Aumento teorico della media
(100 - 15) / 30


# ======================================================
# 24_dispersione.R
# ======================================================
# Esempi costruiti: misure in mm
x_disp <- c(4, 5, 6)
y_disp <- c(0, 5, 10)
rbind(A = c(media = mean(x_disp),
            sd = sd(x_disp)),
      B = c(media = mean(y_disp),
            sd = sd(y_disp)))


# ======================================================
# 26_varianza.R
# ======================================================
# Dati della slide 24
d_sc <- x_disp - mean(x_disp)
somma_q <- sum(d_sc^2)
s2 <- somma_q / (length(x_disp)-1)
c(formula = s2, R = var(x_disp))
sqrt(s2)
sd(x_disp)                  # 1 mm


# ======================================================
# 27_unita.R
# ======================================================
# Da millimetri a micrometri
y_um <- 1000 * x_disp
sd(y_um)                    # 1000
var(y_um)                   # 1e6
# Traslazione nella stessa unita
sd(x_disp + 20)             # 1


# ======================================================
# 28_quantili.R
# ======================================================
# Esempio ordinato, in mm
x_q <- c(1, 2, 4, 7, 8, 9, 10, 12)
quantile(x_q, c(.25, .5, .75),
         type = 7)
# Primo quartile interpolato
.25 * 2 + .75 * 4           # 3.5


# ======================================================
# 29_iqr.R
# ======================================================
q13 <- quantile(x_q, c(.25, .75),
                type = 7)
diff(q13)                   # 5.75
IQR(x_q, type = 7)          # 5.75
# La mediana e' 7.5 mm
median(x_q)


# ======================================================
# 30_fossili.R
# ======================================================
diam <- fossili$diametro_tot_um
stopifnot(all(is.finite(diam)),
          all(diam > 0))
c(n = length(diam),
  media = mean(diam),
  mediana = median(diam),
  sd = sd(diam))
quantile(diam, c(.25, .5, .75),
         type = 7)


# ======================================================
# 31_lab_quantili.R
# ======================================================
# Simulazione separata dai fossili
qA <- lab_quantili(noise = 1,
                  n = 60, seed = 17)
qB <- lab_quantili(noise = 2,
                  n = 60, seed = 17)
rbind(qA$indicatori, qB$indicatori)


# ======================================================
# 32_classi.R
# ======================================================
x_h <- c(1,1,2,3,3,3,4,5,6,6)
b_h <- c(0, 2, 4, 6)
h_h <- hist(x_h, breaks = b_h,
            plot = FALSE)
h_h$counts                  # 3 4 3
sum(h_h$counts)             # 10


# ======================================================
# 33_confini.R
# ======================================================
h_dx <- hist(x_h, breaks = b_h,
             right = TRUE,
             plot = FALSE)
h_sx <- hist(x_h, breaks = b_h,
             right = FALSE,
             plot = FALSE)
rbind(destra = h_dx$counts,
      sinistra = h_sx$counts)


# ======================================================
# 34_ampiezza.R
# ======================================================
h05 <- hist(diam, plot = FALSE,
            breaks = seq(2,14,by=.5))
h10 <- hist(diam, plot = FALSE,
            breaks = seq(2,14,by=1))
plot(h10, xlim = c(2,10),
     ylim = c(0,70), border = 2)
plot(h05, add = TRUE, border = 4)


# ======================================================
# 35_densita.R
# ======================================================
# h_h viene dalla slide 32
amp_h <- diff(h_h$breaks)
data.frame(n = h_h$counts,
           densita = h_h$density)
quote_h <- h_h$density * amp_h
quote_h                     # .3 .4 .3
sum(quote_h)                # 1


# ======================================================
# 36_classi_disuguali.R
# ======================================================
x_u <- c(.2,.4,.5,.6,.8,
         1.2,1.8,2,3,3.8)
h_u <- hist(x_u, breaks = c(0,1,4),
            plot = FALSE)
h_u$counts                  # 5 5
h_u$density                 # .5 1/6
plot(h_u, freq = FALSE)


# ======================================================
# 38_banda.R
# ======================================================
k15 <- density(diam, bw = .15,
  from = 2, to = 14, n = 256)
k40 <- density(diam, bw = .4,
  from = 2, to = 14, n = 256)
k12 <- density(diam, bw = 1.2,
  from = 2, to = 14, n = 256)
plot(k15, xlim = c(3,9),
     ylim = c(0,.65))
lines(k40, col = 2)
lines(k12, col = 4)


# ======================================================
# 40_ecdf.R
# ======================================================
x_e <- c(4.1,4.8,5.2,5.2,6.4)
F_e <- ecdf(x_e)
F_e(5.2)                    # 0.8
plot(F_e, verticals = TRUE,
     xlab = "Misura [mm]",
     ylab = "Quota cumulata")


# ======================================================
# 41_lab_smoothing.R
# ======================================================
sA <- lab_smoothing(bins = 18,
  bw = .5, seed = 17)
sB <- lab_smoothing(bins = 8,
  bw = .5, seed = 17)
sC <- lab_smoothing(bins = 8,
  bw = 1.5, seed = 17)
identical(sA$dati, sB$dati)  # TRUE
identical(sA$dati, sC$dati)  # TRUE


# ======================================================
# 42_boxplot.R
# ======================================================
x_b <- c(1:8, 20)
bx <- boxplot.stats(x_b, coef = 1.5)
bx$stats                  # 1 3 5 7 8
bx$out                      # 20
boxplot(x_b, horizontal = TRUE,
        xlab = "Misura [mm]")


# ======================================================
# 43_cerniere.R
# ======================================================
v_b <- 1:8
quantile(v_b, c(.25,.5,.75),
         type = 7)
# Cerniere e mediana di R base
boxplot.stats(v_b)$stats[2:4]


# ======================================================
# 44_controllo.R
# ======================================================
check_b <- data.frame(
  id = paste0("P", seq_along(x_b)),
  valore = x_b)
check_b$oltre <- x_b %in% bx$out
# Selezione per ispezione
check_b[check_b$oltre, ]


# ======================================================
# 45_jitter.R
# ======================================================
set.seed(303)
g_f <- fossili$morfotipo
pos <- as.integer(g_f)
pos <- pos +
  runif(length(pos), -.12, .12)
plot(pos, diam, xaxt = "n",
     xlim = c(.5,2.5), ylim = c(3,9),
     xlab = "Morfotipo",
     ylab = "Diametro [um]")
axis(1, at = 1:2,
     labels = levels(g_f))


# ======================================================
# 46_scale_comuni.R
# ======================================================
# Stesso asse per entrambi i gruppi
boxplot(diam ~ g_f,
        ylim = range(diam),
        xlab = "Morfotipo",
        ylab = "Diametro [um]")
table(g_f)                  # 80 e 80


# ======================================================
# 48_ecdf_gruppi.R
# ======================================================
gr_f <- split(diam, g_f)
F_R <- ecdf(gr_f[["Rounded"]])
F_S <- ecdf(gr_f[["Spiky"]])
plot(F_R, xlim = c(3,9),
     verticals = TRUE, col = 4,
     xlab = "Diametro [um]")
plot(F_S, add = TRUE,
     verticals = TRUE, col = 2)


# ======================================================
# 49_sintesi_gruppi.R
# ======================================================
riassumi_f <- function(v) {
  c(n = length(v), media = mean(v),
    mediana = median(v), sd = sd(v),
    IQR = IQR(v, type = 7))
}
# gr_f e' la lista della slide 48
round(t(sapply(gr_f, riassumi_f)), 3)


# ======================================================
# 50_lab_gruppi.R
# ======================================================
# Stesso delta e stesso seme
gA <- lab_gruppi(delta = 1,
                ratio = 1, seed = 17)
gB <- lab_gruppi(delta = 1,
                ratio = 2, seed = 17)
rbind(gA$indicatori, gB$indicatori)


# ======================================================
# 51_coppie.R
# ======================================================
# Misure in micrometri: stessa riga
r_x <- fossili$diametro_tot_um
r_y <- fossili$diaframma_um
stopifnot(all(is.finite(r_x)),
          all(is.finite(r_y)))
r_xy <- data.frame(id = fossili$id,
                   x = r_x, y = r_y)
head(r_xy, 3)


# ======================================================
# 52_scatter.R
# ======================================================
# Un punto per ogni coppia
plot(r_x, r_y,
     pch = 16, col = "#1D7890",
     xlab = "Diametro totale [um]",
     ylab = "Diaframma [um]")


# ======================================================
# 53_covarianza.R
# ======================================================
# Scarti dalle rispettive medie
r_dx <- r_x - mean(r_x)
r_dy <- r_y - mean(r_y)
r_n <- length(r_x)
r_cov <- sum(r_dx * r_dy) /
  (r_n - 1)
c(manuale = r_cov, R = cov(r_x,r_y))


# ======================================================
# 54_pearson.R
# ======================================================
# Due deviazioni standard positive
stopifnot(sd(r_x)>0, sd(r_y)>0)
r_p <- cor(r_x, r_y)
r_formula <- r_cov /
  (sd(r_x) * sd(r_y))
c(Pearson = r_p, formula = r_formula)
all.equal(r_p, r_formula)


# ======================================================
# 55_unita.R
# ======================================================
# Da micrometri a millimetri
r_mm <- r_x / 1000
c(cor(r_x,r_y), cor(r_mm,r_y))
c(cov(r_x,r_y), cov(r_mm,r_y))
# Invertire un asse cambia il segno
cor(-r_x, r_y)


# ======================================================
# 56_spearman.R
# ======================================================
# Esempio deterministico positivo
r_a <- c(1, 2, 2, 5, 8)
r_b <- r_a^2
rank(r_a)
cor(r_a, r_b)
cor(r_a, r_b, method="spearman")
cor(rank(r_a), rank(r_b))


# ======================================================
# 57_curva.R
# ======================================================
# Parabola simmetrica, senza rumore
r_u <- seq(-2, 2, by=.5)
r_v <- r_u^2
round(c(cor(r_u,r_v),
  cor(r_u,r_v,method="spearman")),8)
plot(r_u, r_v, pch=16,
     xlab="x", ylab="y = x^2")


# ======================================================
# 58_gruppi.R
# ======================================================
# Ordine esplicito dei morfotipi
r_g <- factor(fossili$morfotipo,
  levels=c("Rounded","Spiky"))
r_col <- c("#1D7890","#C57E42")[r_g]
plot(r_x,r_y,pch=c(16,17)[r_g],
  col=adjustcolor(r_col,alpha.f=.65),
  xlab="Diametro totale [um]",
  ylab="Diaframma [um]")
legend("topleft",levels(r_g),
 col=c("#1D7890","#C57E42"),pch=16:17)


# ======================================================
# 59_lab_relazioni.R
# ======================================================
# Stesso seme, forme differenti
rL <- lab_relazioni(shape="line",
  noise=1, seed=17)
rQ <- lab_relazioni(shape="curve",
  noise=1, seed=17)
rbind(lineare=rL$indicatori,
      quadratica=rQ$indicatori)


# ======================================================
# 61_copertura.R
# ======================================================
# Posizioni deterministiche in metri
s_est <- seq(0,100,length.out=30)
s_nord <- 50 + 5*sin(s_est/8)
plot(s_est,s_nord,pch=16,asp=1,
     xlim=c(0,100),ylim=c(0,100),
     xlab="Est [m]",ylab="Nord [m]")


# ======================================================
# 62_griglia.R
# ======================================================
# E varia piu rapidamente di N
s_rete <- expand.grid(E=1:4,N=1:4)
s_rete$valore <- rep(1:4,4)
s_mat <- matrix(s_rete$valore,4,4)
s_pal <- colorRampPalette(
  c("#F0F4F3","#087C74"))(4)
image(1:4,1:4,s_mat,col=s_pal,
      xlab="Est [km]",
      ylab="Nord [km]",asp=1)


# ======================================================
# 63_permutazione.R
# ======================================================
# Trasporre cambia solo la posizione
s_z2 <- as.vector(t(s_mat))
all(sort(s_z2)==sort(s_rete$valore))
rbind(A=table(s_rete$valore),
      B=table(s_z2))


# ======================================================
# 64_simboli.R
# ======================================================
# Le aree sono nel rapporto 1:4:9
s_v <- c(1,4,9)
symbols(1:3,rep(1,3),
  circles=sqrt(s_v),inches=.35,
  bg="#1D7890",fg="#1D7890",
  xlab="Posizione dimostrativa",
  ylab="",ylim=c(0,2))


# ======================================================
# 66_lab_mappa.R
# ======================================================
# Stesso seme: stesso rumore
s0 <- lab_mappa(gradient=0,seed=17)
s4 <- lab_mappa(gradient=4,seed=17)
rbind(A=s4$indicatori,
      B=s0$indicatori)
range(s4$dati$x)            # 1, 20


# ======================================================
# 67_log_distanze.R
# ======================================================
# Riferimento esplicito: 1 mm
l_x <- c(1,2,5,10,20,50,100)
l_ref <- 1
cbind(mm=l_x,log10=log10(l_x/l_ref))
# Due rapporti pari a 10
diff(log10(c(1,10,100)/l_ref))


# ======================================================
# 68_dominio.R
# ======================================================
# Grana in mm; riferimento 1 mm
l_g <- rocce$grana_mm
l_ref <- 1
stopifnot(all(is.finite(l_g)),
          all(l_g > 0))
l_y <- log(l_g/l_ref)
head(l_y)


# ======================================================
# 69_asse_variabile.R
# ======================================================
# Scala grafica; dati invariati
plot(l_g,seq_along(l_g),log="x",
     xlab="Grana [mm]",ylab="Indice")
# Nuova variabile: log naturale
hist(l_y,breaks=12,
     xlab="log(grana / 1 mm)",
     main="Grana trasformata")


# ======================================================
# 70_geometrica.R
# ======================================================
# Misure in mm; riferimento 1 mm
l_es <- c(1,4,16)
c(aritmetica=mean(l_es),
  geometrica=l_ref*
    exp(mean(log(l_es/l_ref))))


# ======================================================
# 71_sintesi.R
# ======================================================
# Riferimento delle misure: 1 mm
l_a <- c(1,4,16)
l_b <- c(7,7,7)
l_medie <- function(v) {
  c(aritmetica=mean(v),
    geometrica=exp(mean(log(v/1))))
}
rbind(A=l_medie(l_a),B=l_medie(l_b))


# ======================================================
# 72_standardizzare.R
# ======================================================
# Esempio deterministico asimmetrico
l_s <- c(1,2,3,12)
stopifnot(sd(l_s)>0)
l_z <- as.numeric(scale(l_s))
c(media=mean(l_z),sd=sd(l_z))
all.equal(l_z,
  (l_s-mean(l_s))/sd(l_s))


# ======================================================
# 73_lab_scale.R
# ======================================================
# Stesso seme; diversa dispersione
lA <- lab_scale(sdlog=.7,seed=17)
lB <- lab_scale(sdlog=1.2,seed=17)
rbind(A=lA$indicatori,
      B=lB$indicatori)
head(lA$dati)


# ======================================================
# 74_ggplot_opzionale.R
# ======================================================
# Estensione facoltativa
if (requireNamespace("ggplot2",
    quietly = TRUE)) {
  g74 <- ggplot2::ggplot(fossili,
    ggplot2::aes(diametro_tot_um,
                diametro_int_um,
                colour = morfotipo))
  print(g74 + ggplot2::geom_point())
}


# ======================================================
# 75_figura.R
# ======================================================
# Coppie riferite allo stesso fossile
col75 <- c("#1D7890", "#C57E42")
i75 <- as.integer(fossili$morfotipo)
plot(fossili$diametro_tot_um,
     fossili$diametro_int_um,
     col = col75[i75], pch = 16,
     xlab = "D totale [micrometri]",
     ylab = "D interno [micrometri]")
legend("topleft",
  legend = levels(fossili$morfotipo),
  col = col75, pch = 16, bty = "n")


# ======================================================
# 76_didascalia.R
# ======================================================
cap76 <- c(
 "Diametri dei 160 fossili simulati.",
 "80 Rounded, 80 Spiky; un punto",
 "per individuo. Unita': micrometri.",
 "Relazione positiva nel campione.",
 "Fonte: fossili_simulati.csv.")
dir.create("Risultati",
           showWarnings = FALSE)
writeLines(cap76,
 "Risultati/Fossili_didascalia.txt")


# ======================================================
# 77_esporta.R
# ======================================================
# Un dispositivo separato per il PDF
salva77 <- function() {
  pdf("Risultati/Fossili.pdf",
      width = 7.2, height = 4.8)
  on.exit(dev.off())
  source("Codice/75_figura.R",
         local = TRUE)
}
salva77()


# Chiudere il documento delle figure.
dev.off()
