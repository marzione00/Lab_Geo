v <- c(40, NA, 50)
c(validi=sum(!is.na(v)),
  media=mean(v, na.rm=TRUE))
