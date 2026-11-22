# Identita' delle misure sintetiche.
scarto67 <- with(f, diametro_tot_um -
  diametro_int_um - 2*spessore_um)
max(abs(scarto67))
# Anche l'arrotondamento conta.
summary(scarto67)
