ii <- rev(seq_len(n))
stopifnot(isTRUE(all.equal(
 drop(W[ii,ii]%*%z[ii]),
 lag_z[ii],check.attributes=FALSE)))
