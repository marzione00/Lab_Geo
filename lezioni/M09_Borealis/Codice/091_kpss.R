kL91 <- tseries::kpss.test(as.numeric(y),
  null = "Level", lshort = TRUE)
kT91 <- tseries::kpss.test(as.numeric(y),
  null = "Trend", lshort = TRUE)
kL91
kT91
