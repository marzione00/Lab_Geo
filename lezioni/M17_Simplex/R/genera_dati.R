# Simplex (M17): generatore del file dati/composizioni_v1.csv.
# Composizioni sintetiche a sei parti, generate nel simplesso: coordinate clr normali attorno al centro di ogni
# litologia, con un effetto di stazione condiviso, poi chiusura a 100. Le misure sotto il limite di rivelabilita
# (0,1 % in massa per MgO e FeO) sono registrate come 0 e marcate nella colonna limite.
# Codice: PolyForm Noncommercial 1.0.0. Required Notice: Copyright 2026 Marzio De Corato.
set.seed(20261128)
parti <- c('SiO2', 'Al2O3', 'CaO', 'MgO', 'FeO', 'Altro')
centri <- rbind(
  Arenaria = c(85.0, 6.0, 2.0, 0.15, 1.2, 5.65),
  Basalto  = c(49.5, 15.0, 10.5, 7.5, 11.0, 6.5),
  Calcare  = c(6.0, 1.5, 50.0, 0.9, 0.14, 41.46))
colnames(centri) <- parti
clr <- function(x) log(x) - mean(log(x))
chiudi <- function(x) 100 * x / sum(x)
# Dispersione in clr (deviazioni standard per parte) e correlazione comune fra Mg e Fe.
sdp <- c(SiO2 = .05, Al2O3 = .18, CaO = .25, MgO = .45, FeO = .35, Altro = .15)
R <- diag(6); R[4, 5] <- R[5, 4] <- .6
S <- diag(sdp) %*% R %*% diag(sdp)
L <- chol(S)
righe <- list(); k <- 0
for (lit in rownames(centri)) {
  m <- clr(centri[lit, ])
  for (s in 1:6) {
    staz <- paste0(substr(lit, 1, 1), s)
    u <- rnorm(6, 0, .08)
    for (i in 1:8) {
      z <- m + u + drop(rnorm(6) %*% L)
      x <- chiudi(exp(z - mean(z)))
      k <- k + 1
      righe[[k]] <- data.frame(id = sprintf('C%03d', k), stazione = staz, litologia = lit, t(round(x, 3)))
    }
  }
}
d <- do.call(rbind, righe)
names(d)[4:9] <- parti
stopifnot(nrow(d) == 144, all(abs(rowSums(d[parti]) - 100) < .02))
# Densita apparente (g/cm3): dipende dal bilancio fra parti femiche e silice, dalla litologia e da un errore.
b <- sqrt(2 / 3) * log(sqrt(d$MgO * d$FeO) / d$SiO2)
d$densita <- round(c(Arenaria = 2.45, Basalto = 2.95, Calcare = 2.68)[d$litologia] + .08 * (b - ave(b, d$litologia)) +
  rnorm(nrow(d), 0, .03), 3)
# Limite di rivelabilita 0,1 %: i valori inferiori sono registrati come 0.
lim <- .1
d$sotto_limite <- apply(cbind(d$MgO < lim, d$FeO < lim), 1, function(r) paste(c('MgO', 'FeO')[r], collapse = ';'))
d$MgO[d$MgO < lim] <- 0
d$FeO[d$FeO < lim] <- 0
stopifnot(all(d[parti] >= 0), all(rowSums(d[parti]) > 99.8))
write.csv(d, 'dati/composizioni_v1.csv', row.names = FALSE)
cat('Righe:', nrow(d), ' valori sotto il limite:', sum(d$sotto_limite != ''), '\n')
print(table(d$litologia, d$sotto_limite != ''))
