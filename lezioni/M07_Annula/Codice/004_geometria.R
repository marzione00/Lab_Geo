# La relazione deriva dalla costruzione
# geometrica delle tre misure.
scarto <- with(f, diametro_tot_um -
  diametro_int_um - 2 * spessore_um)
max(abs(scarto))
# Circa 1e-8: arrotondamento del CSV.
