# Confronto con i nuclei originali del sito, senza dipendenze grafiche.
# Le formule metriche originali sono valutate senza il loro arrotondamento f().
options(warn = 2)
source("setup.R", encoding = "UTF-8")
source("R/scenari_gemina.R", encoding = "UTF-8")

originale_gemina <- function(id, parametri) {
  percorso <- paste0("Risorse/Sorgenti_originali/m06-", id, ".R")
  espressioni <- parse(percorso, encoding = "UTF-8")
  env <- new.env(parent = globalenv())
  env$metric <- .metriche_gemina
  env$f <- function(x, d = 3) x
  attivo <- FALSE
  for (espr in espressioni) {
    assegna <- is.call(espr) && identical(espr[[1]], as.name("<-"))
    nome <- if (assegna && is.symbol(espr[[2]])) as.character(espr[[2]]) else ""
    if (nome == "p") {
      env$p <- parametri
      attivo <- TRUE
      next
    }
    if (!attivo || nome == "plots") next
    eval(espr, env)
    if (nome == "metrics") break
  }
  list(data = env$data, metrics = env$metrics)
}

righe <- list()
for (s in scenari_gemina) {
  nostro <- do.call(get(paste0("lab_", s$id)), s$p)
  sito <- originale_gemina(s$id, s$p)
  stopifnot(isTRUE(all.equal(nostro$data, sito$data, tolerance = 1e-13)))
  stopifnot(isTRUE(all.equal(nostro$metrics, sito$metrics, tolerance = 1e-13)))
  righe[[length(righe) + 1]] <- data.frame(laboratorio = s$id,
    scenario = s$scenario, metrica = names(nostro$metrics),
    valore = as.numeric(nostro$metrics))
  cat("OK", s$id, s$scenario, "- dati e metriche\n")
}
tabella <- do.call(rbind, righe)
write.csv(tabella, "Risultati/Valori_riferimento_22_scenari.csv", row.names = FALSE)

# Controlli legati al significato degli esperimenti.
x <- lab_permutazione(); y <- lab_permutazione(B = 1000)
stopifnot(identical(x$osservazioni, y$osservazioni))
stopifnot(identical(x$data$contrasto, head(y$data$contrasto, 200)))
for (id in c("pvalue", "potenza", "categorie")) {
  fun <- get(paste0("lab_", id))
  stopifnot(identical(fun(seed = 17)$metrics, fun(seed = 91)$metrics))
}
a <- lab_appaiati(tau = 3); b <- lab_appaiati(tau = 5)
stopifnot(max(abs(a$differenze - b$differenze)) < 1e-13)
stopifnot(all.equal(p.adjust(c(.003, .018, .041, .2), "holm"),
                    c(.012, .054, .082, .2)))
cat("22 scenari verificati con tolleranza 1e-13; controlli semantici superati.\n")
cat(R.version.string, "\n")
