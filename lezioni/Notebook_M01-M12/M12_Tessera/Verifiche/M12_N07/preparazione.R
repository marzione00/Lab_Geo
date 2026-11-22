# Trova il modulo dal progetto autonomo o da quello generale dei notebook.
.gs_cerca <- normalizePath(getwd(),winslash="/",mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca,file.path(.gs_cerca,"M12_Tessera"),
    file.path(.gs_cerca,"03_Notebook_svolti","M12_Tessera"),
    file.path(.gs_cerca,"M12","03_Notebook_svolti","M12_Tessera"))
  .gs_ok <- file.exists(file.path(.gs_candidati,"M12_N01.Rmd")) &
    file.exists(file.path(.gs_candidati,"R","funzioni_notebook.R"))
  if(any(.gs_ok)) { .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]];break }
  .gs_padre <- dirname(.gs_cerca)
  if(.gs_padre==.gs_cerca) stop("Aprire il progetto M12_Tessera o quello generale dei notebook.")
  .gs_cerca <- .gs_padre
}
source(file.path(.gs_modulo,"R","funzioni_notebook.R"),local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo,"M12_N07")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88,digits=6)
if(requireNamespace("knitr",quietly=TRUE)) {
  knitr::opts_chunk$set(echo=TRUE,error=FALSE,warning=TRUE,message=TRUE,
    fig.width=8,fig.height=5,dpi=150,fig.align="center")
}
set.seed(20261104)
