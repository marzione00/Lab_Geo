c2 <- prepara_co2(carica_dati("co2_1985_2001.csv"))
train <- c2$train; test <- c2$test; h <- c2$h
 origini <- c(120L,132L,144L)
 data.frame(origine=origini,data_origine=c2$dati$data[origini],
            primo_bersaglio=c2$dati$data[origini+1],
            ultimo_bersaglio=c2$dati$data[origini+12])
 stopifnot(all(origini+12<=length(train)))
