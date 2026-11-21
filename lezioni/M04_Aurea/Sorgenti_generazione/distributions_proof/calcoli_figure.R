# Aurea M04, slide 26-49.
# Tutti i calcoli sono in R base. Eseguire da questa cartella.
dir.create("figure_data", showWarnings = FALSE)
set.seed(17)
sim32 <- rbinom(400, size = 20, prob = .3)
bin32 <- data.frame(
  k = 0:20,
  probabilita = dbinom(0:20, 20, .3),
  frequenza = tabulate(sim32 + 1, nbins = 21) / 400
)
write.csv(bin32, "figure_data/binomiale_400.csv", row.names = FALSE)
q <- c(
  binomiale_esatto_8 = dbinom(8, 20, .3),
  binomiale_almeno_8 = pbinom(7, 20, .3, lower.tail = FALSE),
  binomiale_q95 = qbinom(.95, 20, .3),
  binomiale_media_400 = mean(sim32),
  poisson_almeno_10 = ppois(9, 6, lower.tail = FALSE),
  poisson_q95 = qpois(.95, 6),
  poisson_q999 = qpois(.999, 6),
  binom_pois_maxdiff = max(abs(dbinom(0:25, 200, .03) - dpois(0:25, 6))),
  normale_q95 = qnorm(.95, 10, 2),
  normale_z95 = qnorm(.95),
  normale_low95 = qnorm(.025, 10, 2),
  normale_up95 = qnorm(.975, 10, 2),
  normale_centrale1sd = pnorm(12, 10, 2) - pnorm(8, 10, 2),
  normale_negativa = pnorm(0, 1, .8)
)
write.csv(data.frame(quantita = names(q), valore = unname(q)),
          "figure_data/risultati_esatti.csv", row.names = FALSE)
# Coordinate teoriche per rendere verificabili le curve TikZ.
write.csv(data.frame(k = 0:25, pois6 = dpois(0:25, 6),
                    bin200 = dbinom(0:25, 200, .03),
                    miscela = .5*dpois(0:25, 2) + .5*dpois(0:25, 10)),
          "figure_data/conteggi.csv", row.names = FALSE)
x <- seq(2, 18, length.out = 201)
write.csv(data.frame(x = x, densita = dnorm(x, 10, 2)),
          "figure_data/normale_10_2.csv", row.names = FALSE)
print(q)
stopifnot(abs(sum(dbinom(0:20, 20, .3))-1) < 1e-13)
stopifnot(abs(sum((0:20)*dbinom(0:20, 20, .3))-6) < 1e-13)
