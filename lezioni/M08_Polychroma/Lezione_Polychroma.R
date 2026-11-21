# Polychroma M08: frammenti eseguibili nell’ordine della presentazione.
# Aprire Polychroma_M08.Rproj e lanciare source("Lezione_Polychroma.R", echo=TRUE).
source("setup.R", encoding="UTF-8")
dir.create("Risultati", showWarnings=FALSE)
pdf("Risultati/Figure_lezione.pdf", width=9, height=5.5)

# 003_dati.R
# Aprire il progetto Polychroma_M08.
source("setup.R", encoding = "UTF-8")
dim(d)
head(d[, c("id", "SiO2", "densita")])
# Un identificativo per campione.
stopifnot(!anyDuplicated(d$id))

# 006_etichette.R
# Colonne con ruoli diversi.
id <- d$id
etichette <- d$litologia_generatrice
X <- as.matrix(d[v])
stopifnot(!"id" %in% colnames(X),
  !"litologia_generatrice" %in%
    colnames(X))

# 007_matrice.R
# Evitare selezioni per posizione.
v <- c("SiO2", "CaO", "MgO", "FeO",
       "densita", "grana_mm",
       "colore", "fossili")
X <- as.matrix(d[v])
stopifnot(all(is.finite(X)),
  all(apply(X, 2, sd) > 0))
dim(X)

# 008_unita.R
# Stessa granulometria: mm oppure um.
a <- X[, c("SiO2", "grana_mm")]
b <- a
b[, "grana_mm"] <- 1000 * b[, "grana_mm"]
c(mm = as.numeric(dist(a))[1],
  um = as.numeric(dist(b))[1])

# 009_distanza.R
# Due righe della matrice originale.
scarti <- X[1, ] - X[2, ]
sqrt(sum(scarti^2))
# Stesso valore nella matrice distanze.
as.matrix(dist(X))[1, 2]

# 011_standardizzazione.R
Z <- scale(X, center = TRUE,
           scale = TRUE)
medie <- attr(Z, "scaled:center")
devstd <- attr(Z, "scaled:scale")
# Verificare la trasformazione.
round(colMeans(Z), 10)
apply(Z, 2, sd)

# 012_nuovo_campione.R
# Esempio di applicazione ai primi casi.
# Non sono dati nuovi indipendenti.
nuovi <- X[1:3, , drop = FALSE]
Znuovi <- scale(nuovi,
  center = medie, scale = devstd)
max(abs(Znuovi - Z[1:3, ]))

# 013_controlli.R
data.frame(variabile = colnames(X),
  mancanti = colSums(is.na(X)),
  deviazione = apply(X, 2, sd))
# Un valore NA non significa zero.
# Una colonna costante non ammette z-score.

# 014_correlazioni.R
# Stesse relazioni, nuove unità.
max(abs(cor(X) - cor(Z)))
round(cor(Z)[1:4, 1:4], 2)
# Zero è atteso entro l'errore numerico.

# 015_duplicazione.R
# Ripetere SiO2 cambia la distanza.
Zd <- cbind(Z, SiO2_copia = Z[, "SiO2"])
c(prima = as.matrix(dist(Z))[1, 2],
  dopo = as.matrix(dist(Zd))[1, 2])

# 016_pesi.R
# Esempio: dimezzare il peso di SiO2.
pesi <- rep(1, ncol(Z))
pesi[1] <- 0.5
Zw <- sweep(Z, 2, sqrt(pesi), "*")
as.matrix(dist(Zw))[1:3, 1:3]

# 017_ridondanza.R
# Esaminare la struttura, non una soglia sola.
R <- cor(Z)
round(R, 2)
# Gli ossidi sono una parte di una
# composizione: la chiusura conta.

# 018_fossili.R
f <- read.csv("Dati/fossili_simulati.csv")
M <- as.matrix(f[c("diametro_tot_um",
  "diametro_int_um", "spessore_um")])
max(abs(M[, 1] - M[, 2] - 2*M[, 3]))
prcomp(M, scale. = TRUE)$sdev

