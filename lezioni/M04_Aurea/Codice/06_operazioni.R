# A: massa >=110 g; B: tipo M
mean(A05 & B05)  # entrambi: 2/6
mean(A05 | B05)  # almeno uno: 4/6
mean(!A05)       # complemento: 3/6
# Controllo della formula dell'unione
mean(A05) + mean(B05) -
  mean(A05 & B05)
