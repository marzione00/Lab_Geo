# Parametri appresi soltanto nel training.
mu_x <- mean(training$diametro_tot_um)
sd_x <- sd(training$diametro_tot_um)
z_train <- (training$diametro_tot_um - mu_x) / sd_x
z_test <- (test$diametro_tot_um - mu_x) / sd_x
# Nei fold, mu_x e sd_x si ristimano
# ogni volta sui quattro fold di stima.
