origini <- c(120,132,144)
stopifnot(all(origini+12<=
              length(train)))
cv <- valida_origini(train,origini)
