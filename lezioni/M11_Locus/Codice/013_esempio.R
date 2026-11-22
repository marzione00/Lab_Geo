stopifnot(!anyDuplicated(d$id))
rownames(xy) <- d$id
dimnames(D) <- list(d$id,d$id)
stopifnot(identical(rownames(D),
                    d$id))
