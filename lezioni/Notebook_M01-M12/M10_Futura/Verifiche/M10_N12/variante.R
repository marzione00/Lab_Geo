stile_grafico()
qqnorm(residuals(mod),pch=19,col=palette_geo[1],main="Residui della regressione e riferimento normale")
qqline(residuals(mod),col=palette_geo[2])
