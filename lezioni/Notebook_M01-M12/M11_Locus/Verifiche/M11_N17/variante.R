piccolo <- c(10,10);grande <- rep(20,8)
medie <- c(mean(piccolo),mean(grande));n <- c(length(piccolo),length(grande))
data.frame(peso=c("Uguale ai blocchi","Uguale ai siti"),
  media=c(mean(medie),weighted.mean(medie,n)))
stopifnot(mean(medie)==15,weighted.mean(medie,n)==18,mean(c(piccolo,grande))==18)
