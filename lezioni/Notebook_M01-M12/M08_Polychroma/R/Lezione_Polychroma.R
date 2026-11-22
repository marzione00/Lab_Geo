# POLYCHROMA M08 - Esercitazioni svolte in R
# Aprire il progetto del modulo o il progetto generale dei notebook.
# Ogni sezione corrisponde al notebook indicato.


# M08_N01 - La matrice delle misure e le colonne da escludere
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M08_Polychroma"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M08_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M08_Polychroma o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M08_N01")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(8001)


# Campioni e variabili
# Seleziona le misure per nome: ID ed etichetta non entrano nella matrice.
r <- carica_dati("rocce_simulate.csv")
v <- c("SiO2", "CaO", "MgO", "FeO", "densita", "grana_mm", "colore", "fossili")
X <- as.matrix(r[v])
stopifnot(nrow(X)==90L, ncol(X)==8L, !anyDuplicated(r$id),
          all(is.finite(X)), all(apply(X,2,sd)>0))
Z <- scale(X)
D <- dist(Z)
dim(X)
head(data.frame(id=r$id,X),4)
data.frame(variabile=v,media=colMeans(X),SD=apply(X,2,sd))


# La colonna numerica non basta
# Mostra che il tipo numerico non decide da solo la matrice di analisi.
numeriche <- names(r)[vapply(r,is.numeric,logical(1))]
list(colonne_numeriche=numeriche,
     analisi_principale=v,
     numeriche_escluse=setdiff(numeriche,v))
table(r$litologia_generatrice)


# Conservare gli identificativi
tabella <- data.frame(id=r$id,Z,check.names=FALSE)
head(tabella,3)
stopifnot(identical(tabella$id,r$id))
# Salva una tabella leggibile conservando gli ID.
write.csv(tabella,percorso_risultati("matrice_standardizzata.csv"),row.names=FALSE)


# Variante svolta
ordinata <- tabella[order(tabella$SiO2),]
ordinata$generatore <- r$litologia_generatrice[match(ordinata$id,r$id)]
head(ordinata[,c("id","SiO2","generatore")],5)


# M08_N02 - Standardizzare non significa rendere indipendenti
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M08_Polychroma"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M08_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M08_Polychroma o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M08_N02")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(8002)


# Media e scala di riferimento
# Seleziona le misure per nome: ID ed etichetta non entrano nella matrice.
r <- carica_dati("rocce_simulate.csv")
v <- c("SiO2", "CaO", "MgO", "FeO", "densita", "grana_mm", "colore", "fossili")
X <- as.matrix(r[v])
stopifnot(nrow(X)==90L, ncol(X)==8L, !anyDuplicated(r$id),
          all(is.finite(X)), all(apply(X,2,sd)>0))
Z <- scale(X)
D <- dist(Z)
parametri <- data.frame(variabile=v,media=attr(Z,"scaled:center"),
 SD=attr(Z,"scaled:scale"),media_z=colMeans(Z),SD_z=apply(Z,2,sd))
parametri
stopifnot(max(abs(colMeans(Z)))<1e-12,
          max(abs(apply(Z,2,sd)-1))<1e-12)


# Le correlazioni rimangono
round(cor(Z),2)
c(massima_differenza_correlazioni=max(abs(cor(X)-cor(Z))))
plot(Z[,"SiO2"],Z[,"CaO"],pch=19,col="#087C74",
 xlab="SiO2 standardizzato",ylab="CaO standardizzato")
abline(h=0,v=0,lty=3,col="grey65")


# Una conversione delle unità
X_um <- X
X_um[,"grana_mm"] <- 1000*X_um[,"grana_mm"]
c(distanza_grezza_mm=as.matrix(dist(X))[1,2],
  distanza_grezza_um=as.matrix(dist(X_um))[1,2],
  differenza_standardizzata=max(abs(scale(X_um)-Z)))


# Variante svolta
nuovo <- X[1,,drop=FALSE]
nuovo_z <- sweep(sweep(nuovo,2,attr(Z,"scaled:center"),"-"),
                 2,attr(Z,"scaled:scale"),"/")
max(abs(nuovo_z-Z[1,,drop=FALSE]))


# M08_N03 - PCA: costruire nuovi assi
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M08_Polychroma"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M08_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M08_Polychroma o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M08_N03")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(8003)


# La stima sulle otto variabili
# Seleziona le misure per nome: ID ed etichetta non entrano nella matrice.
r <- carica_dati("rocce_simulate.csv")
v <- c("SiO2", "CaO", "MgO", "FeO", "densita", "grana_mm", "colore", "fossili")
X <- as.matrix(r[v])
stopifnot(nrow(X)==90L, ncol(X)==8L, !anyDuplicated(r$id),
          all(is.finite(X)), all(apply(X,2,sd)>0))
Z <- scale(X)
D <- dist(Z)
# La PCA conserva medie, scale e rotazione per eventuali nuovi campioni.
pc <- prcomp(X, center=TRUE, scale.=TRUE)
lambda <- pc$sdev^2
quota <- lambda/sum(lambda)
summary(pc)
head(pc$x[,1:2],4)
pc$rotation[,1:2]


# Scores come prodotti scalari
T_manuale <- Z %*% pc$rotation
c(differenza_scores=max(abs(T_manuale-pc$x)),
  errore_ortogonalita=max(abs(crossprod(pc$rotation)-diag(8))))
# Nuovi assi, stessi campioni: nessuna etichetta di gruppo viene usata.
plot(pc$x[,1:2],pch=19,col="#087C74",asp=1,
 xlab="PC1",ylab="PC2")
abline(h=0,v=0,lty=3,col="grey70")


# La proiezione di un singolo campione
contributi <- Z[1,]*pc$rotation[,1]
data.frame(variabile=v,z=Z[1,],coefficiente=pc$rotation[,1],
           contributo=contributi)
c(somma=sum(contributi),score_R=pc$x[1,1])


# Variante svolta
T_inv <- pc$x;V_inv <- pc$rotation
T_inv[,1] <- -T_inv[,1]
V_inv[,1] <- -V_inv[,1]
max(abs(T_inv %*% t(V_inv)-Z))


