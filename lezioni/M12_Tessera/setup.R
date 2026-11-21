# Aprire R dalla cartella M12_Tessera. Nessuna installazione durante l'analisi.
if(!file.exists("Dati/raster_v3.csv"))stop("Aprire la sessione dalla cartella M12_Tessera.")
if(!suppressPackageStartupMessages(requireNamespace("terra",quietly=TRUE)))stop("Installare il pacchetto terra prima dell'analisi.")
options(stringsAsFactors=FALSE,digits=12)
source("R/funzioni_M12.R",encoding="UTF-8")
