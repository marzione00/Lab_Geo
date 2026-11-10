pacchetti <- c('ggplot2','jsonlite','dplyr','class','cluster','rpart','randomForest','sf','terra','tseries','knitr')
assenti <- pacchetti[!vapply(pacchetti,requireNamespace,logical(1),quietly=TRUE)]
if(length(assenti)) stop(paste('Pacchetti mancanti:',paste(assenti,collapse=', '),'. Eseguire esplicitamente R/00_installazione.R prima delle analisi.'))
if(!capabilities('cairo')) stop('Il salvataggio delle figure richiede il supporto Cairo di R.')
if(!nzchar(Sys.which('git'))) stop('Installare Git per il macroprogetto P10.')
writeLines(capture.output(sessionInfo()),'verifiche/ambiente_R.txt')
write.csv(data.frame(pacchetto=pacchetti,versione=vapply(pacchetti,function(p)as.character(packageVersion(p)),character(1))),'verifiche/versioni_R.csv',row.names=FALSE)
cat('Dipendenze R disponibili. Verificare che Nimbus Sans sia installato per le figure Cairo.\n')
