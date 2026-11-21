# Esecuzione dei blocchi R di un notebook senza knitr o rmarkdown.
# Dalla cartella del progetto:
# source("R/esegui_notebook.R")
# esegui_notebook("M01_Terra/M01_N01.Rmd")

esegui_notebook <- function(file, salva_grafici=TRUE) {
  file <- normalizePath(file, winslash="/", mustWork=TRUE)
  righe <- readLines(file, encoding="UTF-8", warn=FALSE)
  inizio <- grep("^```\\{r[ ,}]", righe)
  if (!length(inizio)) stop("Il file non contiene blocchi R.")
  radice <- dirname(file)
  while (!file.exists(file.path(radice,"GeoStat_Lab_Notebooks.Rproj"))) {
    padre <- dirname(radice)
    if (padre==radice) stop("Progetto GeoStat Lab non trovato.")
    radice <- padre
  }
  precedente <- getwd()
  on.exit(setwd(precedente), add=TRUE)
  setwd(radice)
  opzioni <- options(warn=2)
  on.exit(options(opzioni), add=TRUE)
  ambiente <- new.env(parent=globalenv())
  id <- sub("[.]Rmd$", "", basename(file))
  destinazione <- file.path(radice,"Risultati",id)
  dir.create(destinazione, recursive=TRUE, showWarnings=FALSE)
  if (salva_grafici) {
    pdf(file.path(destinazione,"figure_esecuzione.pdf"),
        width=7.2, height=4.6, onefile=TRUE, useDingbats=FALSE)
    dispositivo <- dev.cur()
    on.exit({
      if (dispositivo %in% dev.list()) dev.off(dispositivo)
    }, add=TRUE)
  }
  for (i in seq_along(inizio)) {
    apertura <- inizio[i]
    fine <- which(seq_along(righe)>apertura & grepl("^```[[:space:]]*$",righe))[1]
    if (is.na(fine)) stop("Blocco R senza chiusura.")
    codice <- paste(righe[seq.int(apertura+1L,fine-1L)],collapse="\n")
    cat("\n",id," - ",righe[apertura],"\n",sep="")
    for (espressione in parse(text=codice)) {
      risultato <- withVisible(eval(espressione,envir=ambiente))
      if (risultato$visible) print(risultato$value)
    }
  }
  cat("\nCompletato: ",id,". File prodotti in ",destinazione,"\n",sep="")
  invisible(ambiente)
}
