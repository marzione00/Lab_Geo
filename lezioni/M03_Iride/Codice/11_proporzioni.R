# Stesso conteggio, denominatore noto
p11 <- prop.table(n10)
100 * p11  # Percentuali
stopifnot(abs(sum(p11) - 1) < 1e-12)
