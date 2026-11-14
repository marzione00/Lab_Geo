# Valuta separatamente la disponibilità delle misure, prima di ogni filtro.
has_diameter <- is.finite(observations$diameter) & observations$diameter > 0
has_albedo <- is.finite(observations$albedo) & observations$albedo >= 0
complete <- has_diameter & has_albedo

# La soglia riguarda soltanto gli oggetti con entrambe le misure disponibili.
keep <- complete & observations$diameter >= p$min_diameter
keep[is.na(keep)] <- FALSE
data <- observations[keep, , drop = FALSE]
stopifnot(nrow(data) >= 3)
rho <- cor(data$diameter, data$albedo, method = "spearman")
metrics <- metric(
  "Asteroidi estratti" = nrow(observations),
  "Coppie disponibili prima della soglia" = sum(complete),
  "Oggetti selezionati" = nrow(data),
  "Correlazione di Spearman" = f(rho),
  "Diametro mediano [km]" = f(median(data$diameter))
)

# La scala logaritmica rende leggibili diametri di ordine di grandezza diverso.
g1 <- ggplot(data, aes(x = diameter, y = albedo)) +
  geom_point(colour = col_geo[1], size = 2.2, alpha = 0.60) +
  scale_x_log10() +
  labs(title = "Diametro e albedo geometrica",
       subtitle = "NASA/JPL SBDB · asteroidi numerati selezionati",
       x = "Diametro [km, scala logaritmica]", y = "Albedo geometrica [adimensionale]")

# Mostra la disponibilità originaria: il filtro dimensionale non modifica questi conteggi.
availability <- data.frame(
  misura = rep(c("Diametro", "Albedo"), each = 2),
  stato = rep(c("Disponibile", "Assente/non valida"), times = 2),
  conteggio = c(sum(has_diameter), sum(!has_diameter), sum(has_albedo), sum(!has_albedo))
)
g2 <- ggplot(availability, aes(x = misura, y = conteggio, fill = stato)) +
  geom_col(position = "stack", width = 0.60) +
  scale_fill_manual(values = c("Disponibile" = col_geo[1], "Assente/non valida" = col_geo[2])) +
  labs(title = "Disponibilità delle misure nel CSV",
       subtitle = "Conteggi prima della selezione per diametro",
       x = NULL, y = "Numero di asteroidi")
plots <- list(g1, g2)
