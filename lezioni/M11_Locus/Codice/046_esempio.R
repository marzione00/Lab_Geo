D_nn <- D
diag(D_nn) <- Inf
j_nn <- apply(D_nn,1,which.min)
stopifnot(all(j_nn!=seq_len(n)))
head(d$id[j_nn])
