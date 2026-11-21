A <- rbind(coef(fit_x)[c("x_lag","y_lag")],coef(fit_y)[c("x_lag","y_lag")])
rownames(A) <- c("X","Y")
intercetta <- c(coef(fit_x)[1],coef(fit_y)[1])
A
z250 <- as.numeric(v[250,])
primo <- as.numeric(intercetta+A%*%z250)
data.frame(variabile=c("X","Y"),prevista_passo251=primo)
