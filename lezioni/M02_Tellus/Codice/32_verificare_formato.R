# Unita' esplicite nel formato lungo
lunga$unita <- ifelse(
 lunga$variabile == "massa_g",
 "g", "cm3")
stopifnot(nrow(lunga) ==
          2L * nrow(campioni))
k <- lunga[c("id", "variabile")]
stopifnot(!anyDuplicated(k))
table(lunga$variabile, lunga$unita)