# M08_N04 - Varianza spiegata e perdita di informazione
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M08_Polychroma"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M08_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M08_Polychroma o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M08_N04")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(8004)


# Gli autovalori come varianze
# Seleziona le misure per nome: ID ed etichetta non entrano nella matrice.
r <- carica_dati("rocce_simulate.csv")
v <- c("SiO2", "CaO", "MgO", "FeO", "densita", "grana_mm", "colore", "fossili")
X <- as.matrix(r[v])
stopifnot(nrow(X)==90L, ncol(X)==8L, !anyDuplicated(r$id),
          all(is.finite(X)), all(apply(X,2,sd)>0))
Z <- scale(X)
D <- dist(Z)
# La PCA conserva medie, scale e rotazione per eventuali nuovi campioni.
pc <- prcomp(X, center=TRUE, scale.=TRUE)
lambda <- pc$sdev^2
quota <- lambda/sum(lambda)
varianza <- data.frame(PC=1:8,lambda=lambda,quota=quota,
 cumulata=cumsum(quota))
varianza
c(somma_autovalori=sum(lambda),varianza_totale=sum(apply(Z,2,var)))


# Quote singole e cumulate
posizioni <- barplot(100*quota,names.arg=1:8,col="#087C74",
 ylim=c(0,100),xlab="Componente",ylab="Varianza (%)")
lines(posizioni,100*cumsum(quota),type="b",pch=19,col="#C57E42",lwd=2)
abline(h=90,lty=3,col="grey45")
c(prime_due=100*sum(quota[1:2]),
  componenti_per_90=which(cumsum(quota)>=.90)[1])


# Quanta informazione manca nel piano
Z2 <- pc$x[,1:2,drop=FALSE] %*% t(pc$rotation[,1:2,drop=FALSE])
perdita <- sum((Z-Z2)^2)/sum(Z^2)
c(perdita_quadratica=perdita,quota_esclusa=1-sum(quota[1:2]))
stopifnot(abs(perdita-(1-sum(quota[1:2])))<1e-10)


# Variante svolta
data.frame(q=1:8,perdita=vapply(1:8,function(q) {
 rec <- pc$x[,seq_len(q),drop=FALSE] %*%
   t(pc$rotation[,seq_len(q),drop=FALSE])
 sum((Z-rec)^2)/sum(Z^2)
},numeric(1)))


# M08_N05 - Scores: che cosa rappresenta un punto?
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M08_Polychroma"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M08_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M08_Polychroma o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M08_N05")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(8005)


# Coordinate e identità del campione
# Seleziona le misure per nome: ID ed etichetta non entrano nella matrice.
r <- carica_dati("rocce_simulate.csv")
v <- c("SiO2", "CaO", "MgO", "FeO", "densita", "grana_mm", "colore", "fossili")
X <- as.matrix(r[v])
stopifnot(nrow(X)==90L, ncol(X)==8L, !anyDuplicated(r$id),
          all(is.finite(X)), all(apply(X,2,sd)>0))
Z <- scale(X)
D <- dist(Z)
# La PCA conserva medie, scale e rotazione per eventuali nuovi campioni.
pc <- prcomp(X, center=TRUE, scale.=TRUE)
lambda <- pc$sdev^2
quota <- lambda/sum(lambda)
scores <- data.frame(id=r$id,PC1=pc$x[,1],PC2=pc$x[,2])
head(scores)
write.csv(scores,percorso_risultati("scores_PC1_PC2.csv"),row.names=FALSE)


# La figura e la varianza rappresentata
g <- factor(r$litologia_generatrice)
palette <- c("#087C74","#C57E42","#7363AA")
plot(scores$PC1,scores$PC2,pch=as.integer(g)+14,col=palette[g],asp=1,
 xlab=sprintf("PC1 (%.2f%%)",100*quota[1]),
 ylab=sprintf("PC2 (%.2f%%)",100*quota[2]))
legend("topright",levels(g),col=palette,pch=15:17,bty="n",cex=.85)


# Distanza nel piano e distanza completa
d_full <- as.matrix(dist(Z))
d_piano <- as.matrix(dist(pc$x[,1:2]))
stopifnot(all(d_piano<=d_full+1e-10))
c(coppia_1_2_completa=d_full[1,2],coppia_1_2_piano=d_piano[1,2],
  contrazione_massima=max(d_full-d_piano))


# Variante svolta
scarto <- d_full-d_piano
scarto[!upper.tri(scarto)] <- -Inf
ij <- which(scarto==max(scarto),arr.ind=TRUE)[1,]
data.frame(id1=r$id[ij[1]],id2=r$id[ij[2]],
 completa=d_full[ij[1],ij[2]],piano=d_piano[ij[1],ij[2]])


# M08_N06 - Loadings e correlazioni con le componenti
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M08_Polychroma"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M08_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M08_Polychroma o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M08_N06")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(8006)


# Coefficienti degli assi
# Seleziona le misure per nome: ID ed etichetta non entrano nella matrice.
r <- carica_dati("rocce_simulate.csv")
v <- c("SiO2", "CaO", "MgO", "FeO", "densita", "grana_mm", "colore", "fossili")
X <- as.matrix(r[v])
stopifnot(nrow(X)==90L, ncol(X)==8L, !anyDuplicated(r$id),
          all(is.finite(X)), all(apply(X,2,sd)>0))
Z <- scale(X)
D <- dist(Z)
# La PCA conserva medie, scale e rotazione per eventuali nuovi campioni.
pc <- prcomp(X, center=TRUE, scale.=TRUE)
lambda <- pc$sdev^2
quota <- lambda/sum(lambda)
round(pc$rotation[,1:2],4)
colSums(pc$rotation^2)


# Correlazioni calcolate sulla scala corretta
corr_PC <- sweep(pc$rotation,2,pc$sdev,"*")
confronto <- cbind(coefficiente_PC1=pc$rotation[,1],
 correlazione_PC1=corr_PC[,1],correlazione_PC2=corr_PC[,2])
round(confronto,3)
stopifnot(max(abs(corr_PC-cor(Z,pc$x)))<1e-10)
barplot(t(corr_PC[,1:2]),beside=TRUE,horiz=TRUE,las=1,
 col=c("#087C74","#C57E42"),xlim=c(-1,1),
 xlab="Correlazione con la componente",cex.names=.75)
