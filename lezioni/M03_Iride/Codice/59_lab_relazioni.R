# Stesso seme, forme differenti
rL <- lab_relazioni(shape="line",
  noise=1, seed=17)
rQ <- lab_relazioni(shape="curve",
  noise=1, seed=17)
rbind(lineare=rL$indicatori,
      quadratica=rQ$indicatori)
