resoconto96 <- list(
  serie = "CO2 mensile storica, livelli",
  periodo = range(d$data),
  osservazioni = length(y),
  adf = adf88,
  kpss_livello = kL91,
  kpss_trend = kT91)
resoconto96$periodo
