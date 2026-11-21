T <- pc$x
cov_T <- cov(T)
max(abs(cov_T - diag(lam)))
# Le piccole differenze sono numeriche.
