# Eseguire una volta in R o RStudio, con connessione disponibile.
# tseries serve per ADF/KPSS; rmarkdown e knitr per rigenerare gli HTML.
richiesti <- c("tseries", "rmarkdown", "knitr")
mancanti <- richiesti[!vapply(richiesti, requireNamespace, logical(1), quietly=TRUE)]
if (length(mancanti)) install.packages(mancanti, repos="https://cloud.r-project.org")
stopifnot(all(vapply(richiesti, requireNamespace, logical(1), quietly=TRUE)))
# RStudio include Pandoc. Per altri ambienti verificare rmarkdown::pandoc_available().
packageVersion("tseries")
