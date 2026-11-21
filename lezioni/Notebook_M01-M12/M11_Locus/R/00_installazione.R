# Preparazione iniziale esplicita. Connessione necessaria solo per installare.
# sf serve ai notebook05,06,20; rmarkdown+knitr soltanto al percorso Knit.
richiesti<-c("sf","rmarkdown","knitr")
mancanti<-richiesti[!vapply(richiesti,requireNamespace,logical(1),quietly=TRUE)]
if(length(mancanti)) install.packages(mancanti,repos="https://cloud.r-project.org")
