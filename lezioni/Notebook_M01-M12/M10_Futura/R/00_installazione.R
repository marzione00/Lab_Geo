# Eseguire una sola volta, con connessione, per rigenerare gli HTML con Knit.
# I calcoli dei notebook richiedono soltanto R base e stats, inclusi in R.
richiesti <- c("rmarkdown", "knitr")
mancanti <- richiesti[!vapply(richiesti,requireNamespace,logical(1),quietly=TRUE)]
if(length(mancanti)) install.packages(mancanti)
message("Preparazione terminata. Gli HTML forniti si leggono anche offline.")
