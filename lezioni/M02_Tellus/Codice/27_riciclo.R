# Esempio con due volumi mancanti
massa <- c(10, 20, 30, 40)
volume <- c(2, 5)
massa / volume      # 5, 4, 15, 8
length(massa) == length(volume)
# FALSE: mancano due volumi associati

# Nei provini le lunghezze coincidono
stopifnot(length(campioni$massa_g) ==
          length(campioni$volume_cm3))
