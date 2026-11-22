mappa_matrice(matrix(indice,24,byrow=TRUE),titolo="Indice da bande sintetiche allineate",
  unita="Indice",limiti=c(-1,1),colori=colorRampPalette(c("#985052","#F3F0DF","#1D7890"))(40))
write.csv(risultato,percorso_risultati("bande_e_indice.csv"),row.names=FALSE)