legend("bottomright",c("PC1","PC2"),fill=c("#087C74","#C57E42"),bty="n",cex=.8)


# La qualità per ciascuna variabile
qualita <- rowSums(corr_PC[,1:2,drop=FALSE]^2)
data.frame(variabile=v,quota_rappresentata=qualita,
 quota_omessa=1-qualita)[order(qualita),]
stopifnot(all(qualita>=0),all(qualita<=1+1e-10))


# Variante svolta
data.frame(variabile=v,due_PC=rowSums(corr_PC[,1:2]^2),
 tre_PC=rowSums(corr_PC[,1:3]^2))


# M08_N07 - Ricostruire con due componenti
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M08_Polychroma"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M08_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M08_Polychroma o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M08_N07")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(8007)


# Ricostruzione nella scala standardizzata
# Seleziona le misure per nome: ID ed etichetta non entrano nella matrice.
r <- carica_dati("rocce_simulate.csv")
v <- c("SiO2", "CaO", "MgO", "FeO", "densita", "grana_mm", "colore", "fossili")
X <- as.matrix(r[v])
stopifnot(nrow(X)==90L, ncol(X)==8L, !anyDuplicated(r$id),
          all(is.finite(X)), all(apply(X,2,sd)>0))
Z <- scale(X)
D <- dist(Z)
# La PCA conserva medie, scale e rotazione per eventuali nuovi campioni.
pc <- prcomp(X, center=TRUE, scale.=TRUE)
lambda <- pc$sdev^2
quota <- lambda/sum(lambda)
Z2 <- pc$x[,1:2,drop=FALSE] %*% t(pc$rotation[,1:2,drop=FALSE])
c(righe=nrow(Z2),colonne=ncol(Z2),RMSE=sqrt(mean((Z-Z2)^2)))
head(Z2,3)


# Ritorno alle unità originali
X2 <- sweep(sweep(Z2,2,pc$scale,"*"),2,pc$center,"+")
data.frame(variabile=v,osservato=X[1,],ricostruito=X2[1,],
 scarto=X[1,]-X2[1,])
plot(X[,"grana_mm"],X2[,"grana_mm"],pch=19,col="#087C74",
 xlab="Grana osservata (mm)",ylab="Grana ricostruita (mm)")
abline(0,1,col="#C57E42",lwd=2)


# L’errore e gli autovalori esclusi
SSE <- sum((Z-Z2)^2)
da_autovalori <- (nrow(Z)-1)*sum(lambda[-(1:2)])
c(SSE=SSE,da_autovalori=da_autovalori,differenza=SSE-da_autovalori)
RMSE_colonne <- sqrt(colMeans((X-X2)^2))
data.frame(variabile=v,RMSE_unita_originali=RMSE_colonne)


# Variante svolta
Ztutto <- pc$x %*% t(pc$rotation)
Xtutto <- sweep(sweep(Ztutto,2,pc$scale,"*"),2,pc$center,"+")
max(abs(X-Xtutto))


# M08_N08 - Ridondanza esatta nelle misure derivate
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M08_Polychroma"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M08_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M08_Polychroma o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M08_N08")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(8008)


# Il vincolo geometrico dei fossili
f <- carica_dati("fossili_simulati.csv")
nomi <- c("diametro_tot_um","diametro_int_um","spessore_um")
M <- as.matrix(f[nomi])
# Tutte e tre le misure sono in micrometri.
errore <- M[,1]-M[,2]-2*M[,3]
c(n=nrow(M),massimo_errore_identita=max(abs(errore)))
head(M,4)


# Una componente quasi nulla
pc_r <- prcomp(M,center=TRUE,scale.=TRUE)
pc_r$sdev
pc_r$sdev^2/sum(pc_r$sdev^2)
barplot(pc_r$sdev^2,names.arg=1:3,col="#7363AA",
 xlab="Componente",ylab="Varianza")


# Duplicare modifica il peso
Z <- scale(M[,1:2])
Zdup <- cbind(Z,copia_diametro_totale=Z[,1])
d2 <- sum((Z[1,]-Z[2,])^2)
d2_dup <- sum((Zdup[1,]-Zdup[2,])^2)
c(distanza2=d2,distanza2_con_copia=d2_dup,
  aumento_atteso=(Z[1,1]-Z[2,1])^2)


# Variante svolta
Mr <- scale(M)
rec <- pc_r$x[,1:2,drop=FALSE] %*% t(pc_r$rotation[,1:2,drop=FALSE])
max(abs(Mr-rec))


# M08_N09 - Composizioni e log-rapporti
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M08_Polychroma"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M08_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M08_Polychroma o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M08_N09")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(8009)


# Definire la composizione completa
# Seleziona le misure per nome: ID ed etichetta non entrano nella matrice.
r <- carica_dati("rocce_simulate.csv")
v <- c("SiO2", "CaO", "MgO", "FeO", "densita", "grana_mm", "colore", "fossili")
X <- as.matrix(r[v])
stopifnot(nrow(X)==90L, ncol(X)==8L, !anyDuplicated(r$id),
          all(is.finite(X)), all(apply(X,2,sd)>0))
Z <- scale(X)
D <- dist(Z)
parti <- c("SiO2","CaO","MgO","FeO","resto_wt")
C <- as.matrix(r[parti])
c(minimo=min(C),scarto_chiusura=max(abs(rowSums(C)-100)))
head(data.frame(id=r$id,somma_ossidi=rowSums(C[,1:4]),resto=C[,5]),4)
stopifnot(all(C>0),max(abs(rowSums(C)-100))<1e-5)


# Coordinate CLR e vincolo
L <- log(C)
clr <- L-rowMeans(L)
c(massima_somma_righe=max(abs(rowSums(clr))))
pc_clr <- prcomp(clr,center=TRUE,scale.=FALSE)
pc_clr$sdev
summary(pc_clr)


