densita <- function(massa, volume) {
  massa / volume
}
# Chiamata sul dataset dei provini
rho <- densita(campioni$massa_g,
               campioni$volume_cm3)
head(rho)
length(rho)                  # 24
