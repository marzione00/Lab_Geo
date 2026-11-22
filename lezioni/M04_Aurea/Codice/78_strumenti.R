# Densita': 106 g / 40 cm^3
u78 <- function(um, uV) {
  2.65*sqrt((um/106)^2+(uV/40)^2)
}
u78(1, .6)    # situazione iniziale
u78(.5, .6)   # migliora la massa
u78(1, .3)    # migliora il volume
# Incertezze in g/cm^3; c=0
