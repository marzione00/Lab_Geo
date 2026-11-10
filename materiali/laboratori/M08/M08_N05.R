# Scores: che cosa rappresenta un punto?
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
ctx <- inizia_notebook("M08_N05")
set.seed(1015)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Preparazione: La matrice delle misure e le colonne da escludere
r <- leggi_dati("rocce_simulate.csv")
variabili <- c("SiO2","CaO","MgO","FeO","densita","grana_mm","colore","fossili")
richiedi_colonne(r,c("id","litologia_generatrice",variabili))
X <- as.matrix(r[variabili])
stopifnot(nrow(X)==90L,all(is.finite(X)),all(apply(X,2,sd)>0))
dim(X)
apply(X,2,sd)


# Preparazione: Standardizzare non significa rendere indipendenti
Z <- scale(X,center=TRUE,scale=TRUE)
controllo <- data.frame(variabile=colnames(X),
                        media_originale=colMeans(X),SD_originale=apply(X,2,sd),
                        media_z=colMeans(Z),SD_z=apply(Z,2,sd))
controllo
stopifnot(max(abs(colMeans(Z)))<1e-10,
          max(abs(apply(Z,2,sd)-1))<1e-10)
round(cor(Z),2)


# Preparazione: PCA: costruire nuovi assi
pca <- prcomp(Z,center=FALSE,scale.=FALSE)
summary(pca)
head(pca$x[,1:2])
pca$rotation[,1:2]
# Verifica geometrica: scores = dati standardizzati per matrice dei loadings.
stopifnot(max(abs(pca$x-as.matrix(Z)%*%pca$rotation))<1e-8)


# Preparazione: Varianza spiegata e perdita di informazione
quota <- pca$sdev^2/sum(pca$sdev^2)
varianza <- data.frame(PC=paste0("PC",seq_along(quota)),
                       quota=quota,cumulata=cumsum(quota))
varianza
stopifnot(abs(sum(quota)-1)<1e-12)
stile_grafico()
barplot(100*quota,names.arg=seq_along(quota),col=palette_geo[1],
        xlab="Componente principale",ylab="Varianza spiegata (%)",
        main="PCA sulle otto variabili standardizzate")


# Analisi principale: Scores: che cosa rappresenta un punto?
gruppo <- factor(r$litologia_generatrice)
stile_grafico()
plot(pca$x[,1],pca$x[,2],pch=as.integer(gruppo)+14,
     col=palette_geo[as.integer(gruppo)],
     xlab=sprintf("PC1 (%.1f%%)",100*quota[1]),
     ylab=sprintf("PC2 (%.1f%%)",100*quota[2]),
     main="Scores: etichette usate soltanto per leggere")
abline(h=0,v=0,lty=3,col="grey70")
legend("topright",levels(gruppo),col=palette_geo[seq_along(levels(gruppo))],
       pch=seq_along(levels(gruppo))+14,bty="n")
