# Scenari A e B di un esperimento del catalogo per le pagine Scenario A e Confronto di una lezione.
# Uso, dalla radice del repository:
#   Rscript lezioni/Edizione_M17-M21/scenari.R <cartella-lezione> <id> '<json parametri A>' '<json parametri B>'
# Scrive Esperimenti/<id>-A.R, -B.R, i grafici SVG, i PDF (rsvg-convert) e <id>.json con parametri e metriche.
# Codice: PolyForm Noncommercial 1.0.0. Required Notice: Copyright 2026 Marzio De Corato.
args <- commandArgs(TRUE)
stopifnot(length(args) == 4)
dir <- args[1]; id <- args[2]
cat_ <- jsonlite::fromJSON('content/experiments.json', simplifyVector = FALSE)
a <- Filter(function(x) x$id == id, cat_$activities)[[1]]
comune <- readLines('R/lab-common.R', encoding = 'UTF-8')
uscita <- list()
for (k in c('A', 'B')) {
  par <- jsonlite::fromJSON(args[if (k == 'A') 3 else 4])
  def <- setNames(lapply(a$controls, function(c) c$value), vapply(a$controls, function(c) c$key, ''))
  def[names(par)] <- par
  val <- vapply(def, function(v) if (is.character(v)) deparse(v) else format(v, scientific = FALSE), '')
  testo <- c(comune, paste0('p <- list(', paste(names(def), '=', val, collapse = ', '), ')'), 'set.seed(p$seed)', a$code,
             'print(metrics,row.names=FALSE)',
             sprintf("ggplot2::ggsave('%s-%s.svg',plots[[1]],device=svglite::svglite,width=7.7,height=5.0,bg='#F8F6F1')", id, k))
  f <- file.path(dir, 'Esperimenti', paste0(id, '-', k, '.R'))
  writeLines(testo, f, useBytes = TRUE)
  env <- new.env()
  owd <- setwd(file.path(dir, 'Esperimenti'))
  capture.output(sys.source(basename(f), envir = env))
  setwd(owd)
  svg <- file.path(dir, 'Esperimenti', paste0(id, '-', k, '.svg'))
  system2('rsvg-convert', c('-f', 'pdf', '-o', sub('svg$', 'pdf', svg), svg))
  m <- env$metrics
  uscita[[k]] <- list(metrics = lapply(seq_len(nrow(m)), function(i) list(grandezza = m$grandezza[i], valore = m$valore[i])),
                      version = R.version.string, params = def)
  cat(k, ':', paste(m$grandezza, m$valore, sep = ' = ', collapse = '; '), '\n')
}
jsonlite::write_json(unname(uscita), file.path(dir, 'Esperimenti', paste0(id, '.json')), auto_unbox = TRUE, pretty = TRUE)
