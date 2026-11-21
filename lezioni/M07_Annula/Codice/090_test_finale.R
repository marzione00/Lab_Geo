# Ristima sui 128 casi di training.
mod_finale <- lm(formule[[scelta]],
                 data = training)
prev_test <- predict(mod_finale, newdata = test)
metriche(test$diametro_int_um, prev_test)
metriche(test$diametro_int_um, prev_base)
