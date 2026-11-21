# Borealis M09: aprire il progetto del modulo prima di eseguire la lezione.
# La lettura usa i cinque CSV locali, senza accessi alla rete.
leggi_tabella <- function(nome) {
  p <- file.path("Dati", nome)
  if (!file.exists(p)) stop("Aprire il progetto Borealis_M09 nella sua cartella.")
  x <- read.csv(p, stringsAsFactors = FALSE, na.strings = c("", "NA"))
  if ("data" %in% names(x)) x$data <- as.Date(x$data)
  x
}
wk <- leggi_tabella("co2_settimanale_storica.csv")
mon <- leggi_tabella("co2_mensile_derivata.csv")
d <- leggi_tabella("co2_1985_2001.csv")
temp <- leggi_tabella("temperatura_simulata.csv")
proc <- leggi_tabella("processi_simulati.csv")
stopifnot(identical(d$data, seq(as.Date("1985-01-01"),
  as.Date("2001-12-01"), by = "month")), !anyNA(d$co2_ppm))
y <- ts(d$co2_ppm, start = c(1985, 1), frequency = 12)
z <- ts(temp$temperatura_C, start = c(2000, 1), frequency = 12)
if (!requireNamespace("tseries", quietly = TRUE))
  stop("Per ADF e KPSS installare tseries: install.packages('tseries').")
# Gli avvisi statistici restano visibili. Non sono convertiti in errori.
options(warn = 0)