# 019_rango.R
sv_f <- svd(scale(M))$d
sv_f / max(sv_f)
# La terza direzione è trascurabile
# alla precisione dei dati forniti.
sum(sv_f > max(sv_f) * 1e-7)

# 020_chiusura.R
parti <- c("SiO2", "CaO", "MgO",
           "FeO", "resto_wt")
comp <- as.matrix(d[parti])
range(rowSums(comp))
max(abs(rowSums(comp) - 100))

# 021_correlazione_chiusura.R
set.seed(17)
assolute <- matrix(rlnorm(450), ncol = 3)
frazioni <- assolute / rowSums(assolute)
c(prima = cor(assolute)[1, 2],
  dopo = cor(frazioni)[1, 2])

# 022_rapporti.R
# Il totale si semplifica nel rapporto.
lr_prima <- log(assolute[, 1] /
                assolute[, 2])
lr_dopo <- log(frazioni[, 1] /
               frazioni[, 2])
max(abs(lr_prima - lr_dopo))

# 023_clr.R
# Solo le cinque parti chimiche.
stopifnot(all(comp > 0))
log_comp <- log(comp)
clr <- log_comp - rowMeans(log_comp)
head(clr, 3)
max(abs(rowSums(clr)))

# 024_pca_clr.R
# PCA nella geometria CLR dichiarata.
pc_clr <- prcomp(clr, center = TRUE,
                 scale. = FALSE)
pc_clr$sdev
# Ultima SD circa zero: vincolo noto.

# 028_prodotto_scalare.R
z_es <- c(2, 1)
v_es <- c(0.8, 0.6)
sum(v_es^2)  # norma unitaria
t_es <- sum(z_es * v_es)
t_es

# 029_proiezione.R
z_hat <- t_es * v_es
res_es <- z_es - z_hat
z_hat
# Proiezione e residuo sono ortogonali.
sum(res_es * v_es)

# 031_covarianza.R
S <- crossprod(Z) / (nrow(Z) - 1)
max(abs(S - cov(Z)))
# Su colonne standardizzate, S è
# anche la matrice di correlazione.
max(abs(S - cor(X)))

# 034_ortogonali.R
v2_es <- c(-0.6, 0.8)
sum(v_es * v2_es)
sum(v2_es^2)
# Due direzioni per descrivere il piano.

# 036_svd.R
# d contiene i valori singolari.
sv <- svd(Z)
lambda_svd <- sv$d^2 / (nrow(Z) - 1)
lambda_svd
max(abs(crossprod(sv$v) - diag(8)))

# 038_prcomp.R
pc <- prcomp(X, center = TRUE,
             scale. = TRUE)
head(pc$x[, 1:2])  # scores
pc$rotation[, 1:2] # direzioni
pc$center          # medie
pc$scale           # deviazioni standard

# 039_autovalori.R
lam <- pc$sdev^2
lam
sum(lam) # otto colonne di varianza 1
max(abs(lam - lambda_svd))
# Il confronto controlla la convenzione n-1.

# 040_scores_covarianza.R
T <- pc$x
cov_T <- cov(T)
max(abs(cov_T - diag(lam)))
# Le piccole differenze sono numeriche.

# 041_dipendenza_curva.R
# Relazione deterministica non lineare.
u <- seq(-2, 2, length.out = 41)
y_curva <- u^2
cor(u, y_curva)
plot(u, y_curva, pch = 19,
  xlab = "x", ylab = "x^2")

# 042_segno.R
# Ricostruzione della sola PC1.
R1 <- pc$x[, 1] %o% pc$rotation[, 1]
R1_opposta <- (-pc$x[, 1]) %o%
              (-pc$rotation[, 1])
max(abs(R1 - R1_opposta))

# 045_quote.R
quota <- pc$sdev^2 / sum(pc$sdev^2)
data.frame(PC = 1:8,
  quota = quota, cumulata = cumsum(quota))

