fit_x <- lm(x~x_lag+y_lag,data=lagged)
fit_y <- lm(y~x_lag+y_lag,data=lagged)
coefficienti <- rbind(X=coef(fit_x),Y=coef(fit_y))
coefficienti
