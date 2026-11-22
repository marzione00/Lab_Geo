phi2 <- c(0.6,-0.2)
radici <- polyroot(c(1,-phi2))
Mod(radici)
stopifnot(all(Mod(radici)>1))
