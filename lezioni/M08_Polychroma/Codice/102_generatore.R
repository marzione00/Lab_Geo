# L'etichetta non e stata usata nella stima.
generatore <- d$litologia_generatrice
table(gruppo = km$cluster, generatore)
indice_rand_corretto(km$cluster, generatore)
