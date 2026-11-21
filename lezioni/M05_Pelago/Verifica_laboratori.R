# Verifica dei nuclei numerici dei nove esperimenti, senza interfaccia web.
# Il formatter originale f() viene sostituito dall'identita' per usare
# tutta la precisione. I grafici ggplot2 originali non vengono eseguiti.
source("setup.R", encoding = "UTF-8")
originale <- function(slug, modifiche = list()) {
  percorso <- paste0("Risorse/Sorgenti_originali/m05-", slug, ".R")
  espr <- parse(percorso, encoding = "UTF-8")
  env <- new.env(parent = globalenv())
  env$f <- function(x, d = 3) x
  env$metric <- function(...) unlist(list(...))
  avviato <- FALSE
  for (expr in espr) {
    ass <- is.call(expr) && identical(expr[[1]], as.name("<-"))
    lhs <- if (ass) as.character(expr[[2]])[1] else ""
    if (!avviato && lhs == "ar_series") eval(expr, env)
    if (!avviato && lhs == "p") {
      eval(expr, env)
      env$p <- modifyList(env$p, modifiche)
      avviato <- TRUE
      next
    }
    if (!avviato) next
    if (lhs == "plots") next
    eval(expr, env)
    if (lhs == "metrics") break
  }
  stopifnot(exists("data", env), exists("metrics", env))
  env
}
scenari <- list(
  estimandi = list(list(), list(nHigh = 10L)),
  selezione = list(list(), list(n = 240L)),
  distribuzioni = list(list(), list(population = "exp")),
  dipendenza = list(list(), list(rho = 0)),
  intervalli = list(list(), list(rho = .2)),
  bootstrap = list(list(), list(B = 800L)),
  ricampionamento = list(list(), list(tau = 0)),
  blocchi = list(list(), list(length = 1L)),
  precisione = list(list(), list(B = 800L))
)
n_controlli <- 0L
for (nome in names(scenari)) {
  for (j in 1:2) {
    args <- scenari[[nome]][[j]]
    fonte <- originale(nome, args)
    locale <- do.call(get(paste0("lab_", nome)), args)
    stopifnot(isTRUE(all.equal(locale$dati, fonte$data, tolerance = 1e-13)))
    stopifnot(isTRUE(all.equal(unname(locale$indicatori),
      as.numeric(fonte$metrics), tolerance = 1e-13)))
    if (nome %in% c("bootstrap", "ricampionamento", "blocchi", "precisione"))
      stopifnot(isTRUE(all.equal(locale$campione, fonte$x, tolerance = 1e-13)))
    if (nome == "intervalli")
      stopifnot(identical(locale$mostrati, fonte$shown))
    n_controlli <- n_controlli + 1L
    cat(nome, c("A", "B")[j], ": dati e indicatori concordi\n")
  }
}
# Proprieta' specifiche dei modelli e degli estimandi.
a <- lab_estimandi(nHigh = 10)
stopifnot(abs(diff(a$indicatori)) < 1e-12)
a <- lab_dipendenza(rho = 0)
stopifnot(a$indicatori["n_eff"] == 60,
          a$indicatori["se_corretto"] == a$indicatori["se_indipendenza"])
stopifnot(abs(lab_dipendenza()$indicatori["n_eff"]-4.6875) < 1e-12)
a <- lab_bootstrap(B = 200)
b <- lab_bootstrap(B = 800)
stopifnot(identical(a$campione, b$campione),
          identical(a$dati$media, b$dati$media[1:200]))
a <- lab_precisione(B = 200)
b <- lab_precisione(B = 800)
stopifnot(identical(a$campione, b$campione), nrow(a$dati) == 30)
# Il ciclo circolare di lunghezza n conserva la media e collassa la varianza.
a <- lab_blocchi(length = 120, B = 40)
stopifnot(abs(a$indicatori["se_blocchi"]) < 1e-14)
# I due dataset del corso hanno le unita' indicate nelle slide.
stopifnot(nrow(fossili) == 160, all(table(fossili$morfotipo) == 80),
          nrow(provini) == 24, nrow(stazioni) == 6,
          all(table(provini$stazione) == 4),
          all(table(stazioni$affioramento) == 3))
cat("OK:", n_controlli, "confronti A/B, campione fisso, pesi e casi limite.\n")

