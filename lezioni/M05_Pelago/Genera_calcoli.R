# Rigenera i dati dei laboratori e i riepiloghi dalla radice del progetto.
source("setup.R", encoding = "UTF-8")
dir.create("Calcoli", showWarnings = FALSE)
scenari <- list(
  estimandi = list(list(), list(nHigh = 10L)),
  selezione = list(list(), list(n = 240L)),
  distribuzioni = list(list(), list(population = "exp")),
  dipendenza = list(list(), list(rho = 0)),
  intervalli = list(list(), list(rho = .2)),
  bootstrap = list(list(), list(B = 800L)),
  ricampionamento = list(list(), list(tau = 0)),
  blocchi = list(list(), list(length = 1L)),
  precisione = list(list(), list(B = 800L)))
riepilogo <- list()
for (nome in names(scenari)) {
  for (j in 1:2) {
    z <- do.call(get(paste0("lab_", nome)), scenari[[nome]][[j]])
    riepilogo[[length(riepilogo)+1L]] <- data.frame(
      laboratorio = paste0("m05-", nome), scenario = c("A", "B")[j],
      parametro = names(z$indicatori), valore = as.numeric(z$indicatori))
    if (j == 1L) {
      write.csv(z$dati, paste0("Dati/m05-", nome, "_default.csv"), row.names = FALSE)
      if (!is.null(z$campione))
        write.csv(z$campione, paste0("Calcoli/m05-", nome, "_campione.csv"), row.names = FALSE)
    }
  }
}
attesi <- do.call(rbind, riepilogo)
write.csv(attesi, "Risultati_attesi_laboratori.csv", row.names = FALSE)
write.csv(attesi, "Calcoli/Scenari_A_B.csv", row.names = FALSE)
write.csv(stazioni, "Calcoli/Medie_stazioni.csv", row.names = FALSE)
# Riepilogo di alcune grandezze del caso del corso.
x <- subset(fossili, morfotipo == "Rounded")$diametro_tot_um
y <- subset(fossili, morfotipo == "Spiky")$diametro_tot_um
riassunto <- data.frame(grandezza = c("media_Rounded_um", "media_Spiky_um",
  "contrasto_Spiky_meno_Rounded_um", "media_densita_g_cm3",
  "SD_medie_stazione_g_cm3", "SE_media_stazioni_g_cm3"),
  valore = c(mean(x), mean(y), mean(y)-mean(x), mean(provini$densita),
    sd(stazioni$densita), sd(stazioni$densita)/sqrt(nrow(stazioni))))
write.csv(riassunto, "Calcoli/Riepilogo_corso.csv", row.names = FALSE)
writeLines(capture.output(sessionInfo()), "Calcoli/sessionInfo_R.txt")
print(attesi, row.names = FALSE)
print(riassunto, row.names = FALSE)

