# Almeno 10 eventi, media 6
ppois(9, lambda=6,
      lower.tail=FALSE)
# Primo conteggio con cumulata >= .95
qpois(.95, lambda=6)
ppois(10, lambda=6)
