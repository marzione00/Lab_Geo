# Ricalcolo dei due coefficienti della slide 58 dai dati archiviati.
# Fonte: Meteostat e fornitori, Roma/Ciampino, ID 16239, anno 2024.
# Il dataset integra anche dati di modello: leggere PROVENIENZA_DATI.txt.
# Nessun accesso alla rete e nessun pacchetto aggiuntivo.

meteo <- read.csv("Dati/meteostat_ciampino_2024.csv")
meteo$data <- as.Date(meteo$data)

# Si selezionano le coppie complete separatamente per ciascuna relazione.
pos <- meteo[complete.cases(meteo[c("sole", "tmax")]), ]
neg <- meteo[complete.cases(meteo[c("sole", "nubi_ottavi")]), ]
r_pos <- cor(pos$sole, pos$tmax)
r_neg <- cor(neg$sole, neg$nubi_ottavi)

print(data.frame(
  relazione = c("Sole-Tmax", "Sole-nuvolosita"),
  n = c(nrow(pos), nrow(neg)),
  r = c(r_pos, r_neg),
  dal = c(min(pos$data), min(neg$data)),
  al = c(max(pos$data), max(neg$data))
))

# Queste 62 coppie coprono soltanto 31 ottobre-31 dicembre 2024.
# L'unita' della nuvolosita' e' l'ottavo (okta), non la percentuale.
# Le rette hanno funzione descrittiva e non dimostrano causalita'.
if (interactive()) {
  par(mfrow=c(1,2))
  plot(pos$sole, pos$tmax, pch=19, col="#1D7890",
       xlab="Sole [minuti/giorno]", ylab="Tmax [gradi Celsius]",
       main="Insolazione e Tmax")
  abline(lm(tmax ~ sole, data=pos), col="#1D7890", lwd=2)
  plot(neg$sole, neg$nubi_ottavi, pch=19, col="#C57E42",
       xlab="Sole [minuti/giorno]", ylab="Nuvolosita [ottavi]",
       main="Insolazione e nuvolosita", ylim=c(0,8))
  abline(lm(nubi_ottavi ~ sole, data=neg), col="#C57E42", lwd=2)
  par(mfrow=c(1,1))
}
