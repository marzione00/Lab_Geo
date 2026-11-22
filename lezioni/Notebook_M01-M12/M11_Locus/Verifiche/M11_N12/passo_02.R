risultato <- data.frame(id=d$id,n_vicini=nv,somma_riga=rowSums(W))
head(risultato,10)
data.frame(S0_normalizzato=sum(W),scarto_somma=max(abs(rowSums(W)-1)),
  asimmetria_massima=max(abs(W-t(W))))
stopifnot(max(abs(rowSums(W)-1))<1e-12,abs(sum(W)-64)<1e-12)
data.frame(direzione=c("S01 verso S02","S02 verso S01"),peso=c(W[1,2],W[2,1]))
