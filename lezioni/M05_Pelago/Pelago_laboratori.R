# Pelago M05 - calcoli dei nove esperimenti interattivi
# Fonte: marzione00/Lab_Geo, R/experiments/m05-*.R, 18 novembre 2026.
# R base. Caricare il file definisce funzioni senza generare dati o figure.
# Le estrazioni seguono lo stesso ordine dei sorgenti del sito.
# Gli indicatori conservano la precisione completa.

.numero <- function(x) length(x) == 1L && is.numeric(x) && is.finite(x)
.intero <- function(x, minimo = 1) .numero(x) && x >= minimo && x == floor(x)
.rho <- function(x) .numero(x) && x >= 0 && x < 1

lab_estimandi <- function(nHigh = 40L, seed = 17L) {
  stopifnot(.intero(nHigh))
  set.seed(seed)
  dati <- data.frame(
    stazione = rep(c("A", "B", "C"), c(10, 10, nHigh)),
    valore = c(rnorm(10, 5), rnorm(10, 6), rnorm(nHigh, 12)))
  medie <- aggregate(valore ~ stazione, dati, mean)
  list(dati = dati, medie_stazioni = medie,
       indicatori = c(media_misure = mean(dati$valore),
                       media_stazioni = mean(medie$valore)),
       parametri = list(nHigh = nHigh, seed = seed))
}

lab_selezione <- function(n = 60L, B = 200L, bias = 1, seed = 17L) {
  stopifnot(.intero(n, 2), .intero(B, 2), .numero(bias))
  set.seed(seed)
  a <- rnorm(B, 10, 2/sqrt(n))
  b <- rnorm(B, 10-bias, 2/sqrt(n))
  dati <- data.frame(valore = c(a, b),
                     disegno = rep(c("Casuale", "Selezionato"), each = B))
  list(dati = dati,
       indicatori = c(bias_teorico = -bias, se_teorico = 2/sqrt(n),
                       mse_simulato = mean((b-10)^2)),
       parametri = list(n = n, B = B, bias = bias, seed = seed))
}

lab_distribuzioni <- function(n = 60L, B = 200L,
                             population = "normal", seed = 17L) {
  stopifnot(.intero(n, 2), .intero(B, 2),
            population %in% c("normal", "exp"))
  set.seed(seed)
  medie <- replicate(B, mean(
    if (population == "normal") rnorm(n, 1, 1) else rexp(n)))
  list(dati = data.frame(media = medie),
       indicatori = c(media_delle_medie = mean(medie),
                       sd_delle_medie = sd(medie), se_teorico = 1/sqrt(n)),
       parametri = list(n = n, B = B, population = population, seed = seed))
}

lab_dipendenza <- function(n = 60L, B = 200L, rho = .2, seed = 17L) {
  stopifnot(.intero(n, 2), .intero(B, 2), .rho(rho))
  set.seed(seed)
  medie <- replicate(B, {
    u <- rnorm(1)
    mean(sqrt(rho)*u + sqrt(1-rho)*rnorm(n))
  })
  list(dati = data.frame(media = medie),
       indicatori = c(se_indipendenza = 1/sqrt(n),
                       se_corretto = sqrt((1+(n-1)*rho)/n),
                       sd_delle_medie = sd(medie),
                       n_eff = n/(1+(n-1)*rho)),
       parametri = list(n = n, B = B, rho = rho, seed = seed))
}

lab_intervalli <- function(n = 30L, B = 200L, rho = 0,
                          level = .95, seed = 17L) {
  stopifnot(.intero(n, 2), .intero(B, 2), .rho(rho),
            .numero(level), level > 0, level < 1)
  set.seed(seed)
  z <- t(replicate(B, {
    # u viene estratto anche quando rho=0, come nel sito.
    u <- rnorm(1)
    x <- 10 + sqrt(rho)*u + sqrt(1-rho)*rnorm(n)
    c(mean(x), sd(x)/sqrt(n))
  }))
  q <- qt((1+level)/2, n-1)
  dati <- data.frame(replica = 1:B, media = z[,1],
                     inferiore = z[,1]-q*z[,2],
                     superiore = z[,1]+q*z[,2])
  dati$copre <- dati$inferiore <= 10 & dati$superiore >= 10
  copertura <- mean(dati$copre)
  list(dati = dati, mostrati = head(dati, 80),
       indicatori = c(copertura = copertura, livello_nominale = level,
                       B = B, errore_mc = sqrt(copertura*(1-copertura)/B)),
       parametri = list(n = n, B = B, rho = rho, level = level, seed = seed))
}

