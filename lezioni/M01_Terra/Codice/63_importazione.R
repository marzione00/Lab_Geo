# File didattico fornito nel progetto.
demo <- read.csv(
  "Dati/meteo_simulati.csv",
  na.strings = c("", "NA"))
demo$data <- as.Date(demo$data)
str(demo)               # tipi
stopifnot(!anyNA(demo$data))
range(demo$data)        # periodo
