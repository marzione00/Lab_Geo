originale_piccolo <- (nir[3]-rosso[3])/(nir[3]+rosso[3])
perturbato <- (nir[3]-(rosso[3]+1e-10))/(nir[3]+rosso[3]+1e-10)
data.frame(indice_non_mascherato=originale_piccolo,indice_perturbato=perturbato,
  variazione=perturbato-originale_piccolo,perturbazione_assoluta=1e-10)
