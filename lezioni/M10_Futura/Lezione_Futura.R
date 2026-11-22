# M10 Futura — ingresso per la lezione e l'esplorazione interattiva.
# Aprire il progetto .Rproj, quindi eseguire questo file.
# Dipendenze: soltanto R base, stats, graphics, grDevices, utils.
source("R/stato_lezione.R",encoding="UTF-8")

cat("M10 Futura: oggetti didattici pronti.\n")
cat("CO2 storica: 168 mesi train, 36 mesi test; origine dicembre 1998.\n")
print(coef(fit))
print(metriche(as.numeric(test),fc$previsto))
print(Box.test(res,lag=24,type="Ljung-Box",fitdf=2))
cat("\nProgetto fossili: 128 train / 32 test, dati simulati.\n")
print(coef(fossilifit))
cat("\nApprofondimento VAR(1): train250, previsione ricorsiva10 passi.\n")
print(varfit$A)
print(varfit$autovalori)

# Rigenerazione integrale dei CSV, modelli, figure PDF e controlli:
# source("R/rigenera_calcoli.R",encoding="UTF-8")

# Esecuzione di uno specifico frammento delle slide, dopo questo stato:
# source("Codice/NNN.R",echo=TRUE,encoding="UTF-8")
