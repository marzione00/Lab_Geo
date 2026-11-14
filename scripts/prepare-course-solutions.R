# Format the existing, verified course programs without changing their R expressions.
suppressPackageStartupMessages(library(jsonlite))
guides <- fromJSON('content/course-solutions.json', simplifyVector=FALSE)
stopifnot(length(guides)==11)
prepared <- list()
format_expression <- function(x) {
 controls <- c("keepInteger","niceNames","showAttributes","keepNA")
 result <- paste(deparse(x,width.cutoff=85,control=controls),collapse="\n")
 if(!identical(x,parse(text=result,keep.source=FALSE)[[1]]))
   result <- paste(deparse(x,width.cutoff=85,control=c(controls,"digits17")),collapse="\n")
 result
}
for (id in names(guides)) {
  g <- guides[[id]]
  original <- readLines(paste0('materiali/R/',id,'_figure.R'),warn=FALSE)
  next_line <- 1L
  chunks <- list()
  for (i in seq_along(g$stages)) {
    stage <- g$stages[[i]]
    stopifnot(stage$fromLine==next_line, stage$toLine>=stage$fromLine)
    expr <- parse(text=original[stage$fromLine:stage$toLine], keep.source=FALSE)
    stage$code <- paste(vapply(expr,format_expression,''),collapse='\n\n')
    g$stages[[i]] <- stage
    chunks[[i]] <- paste(paste0('# ',i,'. ',stage$title),
                         paste(paste0('# ',strwrap(stage$explanation,width=86)),collapse='\n'),
                         stage$code,sep='\n')
    next_line <- stage$toLine+1L
  }
  stopifnot(next_line==length(original)+1L)
  g$code <- paste('# GeoStat Lab · Marzio De Corato',
                 '# Soluzione commentata del progetto originale; eseguire dalla cartella materiali.',
                 paste(chunks,collapse='\n\n'),sep='\n')
  if(!identical(parse(text=original,keep.source=FALSE),parse(text=g$code,keep.source=FALSE))) stop(paste('R expression mismatch:',id))
  prepared[[id]] <- g
}
write_json(prepared,'content/course-solutions-prepared.json',auto_unbox=TRUE,pretty=TRUE)
cat('11 course solutions formatted; R expression trees identical to original programs.\n')
