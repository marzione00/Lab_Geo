stile_grafico()
plot(fitted(mod),residuals(mod),pch=19,col=palette_geo[2],
  xlab="Stimato nel train (micrometri)",ylab="Residuo nel train (micrometri)",
  main="Diagnostica della regressione")
abline(h=0,lty=2)
data.frame(n_train=nobs(mod),sd_residua=sigma(mod),df_residui=df.residual(mod))