# Invarianza a un fattore comune
fattore <- seq(.5,2,length.out=nrow(C))
C2 <- C*fattore
clr2 <- log(C2)-rowMeans(log(C2))
max(abs(clr-clr2))
plot(pc_clr$x[,1:2],pch=19,col="#7363AA",asp=1,
 xlab="PC1 dei log-rapporti",ylab="PC2 dei log-rapporti")


# Variante svolta
esempio <- c(A=50,B=50,C=0)
valido <- all(esempio>0)
c(CLR_applicabile=valido)
# Il controllo precede log(); non viene aggiunta una costante agli zeri.
if (valido) log(esempio)-mean(log(esempio)) else
  "Prima distinguere zero strutturale, arrotondamento e limite analitico."


# M08_N10 - Preparare le distanze senza usare l’etichetta
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M08_Polychroma"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M08_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M08_Polychroma o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M08_N10")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(8010)


# La distanza nello spazio scelto
# Seleziona le misure per nome: ID ed etichetta non entrano nella matrice.
r <- carica_dati("rocce_simulate.csv")
v <- c("SiO2", "CaO", "MgO", "FeO", "densita", "grana_mm", "colore", "fossili")
X <- as.matrix(r[v])
stopifnot(nrow(X)==90L, ncol(X)==8L, !anyDuplicated(r$id),
          all(is.finite(X)), all(apply(X,2,sd)>0))
Z <- scale(X)
D <- dist(Z)
DD <- as.matrix(D)
c(campioni=nrow(DD),coppie=length(D),minimo=min(D),massimo=max(D))
stopifnot(max(abs(DD-t(DD)))<1e-12,all(diag(DD)==0))


# Contributi alla distanza
i <- 1;j <- 40
contributi <- (Z[i,]-Z[j,])^2
data.frame(variabile=v,contributo=contributi,
 quota=contributi/sum(contributi))
c(somma=sum(contributi),da_dist=DD[i,j]^2)
barplot(contributi,horiz=TRUE,las=1,col="#087C74",cex.names=.75,
 xlab="Contributo alla distanza quadratica")


# L’etichetta rimane fuori
metadati <- r[c("id","litologia_generatrice")]
stopifnot(!any(c("id","litologia_generatrice") %in% colnames(Z)))
prima_coppia <- data.frame(id1=r$id[i],id2=r$id[j],distanza=DD[i,j])
prima_coppia
write.csv(data.frame(id=r$id,Z),percorso_risultati("coordinate_per_clustering.csv"),row.names=FALSE)


# Variante svolta
pesi <- rep(1,ncol(Z));pesi[which(v=="grana_mm")] <- 2
Zp <- sweep(Z,2,sqrt(pesi),"*")
c(originale=DD[i,j]^2,pesata=as.matrix(dist(Zp))[i,j]^2)


# M08_N11 - K-means: centroidi e variabilità interna
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M08_Polychroma"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M08_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M08_Polychroma o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M08_N11")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(8011)


# Tre centroidi nella matrice standardizzata
# Seleziona le misure per nome: ID ed etichetta non entrano nella matrice.
r <- carica_dati("rocce_simulate.csv")
v <- c("SiO2", "CaO", "MgO", "FeO", "densita", "grana_mm", "colore", "fossili")
X <- as.matrix(r[v])
stopifnot(nrow(X)==90L, ncol(X)==8L, !anyDuplicated(r$id),
          all(is.finite(X)), all(apply(X,2,sd)>0))
Z <- scale(X)
D <- dist(Z)
# Gli avvii multipli confrontano soluzioni locali sullo stesso spazio.
set.seed(816)
km <- kmeans(Z, centers=3, nstart=50, iter.max=100)
km$size
round(km$centers,3)
c(WSS=km$tot.withinss,TSS=km$totss,quota_interna=km$tot.withinss/km$totss)


# Verificare centroidi e obiettivo
centri_manual <- do.call(rbind,lapply(1:3,function(g) colMeans(Z[km$cluster==g,,drop=FALSE])))
scarti <- Z-km$centers[km$cluster,,drop=FALSE]
distanza2 <- rowSums(scarti^2)
c(errore_centri=max(abs(centri_manual-km$centers)),
  WSS_diretta=sum(distanza2),WSS_R=km$tot.withinss)
stopifnot(abs(sum(distanza2)-km$tot.withinss)<1e-9)


# Centroidi nel piano di visualizzazione
# La PCA conserva medie, scale e rotazione per eventuali nuovi campioni.
pc <- prcomp(X, center=TRUE, scale.=TRUE)
lambda <- pc$sdev^2
quota <- lambda/sum(lambda)
colori <- c("#087C74", "#C57E42", "#7363AA", "#1D7890", "#A17B19", "#657180", "#B55353")
centri_pc <- km$centers %*% pc$rotation
plot(pc$x[,1:2],col=colori[km$cluster],pch=19,asp=1,
 xlab="PC1",ylab="PC2")
points(centri_pc[,1:2],pch=4,cex=2.5,lwd=3)
text(centri_pc[,1:2],labels=paste("Centro",1:3),pos=3,cex=.8)


# Variante svolta
set.seed(818)
uno <- kmeans(Z,3,nstart=1,iter.max=100)
c(WSS_un_avvio=uno$tot.withinss,WSS_50_avvii=km$tot.withinss,
  ARI=indice_rand_corretto(uno$cluster,km$cluster))


# M08_N12 - Silhouette: separazione relativa del campione
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M08_Polychroma"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M08_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M08_Polychroma o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M08_N12")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(8012)


# Distanze medie, non distanze dai centroidi
# Seleziona le misure per nome: ID ed etichetta non entrano nella matrice.
r <- carica_dati("rocce_simulate.csv")
v <- c("SiO2", "CaO", "MgO", "FeO", "densita", "grana_mm", "colore", "fossili")
X <- as.matrix(r[v])
stopifnot(nrow(X)==90L, ncol(X)==8L, !anyDuplicated(r$id),
          all(is.finite(X)), all(apply(X,2,sd)>0))
