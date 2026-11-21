griglia <- seq(as.Date("1985-01-01"),
               as.Date("2001-12-01"), by = "month")
stopifnot(identical(d$data, griglia),
          nrow(d) == 204L,
          !anyNA(d$co2_ppm),
          !anyDuplicated(d$data))
# Solo ora la frequenza descrive il file.
