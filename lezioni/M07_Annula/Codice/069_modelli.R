# Formule motivate da ipotesi diverse.
formule69 <- list(
  comune = diametro_int_um ~
    diametro_tot_um,
  additivo = diametro_int_um ~
    diametro_tot_um + morfotipo,
  interazione = diametro_int_um ~
    diametro_tot_um * morfotipo)
# La valutazione seguira' un protocollo.
names(formule69)
