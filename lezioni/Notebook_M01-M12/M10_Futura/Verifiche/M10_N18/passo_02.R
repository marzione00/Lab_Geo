ultimo <- matrix(rep(as.numeric(tail(mod$v,1)),each=10),ncol=2)
metriche_var <- data.frame(variabile=c("X","Y"),
  RMSE_VAR=sqrt(colMeans((obs-pr)^2)),
  RMSE_ultimo=sqrt(colMeans((obs-ultimo)^2)))
gy <- anova(lm(y~y_lag,data=mod$lagged),mod$fit_y)
gx <- anova(lm(x~x_lag,data=mod$lagged),mod$fit_x)
pval <- c(gy$`Pr(>F)`[2],gx$`Pr(>F)`[2])
granger <- data.frame(direzione=c("X verso Y","Y verso X"),p=pval,
                       p_Holm=p.adjust(pval,"holm"))
write.csv(metriche_var,percorso_risultati("metriche_VAR.csv"))
write.csv(granger,percorso_risultati("Granger.csv"),row.names=FALSE)
metriche_var
granger
