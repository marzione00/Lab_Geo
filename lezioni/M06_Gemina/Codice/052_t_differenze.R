d52 <- read.csv(
  "Dati/misure_appaiate_simulate.csv")
D52 <- d52$dopo-d52$prima
n52 <- length(D52)
se52 <- sd(D52)/sqrt(n52)
t52 <- mean(D52)/se52  # H0: Delta=0
p52 <- 2*pt(-abs(t52),df=n52-1)
c(t=t52,p=p52)
