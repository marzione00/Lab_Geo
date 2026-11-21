# Esegue i nove file del quaderno dalla radice del progetto.
files <- sort(list.files("Esercizi", pattern="\\.R$", full.names=TRUE))
stopifnot(length(files) == 9L)
for (file in files) {
  cat("\n",file,"\n")
  source(file,echo=FALSE,print.eval=TRUE,encoding="UTF-8")
}
cat("\nOK: nove script di esercitazione eseguiti.\n")
