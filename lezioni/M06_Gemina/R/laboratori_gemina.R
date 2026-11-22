# Gemina M06: esperimenti riproducibili con le sole funzioni di R base.
# Gli argomenti seguono il pannello del sito. Ogni chiamata restituisce:
# data = dati del grafico; metrics = risultati numerici non arrotondati;
# parametri = impostazioni; id = identificatore dell'esperimento.
# Le variabili simulate non hanno un'unita fisica assegnata.

.metriche_gemina <- function(...) {
  z <- list(...)
  setNames(vapply(z, function(x) as.numeric(x)[1], numeric(1)), names(z))
}
.risultato_gemina <- function(id, data, metrics, parametri, ...) {
  list(id = id, data = data, metrics = metrics, parametri = parametri, ...)
}

lab_contrasto <- function(delta = 1, n = 30, seed = 17) {
  set.seed(seed)
  a <- rnorm(n); b <- rnorm(n, delta)
  test <- t.test(b, a)
  dati <- data.frame(gruppo = rep(c("A", "B"), each = n),
                     valore = c(a, b))
  valori <- .metriche_gemina(`Differenza stimata` = mean(b) - mean(a),
    `Limite inferiore` = test$conf.int[1],
    `Limite superiore` = test$conf.int[2])
  .risultato_gemina("contrasto", dati, valori,
    list(delta = delta, n = n, seed = seed), test = test)
}

lab_permutazione <- function(delta = 0.6, B = 200, seed = 17) {
  set.seed(seed)
  x <- c(rnorm(20), rnorm(20, delta))
  gruppi <- rep(0:1, each = 20)
  osservato <- diff(tapply(x, gruppi, mean))
  permutati <- replicate(B, {
    etichette <- sample(gruppi)
    diff(tapply(x, etichette, mean))
  })
  p_mc <- (1 + sum(abs(permutati) >= abs(osservato))) / (B + 1)
  valori <- .metriche_gemina(`Contrasto osservato` = osservato,
    `p Monte Carlo bilaterale` = p_mc, Permutazioni = B)
  .risultato_gemina("permutazione", data.frame(contrasto = permutati),
    valori, list(delta = delta, B = B, seed = seed),
    osservazioni = data.frame(gruppo = gruppi, valore = x))
}

lab_pvalue <- function(t = 2, df = 20, seed = 17) {
  # Nessun campione: seed non cambia le probabilita teoriche.
  griglia <- seq(-6, 6, length.out = 601)
  dati <- data.frame(x = griglia, y = dt(griglia, df),
                     coda = abs(griglia) >= abs(t))
  valori <- .metriche_gemina(`p bilaterale` = 2 * pt(-abs(t), df),
    `Gradi di libertà` = df)
  .risultato_gemina("pvalue", dati, valori,
    list(t = t, df = df, seed = seed))
}

lab_potenza <- function(n = 30, delta = 0.5, alpha = 0.05, seed = 17) {
  # n e il numero PER GRUPPO; sd comune = 1, gruppi indipendenti normali.
  calcola <- function(n) power.t.test(n = n, delta = delta, sd = 1,
    sig.level = alpha, type = "two.sample", alternative = "two.sided",
    strict = TRUE)$power
  ns <- seq(5, 300, 5)
  dati <- data.frame(x = ns, y = vapply(ns, calcola, numeric(1)))
  valori <- .metriche_gemina(`Potenza alla numerosità scelta` = calcola(n),
    Alfa = alpha)
  .risultato_gemina("potenza", dati, valori,
    list(n = n, delta = delta, alpha = alpha, seed = seed))
}

lab_welch <- function(ratio = 2, n = 30, seed = 17) {
  # ratio e il rapporto delle deviazioni standard, non delle varianze.
  set.seed(seed)
  a <- rnorm(n); b <- rnorm(n, 0.5, ratio)
  test <- t.test(b, a)
  dati <- data.frame(gruppo = rep(c("A", "B"), each = n),
                     valore = c(a, b))
  valori <- .metriche_gemina(Differenza = mean(b) - mean(a),
    `SE Welch` = sqrt(var(a) / n + var(b) / n),
    `Gradi di libertà` = test$parameter, p = test$p.value)
  .risultato_gemina("welch", dati, valori,
    list(ratio = ratio, n = n, seed = seed), test = test)
}

