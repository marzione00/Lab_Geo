p <- carica_dati("processi_simulati.csv")
mod <- stima_var(p)
ev <- eigen(mod$A,only.values=TRUE)$values
data.frame(parte_reale=Re(ev),parte_immaginaria=Im(ev),modulo=Mod(ev))
data.frame(stabile=all(Mod(ev)<1))
