# Esempio di applicazione ai primi casi.
# Non sono dati nuovi indipendenti.
nuovi <- X[1:3, , drop = FALSE]
Znuovi <- scale(nuovi,
  center = medie, scale = devstd)
max(abs(Znuovi - Z[1:3, ]))
