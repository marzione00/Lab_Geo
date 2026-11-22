nullo <- sapply(seq_len(B),function(b) {
  ind <- ((b-1L)*64L+1L):(b*64L)
  stopifnot(!anyDuplicated(u[ind]))
  permutazione <- order(u[ind])
  f(v[permutazione])
})
eccedenze <- sum(nullo>=osservato)
p <- (1+eccedenze)/(B+1)
risultato <- data.frame(I=osservato,eccedenze=eccedenze,B=B,p_unilaterale=p,
  risoluzione=1/(B+1),media_permutata=mean(nullo))
risultato
stopifnot(p>=1/101,p<=1)
