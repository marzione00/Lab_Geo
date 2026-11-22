# Simulazione diretta delle stime
n17 <- 60
set.seed(17)
t17 <- rnorm(200,mean=9,
             sd=2/sqrt(n17))
mean(t17)-10 # bias simulato
9-10         # bias del modello
