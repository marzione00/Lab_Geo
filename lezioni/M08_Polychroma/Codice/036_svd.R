# d contiene i valori singolari.
sv <- svd(Z)
lambda_svd <- sv$d^2 / (nrow(Z) - 1)
lambda_svd
max(abs(crossprod(sv$v) - diag(8)))
