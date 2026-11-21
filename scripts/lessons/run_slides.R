# GeoStat Lab: esecuzione di riferimento del codice delle slide di una lezione.
# Codice: PolyForm Noncommercial 1.0.0, https://polyformproject.org/licenses/noncommercial/1.0.0
# Required Notice: Copyright 2026 Marzio De Corato (https://github.com/marzione00/Lab_Geo)
#
# Uso: Rscript run_slides.R <cartella-lezione> <uscita.json> [preludio, predefinito setup.R]
# Esegue i file Codice/NNN_*.R in ordine, come in Lezione_Pelago.R, e registra per ciascuno
# l'eco della console. Calcola poi i file precedenti di cui ogni slide ha bisogno
# (simboli definiti al livello superiore e usati dopo) e verifica che l'esecuzione
# del solo insieme di dipendenze riproduca esattamente l'uscita sequenziale.
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) %in% 2:3)
prelude <- if (length(args) == 3L) args[[3]] else "setup.R"
# Presentazioni con script autonomi (T00, M13-M16): ogni file di Codice si esegue da solo, senza preludio.
standalone <- Sys.getenv("GEOSTAT_STANDALONE") == "1"
origin <- normalizePath(args[[1]], mustWork = TRUE)
out_file <- args[[2]]
max_chars <- 6000L
# I frammenti possono scrivere file (Risultati/...): si lavora su una copia della cartella.
src <- file.path(tempfile("lezione-"), basename(origin))
dir.create(dirname(src))
stopifnot(file.copy(origin, dirname(src), recursive = TRUE))

files <- list.files(file.path(src, "Codice"), pattern = if (standalone) "\\.R$" else "^[0-9]{2,3}_.*\\.R$")
if (!standalone) files <- files[order(as.integer(sub("_.*", "", files)), files)]
stopifnot(length(files) > 0L)
code <- vapply(files, function(f) paste(readLines(file.path(src, "Codice", f), warn = FALSE, encoding = "UTF-8"), collapse = "\n"), "")

targets <- function(e) {
  if (!is.call(e)) return(character())
  head <- as.character(e[[1]])[1]
  if (head %in% c("<-", "=", "<<-")) {
    lhs <- e[[2]]
    while (is.call(lhs)) lhs <- if (as.character(lhs[[1]])[1] %in% c("$", "[", "[[", "@")) lhs[[2]] else lhs[[2]]
    return(c(as.character(lhs), targets(e[[3]])))
  }
  if (head %in% c("{", "(", "if", "for", "while", "local", "suppressWarnings", "invisible"))
    return(unlist(lapply(as.list(e)[-1], targets)))
  character()
}
exprs <- lapply(code, function(x) parse(text = x, keep.source = FALSE))
defs <- lapply(exprs, function(ex) unique(unlist(lapply(ex, targets))))
uses <- lapply(exprs, function(ex) unique(all.names(ex)))

direct <- vector("list", length(files))
for (i in seq_along(files)) {
  need <- integer()
  for (s in uses[[i]]) {
    j <- which(vapply(defs[seq_len(i - 1L)], function(d) s %in% d, TRUE))
    if (length(j)) need <- c(need, max(j))
  }
  direct[[i]] <- if (standalone) integer() else sort(unique(need))
}
closure <- function(i) {
  seen <- integer(); todo <- direct[[i]]
  while (length(todo)) {
    j <- todo[[1]]; todo <- todo[-1]
    if (!(j %in% seen)) { seen <- c(seen, j); todo <- c(todo, direct[[j]]) }
  }
  sort(seen)
}

run_one <- function(text, env) {
  lines <- character()
  tc <- textConnection("lines", "w", local = TRUE)
  sink(tc)
  # Come nel sito (webR): messaggi, avvisi ed errori nella stessa connessione dell'uscita, in ordine.
  status <- tryCatch(
    withCallingHandlers({
      source(exprs = parse(text = text, keep.source = TRUE), local = env, echo = TRUE,
             print.eval = TRUE, spaced = FALSE, max.deparse.length = Inf)
      "ok"
    }, message = function(m) {
      cat(conditionMessage(m), file = tc)
      invokeRestart("muffleMessage")
    }, warning = function(w) {
      cat("Avviso: ", conditionMessage(w), "\n", sep = "", file = tc)
      invokeRestart("muffleWarning")
    }),
    error = function(e) { cat("Errore: ", conditionMessage(e), "\n", sep = "", file = tc); "error" }
  )
  sink(); close(tc)
  text <- paste(lines, collapse = "\n")
  if (nchar(text) > max_chars) text <- paste0(substr(text, 1, max_chars), "\n[...] uscita abbreviata")
  list(output = text, status = status)
}
browser <- Sys.getenv("GEOSTAT_BROWSER") == "1"
fresh <- function() {
  owd <- setwd(src)
  env <- new.env(parent = globalenv())
  if (!nzchar(prelude)) {
    setwd(owd)
    return(env)
  }
  if (browser) {
    # Come nel sito: ogni espressione del preludio è eseguita da sola, gli errori non fermano le successive.
    for (ex in parse(file.path(src, prelude), keep.source = FALSE))
      invisible(utils::capture.output(suppressMessages(try(eval(ex, env), silent = TRUE))))
    setwd(owd)
    return(env)
  }
  invisible(utils::capture.output(suppressMessages(sys.source(file.path(src, prelude), envir = env, keep.source = FALSE))))
  setwd(owd)
  env
}
in_project <- function(f) { owd <- setwd(src); on.exit(setwd(owd)); f() }

