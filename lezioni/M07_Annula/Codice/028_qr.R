X <- model.matrix(m0)
# QR evita di formare esplicitamente
# l'inversa di t(X) %*% X.
b_qr <- qr.coef(qr(X), y)
max(abs(b_qr - coef(m0)))
# Equazioni normali: quasi zero.
max(abs(crossprod(X, residuals(m0))))
