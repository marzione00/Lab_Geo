# Colonne con ruoli diversi.
id <- d$id
etichette <- d$litologia_generatrice
X <- as.matrix(d[v])
stopifnot(!"id" %in% colnames(X),
  !"litologia_generatrice" %in%
    colnames(X))
