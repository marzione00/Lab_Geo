# GeoStat Lab: controlli numerici delle schede del quaderno.
# Codice: PolyForm Noncommercial 1.0.0, https://polyformproject.org/licenses/noncommercial/1.0.0
# Required Notice: Copyright 2026 Marzio De Corato (https://github.com/marzione00/Lab_Geo)
#
# Uso: Rscript exercise_checks.R <repo> <lezione> <specifica.json> <uscita.json>
# La specifica, preparata dall'importatore, elenca per ogni scheda il laboratorio del sito e gli
# scenari A e B, come chiamate alle funzioni lab_* del progetto o come parametri espliciti, con
# gli eventuali valori attesi. Per ogni scenario esegue il programma R del laboratorio del sito con
# quei parametri, associa ogni valore atteso all'indicatore che il sito mostra e riporta gli
# indicatori mostrati. I valori attesi che il sito non mostra sono elencati a parte.
suppressPackageStartupMessages({ library(jsonlite); library(ggplot2) })
a <- commandArgs(trailingOnly = TRUE)
stopifnot(length(a) == 4L)
repo <- a[[1]]; lesson <- a[[2]]; spec <- fromJSON(a[[3]], simplifyVector = FALSE); out_file <- a[[4]]
acts <- fromJSON(file.path(repo, "content/experiments.json"), simplifyVector = FALSE)$activities
acts <- setNames(acts, vapply(acts, `[[`, "", "id"))
env0 <- new.env()
sys.source(file.path(repo, "R/lab-common.R"), envir = env0)
f <- get("f", env0)
# Funzioni lab_* del progetto: soltanto le definizioni, per leggere gli argomenti delle chiamate.
labs <- new.env()
if (!is.null(spec$labs_file)) {
  for (ex in parse(file.path(lesson, spec$labs_file), keep.source = FALSE))
    if (is.call(ex) && as.character(ex[[1]]) %in% c("<-", "=") && is.call(ex[[3]]) &&
        identical(as.character(ex[[3]][[1]]), "function"))
      eval(ex, labs)
}
given_of <- function(call) {
  cl <- parse(text = call, keep.source = FALSE)[[1]]
  fn <- get(as.character(cl[[1]]), envir = labs)
  lapply(as.list(match.call(fn, cl))[-1], eval, envir = baseenv())
}
out <- list()
for (card in spec$cards) {
  act <- acts[[card$id]]
  if (is.null(act)) stop("laboratorio assente nel sito: ", card$id)
  res <- list(scenarios = list(), checks = list(), metrics = list(), missing = list())
  for (sc in c("A", "B")) {
    given <- if (!is.null(card$calls)) given_of(card$calls[[sc]]) else card$params[[sc]]
    p <- setNames(lapply(act$controls, `[[`, "value"), vapply(act$controls, `[[`, "", "key"))
    for (k in names(given)) {
      if (!k %in% names(p)) stop("parametro ", k, " assente in ", card$id)
      p[[k]] <- given[[k]]
    }
    ev <- new.env(parent = env0)
    assign("p", p, ev)
    set.seed(p$seed)
    eval(parse(text = act$code), envir = ev)
    m <- get("metrics", ev)
    shown <- trimws(m$valore)
    res$scenarios[[sc]] <- list(params = given, full = p)
    res$metrics[[sc]] <- lapply(seq_len(nrow(m)), function(i) list(grandezza = m$grandezza[i], mostrato = shown[i]))
    for (row in card$expected[[sc]]) {
      hit <- which(shown == trimws(f(row$valore)) | shown == as.character(row$valore))
      if (!length(hit)) {
        # Indicatore del progetto locale che il laboratorio del sito non mostra: non si può verificare.
        res$missing[[length(res$missing) + 1L]] <- list(scenario = sc, parametro = row$parametro, valore = row$valore)
        next
      }
      res$checks[[length(res$checks) + 1L]] <- list(
        scenario = sc, parametro = row$parametro, valore = row$valore,
        metrica = m$grandezza[hit[1]], mostrato = shown[hit[1]])
    }
  }
  out[[card$id]] <- res
}
writeLines(toJSON(out, auto_unbox = TRUE, digits = NA, null = "null"), out_file, useBytes = TRUE)
cat(sprintf("%d schede, %d valori attesi associati agli indicatori del sito\n", length(out),
            sum(vapply(out, function(x) length(x$checks), 0L))))
