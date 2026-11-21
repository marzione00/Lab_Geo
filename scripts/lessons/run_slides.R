# GeoStat Lab: esecuzione di riferimento del codice delle slide di una lezione.
# Codice: PolyForm Noncommercial 1.0.0, https://polyformproject.org/licenses/noncommercial/1.0.0
# Required Notice: Copyright 2026 Marzio De Corato (https://github.com/marzione00/Lab_Geo)
#
# Uso: Rscript run_slides.R <cartella-lezione> <uscita.json>
# Esegue i file Codice/NNN_*.R in ordine, come in Lezione_Pelago.R, e registra per ciascuno
# l'eco della console. Calcola poi i file precedenti di cui ogni slide ha bisogno
# (simboli definiti al livello superiore e usati dopo) e verifica che l'esecuzione
# del solo insieme di dipendenze riproduca esattamente l'uscita sequenziale.
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 2L)
src <- normalizePath(args[[1]], mustWork = TRUE)
out_file <- args[[2]]
max_chars <- 6000L

files <- sort(list.files(file.path(src, "Codice"), pattern = "^[0-9]{3}_.*\\.R$"))
stopifnot(length(files) > 0L, !anyDuplicated(substr(files, 1, 3)))
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
  direct[[i]] <- sort(unique(need))
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
  sink(tc); sink(tc, type = "message")
  status <- tryCatch(
    withCallingHandlers({
      source(exprs = parse(text = text, keep.source = TRUE), local = env, echo = TRUE,
             print.eval = TRUE, spaced = FALSE, max.deparse.length = Inf)
      "ok"
    }, warning = function(w) {
      message("Avviso: ", conditionMessage(w))
      invokeRestart("muffleWarning")
    }),
    error = function(e) { message("Errore: ", conditionMessage(e)); "error" }
  )
  sink(type = "message"); sink(); close(tc)
  text <- paste(lines, collapse = "\n")
  if (nchar(text) > max_chars) text <- paste0(substr(text, 1, max_chars), "\n[...] uscita abbreviata")
  list(output = text, status = status)
}
fresh <- function() {
  owd <- setwd(src)
  env <- new.env(parent = globalenv())
  sys.source(file.path(src, "setup.R"), envir = env, keep.source = FALSE)
  setwd(owd)
  env
}
in_project <- function(f) { owd <- setwd(src); on.exit(setwd(owd)); f() }

grDevices::pdf(NULL)
options(pager = function(files, header, title, delete.file) invisible(NULL))
# Esecuzione sequenziale di riferimento.
seq_env <- fresh()
reference <- in_project(function() lapply(code, run_one, env = seq_env))
# Esecuzione con le sole dipendenze, file per file.
result <- list()
for (i in seq_along(files)) {
  deps <- closure(i)
  env <- fresh()
  in_project(function() for (j in deps) invisible(run_one(code[[j]], env)))
  alone <- in_project(function() run_one(code[[i]], env))
  exact <- identical(alone$output, reference[[i]]$output)
  if (!exact) deps <- seq_len(i - 1L)
  result[[files[[i]]]] <- list(
    output = reference[[i]]$output,
    status = reference[[i]]$status,
    deps = I(files[deps]),
    closure = exact,
    plots = grepl("\\b(plot|hist|barplot|boxplot|curve|matplot|image)\\(", code[[i]])
  )
}
invisible(grDevices::dev.off())
meta <- list(R = R.version.string, files = length(files),
             exact = sum(vapply(result, function(x) x$closure, TRUE)),
             errors = I(names(result)[vapply(result, function(x) x$status != "ok", TRUE)]))
writeLines(jsonlite::toJSON(list(meta = meta, files = result), auto_unbox = TRUE, pretty = TRUE), out_file, useBytes = TRUE)
cat(sprintf("%d file; dipendenze minime verificate per %d; errori: %s\n", meta$files, meta$exact,
            if (length(meta$errors)) paste(meta$errors, collapse = ", ") else "nessuno"))