# 046_cumulata.R
barplot(100 * quota, names.arg = 1:8,
  xlab = "Componente",
  ylab = "Varianza (%)")
cumsum(quota)

# 047_distanze_proiezione.R
DT <- as.matrix(dist(pc$x))
D2 <- as.matrix(dist(pc$x[, 1:2]))
max(D2 - DT)
# Differenza non positiva, salvo
# arrotondamenti numerici.

# 048_loadings.R
pc$rotation[, 1]
# Contributi della prima riga allo score.
a48 <- pc$rotation[, 1]
contributi_riga <- Z[1, ] * a48
sum(contributi_riga)
pc$x[1, 1]

# 049_correlazioni_pc.R
cor_PC <- sweep(pc$rotation, 2,
                pc$sdev, "*")
round(cor_PC[, 1:2], 3)
max(abs(cor_PC - cor(Z, pc$x)))

# 051_qualita.R
peso_PC1 <- pc$rotation[, 1]^2
qualita2 <- rowSums(cor_PC[, 1:2]^2)
data.frame(variabile = v,
  peso_PC1 = peso_PC1,
  rappresentata_2PC = qualita2)

# 053_ricostruzione.R
Z2 <- pc$x[, 1:2, drop = FALSE] %*%
  t(pc$rotation[, 1:2, drop = FALSE])
sqrt(mean((Z - Z2)^2))
# RMSE nelle unità standardizzate.

# 054_errore_ricostruzione.R
errore <- sum((Z - Z2)^2)
teoria <- (nrow(Z)-1) * sum(lam[3:8])
c(calcolato = errore, teoria = teoria)
errore / sum(Z^2)

# 055_unita_originali.R
X2 <- sweep(Z2, 2, pc$scale, "*")
X2 <- sweep(X2, 2, pc$center, "+")
head(cbind(originale = X[, "densita"],
  ricostruita = X2[, "densita"]))

# 056_dimensioni.R
# Perdita relativa per q = 1,...,8.
data.frame(q = 1:8,
  conservata = cumsum(quota),
  persa = 1 - cumsum(quota))

# 057_predict_pca.R
# Esempio su righe già presenti:
# verifica della trasformazione.
scores_nuovi <- predict(pc, X[1:3, ])
max(abs(scores_nuovi - pc$x[1:3, ]))
# Per veri nuovi campioni mantenere
# nomi, unità e ordine delle variabili.

# 059_obiettivo.R
# Sei punti illustrativi, due gruppi.
u59 <- rbind(c(1,1), c(1.2,2.1),
 c(2.2,1.35), c(5.3,2.4),
 c(6.7,2.9), c(6,1.6))
g59 <- rep(1:2, each = 3)
cent59 <- rowsum(u59, g59) / 3
# Somma dei quadrati delle distanze.
sum((u59 - cent59[g59, ])^2)

# 060_centroide.R
# Tre osservazioni di un gruppo.
A60 <- rbind(c(0,0), c(2,0),
             c(1,3))
mu60 <- colMeans(A60)
mu60  # Il centroide e' (1, 1).
w60 <- function(candidato) {
 sum(sweep(A60, 2, candidato)^2)
}
c(centroide = w60(mu60),
  alternativa = w60(c(1,2)))

# 061_assegnazione.R
# Centri provvisori dello schema.
cent61 <- rbind(c(1,1), c(6,3))
dist261 <- sapply(1:2, function(g) {
 rowSums(sweep(u59, 2,
               cent61[g, ])^2)
})
# Righe: punti. Colonne: centri.
round(dist261, 2)
max.col(-dist261,
        ties.method = "first")

# 062_aggiornamento.R
# Manteniamo i gruppi appena trovati.
g62 <- max.col(-dist261,
              ties.method = "first")
cent62 <- rowsum(u59, g62) /
 as.vector(table(g62))
cent62
# Controllo prima e dopo le medie.
c(prima = sum((u59-
               cent61[g62, ])^2),
  dopo = sum((u59-
              cent62[g62, ])^2))