lab_appaiati <- function(tau = 3, seed = 17) {
  set.seed(seed)
  u <- rnorm(30, 0, tau)
  prima <- 10 + u + rnorm(30)
  dopo <- 10 + u + 0.6 + rnorm(30)
  dati <- data.frame(id = rep(1:30, 2),
    tempo = factor(rep(c("Prima", "Dopo"), each = 30),
                   levels = c("Prima", "Dopo")), valore = c(prima, dopo))
  valori <- .metriche_gemina(`Media differenze` = mean(dopo - prima),
    `SE appaiato` = sd(dopo - prima) / sqrt(30),
    `SE indipendente` = sqrt(var(prima) / 30 + var(dopo) / 30))
  .risultato_gemina("appaiati", dati, valori,
    list(tau = tau, seed = seed), differenze = dopo - prima)
}

lab_ranghi <- function(delta = 0.5, ratio = 1, seed = 17) {
  set.seed(seed)
  a <- rnorm(35); b <- rnorm(35, delta, ratio)
  test <- wilcox.test(b, a, exact = FALSE)
  dati <- data.frame(gruppo = rep(c("A", "B"), each = 35),
                     valore = c(a, b))
  # Con dati continui simulati le uguaglianze hanno probabilita zero.
  valori <- .metriche_gemina(`P empirica B > A` = mean(outer(b, a, ">")),
    `Differenza mediane` = median(b) - median(a),
    `p Wilcoxon` = test$p.value)
  .risultato_gemina("ranghi", dati, valori,
    list(delta = delta, ratio = ratio, seed = seed), test = test)
}

lab_categorie <- function(count = 25, seed = 17) {
  # Conteggi assegnati: seed non modifica la tabella.
  tab <- matrix(c(15, 35, count, 60 - count), nrow = 2, byrow = TRUE)
  test <- suppressWarnings(chisq.test(tab, correct = FALSE))
  dati <- as.data.frame(as.table(tab))
  names(dati) <- c("gruppo", "esito", "conteggio")
  valori <- .metriche_gemina(`Chi-quadrato` = test$statistic,
    `Minimo atteso` = min(test$expected), `p asintotico` = test$p.value,
    `p Fisher` = fisher.test(tab)$p.value)
  .risultato_gemina("categorie", dati, valori,
    list(count = count, seed = seed), tabella = tab, attesi = test$expected)
}

lab_multipli <- function(m = 20, alpha = 0.05, seed = 17) {
  set.seed(seed)
  grezzi <- runif(m); corretti <- p.adjust(grezzi, "holm")
  dati <- data.frame(x = 1:m, y = grezzi, corretto = corretti)
  valori <- .metriche_gemina(`Rifiuti grezzi` = sum(grezzi < alpha),
    `Rifiuti Holm` = sum(corretti < alpha),
    `FWER teorica grezza` = 1 - (1 - alpha)^m)
  .risultato_gemina("multipli", dati, valori,
    list(m = m, alpha = alpha, seed = seed))
}

lab_anova <- function(delta = 0.5, ratio = 2, n = 30, seed = 17) {
  set.seed(seed)
  gruppo <- factor(rep(LETTERS[1:4], each = n))
  medie <- rep((0:3) * delta, each = n)
  sd_gruppi <- rep(seq(1, ratio, length.out = 4), each = n)
  y <- rnorm(4 * n, medie, sd_gruppi)
  dati <- data.frame(gruppo = gruppo, valore = y)
  classica <- anova(lm(y ~ gruppo))
  welch <- oneway.test(y ~ gruppo, var.equal = FALSE)
  valori <- .metriche_gemina(`F classica` = classica$"F value"[1],
    `p ANOVA classica` = classica$"Pr(>F)"[1],
    `F Welch` = welch$statistic, `p Welch` = welch$p.value)
  .risultato_gemina("anova", dati, valori,
    list(delta = delta, ratio = ratio, n = n, seed = seed),
    classica = classica, welch = welch)
}

