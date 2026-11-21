pos <- match(format(mon$data, "%Y-%m"),
             names(media_m))
ricostruita <- unname(media_m[pos])
stopifnot(identical(is.na(ricostruita),
                    is.na(mon$co2_ppm)))
scarto <- max(abs(ricostruita - mon$co2_ppm),
              na.rm = TRUE)
stopifnot(scarto < 1e-6)
scarto
