d <- read.csv('dati/fossili_simulati.csv')
x <- d$diametro_tot_um[d$morfotipo=='Spiky']
y <- d$diametro_tot_um[d$morfotipo=='Rounded']
w <- t.test(x,y,var.equal=FALSE)
c(differenza=mean(x)-mean(y),
  t=unname(w$statistic),df=unname(w$parameter),
  p=w$p.value)
w$conf.int
