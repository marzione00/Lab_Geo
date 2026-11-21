controllo <- data.frame(area_conteggio_m2=sum(risultato$area_m2),
  area_estensione_m2=(870-0+30)*(690-0+30),
  quota_area=sum(risultato$area_ha))
controllo
stopifnot(controllo$area_conteggio_m2==controllo$area_estensione_m2)
