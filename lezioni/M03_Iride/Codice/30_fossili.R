diam <- fossili$diametro_tot_um
stopifnot(all(is.finite(diam)),
          all(diam > 0))
c(n = length(diam),
  media = mean(diam),
  mediana = median(diam),
  sd = sd(diam))
quantile(diam, c(.25, .5, .75),
         type = 7)
