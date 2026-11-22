# Formula per il campione R001.
s77 <- (b76-a76)/max(a76,b76)
s77
# Funzione fornita nel file
# R/funzioni_analisi.R.
sil <- silhouette_base(km$cluster,D)
stopifnot(abs(s77-sil[i76])<1e-8)
summary(sil)
