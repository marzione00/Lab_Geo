c2 <- prepara_co2(carica_dati("co2_1985_2001.csv"))
train <- c2$train; test <- c2$test; h <- c2$h
 ultimo <- rep(as.numeric(tail(train,1)),h)
 stagionale <- rep(as.numeric(tail(train,12)),length.out=h)
 head(data.frame(h=1:h,ultimo=ultimo,stagionale=stagionale),6)
 stopifnot(identical(stagionale[1:12],stagionale[13:24]))
