previsione$inferiore95 <- previsione$media-qnorm(.975)*previsione$se
previsione$superiore95 <- previsione$media+qnorm(.975)*previsione$se
previsione$ampiezza95 <- previsione$superiore95-previsione$inferiore95
previsione[c(1,12,24,36),]
write.csv(previsione,percorso_risultati("previsione_condizionale.csv"),row.names=FALSE)
