# Esecutore riproducibile di soli blocchi R. Non richiede knitr o rmarkdown.
# Da R nella cartella M10_Futura: source("R/esegui_notebook.R"); esegui_notebook()
# Gli HTML si generano poi con Sorgenti_generazione/crea_html.py e Pandoc.
esegui_notebook <- function(ids=sprintf("M10_N%02d",1:20),radice=getwd()) {
  radice <- normalizePath(radice,winslash="/",mustWork=TRUE)
  vecchia <- getwd(); on.exit(setwd(vecchia),add=TRUE); setwd(radice)
  if(!file.exists("M10_N01.Rmd")) stop("radice deve indicare M10_Futura.")
  dir.create("Verifiche",showWarnings=FALSE)
  righe <- list(); ri <- 0L
  for(id in ids) {
    # Ogni notebook parte da un ambiente nuovo; i suoi blocchi condividono gli oggetti.
    ambiente <- new.env(parent=globalenv())
    sorgente <- readLines(paste0(id,".Rmd"),warn=FALSE,encoding="UTF-8")
    inizi <- grep("^```\\{r[ ,}]",sorgente)
    cartella <- file.path("Verifiche",id)
    dir.create(cartella,recursive=TRUE,showWarnings=FALSE)
    writeLines(sorgente,file.path(cartella,"sorgente_eseguito.Rmd"),useBytes=TRUE)
    for(inizio in inizi) {
      nome <- sub("^```\\{r[ ]*([^,} ]+).*$","\\1",sorgente[inizio])
      fine <- which(seq_along(sorgente)>inizio & sorgente=="```")[1L]
      if(is.na(fine)) stop("Blocco R senza chiusura: ",id,"/",nome)
      codice <- sorgente[seq.int(inizio+1L,fine-1L)]
      percorso <- file.path(cartella,paste0(nome,".R"))
      writeLines(codice,percorso,useBytes=TRUE)
      pdf_path <- file.path(cartella,paste0(nome,".pdf"))
      out_path <- file.path(cartella,paste0(nome,".txt"))
      warning_path <- file.path(cartella,paste0(nome,"_avvisi.txt"))
      errore <- character(); avvisi <- character(); messaggi <- character()
      t0 <- proc.time()[[3L]]
      pdf(pdf_path,width=8,height=5,family="Helvetica",useDingbats=FALSE)
      dispositivo <- dev.cur()
      output <- capture.output(
        tryCatch(withCallingHandlers(
          source(percorso,local=ambiente,echo=FALSE,print.eval=TRUE,encoding="UTF-8"),
          warning=function(w) { avvisi <<- c(avvisi,conditionMessage(w)); invokeRestart("muffleWarning") },
          message=function(m) { messaggi <<- c(messaggi,conditionMessage(m)); invokeRestart("muffleMessage") }
        ),error=function(e) { errore <<- conditionMessage(e); invisible(NULL) }),
        type="output")
      if(dispositivo %in% dev.list()) invisible(dev.off(dispositivo))
      writeLines(output,out_path,useBytes=TRUE)
      writeLines(c(avvisi,messaggi,if(length(errore))paste("ERRORE:",errore)),warning_path,useBytes=TRUE)
      ri <- ri+1L
      righe[[ri]] <- data.frame(id=id,blocco=nome,esito=if(length(errore))"ERRORE" else "OK",
        secondi=round(proc.time()[[3L]]-t0,3),avvisi=length(avvisi),messaggi=length(messaggi),
        errore=paste(errore,collapse=" | "),output=out_path,grafico_pdf=pdf_path,
        R_version=R.version.string,
        runtime=if("webr" %in% loadedNamespaces()) paste("WebR",packageVersion("webr")) else "R nativo",
        data_UTC=format(Sys.time(),tz="UTC",usetz=TRUE),stringsAsFactors=FALSE)
      write.csv(do.call(rbind,righe),"Verifiche/esecuzione_blocchi.csv",row.names=FALSE)
      cat(sprintf("%s %s %s (%.2fs; %d avvisi)\n",id,nome,righe[[ri]]$esito,
                  righe[[ri]]$secondi,length(avvisi)))
    }
  }
  writeLines(capture.output(sessionInfo()),"Verifiche/sessionInfo.txt",useBytes=TRUE)
  stato <- do.call(rbind,righe)
  if(any(stato$esito!="OK")) stop("Almeno un blocco contiene un errore: leggere Verifiche/esecuzione_blocchi.csv.")
  invisible(stato)
}
