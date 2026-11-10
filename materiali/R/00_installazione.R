# Avvio esplicito dell'utente: installare prima delle analisi.
# sf e terra possono richiedere GDAL, GEOS, PROJ e UDUNITS sul sistema operativo.
p <- c('ggplot2','jsonlite','dplyr','class','cluster','rpart','randomForest','sf','terra','tseries','knitr')
assenti <- p[!vapply(p,requireNamespace,logical(1),quietly=TRUE)]
if(length(assenti)) install.packages(assenti,repos='https://cloud.r-project.org')
