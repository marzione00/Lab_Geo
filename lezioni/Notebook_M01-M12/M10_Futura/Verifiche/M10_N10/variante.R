piano <- data.frame(voce=c("Domanda","Input disponibile","Bersaglio","Split","Riferimento"),
  scelta=c("Prevedere il diametro interno","Diametro totale","Diametro interno in micrometri",
  "Ogni quinta riga nel test","Media del solo train"))
write.csv(piano,percorso_risultati("piano_progetto.csv"),row.names=FALSE)
piano
