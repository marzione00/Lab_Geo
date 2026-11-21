g <- fossili$usabile_geometria
geo <- fossili[g, ]
rapporto <- geo$diametro_int_um /
            geo$diametro_tot_um
soglie <- c(0.8, 0.85, 0.9)
n_soglia <- sapply(soglie,
  function(s) sum(rapporto <= s))
data.frame(soglia = soglie,
           mantenute = n_soglia)
