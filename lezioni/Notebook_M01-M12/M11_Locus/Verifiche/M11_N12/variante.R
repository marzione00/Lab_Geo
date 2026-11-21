piccoli <- pesi_spaziali(d,200)
data.frame(soglia_m=200,isolati=length(piccoli$isolati),somma_pesi=sum(piccoli$W))
stopifnot(length(piccoli$isolati)==64L,all(is.finite(piccoli$W)),sum(piccoli$W)==0)
