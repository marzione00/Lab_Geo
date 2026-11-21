unione <- merge(relazioni,d,by="id",sort=FALSE)
data.frame(unita=c("Sito originale","Relazione sito-zona"),
  n=c(nrow(d),nrow(unione)),media=c(mean(d$concentrazione),mean(unione$concentrazione)))
aggregate(concentrazione~zona,data=unione,mean)
table(unione$zona)
