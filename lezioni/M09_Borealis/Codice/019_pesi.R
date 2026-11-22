medie_es <- c(10, 20)
conteggi_es <- c(2, 8)
mean(medie_es)
weighted.mean(medie_es, conteggi_es)
mean(rep(medie_es, conteggi_es))
# Gli ultimi due risultati coincidono.
