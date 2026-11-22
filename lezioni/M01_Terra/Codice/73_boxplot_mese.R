# Distribuzioni mensili simulate.
mese <- factor(
  format(demo$data, "%m"),
  levels = sprintf("%02d", 1:12))
boxplot(demo$pioggia ~ mese,
        xlab = "Mese",
        ylab = "Pioggia [mm/giorno]")
table(mese)            # numerosita
