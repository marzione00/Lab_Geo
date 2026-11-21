# Diametri costruiti, in micrometri
x07 <- c(4.2,5.1,6.4,7.0,7.3)
mean(x07)        # diametro medio
mean(x07 > 6)    # quota sopra 6
# Contrasto con ordine dichiarato
r07 <- c(4.8,5.2,5.6)
s07 <- c(6.1,6.5,7.2)
mean(s07)-mean(r07) # Spiky-Rounded