Z <- scale(X)
D <- dist(Z)
# Gli avvii multipli confrontano soluzioni locali sullo stesso spazio.
set.seed(816)
km <- kmeans(Z, centers=3, nstart=50, iter.max=100)
s <- silhouette_base(km$cluster,D)
c(media=mean(s),minimo=min(s),massimo=max(s))
# Ricostruisce a e b per il primo campione.
DD <- as.matrix(D); i <- 1L
stesso <- which(km$cluster==km$cluster[i]); stesso <- setdiff(stesso,i)
a <- mean(DD[i,stesso])
altri <- setdiff(unique(km$cluster),km$cluster[i])
b <- min(vapply(altri,function(g) mean(DD[i,km$cluster==g]),numeric(1)))
c(a=a,b=b,s_diretta=(b-a)/max(a,b),s_funzione=s[i])


# Leggere l’intera distribuzione
colori <- c("#087C74", "#C57E42", "#7363AA", "#1D7890", "#A17B19", "#657180", "#B55353")
ord <- order(km$cluster,s)
barplot(s[ord],col=colori[km$cluster[ord]],border=NA,space=0,
 xlab="Campioni ordinati entro il cluster",ylab="Silhouette",ylim=c(-.1,1))
abline(h=0,col="grey40"); abline(h=mean(s),lty=2,col="#C57E42")
aggregate(s,list(cluster=km$cluster),function(x)c(min=min(x),mediana=median(x),media=mean(x)))


# Il caso di un gruppo singolo
piccolo <- matrix(c(0,1,4,5),ncol=1)
gruppi <- c(1,1,2,3)
data.frame(x=piccolo[,1],gruppo=gruppi,
 silhouette=silhouette_base(gruppi,dist(piccolo)))
# Due gruppi su punti coincidenti: a=b=0, convenzione s=0.
silhouette_base(c(1,1,2,2),dist(matrix(0,4,1)))


# Variante svolta
d2 <- rowSums((Z-km$centers[km$cluster,,drop=FALSE])^2)
tab <- data.frame(id=r$id,cluster=km$cluster,silhouette=s,distanza2=d2)
head(tab[order(tab$silhouette),],6)


# M08_N13 - Confrontare k senza imporre la risposta attesa
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M08_Polychroma"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M08_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M08_Polychroma o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M08_N13")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(8013)


# La stessa matrice per ogni confronto
# Seleziona le misure per nome: ID ed etichetta non entrano nella matrice.
r <- carica_dati("rocce_simulate.csv")
v <- c("SiO2", "CaO", "MgO", "FeO", "densita", "grana_mm", "colore", "fossili")
X <- as.matrix(r[v])
stopifnot(nrow(X)==90L, ncol(X)==8L, !anyDuplicated(r$id),
          all(is.finite(X)), all(apply(X,2,sd)>0))
Z <- scale(X)
D <- dist(Z)
ks <- 2:7
set.seed(817)
modelli <- lapply(ks,function(k) kmeans(Z,k,nstart=50,iter.max=100))
tab <- data.frame(k=ks,
 WSS=vapply(modelli,function(m)m$tot.withinss,numeric(1)),
 silhouette=vapply(modelli,function(m)mean(silhouette_base(m$cluster,D)),numeric(1)))
tab
write.csv(tab,percorso_risultati("confronto_k.csv"),row.names=FALSE)


# Due criteri con significati diversi
op <- par(mfrow=c(1,2),mar=c(4,4,2,1))
plot(tab$k,tab$WSS,type="b",pch=19,col="#087C74",
 xlab="Numero di gruppi k",ylab="WSS")
plot(tab$k,tab$silhouette,type="b",pch=19,col="#7363AA",
 xlab="Numero di gruppi k",ylab="Silhouette media",ylim=c(0,.7))
par(op)
tab$riduzione_WSS <- c(NA,-diff(tab$WSS))
tab


# Interpretare dopo la scelta
scelto <- which.max(tab$silhouette)
migliore <- modelli[[scelto]]
c(k_selezionato=ks[scelto],silhouette=tab$silhouette[scelto])
table(cluster=migliore$cluster,generatore=r$litologia_generatrice)
indice_rand_corretto(migliore$cluster,r$litologia_generatrice)


# Variante svolta
pesi <- rep(1,ncol(Z)); pesi[which(v=="grana_mm")] <- 2
Zw <- sweep(Z,2,sqrt(pesi),"*"); Dw <- dist(Zw)
set.seed(817)
modelli_w <- lapply(ks,function(k)kmeans(Zw,k,nstart=50,iter.max=100))
data.frame(k=ks,s_originale=tab$silhouette,
 s_grana_peso2=vapply(modelli_w,function(m)mean(silhouette_base(m$cluster,Dw)),numeric(1)))


# M08_N14 - Visualizzare i cluster con PCA
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M08_Polychroma"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M08_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M08_Polychroma o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M08_N14")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(8014)


# Fit completo e proiezione
# Seleziona le misure per nome: ID ed etichetta non entrano nella matrice.
r <- carica_dati("rocce_simulate.csv")
v <- c("SiO2", "CaO", "MgO", "FeO", "densita", "grana_mm", "colore", "fossili")
X <- as.matrix(r[v])
stopifnot(nrow(X)==90L, ncol(X)==8L, !anyDuplicated(r$id),
          all(is.finite(X)), all(apply(X,2,sd)>0))
Z <- scale(X)
D <- dist(Z)
# Gli avvii multipli confrontano soluzioni locali sullo stesso spazio.
set.seed(816)
km <- kmeans(Z, centers=3, nstart=50, iter.max=100)
# La PCA conserva medie, scale e rotazione per eventuali nuovi campioni.
pc <- prcomp(X, center=TRUE, scale.=TRUE)
lambda <- pc$sdev^2
quota <- lambda/sum(lambda)
colori <- c("#087C74", "#C57E42", "#7363AA", "#1D7890", "#A17B19", "#657180", "#B55353")
plot(pc$x[,1:2],pch=19,col=colori[km$cluster],asp=1,
 xlab=sprintf("PC1 (%.2f%%)",100*quota[1]),
 ylab=sprintf("PC2 (%.2f%%)",100*quota[2]))
legend("topright",legend=paste("Cluster",1:3),col=colori[1:3],pch=19,bty="n")
c(varianza_visibile=sum(quota[1:2]),varianza_omessa=sum(quota[-(1:2)]))


