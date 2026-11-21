# Misure in micrometri: stessa riga
r_x <- fossili$diametro_tot_um
r_y <- fossili$diaframma_um
stopifnot(all(is.finite(r_x)),
          all(is.finite(r_y)))
r_xy <- data.frame(id = fossili$id,
                   x = r_x, y = r_y)
head(r_xy, 3)
