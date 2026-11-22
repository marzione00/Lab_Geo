# PCA nella geometria CLR dichiarata.
pc_clr <- prcomp(clr, center = TRUE,
                 scale. = FALSE)
pc_clr$sdev
# Ultima SD circa zero: vincolo noto.
