mese_T <- as.integer(format(temp$data, "%m"))
base_T <- temp$data >= as.Date("2000-01-01") &
          temp$data <= as.Date("2004-12-01")
clima_T <- tapply(temp$temperatura_C[base_T],
                 mese_T[base_T], mean)
riferimento_T <- unname(clima_T[mese_T])
anomalia_T <- temp$temperatura_C - riferimento_T
