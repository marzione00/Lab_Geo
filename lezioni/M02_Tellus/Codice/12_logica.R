# Intersezione di due condizioni
in_A <- campioni$affioramento == "A"
volume_ok <- campioni$volume_cm3 >= 40
sel <- in_A & volume_ok
sum(sel)           # Righe incluse
# Appartenenza a un insieme di nomi
liv <- c("bassa", "media")
table(campioni$alterazione %in% liv)
