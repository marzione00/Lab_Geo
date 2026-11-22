ritorno <- read.csv(percorso_risultati("consegna_VAR.csv"))
 mod2 <- readRDS(percorso_risultati("modello_VAR.rds"))
 stopifnot(identical(ritorno$passo,251:260),
   isTRUE(all.equal(ritorno$X_prevista,pr[,1],check.attributes=FALSE,tolerance=1e-10)),
   isTRUE(all.equal(prevedi_var(mod2,10),pr)))
 scheda <- c("VAR(1) didattico su processi sintetici.",
   "Train: passi 1-250. Test: passi 251-260. Origine fissa 250.",
   "Due regressioni OLS con intercetta e ritardi X,Y.",
   "Granger: due direzioni pianificate, correzione Holm.",
   "Limiti: simulazione, singola origine, nessuna attribuzione causale fisica.")
 writeLines(scheda,percorso_risultati("scheda_modello.txt"),useBytes=TRUE)
 cat(paste(scheda,collapse="
"))