# Usare tutte le componenti conserva le distanze
d_completo <- as.matrix(D)
d_scores <- as.matrix(dist(pc$x))
d_piano <- as.matrix(dist(pc$x[,1:2]))
c(errore_rotazione=max(abs(d_completo-d_scores)),
  massima_perdita=max(d_completo-d_piano))
stopifnot(max(abs(d_completo-d_scores))<1e-10,
          all(d_piano<=d_completo+1e-10))


# Clustering sul piano: una procedura distinta
set.seed(814)
km_piano <- kmeans(pc$x[,1:2],3,nstart=50,iter.max=100)
c(accordo_coppie=accordo_coppie(km$cluster,km_piano$cluster),
  ARI=indice_rand_corretto(km$cluster,km_piano$cluster))
table(spazio_completo=km$cluster,piano=km_piano$cluster)


# Variante svolta
set.seed(814)
km_tre <- kmeans(pc$x[,1:3],3,nstart=50,iter.max=100)
data.frame(componenti=c(2,3),varianza=c(sum(quota[1:2]),sum(quota[1:3])),
 ARI_con_fit_completo=c(indice_rand_corretto(km_piano$cluster,km$cluster),
                       indice_rand_corretto(km_tre$cluster,km$cluster)))


# M08_N15 - Profili: ritornare alle unità originali
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M08_Polychroma"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M08_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M08_Polychroma o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M08_N15")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(8015)


# Medie originali e medie standardizzate
# Seleziona le misure per nome: ID ed etichetta non entrano nella matrice.
r <- carica_dati("rocce_simulate.csv")
v <- c("SiO2", "CaO", "MgO", "FeO", "densita", "grana_mm", "colore", "fossili")
X <- as.matrix(r[v])
stopifnot(nrow(X)==90L, ncol(X)==8L, !anyDuplicated(r$id),
          all(is.finite(X)), all(apply(X,2,sd)>0))
Z <- scale(X)
D <- dist(Z)
# Gli avvii multipli confrontano soluzioni locali sullo stesso spazio.
set.seed(816)
km <- kmeans(Z, centers=3, nstart=50, iter.max=100)
profili_x <- aggregate(r[v],list(cluster=km$cluster),mean)
profili_z <- aggregate(as.data.frame(Z),list(cluster=km$cluster),mean)
round(profili_x,3)
round(profili_z,3)
write.csv(profili_x,percorso_risultati("profili_unita_originali.csv"),row.names=FALSE)


# Un grafico dei profili standardizzati
colori <- c("#087C74", "#C57E42", "#7363AA", "#1D7890", "#A17B19", "#657180", "#B55353")
op <- par(mar=c(7,4,2,1))
matplot(seq_along(v),t(as.matrix(profili_z[,-1])),type="b",pch=1:3,lty=1,
 col=colori[1:3],xaxt="n",xlab="",ylab="Media standardizzata",
 ylim=c(min(profili_z[,-1])-.1,max(profili_z[,-1])+.65))
axis(1,at=seq_along(v),labels=v,las=2,cex.axis=.85)
abline(h=0,lty=3,col="grey50")
legend("topright",legend=paste("Cluster",1:3),col=colori[1:3],pch=1:3,lty=1,bty="n",horiz=TRUE,cex=.8)
par(op)


# Verifica inversa e metadati del generatore
centri_x <- sweep(sweep(km$centers,2,attr(Z,"scaled:scale"),"*"),
                  2,attr(Z,"scaled:center"),"+")
max(abs(centri_x-as.matrix(profili_x[,-1])))
table(cluster=km$cluster,generatore=r$litologia_generatrice)


# Variante svolta
do.call(rbind,lapply(1:3,function(g){
 x <- r$grana_mm[km$cluster==g]
 data.frame(cluster=g,media=mean(x),mediana=median(x),Q1=unname(quantile(x,.25)),
            Q3=unname(quantile(x,.75)),minimo=min(x),massimo=max(x))
}))


# M08_N16 - Ward: una gerarchia senza fissare subito k
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M08_Polychroma"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M08_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M08_Polychroma o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M08_N16")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(8016)


# Costruire e tagliare la gerarchia
# Seleziona le misure per nome: ID ed etichetta non entrano nella matrice.
r <- carica_dati("rocce_simulate.csv")
v <- c("SiO2", "CaO", "MgO", "FeO", "densita", "grana_mm", "colore", "fossili")
X <- as.matrix(r[v])
stopifnot(nrow(X)==90L, ncol(X)==8L, !anyDuplicated(r$id),
          all(is.finite(X)), all(apply(X,2,sd)>0))
Z <- scale(X)
D <- dist(Z)
# Ward.D2 riceve le distanze euclidee, senza elevarle al quadrato a mano.
h <- hclust(D, method="ward.D2")
ward <- cutree(h, k=3)
plot(h,labels=FALSE,hang=-1,main="Gerarchia di Ward",xlab="90 campioni",
 sub="",ylab="Altezza di Ward.D2")
rect.hclust(h,k=3,border=c("#087C74","#C57E42","#7363AA"))
table(ward)


# Ricostruire l’aumento della WSS
membri <- vector("list",nrow(Z)-1)
delta <- numeric(nrow(Z)-1)
for(t in seq_len(nrow(h$merge))){
 # Valori negativi: singole righe; positivi: fusioni precedenti.
 a <- h$merge[t,1]; b <- h$merge[t,2]
 A <- if(a<0) -a else membri[[a]]
 B <- if(b<0) -b else membri[[b]]
 muA <- colMeans(Z[A,,drop=FALSE]); muB <- colMeans(Z[B,,drop=FALSE])
 delta[t] <- length(A)*length(B)/(length(A)+length(B))*sum((muA-muB)^2)
 membri[[t]] <- c(A,B)
}
c(errore_identita=max(abs(h$height^2/2-delta)),
 somma_incrementi=sum(delta),TSS=sum(Z^2))
tail(data.frame(fusione=seq_along(delta),altezza=h$height,delta_W=delta),5)


