# Una nuova grandezza per ogni provino
stopifnot(all(campioni$volume_cm3>0))
campioni$densita <-
 campioni$massa_g/campioni$volume_cm3
head(campioni[c("id", "densita")], 4)
# Unita' del rapporto: g/cm^3