# 063_iterazioni.R
# Lloyd: una dimostrazione esplicita.
cent63 <- cent61
W63 <- numeric(5)
for (passo in 1:5) {
 dd <- sapply(1:2, function(g)
  rowSums(sweep(u59,2,cent63[g,])^2))
 lab <- max.col(-dd,
                ties.method="first")
 cent63 <- rowsum(u59,lab) /
   as.vector(table(lab))
 scarti63 <- u59-cent63[lab,]
 W63[passo] <- sum(scarti63^2)
}
W63

# 064_avvii.R
# Stessa matrice, singoli avvii.
set.seed(818)
W64 <- replicate(20,
 kmeans(Z, centers=3, nstart=1,
        iter.max=100)$tot.withinss)
range(W64)
# Ora molte inizializzazioni.
set.seed(816)
km <- kmeans(Z, 3, nstart=50,
             iter.max=100)
km$tot.withinss

# 065_kmeans.R
# Otto colonne standardizzate in Z.
set.seed(816)
km <- kmeans(Z, centers = 3,
             nstart = 50,
             iter.max = 100)
km$size
round(km$centers, 2)
c(WSS = km$tot.withinss,
  totale = km$totss)

# 066_controllo_wss.R
# Un centroide per ciascuna riga.
centri66 <- km$centers[
 km$cluster, , drop = FALSE]
dist266 <- rowSums((Z-centri66)^2)
c(manuale = sum(dist266),
  kmeans = km$tot.withinss)
stopifnot(abs(sum(dist266)-
 km$tot.withinss) < 1e-8)

# 067_scomposizione.R
# Variabilita' totale, entro e fra.
T67 <- sum(scale(Z,scale=FALSE)^2)
W67 <- km$tot.withinss
B67 <- sum(km$size *
             rowSums(km$centers^2))
c(T = T67, W = W67, B = B67)
stopifnot(abs(T67-W67-B67)<1e-8)

# 068_profili.R
# Le medie nelle unita' originali.
prof68 <- aggregate(d[v],
 list(cluster=km$cluster), mean)
prof68
# Oppure si inverte la scala di Z.
mu68 <- sweep(km$centers, 2,
 attr(Z,"scaled:scale"), "*")
mu68 <- sweep(mu68, 2,
 attr(Z,"scaled:center"), "+")
round(mu68[,c("SiO2","densita")],2)

# 069_piano_pca.R
# La PCA serve qui alla figura.
pc <- prcomp(Z, center=FALSE,
             scale.=FALSE)
q69 <- pc$sdev^2 / sum(pc$sdev^2)
plot(pc$x[,1:2], pch=19,asp=1,
     col=km$cluster,
     xlab="PC1", ylab="PC2")
sum(q69[1:2])

# 070_distanze_pc.R
# Tutte le PC: rotazione ortogonale.
D70 <- as.matrix(dist(Z))
T70 <- as.matrix(dist(pc$x))
max(abs(D70-T70))
# Due PC: le distanze si contraggono.
Q70 <- as.matrix(dist(pc$x[,1:2]))
stopifnot(max(Q70-D70)<1e-8)

# 071_variabili.R
# Una diversa domanda di somiglianza.
chim71 <- c("SiO2","CaO","MgO","FeO")
Z71 <- scale(d[chim71])
set.seed(819)
km71 <- kmeans(Z71,3,nstart=50)
# Tabella, senza confrontare i nomi.
table(tutte=km$cluster,
      chimica=km71$cluster)

# 074_suddivisione.R
# Una suddivisione di un gruppo.
g74a <- rep(1, nrow(u59))
g74b <- rep(1:2, each=3)
w74 <- function(lab) {
 cent <- rowsum(u59,lab) /
   as.vector(table(lab))
 sum((u59-cent[lab,,drop=FALSE])^2)
}
c(un_gruppo=w74(g74a),
  due_gruppi=w74(g74b))

# 075_confronto_k.R
# Stessa geometria per tutti i k.
set.seed(817)
ks <- 2:7
fits <- lapply(ks, function(k)
 kmeans(Z, k, nstart=50,
        iter.max=100))
