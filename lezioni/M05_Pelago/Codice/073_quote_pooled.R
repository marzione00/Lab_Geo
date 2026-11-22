# Indici del campione riunito
g73 <- fossili$morfotipo
set.seed(17)
j73 <- sample.int(length(g73),
  length(g73), replace = TRUE)
table(g73[j73])
# N_R varia fra repliche.
length(j73)  # Totale sempre 160
