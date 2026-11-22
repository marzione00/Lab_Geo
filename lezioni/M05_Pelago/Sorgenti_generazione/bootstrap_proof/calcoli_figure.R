# Pelago, slide 60-102. Calcoli per i grafici TikZ.
# R base. Avviare dalla cartella che contiene questo file.
dir.create("coordinate", showWarnings = FALSE)
met <- numeric()
reg <- function(nome, valore) {
  met[nome] <<- as.numeric(valore)
}
scrivi <- function(x, nome) {
  write.csv(x, file.path("coordinate", paste0(nome, ".csv")),
            row.names = FALSE)
}
istogramma <- function(x, nome, breaks = "Sturges") {
  h <- hist(x, breaks = breaks, plot = FALSE)
  scrivi(data.frame(sx = head(h$breaks, -1),
    dx = tail(h$breaks, -1), densita = h$density,
    conteggio = h$counts), nome)
}
q95 <- function(x) unname(quantile(x, c(.025, .975), type = 7))

# Quattro osservazioni adimensionali: enumerazione esatta.
x <- c(4, 5, 7, 8)
j <- as.matrix(expand.grid(rep(list(1:4), 4)))
bm <- apply(j, 1, function(ii) mean(x[ii]))
be <- as.data.frame(table(bm))
scrivi(data.frame(media = as.numeric(as.character(be$bm)),
                 probabilita = be$Freq / 256), "esatto")
reg("esatto_media", mean(bm))
reg("esatto_varianza", mean((bm - mean(bm))^2))
set.seed(17)
boot <- replicate(2000, mean(sample(x, replace = TRUE)))
reg("quattro_se", sd(boot))
reg("quattro_media", mean(boot))
reg("quattro_mc_media", sd(boot) / sqrt(length(boot)))
reg("quattro_bias", mean(boot) - mean(x))

# Esperimento browser bootstrap: default n=30, B=200, seed=17.
set.seed(17)
xb <- rlnorm(30, 0, .6)
bb <- replicate(200, mean(sample(xb, replace = TRUE)))
istogramma(bb, "browser_bootstrap", seq(.6, 2.4, by = .05))
scrivi(data.frame(indice = seq_along(xb), x = xb), "browser_campione")
reg("browser_boot_media", mean(xb))
reg("browser_boot_se", sd(bb))
reg("browser_boot_low", q95(bb)[1])
reg("browser_boot_high", q95(bb)[2])
set.seed(17)
med <- replicate(2000, median(sample(xb, replace = TRUE)))
istogramma(med, "mediana")
reg("mediana_osservata", median(xb))
reg("mediana_low", q95(med)[1])
reg("mediana_high", q95(med)[2])

# Dati sintetici del corso, preservati dai moduli precedenti.
f <- read.csv("Dati/fossili_simulati.csv")
rounded <- subset(f, morfotipo == "Rounded")
r <- rounded$diametro_tot_um
s <- subset(f, morfotipo == "Spiky")$diametro_tot_um
z <- c(r, s)
stopifnot(length(r) == 80, length(s) == 80)
set.seed(17)
pooled <- replicate(2000, mean(sample(z, replace = TRUE)))
set.seed(17)
strat <- replicate(2000, .5 * mean(sample(r, replace = TRUE)) +
                          .5 * mean(sample(s, replace = TRUE)))
common <- seq(5.8, 6.9, by = .04)
istogramma(pooled, "fossili_pooled", common)
istogramma(strat, "fossili_strat", common)
reg("fossili_media", mean(z))
reg("fossili_pooled_se", sd(pooled))
reg("fossili_strat_se", sd(strat))
reg("fossili_pooled_var_exact", (159 / 160^2) * var(z))
reg("fossili_strat_var_exact", .25 * 79 / 80^2 * (var(r) + var(s)))
set.seed(17)
contrasto <- replicate(2000, mean(sample(s, replace = TRUE)) -
                              mean(sample(r, replace = TRUE)))
istogramma(contrasto, "contrasto", seq(-.1, 1.3, by = .05))
reg("contrasto", mean(s) - mean(r))
reg("contrasto_low", q95(contrasto)[1])
reg("contrasto_high", q95(contrasto)[2])
d <- rounded$diametro_tot_um - rounded$diametro_int_um
set.seed(17)
bd <- replicate(2000, mean(sample(d, replace = TRUE)))
reg("coppie_media", mean(d))
reg("coppie_se", sd(bd))
scrivi(rounded[1:5, c("id", "diametro_tot_um", "diametro_int_um")],
       "coppie")

