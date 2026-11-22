d <- carica_dati("spazio_v3.csv")
audit_spazio(d)
 ps <- pesi_spaziali(d,260)
 A <- ps$A;nv <- ps$n_vicini;W <- ps$W
 data.frame(siti=nrow(A),collegamenti_non_diretti=sum(A)/2,S0_binario=sum(A),
   isolati=sum(nv==0),simmetrica=all(A==t(A)))
 table(nv)
 stopifnot(sum(A)==224L,all(A==t(A)),all(diag(A)==0),all(nv>0))
