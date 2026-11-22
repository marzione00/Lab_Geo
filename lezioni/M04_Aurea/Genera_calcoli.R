# Rigenera dati e indicatori dei nove esperimenti, dalla radice del progetto.
# Tutti i dati sono simulati oppure calcolati da modelli assegnati.
source("Aurea_laboratori.R", encoding = "UTF-8")
dir.create("Dati", showWarnings = FALSE)
dir.create("Calcoli", showWarnings = FALSE)
scenari <- list(
  eventi = list(list(), list(n = 800L)),
  condizionamento = list(list(), list(prior = .1)),
  distribuzione = list(list(), list(cut = 0)),
  binomiale = list(list(), list(n = 40L)),
  poisson = list(list(), list(exposure = 6)),
  normale = list(list(), list(mu = 15, sd = 3)),
  moltiplicazione = list(list(), list(sdlog = 1.2)),
  monte_carlo = list(list(), list(B = 800L)),
  propagazione = list(list(), list(rho = .8))
)
riepilogo <- list()
for (nome in names(scenari)) {
  fun <- get(paste0("lab_", nome))
  for (j in 1:2) {
    z <- do.call(fun, scenari[[nome]][[j]])
    scenario <- c("A", "B")[j]
    riepilogo[[length(riepilogo)+1L]] <- data.frame(
      laboratorio = paste0("m04-", gsub("_", "-", nome)),
      scenario = scenario,
      parametro = names(z$indicatori),
      valore = as.numeric(z$indicatori))
    if (j == 1L) write.csv(z$dati,
      paste0("Dati/m04-", gsub("_", "-", nome), "_default.csv"),
      row.names = FALSE)
  }
}
attesi <- do.call(rbind, riepilogo)
write.csv(attesi, "Risultati_attesi_laboratori.csv", row.names = FALSE)
write.csv(attesi, "Calcoli/Scenari_A_B.csv", row.names = FALSE)
# Caso fisico: media e SD originali, ingressi indipendenti e positivi.
set.seed(17)
B <- 20000L
m <- rpos(B, 106, 1)
v <- rpos(B, 40, .6)
densita <- m/v
lin <- 2.65*sqrt((1/106)^2+(.6/40)^2)
fisico <- data.frame(grandezza = c("densita_riferimento_g_cm3",
 "sd_differenziale_g_cm3", "media_MC_g_cm3", "sd_MC_g_cm3",
 "quantile025_MC_g_cm3", "quantile975_MC_g_cm3"),
 valore = c(2.65, lin, mean(densita), sd(densita),
            quantile(densita, c(.025,.975), names = FALSE)))
write.csv(fisico, "Calcoli/Caso_densita.csv", row.names = FALSE)
# Coordinate utili a grafici vettoriali e controllo del CV lognormale.
s <- seq(.02, .3, by = .02)
rho <- c(-.8, 0, .8)
griglia <- expand.grid(sdlog = s, corr_log = rho)
t2 <- 2*griglia$sdlog^2*(1-griglia$corr_log)
griglia$sd_esatta <- 2*sqrt(expm1(t2)*exp(t2))
griglia$sd_lineare <- 2*sqrt(t2)
griglia$cv_originale <- sqrt(expm1(griglia$sdlog^2))
write.csv(griglia, "Calcoli/Propagazione_teoria.csv", row.names = FALSE)
print(attesi, row.names = FALSE)
print(fisico, row.names = FALSE)
