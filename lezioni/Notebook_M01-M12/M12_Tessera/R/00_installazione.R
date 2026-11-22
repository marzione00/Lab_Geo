# Preparazione iniziale esplicita. Connessione necessaria solo per installare.
# terra serve ai notebook N03, N08, N18, N19 e N20.
richiesti<-c("terra","rmarkdown","knitr")
mancanti<-richiesti[!vapply(richiesti,requireNamespace,logical(1),quietly=TRUE)]
if(length(mancanti)) install.packages(mancanti,repos="https://cloud.r-project.org")
