# Annula: configurazione comune dei frammenti della lezione.
# Aprire Annula_M07.Rproj oppure impostare questa cartella come directory.
options(stringsAsFactors = FALSE, digits = 6, width = 90)
options(contrasts = c("contr.treatment", "contr.poly"))
f <- read.csv("Dati/fossili_simulati.csv", check.names = FALSE)
f$morfotipo <- factor(f$morfotipo, levels = c("Rounded", "Spiky"))
stopifnot(nrow(f) == 160L, !anyDuplicated(f$id))
x <- f$diametro_tot_um
y <- f$diametro_int_um
m0 <- lm(diametro_int_um ~ diametro_tot_um, data = f)
source("R/protocollo.R", encoding = "UTF-8")