# Sei stazioni, quattro provini in ciascuna.
p <- read.csv("Dati/campioni_modulo1.csv")
p$densita <- p$massa_g / p$volume_cm3
st <- aggregate(densita ~ affioramento + stazione, p, mean)
scrivi(st, "stazioni")
stopifnot(nrow(p) == 24, nrow(st) == 6)
set.seed(17)
br <- replicate(2000, mean(sample(p$densita, replace = TRUE)))
set.seed(17)
bs <- replicate(2000, mean(sample(st$densita, replace = TRUE)))
common <- seq(2.48, 2.72, by = .008)
istogramma(br, "stazioni_righe", common)
istogramma(bs, "stazioni_intere", common)
reg("densita_media", mean(st$densita))
reg("densita_se_righe", sd(br))
reg("densita_se_stazioni", sd(bs))
reg("densita_low", q95(bs)[1])
reg("densita_high", q95(bs)[2])
tst <- t.test(st$densita)$conf.int
reg("densita_t_low", tst[1])
reg("densita_t_high", tst[2])
a <- subset(st, affioramento == "A")$densita
b <- subset(st, affioramento == "B")$densita
set.seed(17)
ab <- replicate(2000, mean(sample(a, replace = TRUE)) -
                       mean(sample(b, replace = TRUE)))
reg("affioramenti", mean(a) - mean(b))
reg("affioramenti_low", q95(ab)[1])
reg("affioramenti_high", q95(ab)[2])
istogramma(ab, "affioramenti", seq(-.01, .21, by = .01))

# Esperimento browser ricampionamento, esatto ordine del generatore.
set.seed(17)
G <- 12
m <- 6
tau <- 2
u <- rnorm(G, 0, tau)
xx <- matrix(10 + rep(u, each = m) + rnorm(G * m), nrow = m)
aa <- replicate(200, mean(sample(as.vector(xx), replace = TRUE)))
bb <- replicate(200, mean(xx[, sample(1:G, replace = TRUE)]))
common <- seq(8, 13, by = .2)
istogramma(aa, "browser_righe", common)
istogramma(bb, "browser_stazioni", common)
reg("browser_st_media", mean(xx))
reg("browser_st_righe_se", sd(aa))
reg("browser_st_stazioni_se", sd(bb))
reg("browser_st_vero_se", sqrt(tau^2 / G + 1 / (G * m)))
scrivi(data.frame(stazione = seq_len(G), media = colMeans(xx)),
       "browser_st_medie")

# AR(1) stazionaria del browser: n=120, rho=.7.
ar_series <- function(n, rho) {
  x <- numeric(n)
  x[1] <- rnorm(1)
  for (i in 2:n)
    x[i] <- rho * x[i - 1] + sqrt(1 - rho^2) * rnorm(1)
  x
}
set.seed(17)
serie <- ar_series(120, .7)
scrivi(data.frame(tempo = 1:120, valore = serie), "serie")
n <- length(serie)
L <- 8
bi <- replicate(200, mean(sample(serie, replace = TRUE)))
bl <- replicate(200, {
  start <- sample(1:n, ceiling(n / L), replace = TRUE)
  indices <- unlist(lapply(start, function(s)
    ((s - 1 + 0:(L - 1)) %% n) + 1))
  mean(serie[indices[1:n]])
})
common <- seq(-.65, .9, by = .05)
istogramma(bi, "blocchi_righe", common)
istogramma(bl, "blocchi_circolari", common)
h <- 1:(n - 1)
se_ar <- sqrt((n + 2 * sum((n - h) * .7^h)) / n^2)
reg("serie_media", mean(serie))
reg("serie_se_righe", sd(bi))
reg("serie_se_blocchi", sd(bl))
reg("serie_se_teorico", se_ar)
res <- lapply(1:30, function(L) {
  set.seed(417)
  z <- replicate(1000, {
    starts <- sample.int(n, ceiling(n / L), replace = TRUE)
    ids <- unlist(lapply(starts, function(s)
      ((s - 1 + 0:(L - 1)) %% n) + 1))
    mean(serie[ids[1:n]])
  })
  data.frame(L = L, se = sd(z))
})
scrivi(do.call(rbind, res), "lunghezza_blocchi")

# Precisione numerica. Campione fissato, 30 ripetizioni del calcolo.
set.seed(17)
xp <- rlnorm(30, 0, .6)
qq <- replicate(30, quantile(replicate(200,
  mean(sample(xp, replace = TRUE))), .975))
scrivi(data.frame(ripetizione = 1:30, limite = qq), "precisione_200")
reg("precisione_sd_200", sd(qq))
# Nuova partenza identica: stesso x, B=1000.
set.seed(17)
xp2 <- rlnorm(30, 0, .6)
stopifnot(identical(xp, xp2))
qq2 <- replicate(30, quantile(replicate(1000,
  mean(sample(xp2, replace = TRUE))), .975))
scrivi(data.frame(ripetizione = 1:30, limite = qq2), "precisione_1000")
reg("precisione_sd_1000", sd(qq2))
set.seed(717)
sev <- do.call(rbind, lapply(c(50, 200, 1000), function(B) {
  z <- replicate(12, sd(replicate(B,
    mean(sample(xp, replace = TRUE)))))
  data.frame(B = B, ripetizione = 1:12, se = z)
}))
scrivi(sev, "mc_se")
reg("precisione_se_exact", sqrt(29 / 30^2 * var(xp)))
scrivi(data.frame(indicatore = names(met), valore = unname(met)),
       "metriche")
print(met)
writeLines(capture.output(sessionInfo()), "sessionInfo_calcoli.txt")
