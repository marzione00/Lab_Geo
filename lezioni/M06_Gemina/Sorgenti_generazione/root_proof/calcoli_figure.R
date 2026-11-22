# Gemina M06: coordinate numeriche delle figure introduttive.
# Eseguire dalla cartella root_proof; dati sintetici del corso.
options(warn = 2)
dir.create("coordinate", showWarnings = FALSE)
f <- read.csv("Dati/fossili_simulati.csv")
a <- f$diametro_tot_um[f$morfotipo == "Rounded"]
b <- f$diametro_tot_um[f$morfotipo == "Spiky"]
tt <- t.test(b, a, var.equal = FALSE)
write.csv(data.frame(
  media_A = mean(a), media_B = mean(b), differenza = mean(b)-mean(a),
  se = tt$stderr, inferiore = tt$conf.int[1], superiore = tt$conf.int[2],
  p = tt$p.value, df = unname(tt$parameter),
  superiorita = mean(outer(b, a, ">"))),
  "coordinate/fossili_riepilogo.csv", row.names = FALSE)

# Sei assegnazioni distinte: i valori restano fissi.
x <- c(1, 2, 4, 7)
ii <- combn(4, 2)
esatto <- apply(ii, 2, function(i) mean(x[-i])-mean(x[i]))
write.csv(data.frame(indice_A1 = ii[1, ], indice_A2 = ii[2, ],
                     contrasto = esatto),
          "coordinate/permutazioni_esatte.csv", row.names = FALSE)

# Generatore e ordine delle chiamate del browser m06-permutazione.
set.seed(17)
x <- c(rnorm(20), rnorm(20, 0.6))
g <- rep(0:1, each = 20)
obs <- diff(tapply(x, g, mean))
B <- 200
ts <- replicate(B, {
  gp <- sample(g)
  diff(tapply(x, gp, mean))
})
h <- hist(ts, breaks = seq(-1.6, 1.6, by = 0.2), plot = FALSE)
write.csv(data.frame(sinistra = head(h$breaks, -1),
                     destra = tail(h$breaks, -1), conteggio = h$counts),
          "coordinate/istogramma_permutazioni.csv", row.names = FALSE)
write.csv(data.frame(contrasto = as.numeric(ts)),
          "coordinate/contrasti_permutati.csv", row.names = FALSE)
K <- sum(abs(ts) >= abs(obs))
write.csv(data.frame(osservato = unname(obs), K = K, B = B,
                     p_MC = (1 + K)/(B + 1)),
          "coordinate/permutazione_riepilogo.csv", row.names = FALSE)
write.csv(data.frame(valore=x, gruppo=g),
          "coordinate/campione_permutazione.csv", row.names=FALSE)
stopifnot(identical(sort(esatto), c(-4, -2, -1, 1, 2, 4)),
          all(abs(ts) <= 1.6), K >= 0)
cat("Coordinate introduttive verificate.\n")
