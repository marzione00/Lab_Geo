p_g <- c(g_xy$`Pr(>F)`[2],g_yx$`Pr(>F)`[2])
tab <- data.frame(direzione=c("X aiuta Y al lag 1","Y aiuta X al lag 1"),
  p_non_corretto=p_g,p_Holm_due_confronti=p.adjust(p_g,method="holm"))
tab
write.csv(tab,percorso_risultati("Granger_due_direzioni.csv"),row.names=FALSE)
