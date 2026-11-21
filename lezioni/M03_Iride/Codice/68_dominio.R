# Grana in mm; riferimento 1 mm
l_g <- rocce$grana_mm
l_ref <- 1
stopifnot(all(is.finite(l_g)),
          all(l_g > 0))
l_y <- log(l_g/l_ref)
head(l_y)
