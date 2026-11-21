cap76 <- c(
 "Diametri dei 160 fossili simulati.",
 "80 Rounded, 80 Spiky; un punto",
 "per individuo. Unita': micrometri.",
 "Relazione positiva nel campione.",
 "Fonte: fossili_simulati.csv.")
dir.create("Risultati",
           showWarnings = FALSE)
writeLines(cap76,
 "Risultati/Fossili_didascalia.txt")
