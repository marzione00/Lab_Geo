# Simulazione separata dai fossili
qA <- lab_quantili(noise = 1,
                  n = 60, seed = 17)
qB <- lab_quantili(noise = 2,
                  n = 60, seed = 17)
rbind(qA$indicatori, qB$indicatori)
