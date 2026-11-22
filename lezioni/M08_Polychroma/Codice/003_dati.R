# Aprire il progetto Polychroma_M08.
source("setup.R", encoding = "UTF-8")
dim(d)
head(d[, c("id", "SiO2", "densita")])
# Un identificativo per campione.
stopifnot(!anyDuplicated(d$id))
