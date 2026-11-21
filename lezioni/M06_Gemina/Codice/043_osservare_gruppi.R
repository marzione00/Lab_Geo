# Controllo descrittivo prima del test
by(f37$diametro_tot_um, f37$morfotipo,
  function(x) c(n = length(x),
    media = mean(x), sd = sd(x),
    minimo = min(x), massimo = max(x)))
