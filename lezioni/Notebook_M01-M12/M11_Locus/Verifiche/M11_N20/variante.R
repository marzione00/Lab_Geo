invertito <- q[nrow(q):1,]
riallineato <- invertito[match(d$id,invertito$id),]
stopifnot(identical(as.character(riallineato$id),d$id),
  max(abs(riallineato$concentrazione-d$concentrazione))<1e-8)
data.frame(ordine_invertito_identico=identical(as.character(invertito$id),d$id),
  ID_riallineati_identici=identical(as.character(riallineato$id),d$id))
