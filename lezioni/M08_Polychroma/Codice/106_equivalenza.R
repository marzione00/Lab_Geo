pa <- prcomp(X, center = TRUE,
             scale. = TRUE)
pb <- prcomp(scale(X), center = FALSE,
             scale. = FALSE)
max(abs(pa$sdev - pb$sdev))
max(abs(pa$x - pb$x))
