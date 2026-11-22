c2 <- prepara_co2(carica_dati("co2_1985_2001.csv"))
train <- c2$train; test <- c2$test; h <- c2$h
 h18 <- 18L
 ultimo_anno <- as.numeric(tail(train,12))
 pred18 <- rep(ultimo_anno,length.out=h18)
 data.frame(h=1:h18,data=as.character(c2$date_test[1:h18]),
            mese_riferimento=rep(as.character(c2$dati$data[157:168]),length.out=h18),
            previsto=pred18)
