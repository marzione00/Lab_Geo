# Conserva gli eventi con misure finite e magnitudo sopra la soglia scelta.
keep <- is.finite(observations$mag) & is.finite(observations$depth) &
  observations$mag >= p$min_mag
data <- observations[keep, , drop = FALSE]
stopifnot(nrow(data) >= 2)

# Riassume il campione selezionato; la mediana conserva l’unità della variabile.
metrics <- metric(
  "Eventi nel CSV" = nrow(observations),
  "Eventi selezionati" = nrow(data),
  "Mediana magnitudo" = f(median(data$mag)),
  "Mediana profondità [km]" = f(median(data$depth)),
  "Soglia magnitudo" = p$min_mag
)

# Il numero di classi cambia la rappresentazione, non le osservazioni selezionate.
g1 <- ggplot(data, aes(x = mag)) +
  geom_histogram(bins = p$bins, fill = col_geo[1], colour = "#F5F6F3") +
  labs(title = "Magnitudo degli eventi selezionati",
       subtitle = "Catalogo USGS · rettangolo californiano · anno 2024",
       x = "Magnitudo riportata nel catalogo", y = "Numero di eventi")

# Colora le scale di magnitudo per rendere visibile l’eterogeneità del catalogo.
types <- sort(unique(data$magType))
g2 <- ggplot(data, aes(x = mag, y = depth, colour = magType)) +
  geom_point(size = 2.3, alpha = 0.70) +
  scale_colour_manual(values = setNames(rep(col_geo, length.out = length(types)), types)) +
  labs(title = "Profondità e magnitudo", subtitle = "Ogni punto rappresenta un evento; il colore identifica magType",
       x = "Magnitudo", y = "Profondità [km]")
plots <- list(g1, g2)
