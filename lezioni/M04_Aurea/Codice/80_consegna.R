# Caso fisico: input indipendenti
set.seed(17)
B80 <- 20000
m80 <- rpos(B80, 106, 1)
v80 <- rpos(B80, 40, .6)
d80 <- m80/v80
dir.create("Risultati",
           showWarnings=FALSE)
write.csv(data.frame(densita=d80),
  "Risultati/densita.csv",
  row.names=FALSE)
