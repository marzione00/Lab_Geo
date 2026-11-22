# Iride M03 - calcoli dei nove esperimenti interattivi
# Fonte: marzione00/Lab_Geo, R/experiments/m03-*.R (18 novembre 2026).
# R di base. Ogni chiamata casuale inizializza esplicitamente il seme.
# Il caricamento del file definisce le funzioni e non simula dati.
# I dati restituiti sono propri dei laboratori, distinti dai CSV del corso.

lab_supporto <- function(noise = 1, seed = 17) {
  stopifnot(length(noise) == 1L, is.finite(noise), noise >= 0)
  set.seed(seed)
  g <- rep(1:6, each = 8)
  d <- data.frame(gruppo = factor(g),
                  valore = rep(seq(2, 7), each = 8) + rnorm(48, sd = noise))
  a <- aggregate(valore ~ gruppo, d, mean)
  list(dati = d, medie = a,
       indicatori = c(misure = nrow(d), medie_stazione = nrow(a)))
}

lab_denominatori <- function(nB = 100, scale = c("count", "rate"), seed = 17) {
  scale <- match.arg(scale)
  stopifnot(length(nB) == 1L, is.finite(nB), nB >= 20, nB == as.integer(nB))
  # Il seme e' ammesso come nel pannello del sito; il modello e' deterministico.
  d <- data.frame(gruppo = c("A", "B"), eventi = c(10, 20), n = c(50, nB))
  d$valore <- if (scale == "count") d$eventi else d$eventi/d$n
  list(dati = d, indicatori = c(proporzione_A = 10/50, proporzione_B = 20/nB))
}

lab_posizione <- function(outlier = 15, seed = 17) {
  stopifnot(length(outlier) == 1L, is.finite(outlier))
  set.seed(seed)
  x <- c(rnorm(29, 10, 1), outlier)
  list(dati = data.frame(x = 1:30, y = x),
       indicatori = c(media = mean(x), mediana = median(x)))
}

lab_quantili <- function(noise = 1, n = 60, seed = 17) {
  stopifnot(length(noise) == 1L, is.finite(noise), noise >= 0,
            length(n) == 1L, is.finite(n), n >= 2, n == as.integer(n))
  set.seed(seed)
  x <- rnorm(n, 10, noise)
  q <- quantile(x, c(.25, .75), type = 7, names = FALSE)
  list(dati = data.frame(gruppo = "Campione", valore = x),
       indicatori = c(sd = sd(x), IQR = q[2] - q[1], Q25 = q[1], Q75 = q[2]))
}

lab_smoothing <- function(bins = 18, bw = 0.5, seed = 17) {
  stopifnot(length(bins) == 1L, is.finite(bins), bins >= 1,
            bins == as.integer(bins), length(bw) == 1L, is.finite(bw), bw > 0)
  set.seed(seed)
  x <- c(rnorm(100, -1, .6), rnorm(80, 1.4, .7))
  # bins e bw descrivono il grafico: a seme fisso i valori restano identici.
  # La funzione restituisce i dati. Le classi di hist() vanno dichiarate.
  list(dati = data.frame(valore = x),
       indicatori = c(n = length(x), bw = bw, bins = bins))
}

lab_gruppi <- function(delta = 1, ratio = 1, seed = 17) {
  stopifnot(length(delta) == 1L, is.finite(delta),
            length(ratio) == 1L, is.finite(ratio), ratio > 0)
  set.seed(seed)
  d <- data.frame(gruppo = rep(c("A", "B"), each = 70),
                  valore = c(rnorm(70), rnorm(70, delta, ratio)))
  differenza <- unname(diff(tapply(d$valore, d$gruppo, mean)))
  rapporto <- sd(d$valore[71:140])/sd(d$valore[1:70])
  list(dati = d, indicatori = c(differenza_media = differenza,
                                rapporto_sd = rapporto))
}

lab_relazioni <- function(shape = c("line", "curve"), noise = 1, seed = 17) {
  shape <- match.arg(shape)
  stopifnot(length(noise) == 1L, is.finite(noise), noise >= 0)
  set.seed(seed)
  x <- seq(-2, 2, length.out = 100)
  y <- if (shape == "line") x else x^2
  y <- y + rnorm(100, sd = noise)
  list(dati = data.frame(x = x, y = y),
       indicatori = c(pearson = cor(x, y),
                       spearman = cor(x, y, method = "spearman")))
}

lab_mappa <- function(gradient = 4, seed = 17) {
  stopifnot(length(gradient) == 1L, is.finite(gradient))
  set.seed(seed)
  d <- expand.grid(x = 1:20, y = 1:20)
  d$z <- 10 + gradient*d$x/20 + rnorm(nrow(d), sd = .3)
  # Le coordinate seguono gli assi Est/Nord [km] del sito.
  # gradient e' l'incremento per il riferimento 20 km, non la pendenza per km.
  list(dati = d, indicatori = c(media = mean(d$z), sd = sd(d$z)))
}

lab_scale <- function(sdlog = 0.7, seed = 17) {
  stopifnot(length(sdlog) == 1L, is.finite(sdlog), sdlog >= 0)
  set.seed(seed)
  x <- rlnorm(200, 1, sdlog)
  list(dati = data.frame(originale = x, logaritmo = log(x)),
       indicatori = c(media_aritmetica = mean(x),
                       media_geometrica = exp(mean(log(x)))))
}
