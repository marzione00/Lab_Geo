a <- c(1, 1, 2, 2, 3, 3)
b <- c(3, 3, 1, 1, 2, 2)
# I numeri dei gruppi sono arbitrari.
mean(a == b)
accordo_coppie(a, b)  # vale 1
indice_rand_corretto(a, b)
