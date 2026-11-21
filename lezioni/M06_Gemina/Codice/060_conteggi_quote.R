# Esempio costruito: 30 unita per sito
T60 <- matrix(c(18,12,9,21),2,
              byrow=TRUE)
dimnames(T60) <- list(
  sito=c("A","B"),
  esito=c("Presenza","Assenza"))
T60
prop.table(T60,1) # Quote per riga
