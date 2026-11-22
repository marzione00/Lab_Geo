c(NA_media3 = sum(is.na(ma3)),
  NA_media13 = sum(is.na(ma13)))
which(is.na(ma13))
# Con 240 dati completi: 2 NA e 12 NA.
stopifnot(sum(is.na(ma3)) == 2L,
          sum(is.na(ma13)) == 12L)