W75 <- vapply(fits, function(m)
 m$tot.withinss, numeric(1))
data.frame(k=ks, WSS=W75)
plot(ks,W75,type="b",pch=19,
     xlab="k",ylab="WSS")

# 076_coesione_separazione.R
# Un campione e il proprio gruppo.
D <- dist(Z)
DD76 <- as.matrix(D)
i76 <- 1
g76 <- km$cluster
stessi76 <- which(g76==g76[i76] &
          seq_along(g76)!=i76)
a76 <- mean(DD76[i76,stessi76])
altri76 <- setdiff(unique(g76),
                   g76[i76])
b76 <- min(sapply(altri76,function(g)
 mean(DD76[i76,g76==g])))
c(a=a76,b=b76)

# 077_silhouette.R
# Formula per il campione R001.
s77 <- (b76-a76)/max(a76,b76)
s77
# Funzione fornita nel file
# R/funzioni_analisi.R.
sil <- silhouette_base(km$cluster,D)
stopifnot(abs(s77-sil[i76])<1e-8)
summary(sil)

# 078_silhouette_grafico.R
# Distribuzione delle 90 silhouette.
ord78 <- order(km$cluster,sil)
barplot(sil[ord78], space=0,
 col=km$cluster[ord78], border=NA,
 ylab="Silhouette",xlab="Campioni")
abline(h=0,lty=2)
c(media=mean(sil),minimo=min(sil),
  massimo=max(sil))

# 079_silhouette_k.R
# Le soluzioni di k = 2,...,7.
S79 <- vapply(fits, function(m)
 mean(silhouette_base(m$cluster,D)),
 numeric(1))
indici <- data.frame(k=ks,WSS=W75,
                      silhouette=S79)
indici
plot(ks,S79,type="b",pch=19,
 xlab="k",ylab="Silhouette media")

# 080_quattro_gruppi.R
# Un'alternativa esplicita: k = 4.
set.seed(1601)
km4 <- kmeans(Z,4,nstart=50,
              iter.max=100)
km4$size
table(k3=km$cluster,k4=km4$cluster)
aggregate(d[v],
 list(cluster=km4$cluster),mean)

# 081_riepilogo.R
# Indici per le stesse soluzioni.
data.frame(k=ks,
 WSS=round(W75,2),
 silhouette=round(S79,3),
 minimo_gruppo=vapply(fits,
  function(m)min(m$size),numeric(1)))
# La scelta non legge la litologia.
ks[which.max(S79)]

# 085_costo_fusione.R
# Due gruppi, una sola coordinata.
A85 <- c(0,2)
B85 <- c(5,7)
w85 <- function(x) sum((x-mean(x))^2)
delta85 <- w85(c(A85,B85))-
           w85(A85)-w85(B85)
f85 <- length(A85)*length(B85) /
 (length(A85)+length(B85)) *
 (mean(A85)-mean(B85))^2
c(incremento=delta85,formula=f85)

# 086_ward.R
# Distanze euclidee ordinarie.
D <- dist(Z, method="euclidean")
h <- hclust(D, method="ward.D2")
plot(h,labels=FALSE,
     xlab="Campioni",sub="Ward.D2",
     ylab="Altezza")
tail(h$height,3)

# 087_altezza.R
# Prima fusione: due campioni.
f87 <- -h$merge[1, ]
delta87 <- sum((Z[f87[1], ]-
                Z[f87[2], ])^2)/2
c(deltaW=delta87,
  altezza2_su_2=h$height[1]^2/2)
stopifnot(abs(delta87-
             h$height[1]^2/2)<1e-8)

# 088_taglio.R
# Taglio della stessa gerarchia.
ward <- cutree(h, k=3)
table(ward)
plot(h,labels=FALSE,sub="Ward.D2")
rect.hclust(h,k=3,border=1:3)
# L'albero resta lo stesso.
ward4 <- cutree(h,k=4)
table(tre=ward,quattro=ward4)

