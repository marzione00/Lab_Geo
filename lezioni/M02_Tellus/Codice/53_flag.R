est <- fossili$diametro_tot_um
int <- fossili$diametro_int_um
pres <- is.finite(est) &
        is.finite(int)
viol <- pres & (est <= 0 |
               int < 0 | int > est)
stopifnot(!anyNA(viol))
table(presente = pres,
      violazione = viol)
