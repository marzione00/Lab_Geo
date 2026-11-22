# Funzioni minime per i notebook GeoStat Lab.
# Il chiamante ha gia individuato la radice del progetto e l'ID.
.gs_prepara_notebook <- function(radice, id) {
  .gs_dati <- file.path(radice,"Dati")
  .gs_uscita <- file.path(radice,"Risultati",id)
  dir.create(.gs_uscita,recursive=TRUE,showWarnings=FALSE)
  list(
    carica_dati=function(nome,...) {
      argomenti <- modifyList(list(file=file.path(.gs_dati,nome),
                          stringsAsFactors=FALSE,check.names=FALSE),list(...))
      do.call(read.csv,argomenti)
    },
    percorso_dati=function(nome) {
      normalizePath(file.path(.gs_dati,nome),winslash="/",mustWork=TRUE)
    },
    percorso_risultati=function(nome) {
      if (length(nome)!=1L || grepl("(^/|[.][.])",nome)) {
        stop("Usare un nome relativo nella cartella dei risultati.")
      }
      destinazione <- file.path(.gs_uscita,nome)
      dir.create(dirname(destinazione),recursive=TRUE,showWarnings=FALSE)
      destinazione
    }
  )
}
