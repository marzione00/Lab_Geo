r85 <- lab_ricampionamento(
  tau = 2, B = 200, seed = 17)
r85$indicatori
# Variante: componente comune nulla
r85b <- lab_ricampionamento(
  tau = 0, B = 200, seed = 17)
r85b$indicatori
