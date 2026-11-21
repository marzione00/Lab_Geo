stopifnot(identical(
  fossili$riga_origine,
  fossili_raw$riga_origine))
flag_geo <- c("duplicato_esatto",
  "misura_mancante",
  "interno_superiore",
  "non_positivo", "usabile_geometria")
registro <- cbind(fossili_raw,
                  fossili[flag_geo])
table(registro$usabile_geometria)
