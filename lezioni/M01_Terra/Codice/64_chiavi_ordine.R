# demo contiene una stazione fittizia.
anyDuplicated(demo$data) # atteso: 0
stopifnot(
  anyDuplicated(demo$data) == 0)
demo <- demo[order(demo$data), ]
head(demo[c("data", "tmax")])
dim(demo)             # righe, colonne
