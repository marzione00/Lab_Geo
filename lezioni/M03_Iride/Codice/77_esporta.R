# Un dispositivo separato per il PDF
salva77 <- function() {
  pdf("Risultati/Fossili.pdf",
      width = 7.2, height = 4.8)
  on.exit(dev.off())
  source("Codice/75_figura.R",
         local = TRUE)
}
salva77()
