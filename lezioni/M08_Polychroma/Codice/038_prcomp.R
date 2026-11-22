pc <- prcomp(X, center = TRUE,
             scale. = TRUE)
head(pc$x[, 1:2])  # scores
pc$rotation[, 1:2] # direzioni
pc$center          # medie
pc$scale           # deviazioni standard