lab_bootstrap <- function(n = 30L, B = 200L, seed = 17L) {
  stopifnot(.intero(n, 2), .intero(B, 2))
  set.seed(seed)
  x <- rlnorm(n, 0, .6)
  boot <- replicate(B, mean(sample(x, replace = TRUE)))
  ci <- quantile(boot, c(.025, .975), type = 7)
  list(dati = data.frame(replica = seq_along(boot), media = boot),
       campione = x,
       indicatori = c(media_osservata = mean(x), se_bootstrap = sd(boot),
                       inferiore = unname(ci[1]), superiore = unname(ci[2])),
       parametri = list(n = n, B = B, seed = seed))
}

lab_ricampionamento <- function(tau = 2, B = 200L, seed = 17L) {
  stopifnot(.numero(tau), tau >= 0, .intero(B, 2))
  set.seed(seed)
  G <- 12L
  m <- 6L
  u <- rnorm(G, 0, tau)
  x <- matrix(10 + rep(u, each = m) + rnorm(G*m), nrow = m)
  a <- replicate(B, mean(sample(as.vector(x), replace = TRUE)))
  b <- replicate(B, mean(x[, sample(1:G, replace = TRUE)]))
  list(dati = data.frame(media = c(a, b),
                         metodo = rep(c("Singole misure", "Stazioni intere"), each = B)),
       campione = x,
       indicatori = c(se_misure = sd(a), se_stazioni = sd(b),
                       stazioni_indipendenti = G),
       parametri = list(tau = tau, B = B, seed = seed, G = G, m = m))
}

# AR(1) stazionaria con media0 e varianza1, per |rho|<1.
ar_series <- function(n, rho) {
  stopifnot(.intero(n, 2), .numero(rho), abs(rho) < 1)
  x <- numeric(n)
  x[1] <- rnorm(1)
  for (i in 2:n) x[i] <- rho*x[i-1] + sqrt(1-rho^2)*rnorm(1)
  x
}

lab_blocchi <- function(length = 8L, rho = .7, B = 200L, seed = 17L) {
  stopifnot(.intero(length), length <= 120, .rho(rho), .intero(B, 2))
  set.seed(seed)
  x <- ar_series(120, rho)
  n <- base::length(x)
  L <- length
  individual <- replicate(B, mean(sample(x, replace = TRUE)))
  blocks <- replicate(B, {
    start <- sample(1:n, ceiling(n/L), replace = TRUE)
    indices <- unlist(lapply(start, function(s) ((s-1+0:(L-1)) %% n)+1))
    mean(x[indices[1:n]])
  })
  list(dati = data.frame(media = c(individual, blocks),
                         metodo = rep(c("Singole osservazioni", "Blocchi circolari"), each = B)),
       campione = x,
       indicatori = c(se_individuale = sd(individual), se_blocchi = sd(blocks),
                       lunghezza_blocco = L, n = n),
       parametri = list(length = length, rho = rho, B = B, seed = seed))
}

lab_precisione <- function(B = 200L, seed = 17L) {
  stopifnot(.intero(B, 2))
  set.seed(seed)
  x <- rlnorm(30, 0, .6)
  q <- replicate(30,
    quantile(replicate(B, mean(sample(x, replace = TRUE))), .975, type = 7))
  list(dati = data.frame(x = 1:30, y = q), campione = x,
       indicatori = c(B = B, sd_limite_superiore = sd(q), n_fisso = 30),
       parametri = list(B = B, seed = seed, R = 30))
}

