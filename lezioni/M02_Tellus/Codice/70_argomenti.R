scarto <- function(x,
                   riferimento=100) {
  x - riferimento
}
# Riferimento esplicito
delta_tot <- scarto(
  x = totale, riferimento = 100)
head(delta_tot)
# Stesso risultato col valore previsto
head(scarto(totale))
