# Separazione su dati simulati.
taglio <- as.Date("2024-01-01")
prima <- demo$data < taglio
addestramento <- demo[prima, ]
valutazione <- demo[!prima, ]
range(addestramento$data)
range(valutazione$data)
# Stima prima, verifica dopo.
