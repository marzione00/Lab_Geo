# Un piccolo file scritto nel codice
csv <- "id;valore\nA;1,25\nB;2,50"
d <- read.csv(text = csv,
              sep = ";", dec = ",")
str(d)
mean(d$valore)       # 1.875