# Confronto con k-means
# Gli avvii multipli confrontano soluzioni locali sullo stesso spazio.
set.seed(816)
km <- kmeans(Z, centers=3, nstart=50, iter.max=100)
table(kmeans=km$cluster,Ward=ward)
c(accordo_coppie=accordo_coppie(km$cluster,ward),
 ARI=indice_rand_corretto(km$cluster,ward))


# Variante svolta
ward4 <- cutree(h,k=4)
set.seed(1601)
km4 <- kmeans(Z,4,nstart=50,iter.max=100)
table(Ward=ward4,kmeans=km4$cluster)
c(ARI=indice_rand_corretto(ward4,km4$cluster),
 silhouette_Ward=mean(silhouette_base(ward4,D)),
 silhouette_kmeans=mean(silhouette_base(km4$cluster,D)))


# M08_N17 - Stabilità senza confrontare i nomi dei cluster
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M08_Polychroma"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M08_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M08_Polychroma o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M08_N17")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(8017)


# Una permutazione delle etichette
# Seleziona le misure per nome: ID ed etichetta non entrano nella matrice.
r <- carica_dati("rocce_simulate.csv")
v <- c("SiO2", "CaO", "MgO", "FeO", "densita", "grana_mm", "colore", "fossili")
X <- as.matrix(r[v])
stopifnot(nrow(X)==90L, ncol(X)==8L, !anyDuplicated(r$id),
          all(is.finite(X)), all(apply(X,2,sd)>0))
Z <- scale(X)
D <- dist(Z)
# Gli avvii multipli confrontano soluzioni locali sullo stesso spazio.
set.seed(816)
km <- kmeans(Z, centers=3, nstart=50, iter.max=100)
rinominata <- c(3,1,2)[km$cluster]
c(uguaglianza_dei_numeri=mean(km$cluster==rinominata),
 accordo_coppie=accordo_coppie(km$cluster,rinominata),
 ARI=indice_rand_corretto(km$cluster,rinominata))
table(originale=km$cluster,rinominata=rinominata)


# Variare gli avvii
set.seed(818)
avvii <- lapply(1:30,function(b)kmeans(Z,3,nstart=1,iter.max=100))
stabilita <- data.frame(ripetizione=1:30,
 WSS=vapply(avvii,function(m)m$tot.withinss,numeric(1)),
 accordo=vapply(avvii,function(m)accordo_coppie(m$cluster,km$cluster),numeric(1)),
 ARI=vapply(avvii,function(m)indice_rand_corretto(m$cluster,km$cluster),numeric(1)))
stabilita
plot(stabilita$WSS,stabilita$ARI,pch=19,col="#087C74",
 xlab="WSS dell'avvio",ylab="ARI con il fit di riferimento")


# Perturbare i dati
set.seed(819)
ampiezze <- c(0,.1,.4,.8)
esperimenti <- do.call(rbind,lapply(ampiezze,function(sigma){
 do.call(rbind,lapply(1:10,function(b){
  Zp <- Z+matrix(rnorm(length(Z),sd=sigma),nrow(Z))
  mp <- kmeans(Zp,3,nstart=50,iter.max=100)
  data.frame(sigma=sigma,ripetizione=b,ARI=indice_rand_corretto(mp$cluster,km$cluster))
 }))
}))
aggregate(ARI~sigma,esperimenti,function(x)c(media=mean(x),minimo=min(x)))


# Variante svolta
set.seed(820)
dieci <- lapply(1:30,function(b)kmeans(Z,3,nstart=10,iter.max=100))
data.frame(nstart=c(1,10),WSS_media=c(mean(stabilita$WSS),
 mean(vapply(dieci,function(m)m$tot.withinss,numeric(1)))),
 ARI_medio=c(mean(stabilita$ARI),
 mean(vapply(dieci,function(m)indice_rand_corretto(m$cluster,km$cluster),numeric(1)))))


# M08_N18 - Campioni atipici e sensibilità alle variabili
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M08_Polychroma"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M08_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M08_Polychroma o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M08_N18")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(8018)


# Distanza dal centro e separazione relativa
# Seleziona le misure per nome: ID ed etichetta non entrano nella matrice.
r <- carica_dati("rocce_simulate.csv")
v <- c("SiO2", "CaO", "MgO", "FeO", "densita", "grana_mm", "colore", "fossili")
X <- as.matrix(r[v])
stopifnot(nrow(X)==90L, ncol(X)==8L, !anyDuplicated(r$id),
          all(is.finite(X)), all(apply(X,2,sd)>0))
Z <- scale(X)
D <- dist(Z)
# Gli avvii multipli confrontano soluzioni locali sullo stesso spazio.
set.seed(816)
km <- kmeans(Z, centers=3, nstart=50, iter.max=100)
d2 <- rowSums((Z-km$centers[km$cluster,,drop=FALSE])^2)
s <- silhouette_base(km$cluster,D)
tab <- data.frame(id=r$id,cluster=km$cluster,distanza2=d2,silhouette=s)
head(tab[order(tab$distanza2,decreasing=TRUE),],8)
plot(d2,s,pch=19,col="#087C74",xlab="Distanza quadratica dal centro",
 ylab="Silhouette")
segnala <- order(d2,decreasing=TRUE)[1:4]
text(d2[segnala],s[segnala],labels=r$id[segnala],pos=3,cex=.7)


# Una soglia descrittiva interna
soglia <- vapply(1:3,function(g)unname(quantile(d2[km$cluster==g],.95)),numeric(1))
tab$da_esaminare <- d2>soglia[km$cluster]
tab[tab$da_esaminare,]
# Scompone il contributo delle variabili per il caso più lontano.
i <- which.max(d2)
sort((Z[i,]-km$centers[km$cluster[i],])^2,decreasing=TRUE)


# Una geometria basata soltanto sugli ossidi
ossidi <- c("SiO2","CaO","MgO","FeO")
Zo <- scale(as.matrix(r[ossidi]))
set.seed(822)
ko <- kmeans(Zo,3,nstart=50,iter.max=100)
c(ARI=indice_rand_corretto(km$cluster,ko$cluster),
 silhouette_8=mean(s),silhouette_4=mean(silhouette_base(ko$cluster,dist(Zo))))
table(otto_variabili=km$cluster,quattro_ossidi=ko$cluster)


