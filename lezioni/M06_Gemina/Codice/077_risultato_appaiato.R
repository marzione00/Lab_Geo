d77 <- read.csv(
  "Dati/misure_appaiate_simulate.csv")
z77 <- d77$dopo-d77$prima
t77 <- t.test(z77)
data.frame(n=length(z77),
  stima=mean(z77),lo=t77$conf.int[1],
  hi=t77$conf.int[2],p=t77$p.value)
