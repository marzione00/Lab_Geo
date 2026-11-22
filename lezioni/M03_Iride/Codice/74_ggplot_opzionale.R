# Estensione facoltativa
if (requireNamespace("ggplot2",
    quietly = TRUE)) {
  g74 <- ggplot2::ggplot(fossili,
    ggplot2::aes(diametro_tot_um,
                diametro_int_um,
                colour = morfotipo))
  print(g74 + ggplot2::geom_point())
}
