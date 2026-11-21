train <- window(y, end=c(1998,12))
test <- window(y, start=c(1999,1))
stopifnot(length(train)==168,
          length(test)==36)
