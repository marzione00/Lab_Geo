# Esempio ridotto con tre scritture
originale <- c("6,40", " 5.40 ", "ND")
t <- trimws(originale)
assente <- t %in% c("", "ND", "NA")
t[assente] <- NA_character_
t <- sub(",", ".", t, fixed = TRUE)
valore <- as.numeric(t)
data.frame(originale, valore)
