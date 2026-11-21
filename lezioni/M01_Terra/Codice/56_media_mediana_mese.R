# demo contiene dati simulati.
mese <- format(demo$data, "%m")
p <- demo$pioggia
tapply(p, mese, mean)   # medie
tapply(p, mese, median) # mediane
mean(p == 0)          # quota asciutti
