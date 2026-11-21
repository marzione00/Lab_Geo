# Flag documentato in setup.R
ok_geo <- fossili$usabile_geometria
geometria <- fossili[ok_geo, ]
geometria$spessore_um <- with(
  geometria,
  (diametro_tot_um-diametro_int_um)/2)
geometria$rapporto_int_tot <- with(
  geometria,
  diametro_int_um/diametro_tot_um)
nrow(geometria)              # 21
