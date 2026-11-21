# Quattro gruppi, SD diverse
z86 <- lab_anova(ratio=2)
w86 <- lab_anova(ratio=1)
rbind(sd_diverse=z86$metrics,
      sd_uguali=w86$metrics)
# Ogni riga contiene due metodi.
