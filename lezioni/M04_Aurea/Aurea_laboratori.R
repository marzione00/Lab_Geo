# Aurea M04 - calcoli dei nove esperimenti interattivi
# Fonte: marzione00/Lab_Geo, R/experiments/m04-*.R, 18 novembre 2026.
# R base; il caricamento definisce funzioni e non genera dati o figure.
# I parametri e l'ordine delle estrazioni riproducono i sorgenti del sito.
# Gli indicatori conservano tutta la precisione, senza arrotondamento f().

.numero <- function(x) length(x) == 1L && is.numeric(x) && is.finite(x)
.probabilita <- function(x) .numero(x) && x >= 0 && x <= 1
.intero_positivo <- function(x) .numero(x) && x >= 1 && x == floor(x)

lab_eventi <- function(prob = .3, n = 200L, seed = 17L) {
  stopifnot(.probabilita(prob), .intero_positivo(n))
  set.seed(seed)
  x <- rbinom(n, 1, prob)
  dati <- data.frame(x = 1:n, y = cumsum(x)/(1:n))
  list(dati = dati, esiti = x,
       indicatori = c(probabilita_teorica = prob, frequenza_finale = mean(x)),
       parametri = list(prob = prob, n = n, seed = seed))
}

lab_condizionamento <- function(prior = .4, pa = .8, pb = .2, seed = 17L) {
  stopifnot(.probabilita(prior), prior > 0, prior < 1,
            .probabilita(pa), .probabilita(pb))
  # prior=P(B), pa=P(A|B), pb=P(A|non B). Nessuna estrazione casuale.
  marginale <- pa*prior + pb*(1-prior)
  stopifnot(marginale > 0)
  post <- pa*prior/marginale
  dati <- data.frame(gruppo = c("P(A|B)", "P(A|non B)", "P(A)", "P(B|A)"),
                     valore = c(pa, pb, marginale, post))
  list(dati = dati,
       indicatori = c(prob_A = marginale, prob_B_dato_A = post,
                       indipendenza = as.numeric(abs(pa-pb) < 1e-10)),
       parametri = list(prior = prior, pa = pa, pb = pb, seed = seed))
}

lab_distribuzione <- function(cut = 1, seed = 17L) {
  stopifnot(.numero(cut))
  # La griglia del disegno e' finita; pnorm usa la distribuzione completa.
  dati <- data.frame(x = seq(-4, 4, length.out = 401))
  dati$y <- dnorm(dati$x)
  list(dati = dati,
       indicatori = c(cumulata = pnorm(cut),
                       superamento = pnorm(cut, lower.tail = FALSE)),
       parametri = list(cut = cut, seed = seed))
}

lab_binomiale <- function(n = 20L, prob = .3, seed = 17L) {
  stopifnot(.intero_positivo(n), .probabilita(prob))
  set.seed(seed)
  k <- 0:n
  dati <- data.frame(k = k, probabilita = dbinom(k, n, prob))
  sim <- rbinom(400, n, prob)
  emp <- tabulate(sim+1, nbins = n+1)/400
  list(dati = dati, simulazioni = sim, frequenze = emp,
       indicatori = c(media_teorica = n*prob,
                       varianza_teorica = n*prob*(1-prob),
                       media_simulata = mean(sim)),
       parametri = list(n = n, prob = prob, seed = seed))
}

lab_poisson <- function(rate = 2, exposure = 3, seed = 17L) {
  stopifnot(.numero(rate), rate >= 0, .numero(exposure), exposure > 0)
  mu <- rate*exposure
  k <- 0:qpois(.999, mu)
  dati <- data.frame(x = k, y = dpois(k, mu))
  # Il grafico omette la coda oltre qpois(.999, mu), senza rinormalizzare.
  list(dati = dati,
       indicatori = c(conteggio_atteso = mu, tasso = rate, sd_conteggio = sqrt(mu)),
       parametri = list(rate = rate, exposure = exposure, seed = seed))
}

lab_normale <- function(mu = 10, sd = 2, q = .95, seed = 17L) {
  stopifnot(.numero(mu), .numero(sd), sd > 0, .probabilita(q), q > 0, q < 1)
  x <- seq(mu-4*sd, mu+4*sd, length.out = 300)
  dati <- data.frame(x = x, y = dnorm(x, mu, sd))
  list(dati = dati,
       indicatori = c(quantile_originale = qnorm(q, mu, sd),
                       quantile_standardizzato = qnorm(q)),
       parametri = list(mu = mu, sd = sd, q = q, seed = seed))
}

lab_moltiplicazione <- function(sdlog = .6, seed = 17L) {
  stopifnot(.numero(sdlog), sdlog >= 0)
  set.seed(seed)
  x <- rlnorm(500, 0, sdlog)
  list(dati = data.frame(valore = x),
       indicatori = c(mediana_teorica = 1, media_teorica = exp(sdlog^2/2),
                       media_simulata = mean(x)),
       parametri = list(sdlog = sdlog, seed = seed))
}

lab_monte_carlo <- function(B = 200L, prob = .1, seed = 17L) {
  stopifnot(.intero_positivo(B), .probabilita(prob))
  set.seed(seed)
  x <- rbinom(B, 1, prob)
  k <- 1:B
  dati <- data.frame(x = k, y = cumsum(x)/k)
  list(dati = dati, esiti = x,
       indicatori = c(stima = mean(x), se_mc_teorico = sqrt(prob*(1-prob)/B)),
       parametri = list(B = B, prob = prob, seed = seed))
}

lab_propagazione <- function(rho = 0, cv = .1, seed = 17L) {
  stopifnot(.numero(rho), abs(rho) <= 1, .numero(cv), cv >= 0)
  # cv nel sito e' SD(log X)=SD(log Y), NON il CV originale.
  # rho e' Corr(log X, log Y), NON la correlazione di X e Y.
  set.seed(seed)
  z <- matrix(rnorm(4000), ncol = 2)
  u <- z[,1]
  v <- rho*u + sqrt(1-rho^2)*z[,2]
  x <- exp(log(10)+cv*u)
  y <- exp(log(5)+cv*v)
  rapporto <- x/y
  tau2 <- 2*cv^2*(1-rho)
  list(dati = data.frame(x = x, y = y, rapporto = rapporto),
       indicatori = c(sd_simulata = sd(rapporto),
                       sd_differenziale_log = 2*cv*sqrt(2*(1-rho)),
                       sd_esatta = 2*sqrt(expm1(tau2)*exp(tau2))),
       parametri = list(rho = rho, cv = cv, seed = seed))
}

# Generatore positivo parametrizzato da MEDIA e SD nella scala originale.
# E' un supporto del caso fisico, distinto dai parametri del browser.
rpos <- function(n, mu, s) {
  stopifnot(.intero_positivo(n), .numero(mu), mu > 0, .numero(s), s >= 0)
  v <- log1p((s/mu)^2)
  rlnorm(n, log(mu)-v/2, sqrt(v))
}
