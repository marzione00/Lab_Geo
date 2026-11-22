# Contributi in (g/cm^3)^2
q70 <- c(massa = (1/40)^2,
         volume = (106*.6/40^2)^2)
u70 <- sqrt(sum(q70))
c(SD_approssimata = u70)
100*q70/sum(q70)
