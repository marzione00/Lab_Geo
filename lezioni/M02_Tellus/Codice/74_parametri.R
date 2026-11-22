cfg <- list(tolleranza = 2, seme = 17)
qc_cfg <- abs(totale - 100) <=
  cfg$tolleranza
table(qc_cfg)
# Estrazione di quattro identificativi
set.seed(cfg$seme)
sample(campioni$id, size = 4)
sessionInfo()
