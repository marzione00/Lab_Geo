c2 <- prepara_co2(carica_dati("co2_1985_2001.csv"))
train <- c2$train; test <- c2$test; h <- c2$h
 data.frame(insieme=c("Train","Test"),n=c(length(train),length(test)),
   inizio=c("1985-01","1999-01"),fine=c("1998-12","2001-12"))
 stopifnot(length(train)==168L,h==36L,max(time(train))<min(time(test)))
