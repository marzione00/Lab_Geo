# Esegue il driver del progetto con un device grafico invisibile.
# I frammenti attuali stampano soltanto risultati; le figure sono nel motore.
pdf(NULL,width=7,height=4.5)
source("Codice/esegui_frammenti.R",echo=FALSE,encoding="UTF-8")
invisible(dev.off())
