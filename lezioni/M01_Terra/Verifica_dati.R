# Controlli numerici del materiale, eseguiti con R in WebR.
source("setup.R", encoding = "UTF-8")

medie <- tapply(terra$valore, terra$stazione, mean)
n <- table(terra$stazione)
media_misure <- mean(terra$valore)
media_stazioni <- mean(medie)
stopifnot(
  abs(media_misure - 5.748234477155) < 1e-10,
  abs(media_stazioni - 6.605156418313334) < 1e-10,
  abs(weighted.mean(medie, n[names(medie)]) - media_misure) < 1e-12
)
cat("Media di tutte le misure:", format(media_misure, digits=12), "\n")
cat("Media delle tre stazioni:", format(media_stazioni, digits=12), "\n")
print(medie, digits=12)

# Il generatore ufficiale produce lo stesso campione archiviato,
# entro la precisione decimale del CSV distribuito.
simula <- function(n_A, seed=17L) {
  set.seed(seed)
  data.frame(
    stazione = rep(c("A", "B", "C"), c(n_A, 10, 10)),
    valore = c(rnorm(n_A, 3, 0.4), rnorm(10, 7, 0.4), rnorm(10, 10, 0.4))
  )
}
riprodotto <- simula(20L)
errore_csv <- max(abs(riprodotto$valore - terra$valore))
stopifnot(errore_csv < 1e-9)
cat("Scarto massimo tra rnorm(seed17) e CSV:", errore_csv, "\n")

scenari <- do.call(rbind, lapply(c(10L, 20L, 50L, 100L), function(n_A) {
  d <- simula(n_A)
  m <- tapply(d$valore, d$stazione, mean)
  data.frame(n_A=n_A, media_misure=mean(d$valore), media_stazioni=mean(m),
             attesa_misure=(3*n_A+170)/(n_A+20), attesa_stazioni=20/3)
}))
stopifnot(abs(scenari$media_misure[1] - scenari$media_stazioni[1]) < 1e-12)
print(scenari, digits=10, row.names=FALSE)
write.csv(scenari, "Terra01_scenari_verificati.csv", row.names=FALSE)

# Verifica indipendente delle due correlazioni della slide 58.
osservazioni <- read.csv("Dati/meteostat_16239_2024_originale.csv")
n_pos <- sum(complete.cases(osservazioni[c("tsun", "tmax")]))
n_neg <- sum(complete.cases(osservazioni[c("tsun", "cldc")]))
r_pos <- with(osservazioni, cor(tsun, tmax, use="complete.obs"))
r_neg <- with(osservazioni, cor(tsun, cldc, use="complete.obs"))
stopifnot(n_pos == 62L, n_neg == 62L,
          abs(r_pos - 0.3662383380086286) < 1e-12,
          abs(r_neg + 0.8605922237257095) < 1e-12)
cat("Correlazioni Meteostat (62 coppie ciascuna):", r_pos, r_neg, "\n")

# Controllo dei dati didattici e delle funzioni impiegate nelle serie temporali.
stopifnot(length(unique(demo$data)) == nrow(demo),
          all(diff(demo$data) == 1), !anyNA(demo))
ma31 <- stats::filter(demo$tmax, rep(1/31,31), sides=2)
med31 <- stats::runmed(demo$tmax, k=31, endrule="median")
fit_loess <- loess(tmax ~ as.numeric(data), data=demo, span=.2)
stopifnot(sum(is.na(ma31)) == 30L,
          length(med31) == 1096L,
          all(is.finite(predict(fit_loess))))
cat("Media mobile31: 30 NA di bordo; mediana mobile e LOESS eseguite.\n")
cat("Tutti i controlli numerici sono passati.\n")
print(sessionInfo())
