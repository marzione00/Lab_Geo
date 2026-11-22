ridotto_y <- lm(y~y_lag,data=dv)
completo_y <- varfit$y
anova(ridotto_y, completo_y)
