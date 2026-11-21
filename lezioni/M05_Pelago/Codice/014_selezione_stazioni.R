# Prima stazioni, poi le loro righe
ids14 <- unique(d05$stazione)
set.seed(17)
scelte14 <- sample(ids14,size=2)
d05[d05$stazione %in% scelte14, ]
# Le righe della stessa stazione
# restano insieme nella selezione.
