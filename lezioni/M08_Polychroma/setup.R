# Polychroma: oggetti comuni ai frammenti della lezione.
# Aprire Polychroma_M08.Rproj e avviare lo script dalla cartella del modulo.
options(stringsAsFactors = FALSE, digits = 6, width = 90)
d <- read.csv("Dati/rocce_simulate.csv", check.names = FALSE)
v <- c("SiO2", "CaO", "MgO", "FeO", "densita", "grana_mm", "colore", "fossili")
stopifnot(nrow(d) == 90L, !anyDuplicated(d$id), all(v %in% names(d)))
X <- as.matrix(d[v])
stopifnot(all(is.finite(X)), all(apply(X, 2, sd) > 0))
Z <- scale(X)
pc <- prcomp(X, center = TRUE, scale. = TRUE)
source("R/funzioni_analisi.R", encoding = "UTF-8")
dir.create("Risultati", showWarnings = FALSE)
