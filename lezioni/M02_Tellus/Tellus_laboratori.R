# Tellus — dieci esperimenti M02 riscritti con sole funzioni distribuite con R.
# Modelli e configurazioni corrispondono al sito Lab_Geo del 18 novembre 2026.
# Eseguire source("Tellus_laboratori.R"), poi modificare gli argomenti mostrati.
# Le funzioni restituiscono dati e indicatori. Non sovrascrivono i CSV del progetto.

lab_progetto <- function(a = 1, b = 0) {
  x <- 1:10
  dati <- data.frame(x = x, y = a*x+b)
  list(dati = dati, indicatori = c(a = a, b = b, media = mean(dati$y)))
}

lab_selezioni <- function(lo = 3, hi = 8) {
  x <- seq(0, 10, 0.5)
  # Il sito ordina gli estremi prima di applicare l'intervallo chiuso.
  a <- min(lo, hi)
  b <- max(lo, hi)
  incluso <- x >= a & x <= b
  list(dati = data.frame(riga = seq_along(x), valore = x, incluso = incluso),
       indicatori = c(inclusi = sum(incluso), esclusi = sum(!incluso)))
}

lab_importazione <- function(decimal = c("comma", "point")) {
  decimal <- match.arg(decimal)
  testo <- c("1,2", "2,4", "3,1", "4,8", "ND")
  convertito <- if (decimal == "comma") sub(",", ".", testo, fixed=TRUE) else testo
  # Le conversioni fallite sono contate esplicitamente subito dopo il calcolo.
  numero <- suppressWarnings(as.numeric(convertito))
  disponibile <- !is.na(numero)
  media <- if (any(disponibile)) mean(numero[disponibile]) else NA_real_
  list(dati = data.frame(testo = testo, valore = numero,
                        disponibile = disponibile),
       indicatori = c(validi = sum(disponibile), media = media))
}

lab_aggregazioni <- function(nA = 50, seed = 17) {
  stopifnot(length(nA) == 1, is.finite(nA), nA >= 1, nA == as.integer(nA))
  set.seed(seed)
  dati <- data.frame(gruppo = rep(c("A", "B"), c(nA, 10)),
                    valore = c(rnorm(nA, 3, 1), rnorm(10, 8, 1)))
  medie <- tapply(dati$valore, dati$gruppo, mean)
  list(dati = dati, indicatori = c(media_osservazioni = mean(dati$valore),
       media_gruppi = mean(medie)),
       attese = c(media_osservazioni = (3*nA + 80)/(nA + 10), media_gruppi = 5.5))
}

lab_join <- function(duplicate = c("no", "yes")) {
  duplicate <- match.arg(duplicate)
  misure <- data.frame(stazione = c("A", "B", "C"), misura = c(2, 5, 9))
  siti <- data.frame(stazione = c("A", "B", "C"), quota = c(100, 200, 300))
  if (duplicate == "yes") siti <- rbind(siti, data.frame(stazione="B", quota=210))
  uniti <- merge(misure, siti, by="stazione", all.x=TRUE)
  list(misure = misure, siti = siti, dati = uniti,
       indicatori = c(righe_iniziali = nrow(misure), righe_finali = nrow(uniti),
         media_iniziale = mean(misure$misura), media_finale = mean(uniti$misura)))
}

lab_mancanti <- function(mechanism = c("random", "high"), rate = 0.3, seed = 17) {
  mechanism <- match.arg(mechanism)
  stopifnot(length(rate) == 1, is.finite(rate), rate >= 0, rate <= 0.8)
  set.seed(seed)
  x <- rlnorm(200, meanlog=1, sdlog=0.5)
  mancante <- if (mechanism == "random") runif(200) < rate else
    rank(x) > 200*(1-rate)
  list(dati = data.frame(riga=seq_along(x), valore_completo=x,
                        disponibile=!mancante),
       indicatori = c(mancanti=sum(mancante), media_completa=mean(x),
                      media_disponibile=mean(x[!mancante])))
}

lab_controlli <- function(bad = 250, seed = 17) {
  set.seed(seed)
  x <- c(rnorm(29, 15, 3), bad)
  nel_dominio <- x >= -50 & x <= 60
  # Intervallo didattico; segnalare non equivale a correggere o eliminare.
  list(dati = data.frame(riga=1:30, temperatura=x, nel_dominio=nel_dominio),
       indicatori = c(segnalate=sum(!nel_dominio), media=mean(x)))
}

lab_composizione <- function(a = 40) {
  stopifnot(length(a) == 1, is.finite(a), a > 0)
  x <- c(A=a, B=35, C=25)
  p <- 100*x/sum(x)
  list(dati = data.frame(componente=names(x), quantita=as.vector(x),
                        percentuale=as.vector(p)),
       indicatori = c(somma=sum(p), rapporto_B_C=unname(x[2]/x[3]),
                      percentuale_B=unname(p[2])))
}

lab_funzioni <- function(spread = 1) {
  stopifnot(length(spread) == 1, is.finite(spread), spread >= 0)
  x <- 5 + spread*c(-2, -1, 0, 1, 2)
  s <- sd(x)
  ok <- s > 0
  z <- if (ok) as.vector(scale(x)) else rep(NA_real_, 5)
  list(dati = data.frame(riga=1:5, valore=x, z=z),
       indicatori = c(sd=s, contratto=as.numeric(ok),
                       media_z=if (ok) mean(z) else NA_real_))
}

lab_tabella <- function(duplicate = c("no", "yes"), unit = c("ok", "wrong")) {
  duplicate <- match.arg(duplicate)
  unit <- match.arg(unit)
  dati <- data.frame(id=1:8, lunghezza=c(1.1, 1.3, 1.2, 1.5, 1.4, 1.1, 1.6, 1.2))
  if (duplicate == "yes") dati$id[8] <- 7
  if (unit == "wrong") dati$lunghezza[8] <- 1200
  list(dati=dati, indicatori=c(chiavi_duplicate=sum(duplicated(dati$id)),
       fuori_dominio=sum(dati$lunghezza > 10), righe=nrow(dati)))
}

# Configurazioni iniziali. La lista permette di confrontare i dieci risultati.
laboratori_iniziali <- list(
  progetto=lab_progetto(), selezioni=lab_selezioni(),
  importazione=lab_importazione(), aggregazioni=lab_aggregazioni(),
  join=lab_join(), mancanti=lab_mancanti(), controlli=lab_controlli(),
  composizione=lab_composizione(), funzioni=lab_funzioni(), tabella=lab_tabella())
lapply(laboratori_iniziali, `[[`, "indicatori")

# Esempi di confronto: togliere il # per eseguire.
# lab_join("yes")$indicatori
# lab_mancanti("high", rate=0.3, seed=17)$indicatori
# lab_composizione(a=80)$dati
# lab_funzioni(spread=0)$indicatori
# lab_tabella("yes", "wrong")$indicatori
