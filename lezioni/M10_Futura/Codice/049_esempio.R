fit$code
coef(fit)
sqrt(diag(fit$var.coef))
stopifnot(fit$code==0)
