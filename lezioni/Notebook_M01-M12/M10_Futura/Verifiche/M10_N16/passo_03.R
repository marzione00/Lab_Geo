sx <- summary(mod$fit_x)$coefficients
sy <- summary(mod$fit_y)$coefficients
data.frame(direzione=c("X verso Y","Y verso X"),
  coefficiente=c(sy["x_lag","Estimate"],sx["y_lag","Estimate"]),
  errore_standard=c(sy["x_lag","Std. Error"],sx["y_lag","Std. Error"]))
