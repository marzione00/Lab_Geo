p <- carica_dati("processi_simulati.csv"); mod <- stima_var(p)
ridotto_y <- lm(y~y_lag,data=mod$lagged)
ridotto_x <- lm(x~x_lag,data=mod$lagged)
g_xy <- anova(ridotto_y,mod$fit_y)
g_yx <- anova(ridotto_x,mod$fit_x)
g_xy
g_yx
