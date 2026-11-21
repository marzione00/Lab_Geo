minimi <- apply(ricerca,1,min)
numero_pareggi <- rowSums(abs(ricerca-minimi)<1e-9)
data.frame(vicini_alla_distanza_minima=as.integer(names(table(numero_pareggi))),
  siti=as.integer(table(numero_pareggi)))
d$id[which(abs(ricerca[1,]-minimi[1])<1e-9)]
stopifnot(all(numero_pareggi>=2L))
