train <- d[d$x_m<1250,]
test <- d[d$x_m>=1250,]
stopifnot(nrow(train)==40L,
          nrow(test)==24L,
 !any(train$id %in% test$id))
