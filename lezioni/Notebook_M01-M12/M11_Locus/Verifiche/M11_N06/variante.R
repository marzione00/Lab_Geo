locale <- sf::st_as_sf(d,coords=c("x_m","y_m"),crs=NA)
errore_atteso <- tryCatch({sf::st_transform(locale,32632);NA_character_},
  error=function(e) conditionMessage(e))
errore_atteso
stopifnot(is.character(errore_atteso),!is.na(errore_atteso))
