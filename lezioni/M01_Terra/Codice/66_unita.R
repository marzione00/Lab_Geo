# Conserva anche le colonne originali.
demo$pioggia_m <- demo$pioggia / 1000
demo$sole_ore <- demo$sole / 60
stopifnot(all(demo$pioggia >= 0))
stopifnot(all(demo$nubi >= 0),
          all(demo$nubi <= 100))
# In demo la nuvolosita e in %.
