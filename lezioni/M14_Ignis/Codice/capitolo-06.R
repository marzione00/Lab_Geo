q <- c(11,14,12,6,8,15,17,13)
oltre <- q > 10
c(giorni=sum(oltre),
  episodi=sum(oltre & !c(FALSE,head(oltre,-1))))
