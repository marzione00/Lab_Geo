liv50 <- c(.80, .90, .95, .99)
q50 <- qt((1+liv50)/2, df = 19)
data.frame(livello = liv50,
           quantile = q50)
# La semiampiezza e' quantile * SE.
