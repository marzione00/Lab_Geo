# Esecutore per verificare ogni notebook in un ambiente indipendente.
.gs_run_notebook <- function(id, codici, etichette, uscita) {
  .gs_env <- new.env(parent=globalenv())
  .gs_dir <- file.path(uscita, id)
  dir.create(.gs_dir, recursive=TRUE, showWarnings=FALSE)
  .gs_record <- list()
  .gs_failure <- FALSE
  .gs_original_options <- options()
  on.exit(options(.gs_original_options), add=TRUE)
  for (.gs_i in seq_along(codici)) {
    .gs_name <- sprintf("%02d", .gs_i)
    .gs_pdf <- file.path(.gs_dir, paste0(.gs_name,".pdf"))
    .gs_txt <- file.path(.gs_dir, paste0(.gs_name,".txt"))
    .gs_error <- ""
    .gs_warnings <- character()
    .gs_start <- proc.time()[[3]]
    options(warn=1, width=88, digits=6, max.print=300)
    .gs_height <- if (grepl("mfrow=c(3,1)",codici[[.gs_i]],fixed=TRUE)) 8.4 else
      if (grepl("mfrow=c(2,",codici[[.gs_i]],fixed=TRUE)) 7.2 else 5.2
    pdf(.gs_pdf, width=8.0, height=.gs_height, family="Helvetica",
        useDingbats=FALSE, onefile=TRUE)
    par(mar=c(4.6,4.7,4.0,1.4), mgp=c(2.8,.75,0), cex=0.95, las=1,
        col.axis="#253344", col.lab="#253344", col.main="#15283E")
    .gs_output <- tryCatch(withCallingHandlers(capture.output({
      .gs_exprs <- parse(text=codici[[.gs_i]], keep.source=FALSE)
      for (.gs_expr in .gs_exprs) {
        .gs_val <- withVisible(eval(.gs_expr, envir=.gs_env))
        if (.gs_val$visible) print(.gs_val$value)
      }
    }, type="output"), warning=function(w) {
      .gs_warnings <<- c(.gs_warnings,conditionMessage(w))
      cat("Avviso R: ",conditionMessage(w),"\n",sep="")
      invokeRestart("muffleWarning")
    }), error=function(e) {
      .gs_error <<- conditionMessage(e)
      character()
    })
    while (!is.null(dev.list())) dev.off()
    writeLines(enc2utf8(.gs_output), .gs_txt, useBytes=TRUE)
    .gs_record[[.gs_i]] <- data.frame(
      id=id, chunk=.gs_i, label=etichette[[.gs_i]],
      ok=!nzchar(.gs_error), error=gsub("[\t\n\r]", " ", .gs_error),
      warnings=length(.gs_warnings),
      warning_text=gsub("[\t\n\r]"," ",paste(.gs_warnings,collapse=" | ")),
      seconds=proc.time()[[3]]-.gs_start, stringsAsFactors=FALSE)
    if (nzchar(.gs_error)) { .gs_failure <- TRUE; break }
  }
  write.table(do.call(rbind,.gs_record), file.path(.gs_dir,"status.tsv"),
              sep="\t", row.names=FALSE, quote=TRUE, fileEncoding="UTF-8")
  if (.gs_failure) return(paste(id,"ERRORE",.gs_error))
  paste(id,"OK",length(codici),"blocchi")
}
