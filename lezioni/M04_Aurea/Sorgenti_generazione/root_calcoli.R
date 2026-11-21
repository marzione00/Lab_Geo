# Coordinate e controlli degli esempi introduttivi.
# R base; eseguire dalla cartella aurea_work.
dir.create("root_proof", showWarnings = FALSE)
set.seed(17)
x07 <- rbinom(200, size = 1, prob = .3)
write.csv(data.frame(k = seq_along(x07),
  frequenza = cumsum(x07) / seq_along(x07)),
  "root_proof/frequenze_07.csv", row.names = FALSE)
z25 <- seq(-4, 4, length.out = 161)
write.csv(data.frame(z = z25, densita = dnorm(z25)),
  "root_proof/normale_25.csv", row.names = FALSE)
# Raffronto fra miglioramenti di due strumenti, indipendenza.
u78 <- function(um, uV) {
  2.65 * sqrt((um / 106)^2 + (uV / 40)^2)
}
write.csv(data.frame(
  scenario = c("iniziale", "massa", "volume"),
  um_g = c(1, .5, 1), uV_cm3 = c(.6, .6, .3),
  u_densita = c(u78(1, .6), u78(.5, .6), u78(1, .3))),
  "root_proof/strumenti_78.csv", row.names = FALSE)
cat("Frequenza finale:", mean(x07), "\n")
cat("Pr(Z<=1):", pnorm(1), "\n")
cat("u densita:", u78(1, .6), u78(.5, .6), u78(1, .3), "\n")
