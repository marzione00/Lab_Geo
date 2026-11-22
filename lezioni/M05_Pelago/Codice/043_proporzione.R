evento43 <- c(rep(1, 18), rep(0, 42))
n43 <- length(evento43)
p43 <- mean(evento43)
sqrt(p43*(1-p43)/n43)
# Con zero eventi la stima e' zero:
# non implica certezza su p.
