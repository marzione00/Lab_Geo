# Iride M03 - oggetti comuni della lezione
# Aprire Iride_M03.Rproj o lavorare dalla cartella del progetto.
# I CSV originali restano invariati. Nessuna simulazione viene eseguita qui.

leggi_csv <- function(nome) {
  percorso <- file.path("Dati", nome)
  stopifnot(file.exists(percorso))
  read.csv(percorso, stringsAsFactors = FALSE, fileEncoding = "UTF-8")
}

fossili <- leggi_csv("fossili_simulati.csv")
fossili$morfotipo <- factor(fossili$morfotipo,
                          levels = c("Rounded", "Spiky"))
rocce <- leggi_csv("rocce_simulate.csv")
campioni <- leggi_csv("campioni_modulo1.csv")

stopifnot(nrow(fossili) == 160L,
          identical(as.vector(table(fossili$morfotipo)), c(80L, 80L)),
          !anyDuplicated(fossili$id),
          all(is.finite(fossili$diametro_tot_um)),
          all(fossili$diametro_tot_um > 0),
          nrow(rocce) == 90L,
          all(is.finite(rocce$grana_mm)), all(rocce$grana_mm > 0),
          nrow(campioni) == 24L)

# Le funzioni descrivono i nove esperimenti interattivi.
# La lettura del file le definisce senza estrarre numeri casuali.
source("Iride_laboratori.R", encoding = "UTF-8")
