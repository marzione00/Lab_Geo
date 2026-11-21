# Verifica operativa delle consegne e delle soluzioni con warning come errori.
options(warn = 2)
source("setup.R", encoding = "UTF-8")
pdf("Risultati/Figure_esercizi_verifica.pdf", width = 9, height = 5.5)
for (file_esercizio_gemina in sort(list.files("Esercizi", pattern = "[.]R$", full.names = TRUE))) {
  source(file_esercizio_gemina, encoding = "UTF-8")
  if (basename(file_esercizio_gemina) != "12_verifica_finale.R") {
    stopifnot(is.matrix(confronto), nrow(confronto) == 2)
  }
  cat("OK", file_esercizio_gemina, "\n")
}
dev.off()
source("Soluzioni_docente.R", encoding = "UTF-8")
cat("11 esercizi di laboratorio, verifica finale e 12 soluzioni eseguiti senza errori o warning.\n")
