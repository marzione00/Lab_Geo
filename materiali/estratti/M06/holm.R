p <- c(.003,.018,.041,.2)
p_adj <- p.adjust(p,method='holm')
data.frame(p,p_adj,rifiuto=p_adj<=.05)
stopifnot(isTRUE(all.equal(
 unname(p_adj),c(.012,.054,.082,.2))))
