# GeoStat Lab: controlli numerici delle schede del quaderno.
# Codice: PolyForm Noncommercial 1.0.0, https://polyformproject.org/licenses/noncommercial/1.0.0
# Required Notice: Copyright 2026 Marzio De Corato (https://github.com/marzione00/Lab_Geo)
#
# Uso: Rscript exercise_checks.R <repo> <lezione> <quaderno.json> <risultati_attesi.csv> <uscita.json>
# Per ogni scheda legge gli scenari A e B dalla verifica locale, esegue il programma R del
# laboratorio del sito con quei parametri e associa ogni valore atteso all'indicatore che il
# sito mostra. Si ferma se un valore atteso non compare fra gli indicatori.
suppressPackageStartupMessages({ library(jsonlite); library(ggplot2) })
a <- commandArgs(trailingOnly = TRUE)
stopifnot(length(a) == 5L)
repo <- a[[1]]; workbook <- a[[3]]; expected <- a[[4]]; out_file <- a[[5]]
acts <- fromJSON(file.path(repo, "content/experiments.json"), simplifyVector = FALSE)$activities
acts <- setNames(acts, vapply(acts, `[[`, "", "id"))
book <- fromJSON(workbook, simplifyVector = FALSE)$esercizi
exp <- read.csv(expected, stringsAsFactors = FALSE)
env0 <- new.env()
sys.source(file.path(repo, "R/lab-common.R"), envir = env0)
f <- get("f", env0)
out <- list()
for (e in book) {
  act <- acts[[e$id]]
  if (is.null(act)) stop("laboratorio assente nel sito: ", e$id)
  calls <- regmatches(e$verifica_locale, gregexpr("r[AB] <- lab_[a-z]+\\([^)]*\\)", e$verifica_locale))[[1]]
  card <- list(scenarios = list(), checks = list())
  for (cl in calls) {
    sc <- substr(cl, 2, 2)
    given <- eval(parse(text = sub("^r[AB] <- lab_[a-z]+", "list", cl)))
    p <- setNames(lapply(act$controls, `[[`, "value"), vapply(act$controls, `[[`, "", "key"))
    for (k in names(given)) {
      if (!k %in% names(p)) stop("parametro ", k, " assente in ", e$id)
      p[[k]] <- given[[k]]
    }
    ev <- new.env(parent = env0)
    assign("p", p, ev)
    set.seed(p$seed)
    eval(parse(text = act$code), envir = ev)
    m <- get("metrics", ev)
    card$scenarios[[sc]] <- list(params = given, full = p)
    rows <- exp[exp$laboratorio == e$id & exp$scenario == sc, ]
    if (!nrow(rows)) stop("nessun valore atteso per ", e$id, " scenario ", sc)
    for (i in seq_len(nrow(rows))) {
      shown <- trimws(m$valore)
      hit <- which(shown == trimws(f(rows$valore[i])) | shown == as.character(rows$valore[i]))
      if (!length(hit)) stop("valore atteso non mostrato dal sito: ", e$id, " ", sc, " ", rows$parametro[i])
      card$checks[[length(card$checks) + 1L]] <- list(
        scenario = sc, parametro = rows$parametro[i], valore = rows$valore[i],
        metrica = m$grandezza[hit[1]], mostrato = shown[hit[1]])
    }
  }
  out[[e$id]] <- card
}
writeLines(toJSON(out, auto_unbox = TRUE, digits = NA, null = "null"), out_file, useBytes = TRUE)
cat(sprintf("%d schede, %d valori attesi associati agli indicatori del sito\n", length(out),
            sum(vapply(out, function(x) length(x$checks), 0L))))
