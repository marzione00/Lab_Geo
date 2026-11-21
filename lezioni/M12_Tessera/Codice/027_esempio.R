area_cella_ha <-
 prod(terra::res(r))/1e4
c(totale=720*area_cella_ha,
 valida=696*area_cella_ha)
