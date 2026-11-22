# Confronto con i sorgenti originali conservati in Risorse/Fonti/Originali.
# Si eseguono solo i calcoli, senza ggplot2 o scrittura delle figure originali.
# Il formatter f() e' reso identita' per confrontare numeri non arrotondati.
source("Aurea_laboratori.R", encoding = "UTF-8")
originale <- function(slug, modifiche = list()) {
  percorso <- paste0("Risorse/Fonti/Originali/m04-", slug, ".R")
  espr <- parse(percorso, encoding = "UTF-8")
  env <- new.env(parent = globalenv())
  env$f <- function(x, d = 3) x
  env$metric <- function(...) unlist(list(...))
  avviato <- FALSE
  for (expr in espr) {
    assegnazione <- is.call(expr) && identical(expr[[1]], as.name("<-"))
    lhs <- if (assegnazione) as.character(expr[[2]])[1] else ""
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
  eventi = list(list(), list(n = 800L)),
  condizionamento = list(list(), list(prior = .1)),
  distribuzione = list(list(), list(cut = 0)),
  binomiale = list(list(), list(n = 40L)),
  poisson = list(list(), list(exposure = 6)),
  normale = list(list(), list(mu = 15, sd = 3)),
  moltiplicazione = list(list(), list(sdlog = 1.2)),
  monte_carlo = list(list(), list(B = 800L)),
  propagazione = list(list(), list(rho = .8))
)
n_controlli <- 0L
for (nome in names(scenari)) {
  for (j in 1:2) {
    args <- scenari[[nome]][[j]]
    fonte <- originale(gsub("_", "-", nome), args)
    locale <- do.call(get(paste0("lab_", nome)), args)
    stopifnot(isTRUE(all.equal(locale$dati, fonte$data, tolerance = 1e-13)))
    stopifnot(isTRUE(all.equal(unname(locale$indicatori),
      as.numeric(fonte$metrics), tolerance = 1e-13)))
    if (nome == "binomiale") {
      stopifnot(identical(locale$simulazioni, fonte$sim),
                identical(locale$frequenze, fonte$emp))
    }
    n_controlli <- n_controlli + 1L
    cat(nome, c("A", "B")[j], ": dati e indicatori concordi\n")
  }
}
# Gli esperimenti deterministici ignorano il seme.
for (nome in c("condizionamento", "distribuzione", "poisson", "normale")) {
  a <- do.call(get(paste0("lab_", nome)), list(seed = 17))
  b <- do.call(get(paste0("lab_", nome)), list(seed = 18))
  stopifnot(identical(a$dati, b$dati), identical(a$indicatori, b$indicatori))
}
# Invarianti teorici: probabilita', parametri e casi degeneri.
stopifnot(abs(sum(lab_distribuzione()$indicatori)-1) < 1e-14)
stopifnot(abs(sum(lab_binomiale()$dati$probabilita)-1) < 1e-14)
stopifnot(lab_condizionamento(pa=.3, pb=.3)$indicatori["indipendenza"] == 1)
stopifnot(lab_monte_carlo(B=800)$indicatori["se_mc_teorico"] ==
            lab_monte_carlo(B=200)$indicatori["se_mc_teorico"]/2)
r <- lab_propagazione(rho=1)
stopifnot(max(abs(r$dati$rapporto-2)) < 1e-13,
            r$indicatori["sd_esatta"] == 0)
cat("OK:", n_controlli, "confronti A/B, seme deterministico e invarianti.\n")
