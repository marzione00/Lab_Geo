# L'ordinamento coinvolge l'intera tabella.
wk <- wk[order(wk$data), ]
stopifnot(!anyNA(wk$data))
anyDuplicated(wk$data)
table(as.integer(diff(wk$data)))
# Una differenza in Date restituisce giorni.
