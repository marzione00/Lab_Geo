sv_f <- svd(scale(M))$d
sv_f / max(sv_f)
# La terza direzione è trascurabile
# alla precisione dei dati forniti.
sum(sv_f > max(sv_f) * 1e-7)
