rid_x <- lm(x~x_lag,data=lagged); rid_y <- lm(y~y_lag,data=lagged)
data.frame(equazione=c("X","Y"),AIC_VAR=c(AIC(fit_x),AIC(fit_y)),
  AIC_solo_memoria_propria=c(AIC(rid_x),AIC(rid_y)))