# Variante svolta
Z_mod <- Z
i <- 1L
Z_mod[i,"grana_mm"] <- Z_mod[i,"grana_mm"]+5
set.seed(823)
km_mod <- kmeans(Z_mod,3,nstart=50,iter.max=100)
c(campione=i,ARI=indice_rand_corretto(km$cluster,km_mod$cluster),
 WSS_originale=km$tot.withinss,WSS_modificata=km_mod$tot.withinss)
r[i,c("id","grana_mm")]


# M08_N19 - Laboratorio applicativo: quattro gruppi
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M08_Polychroma"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M08_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M08_Polychroma o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M08_N19")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(8019)


# Riprodurre la richiesta con k fissato
# Seleziona le misure per nome: ID ed etichetta non entrano nella matrice.
r <- carica_dati("rocce_simulate.csv")
v <- c("SiO2", "CaO", "MgO", "FeO", "densita", "grana_mm", "colore", "fossili")
X <- as.matrix(r[v])
stopifnot(nrow(X)==90L, ncol(X)==8L, !anyDuplicated(r$id),
          all(is.finite(X)), all(apply(X,2,sd)>0))
Z <- scale(X)
D <- dist(Z)
set.seed(1601)
km4 <- kmeans(Z,4,nstart=50,iter.max=100)
km4$size
c(WSS=km4$tot.withinss,silhouette=mean(silhouette_base(km4$cluster,D)))
profili4 <- aggregate(r[v],list(cluster=km4$cluster),mean)
round(profili4,3)


# Confronto con la soluzione a tre gruppi
# Gli avvii multipli confrontano soluzioni locali sullo stesso spazio.
set.seed(816)
km <- kmeans(Z, centers=3, nstart=50, iter.max=100)
table(k3=km$cluster,k4=km4$cluster)
table(k4=km4$cluster,generatore=r$litologia_generatrice)
profili4[,c("cluster","SiO2","CaO","densita","grana_mm")]
data.frame(k=c(3,4),WSS=c(km$tot.withinss,km4$tot.withinss),
 silhouette=c(mean(silhouette_base(km$cluster,D)),mean(silhouette_base(km4$cluster,D))))


# Visualizzare e conservare la soluzione
# La PCA conserva medie, scale e rotazione per eventuali nuovi campioni.
pc <- prcomp(X, center=TRUE, scale.=TRUE)
lambda <- pc$sdev^2
quota <- lambda/sum(lambda)
colori <- c("#087C74", "#C57E42", "#7363AA", "#1D7890", "#A17B19", "#657180", "#B55353")
plot(pc$x[,1:2],pch=19,col=colori[km4$cluster],asp=1,
 xlab="PC1",ylab="PC2")
legend("topright",legend=paste("Cluster",1:4),col=colori[1:4],pch=19,bty="n")
risultato4 <- data.frame(id=r$id,cluster=km4$cluster,
 silhouette=silhouette_base(km4$cluster,D))
write.csv(risultato4,percorso_risultati("assegnazioni_k4.csv"),row.names=FALSE)
head(risultato4,4)


# Variante svolta
set.seed(1602)
km5 <- kmeans(Z,5,nstart=50,iter.max=100)
data.frame(k=c(4,5),WSS=c(km4$tot.withinss,km5$tot.withinss),
 silhouette=c(mean(silhouette_base(km4$cluster,D)),mean(silhouette_base(km5$cluster,D))))
table(k4=km4$cluster,k5=km5$cluster)


# M08_N20 - Laboratorio applicativo: PCA equivalente
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M08_Polychroma"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M08_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M08_Polychroma o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M08_N20")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(8020)


# Due istruzioni, la stessa trasformazione
# Seleziona le misure per nome: ID ed etichetta non entrano nella matrice.
r <- carica_dati("rocce_simulate.csv")
v <- c("SiO2", "CaO", "MgO", "FeO", "densita", "grana_mm", "colore", "fossili")
X <- as.matrix(r[v])
stopifnot(nrow(X)==90L, ncol(X)==8L, !anyDuplicated(r$id),
          all(is.finite(X)), all(apply(X,2,sd)>0))
Z <- scale(X)
D <- dist(Z)
pc_X <- prcomp(X,center=TRUE,scale.=TRUE)
pc_Z <- prcomp(Z,center=FALSE,scale.=FALSE)
c(errore_dev_standard=max(abs(pc_X$sdev-pc_Z$sdev)),
 errore_rotation=max(abs(pc_X$rotation-pc_Z$rotation)),
 errore_scores=max(abs(pc_X$x-pc_Z$x)))
stopifnot(max(abs(pc_X$sdev-pc_Z$sdev))<1e-10,
          max(abs(pc_X$x-pc_Z$x))<1e-10)


# Collegamento con la decomposizione SVD
sv <- svd(Z)
autovalori_svd <- sv$d^2/(nrow(Z)-1)
data.frame(PC=1:ncol(Z),lambda_PCA=pc_X$sdev^2,lambda_SVD=autovalori_svd)
max(abs(Z-sv$u%*%diag(sv$d)%*%t(sv$v)))
# Cambia contemporaneamente segno a scores e vettore di un asse.
T2 <- pc_X$x; V2 <- pc_X$rotation
T2[,1] <- -T2[,1]; V2[,1] <- -V2[,1]
max(abs(pc_X$x%*%t(pc_X$rotation)-T2%*%t(V2)))


# Proiettare nuovi casi con la scala conservata
# Tre righe vengono usate come esempio di input esterno, non come nuovo fit.
nuovi <- as.data.frame(X[c(1,31,61),,drop=FALSE])
previsti <- predict(pc_X,newdata=nuovi)
Zn <- sweep(sweep(as.matrix(nuovi),2,pc_X$center,"-"),2,pc_X$scale,"/")
manuali <- Zn%*%pc_X$rotation
round(previsti[,1:2],4)
max(abs(previsti-manuali))


# Variante svolta
previsti_Z <- predict(pc_Z,newdata=Zn)
c(errore_equivalenza=max(abs(previsti-previsti_Z)))
# Documenta i parametri necessari a ripetere la trasformazione.
data.frame(variabile=v,centro=pc_X$center,scala=pc_X$scale)
