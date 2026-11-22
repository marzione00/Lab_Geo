d53 <- read.csv(
  "Dati/misure_appaiate_simulate.csv")
a53 <- t.test(d53$dopo-d53$prima)
b53 <- t.test(d53$dopo,d53$prima,
              paired=TRUE)
stopifnot(isTRUE(all.equal(
  a53$p.value,b53$p.value)))
a53$conf.int  # Intervallo al 95%