# 090_confronto_ward.R
# Stessi campioni, stessa scala, k=3.
tab90 <- table(Kmeans=km$cluster,
               Ward=ward)
tab90
# I numeri dei gruppi non sono nomi
# geologici ne' ordini di grandezza.

# 091_coappartenenza.R
# Confronto senza nomi dei gruppi.
A91 <- outer(km$cluster,
              km$cluster,"==")
B91 <- outer(ward,ward,"==")
sopra91 <- upper.tri(A91)
mean(A91[sopra91]==B91[sopra91])
# Confronto non sensibile ai nomi.
all(A91==B91)

# 092_wss_ward.R
# WSS della partizione di Ward.
mu92 <- rowsum(Z,ward) /
         as.vector(table(ward))
W92 <- sum((Z-mu92[ward,])^2)
c(Kmeans=km$tot.withinss,Ward=W92)
# Nello stesso spazio, confrontiamo
# la stessa quantita' geometrica.

# 095_avvii.R
set.seed(818)
W_avvii <- replicate(30, {
  m <- kmeans(Z, 3, nstart = 1,
              iter.max = 100)
  m$tot.withinss
})
range(W_avvii)

# 096_perturbazione.R
# Una perturbazione nelle unità di Z.
set.seed(819)
Zp <- Z + matrix(rnorm(length(Z),
  sd = 0.4), nrow(Z))
kp <- kmeans(Zp, 3, nstart = 50,
             iter.max = 100)
accordo_coppie(km$cluster, kp$cluster)

# 097_coappartenenza.R
a <- c(1, 1, 2, 2, 3, 3)
b <- c(3, 3, 1, 1, 2, 2)
# I numeri dei gruppi sono arbitrari.
mean(a == b)
accordo_coppie(a, b)  # vale 1
indice_rand_corretto(a, b)

# 098_sottocampione.R
# Una delle quaranta estrazioni.
set.seed(820)
idx <- sort(sample(1:nrow(Z), 72))
ks <- kmeans(Z[idx, ], 3, nstart = 30,
             iter.max = 100)
outer(ks$cluster, ks$cluster, "==")[1:4, 1:4]

# 099_variabili.R
chim <- c("SiO2", "CaO", "MgO", "FeO")
set.seed(819)
kc <- kmeans(scale(d[chim]), 3,
              nstart = 50)
accordo_coppie(km$cluster, kc$cluster)

# 100_campioni_distanti.R
delta <- Z - km$centers[km$cluster, ]
d2_centro <- rowSums(delta^2)
soglia <- quantile(d2_centro, .95)
segnala <- d2_centro > soglia
d[segnala, c("id", v)]

# 101_profili_originali.R
profili <- aggregate(d[v],
  list(gruppo = km$cluster), mean)
profili[, c("gruppo", "SiO2",
             "densita", "grana_mm")]
# Esaminare anche dispersione e casi.

# 102_generatore.R
# L'etichetta non e stata usata nella stima.
generatore <- d$litologia_generatrice
table(gruppo = km$cluster, generatore)
indice_rand_corretto(km$cluster, generatore)

# 105_quattro_gruppi.R
set.seed(1601)
km4 <- kmeans(Z, 4, nstart = 50)
table(k3 = km$cluster, k4 = km4$cluster)
mean(silhouette_base(km4$cluster, dist(Z)))
aggregate(d[v], list(gruppo = km4$cluster), mean)

# 106_equivalenza.R
pa <- prcomp(X, center = TRUE,
             scale. = TRUE)
pb <- prcomp(scale(X), center = FALSE,
             scale. = FALSE)
max(abs(pa$sdev - pb$sdev))
max(abs(pa$x - pb$x))

# 107_tabella_finale.R
sil <- silhouette_base(km$cluster, dist(Z))
risultati <- data.frame(id = d$id,
  pc$x[, 1:2], kmeans = km$cluster,
  ward = cutree(h, k = 3), silhouette = sil)
write.csv(risultati, "Risultati/campioni.csv",
          row.names = FALSE)

dev.off()
