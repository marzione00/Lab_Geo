data.frame(termine=names(coef(fit)),stima=as.numeric(coef(fit)),
  errore_standard=sqrt(diag(fit$var.coef)))
data.frame(varianza_innovazioni=fit$sigma2,logLik=as.numeric(logLik(fit)),
           AIC=AIC(fit),codice_convergenza=fit$code)
stopifnot(length(coef(fit))==2L,all(is.finite(fit$var.coef)))
