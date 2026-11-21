G <- 0.5*outer(z,z,"-")^2
upper <- upper.tri(D)
h_pair <- D[upper]
g_pair <- G[upper]
stopifnot(length(h_pair)==2016L)
