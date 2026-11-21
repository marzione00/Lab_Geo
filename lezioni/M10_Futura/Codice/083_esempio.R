obs <- as.numeric(test)
p_hat <- as.numeric(fc$previsto)
stopifnot(length(obs)==length(p_hat))
e <- obs-p_hat
stopifnot(all(is.finite(e)))