# Pacchetti disponibili nel browser (webR del sito) e pacchetti di base.
webr <- c(jsonlite::fromJSON(file.path(Sys.getenv("GEOSTAT_ROOT"), "vendor/r-packages-lock.json"))$package,
          rownames(installed.packages(priority = "base")))
static_needs <- function(text) {
  m <- regmatches(text, gregexpr("([A-Za-z][A-Za-z0-9.]*)::|(library|require|requireNamespace)\\(\\s*[\"']?([A-Za-z][A-Za-z0-9.]*)", text))[[1]]
  unique(sub("^(library|require|requireNamespace)\\(\\s*[\"']?", "", sub("::$", "", m)))
}
grDevices::pdf(NULL)
# Come nel sito: le pagine di help() compaiono come testo nell'uscita.
options(pager = function(files, header, title, delete.file)
  for (f in files) cat(gsub(".\b", "", readLines(f, warn = FALSE), useBytes = TRUE), sep = "\n"))
if (browser) {
  # Prova con i soli pacchetti disponibili nel browser: esito di ogni frammento con le sue dipendenze.
  status <- list()
  for (i in seq_along(files)) {
    env <- fresh()
    in_project(function() for (j in closure(i)) invisible(run_one(code[[j]], env)))
    status[[files[[i]]]] <- in_project(function() run_one(code[[i]], env))$status
  }
  writeLines(jsonlite::toJSON(status, auto_unbox = TRUE), out_file)
  quit(save = "no")
}
# Esecuzione sequenziale di riferimento; i pacchetti caricati dal preludio valgono per ogni frammento.
ns0 <- loadedNamespaces()
seq_env <- fresh()
prelude_loaded <- setdiff(setdiff(loadedNamespaces(), ns0), webr)
prelude_static <- if (!nzchar(prelude)) character() else
  intersect(setdiff(static_needs(paste(readLines(file.path(src, prelude), warn = FALSE), collapse = "\n")), webr),
            rownames(installed.packages()))
# Contano i pacchetti caricati davvero dal preludio; il nome mostrato è quello chiamato nel testo, se c'è.
prelude_needs <- if (!length(prelude_loaded)) character() else if (length(prelude_static)) prelude_static else prelude_loaded
reference <- if (standalone) list() else in_project(function() lapply(code, run_one, env = seq_env))
# Esecuzione con le sole dipendenze, file per file.
result <- list()
base_ns <- loadedNamespaces()
for (i in seq_along(files)) {
  deps <- closure(i)
  env <- fresh()
  before <- loadedNamespaces()
  in_project(function() for (j in deps) invisible(run_one(code[[j]], env)))
  alone <- in_project(function() run_one(code[[i]], env))
  if (standalone) reference[[i]] <- alone
  loaded <- setdiff(loadedNamespaces(), before)
  uses <- setdiff(static_needs(paste(code[c(deps, i)], collapse = "\n")), webr)
  needs <- setdiff(unique(c(loaded, uses)), webr)
  needs <- needs[needs %in% rownames(installed.packages())]
  # Per l'avviso del sito bastano i pacchetti chiamati dal codice; le dipendenze caricate restano implicite.
  if (length(needs)) needs <- if (length(intersect(uses, needs))) intersect(uses, needs) else needs
  for (k in 1:3) for (ns in rev(setdiff(loadedNamespaces(), base_ns))) try(unloadNamespace(ns), silent = TRUE)
  exact <- identical(alone$output, reference[[i]]$output)
  if (!exact) deps <- seq_len(i - 1L)
  result[[files[[i]]]] <- list(
    output = reference[[i]]$output,
    status = reference[[i]]$status,
    deps = I(files[deps]),
    closure = exact,
    needs = I(sort(needs)),
    plots = grepl("\\b(plot|hist|barplot|boxplot|curve|matplot|image)\\(", code[[i]])
  )
}
invisible(grDevices::dev.off())
meta <- list(R = R.version.string, files = length(files), prelude = prelude, prelude_needs = I(prelude_needs),
             exact = sum(vapply(result, function(x) x$closure, TRUE)),
             errors = I(names(result)[vapply(result, function(x) x$status != "ok", TRUE)]))
writeLines(jsonlite::toJSON(list(meta = meta, files = result), auto_unbox = TRUE, pretty = TRUE), out_file, useBytes = TRUE)
cat(sprintf("%d file; dipendenze minime verificate per %d; errori: %s\n", meta$files, meta$exact,
            if (length(meta$errors)) paste(meta$errors, collapse = ", ") else "nessuno"))
