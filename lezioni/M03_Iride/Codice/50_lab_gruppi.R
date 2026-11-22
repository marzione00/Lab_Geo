# Stesso delta e stesso seme
gA <- lab_gruppi(delta = 1,
                ratio = 1, seed = 17)
gB <- lab_gruppi(delta = 1,
                ratio = 2, seed = 17)
rbind(gA$indicatori, gB$indicatori)
