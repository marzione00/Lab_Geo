set.seed(17)
j90 <- sample.int(length(x88),
  length(x88), replace = TRUE)
head(j90, 12)
# I valori adiacenti nella replica
# possono essere lontani nella serie.
head(diff(j90), 11)
