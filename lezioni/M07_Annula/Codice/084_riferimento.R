# Il riferimento usa solo il training.
media_train <- mean(
  training$diametro_int_um)
prev_base <- rep(media_train,
                 nrow(test))
media_train
