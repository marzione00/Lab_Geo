# Run downloaded course solutions in an isolated extraction of the original archive.
if(nzchar(Sys.getenv("GEOSTAT_TEST_R_LIBRARY"))) .libPaths(c(Sys.getenv("GEOSTAT_TEST_R_LIBRARY"),.libPaths()))
suppressPackageStartupMessages(library(jsonlite))
root <- normalizePath('.')
guides <- fromJSON('content/course-solutions-prepared.json',simplifyVector=FALSE)
work <- tempfile('geostat_course_');dir.create(work)
unzip('assets/downloads/GeoStatLab_codice_dati_R6.zip',exdir=work)
setwd(file.path(work,'materiali'))
checks <- list()
for(id in names(guides)) {
 cat('Executing',id,'\n')
 stopifnot(identical(parse(file.path('R',paste0(id,'_figure.R')),keep.source=FALSE),
                     parse(text=guides[[id]]$code,keep.source=FALSE)))
 eval(parse(text=guides[[id]]$code),envir=new.env(parent=globalenv()))
 stopifnot(file.exists(file.path('risultati',id,'valori.json')))
 checks[[id]] <- list(status='passed',stages=length(guides[[id]]$stages),
                      expressions=length(parse(text=guides[[id]]$code)))
}
setwd(root)
write_json(list(status='passed',R=R.version.string,checks=checks),
           'qa/course-solutions.json',auto_unbox=TRUE,pretty=TRUE)
unlink(work,recursive=TRUE)
cat('11 complete course solutions executed with their original checks.\n')
