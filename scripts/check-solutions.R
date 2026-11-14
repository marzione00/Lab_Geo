# Execute precisely the stage programs exported by the JavaScript terminal.
suppressPackageStartupMessages(library(jsonlite))
source('R/lab-common.R')
cases <- fromJSON(commandArgs(TRUE)[1],simplifyVector=FALSE)
checks <- list()
for (a in cases) {
 observations <- read.csv(paste0('assets/research/',a$id,'/data.csv'),stringsAsFactors=FALSE,check.names=FALSE)
 for (i in seq_along(a$programs)) {
  e <- new.env(parent=globalenv()); e$observations <- observations; e$p <- a$parameters
  set.seed(e$p$seed); eval(parse(text=a$programs[[i]]),envir=e)
  stopifnot(is.data.frame(e$data),is.data.frame(e$metrics),is.list(e$plots))
  for(g in e$plots)invisible(ggplot_build(g))
  checks[[length(checks)+1L]] <- list(project=a$id,step=i,rows=nrow(e$data),figures=length(e$plots),status='passed')
 }
 original <- fromJSON(paste0('content/research-',a$id,'.json'),simplifyVector=FALSE)
 stopifnot(identical(parse(text=tail(a$programs,1)[[1]],keep.source=FALSE),parse(text=original$code,keep.source=FALSE)))
}
write_json(list(status='passed',R=R.version.string,checks=checks),'qa/solution-stages.json',auto_unbox=TRUE,pretty=TRUE)
cat(length(checks),'step programs executed; final steps match the complete scientific programs.\n')
