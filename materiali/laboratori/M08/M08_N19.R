# Laboratorio applicativo — K=4
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Questo blocco prepara soltanto percorsi, funzioni di servizio e riproducibilità.
# Non scarica dati, non installa pacchetti, non elimina oggetti e non modifica i CSV.
trova_radice <- function() {
  p <- normalizePath(getwd(), winslash = "/", mustWork = TRUE)
  repeat {
    if (file.exists(file.path(p, "Notebook_R_Geologia.Rproj"))) return(p)
    genitore <- dirname(p)
    if (identical(p, genitore)) stop("Aprire Notebook_R_Geologia.Rproj e riprovare.")
    p <- genitore
  }
}
root <- trova_radice()
source(file.path(root, "R", "funzioni_comuni.R"), local = TRUE)
ctx <- inizia_notebook("M08_N19")
set.seed(1016)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Preparazione: Preparare le distanze senza usare l’etichetta
r <- leggi_dati("rocce_simulate.csv")
v <- c("SiO2","CaO","MgO","FeO","densita","grana_mm","colore","fossili")
X <- as.matrix(r[v])
stopifnot(all(is.finite(X)),all(apply(X,2,sd)>0))
Z <- scale(X)
D <- dist(Z,method="euclidean")
range(D)
stopifnot(nrow(Z)==90L)


# Preparazione: K-means: centroidi e variabilità interna
set.seed(816)
km3 <- kmeans(Z,centers=3,nstart=50,iter.max=100)
km3$size
km3$centers
c(WSS=km3$tot.withinss,totale=km3$totss)
# Controllo della funzione obiettivo usando le assegnazioni.
WSS_manual <- sum((Z-km3$centers[km3$cluster,,drop=FALSE])^2)
stopifnot(abs(WSS_manual-km3$tot.withinss)<1e-8)


# Preparazione: Silhouette: separazione relativa del campione
silhouette_base <- function(etichette,distanza) {
  lab <- as.integer(factor(etichette))
  DD <- as.matrix(distanza)
  stopifnot(nrow(DD)==length(lab),length(unique(lab))>=2L)
  vapply(seq_along(lab),function(i){
    stessi <- which(lab==lab[i] & seq_along(lab)!=i)
    if (!length(stessi)) return(0)
    a <- mean(DD[i,stessi])
    altri <- setdiff(unique(lab),lab[i])
    b <- min(vapply(altri,function(k)mean(DD[i,lab==k]),numeric(1)))
    if (max(a,b)==0) 0 else (b-a)/max(a,b)
  },numeric(1))
}
sil3 <- silhouette_base(km3$cluster,D)
summary(sil3)
mean(sil3)
# Confronto facoltativo con l'implementazione del pacchetto cluster.
if (requireNamespace("cluster",quietly=TRUE)) {
  sil_pkg <- cluster::silhouette(km3$cluster,D)[,"sil_width"]
  stopifnot(max(abs(sil3-sil_pkg))<1e-8)
}


# Preparazione: Confrontare k senza imporre la risposta attesa
set.seed(817)
ks <- 2:7
fits <- lapply(ks,function(k)kmeans(Z,centers=k,nstart=50,iter.max=100))
indici <- data.frame(k=ks,
  WSS=vapply(fits,function(m)m$tot.withinss,numeric(1)),
  silhouette=vapply(fits,function(m)mean(silhouette_base(m$cluster,D)),numeric(1)))
indici
stile_grafico()
plot(indici$k,indici$WSS,type="b",pch=19,col=palette_geo[1],
     xlab="Numero di cluster k",ylab="WSS",main="Rendimenti del numero di gruppi")
stile_grafico()
plot(indici$k,indici$silhouette,type="b",pch=19,col=palette_geo[2],
     xlab="Numero di cluster k",ylab="Silhouette media",main="Separazione relativa")


# Preparazione: Visualizzare i cluster con PCA
km <- fits[[which(ks==3)]]
pca <- prcomp(Z,center=FALSE,scale.=FALSE)
quota <- pca$sdev^2/sum(pca$sdev^2)
stile_grafico()
plot(pca$x[,1],pca$x[,2],pch=19,col=palette_geo[km$cluster],
     xlab=sprintf("PC1 (%.1f%%)",100*quota[1]),
     ylab=sprintf("PC2 (%.1f%%)",100*quota[2]),
     main="K-means k=3, mostrato nelle prime due PC")
legend("topright",paste("Cluster",1:3),col=palette_geo[1:3],pch=19,bty="n")


# Preparazione: Profili: ritornare alle unità originali
profili_z <- aggregate(as.data.frame(Z),list(cluster=km$cluster),mean)
profili_originali <- aggregate(r[v],list(cluster=km$cluster),mean)
profili_z
profili_originali
# Il confronto con le etichette avviene soltanto dopo il fit.
confronto_generatore <- table(cluster=km$cluster,generatore=r$litologia_generatrice)
confronto_generatore


# Preparazione: Ward: una gerarchia senza fissare subito k
h <- hclust(D,method="ward.D2")
ward <- cutree(h,k=3)
stile_grafico()
plot(h,labels=FALSE,xlab="Campioni simulati",sub="Ward.D2 su distanze euclidee standardizzate",
     main="Dendrogramma dei 90 campioni")
rect.hclust(h,k=3,border=palette_geo[1:3])
table(Kmeans=km$cluster,Ward=ward)


# Preparazione: Stabilità senza confrontare i nomi dei cluster
accordo_coppie <- function(a,b) {
  stopifnot(length(a)==length(b))
  A <- outer(a,a,"==")
  B <- outer(b,b,"==")
  sopra <- upper.tri(A)
  mean(A[sopra]==B[sopra])
}
set.seed(818)
stabilita <- replicate(20,{
  nuova <- kmeans(Z,3,nstart=1,iter.max=100)$cluster
  accordo_coppie(km$cluster,nuova)
})
summary(stabilita)
accordo_coppie(km$cluster,ward)


# Preparazione: Campioni atipici e sensibilità alle variabili
d2 <- rowSums((Z-km$centers[km$cluster,,drop=FALSE])^2)
soglia <- ave(d2,km$cluster,FUN=function(v)quantile(v,.95))
assegnazioni <- data.frame(id=r$id,cluster=km$cluster,Ward=ward,
                           silhouette=silhouette_base(km$cluster,D),
                           distanza2=d2,da_verificare=d2>soglia)
head(assegnazioni[order(assegnazioni$distanza2,decreasing=TRUE),],8)
set.seed(819)
Z_chimica <- scale(r[c("SiO2","CaO","MgO","FeO")])
km_chimica <- kmeans(Z_chimica,3,nstart=50)
accordo_coppie(km$cluster,km_chimica$cluster)
salva_tabella(indici,"scelta_k.csv",ctx$out)
salva_tabella(profili_originali,"profili_unita_originali.csv",ctx$out)
salva_tabella(profili_z,"profili_zscore.csv",ctx$out)
salva_tabella(assegnazioni,"assegnazioni_e_controlli.csv",ctx$out)
salva_tabella(data.frame(ripetizione=1:20,accordo=stabilita),"stabilita_inizializzazioni.csv",ctx$out)


# Analisi principale: Laboratorio applicativo — K=4
r <- leggi_dati("rocce_simulate.csv")
v <- c("SiO2","CaO","MgO","FeO","densita","grana_mm","colore","fossili")
set.seed(1601)
m <- kmeans(scale(r[v]),4,nstart=50)
m$size
aggregate(r[v],list(cluster=m$cluster),mean)
table(m$cluster,r$litologia_generatrice)