lab_relazione <- function(n = 30, delta = 0.3, seed = 17) {
  set.seed(seed)
  a <- rnorm(n); b <- rnorm(n, delta)
  test <- t.test(b, a)
  dati <- data.frame(x = mean(b) - mean(a), y = 1,
                     lo = test$conf.int[1], hi = test$conf.int[2])
  valori <- .metriche_gemina(`Effetto stimato` = dati$x,
    `Ampiezza intervallo` = diff(test$conf.int), `p Welch` = test$p.value)
  .risultato_gemina("relazione", dati, valori,
    list(n = n, delta = delta, seed = seed), test = test)
}

# Grafici di controllo in R base: risultati numerici identici al sito;
# colori e geometrie sono adattati alla stampa del materiale didattico.
grafico_lab <- function(ris) {
  d <- ris$data; p <- ris$parametri; id <- ris$id
  op <- par(mar = c(4.5, 4.5, 2.5, 1))
  on.exit(par(op))
  colori <- c("#1D7890", "#C57E42", "#7363AA", "#087C74")
  if (id %in% c("contrasto", "welch", "anova")) {
    boxplot(valore ~ gruppo, data = d, col = colori,
            xlab = "Gruppo", ylab = "Risposta simulata", main = id)
    stripchart(valore ~ gruppo, data = d, vertical = TRUE,
               method = "stack", add = TRUE, pch = 16, cex = .45)
  } else if (id == "permutazione") {
    hist(d$contrasto, breaks = 20, col = colori[1], border = "white",
         main = "Etichette permutate", xlab = "Contrasto B - A")
    abline(v = c(-1, 1) * abs(ris$metrics[1]), lty = 2, col = colori[2])
  } else if (id == "pvalue") {
    plot(d$x, d$y, type = "l", lwd = 2, col = colori[1],
         xlab = "t", ylab = "Densita", main = "Riferimento t")
    abline(v = c(-1, 1) * abs(p$t), lty = 2, col = colori[2])
  } else if (id == "potenza") {
    plot(d$x, d$y, type = "l", lwd = 2, col = colori[1], ylim = c(0, 1),
         xlab = "Osservazioni per gruppo", ylab = "Probabilita di rifiuto")
    abline(v = p$n, lty = 2)
  } else if (id == "appaiati") {
    matplot(1:2, rbind(d$valore[1:30], d$valore[31:60]),
            type = "b", pch = 16, lty = 1, col = colori[1],
            xaxt = "n", xlab = "Misura", ylab = "Risposta simulata")
    axis(1, at = 1:2, labels = c("Prima", "Dopo"))
  } else if (id == "ranghi") {
    a <- d$valore[d$gruppo == "A"]; b <- d$valore[d$gruppo == "B"]
    plot(ecdf(a), col = colori[1], xlim = range(d$valore),
         xlab = "Risposta simulata", ylab = "Frazione cumulata", main = "ECDF")
    plot(ecdf(b), add = TRUE, col = colori[2])
    legend("bottomright", c("A", "B"), col = colori[1:2], lty = 1)
  } else if (id == "categorie") {
    barplot(t(ris$tabella), beside = TRUE, col = colori[1:2],
            names.arg = c("A", "B"), xlab = "Gruppo", ylab = "Conteggio")
    legend("topright", c("Esito A", "Esito B"), fill = colori[1:2])
  } else if (id == "multipli") {
    plot(d$x, d$y, ylim = c(0, 1), pch = 16, col = colori[1],
         xlab = "Test nella famiglia", ylab = "p-value")
    points(d$x, d$corretto, pch = 17, col = colori[2])
    abline(h = p$alpha, lty = 2)
  } else if (id == "relazione") {
    plot(d$x, d$y, xlim = range(c(0, d$lo, d$hi)), ylim = c(.7, 1.3),
         pch = 16, col = colori[1], yaxt = "n", ylab = "",
         xlab = "Contrasto B - A: stima e IC al 95%")
    segments(d$lo, d$y, d$hi, d$y, lwd = 2, col = colori[1])
    abline(v = 0, lty = 2)
  }
  invisible(ris)
}
