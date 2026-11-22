# Due misure per ciascun provino
v <- c("massa_g", "volume_cm3")
lunga <- reshape(campioni[c("id", v)],
 varying = v, v.names = "valore",
 times = v, timevar = "variabile",
 idvar = "id", direction = "long")
rownames(lunga) <- NULL
head(lunga, 3)
