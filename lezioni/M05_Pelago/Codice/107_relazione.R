# Registrare risultato e ambiente
r107 <- lab_ricampionamento(
  tau=2,B=1000,seed=17)
dir.create("Risultati",
           showWarnings=FALSE)
saveRDS(r107,"Risultati/stazioni.rds")
writeLines(capture.output(sessionInfo()),
  "Risultati/sessionInfo.txt")
