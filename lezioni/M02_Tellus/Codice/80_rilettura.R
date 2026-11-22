riletta <- read.csv(percorso_tab,
  stringsAsFactors = FALSE)
stopifnot(identical(names(riletta),
                    names(analitica)))
stopifnot(identical(riletta$id,
                    analitica$id))
stopifnot(isTRUE(all.equal(riletta,
  analitica, tolerance = 1e-10)))
