# Scrivere una descrizione che rispetti i dati
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Questo blocco prepara soltanto percorsi, funzioni di servizio e riproducibilità.
# Non scarica dati, non installa pacchetti, non elimina oggetti e non modifica i CSV.
trova_radice <- function() {
  p <- normalizePath(getwd(), winslash = "/", mustWork = TRUE)
  repeat {
    if (file.exists(file.path(p, "Notebook_R_Geologia.Rproj"))) return(p)
    genitore <- dirname(p)
    if (identical(p, genitore)) stop("Aprire Notebook_R_Geologia.Rproj e riprovare.")
    p <- genitore
  }
}
root <- trova_radice()
source(file.path(root, "R", "funzioni_comuni.R"), local = TRUE)
ctx <- inizia_notebook("M03_N10")
set.seed(1005)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Preparazione: Il campione da descrivere
f <- leggi_dati("fossili_simulati.csv")
richiedi_colonne(f, c("id", "morfotipo", "diametro_tot_um", "spessore_um"))
stopifnot(nrow(f) == 160L, anyDuplicated(f$id) == 0L)
stopifnot(all(is.finite(f$diametro_tot_um)))
str(f)
table(f$morfotipo)


# Preparazione: Frequenza assoluta, relativa e percentuale
conteggi <- table(f$morfotipo)
frequenze <- data.frame(
  morfotipo = names(conteggi),
  n = as.integer(conteggi),
  proporzione = as.numeric(prop.table(conteggi)),
  percentuale = 100 * as.numeric(prop.table(conteggi)))
frequenze
stopifnot(sum(frequenze$n) == nrow(f))
stopifnot(abs(sum(frequenze$proporzione) - 1) < 1e-12)


# Preparazione: Quando mancano le categorie
copia <- f
copia$morfotipo[1:6] <- NA_character_
table(copia$morfotipo, useNA = "ifany")
n_noti <- sum(!is.na(copia$morfotipo))
n_spiky <- sum(copia$morfotipo == "Spiky", na.rm = TRUE)
data.frame(
  denominatore = c("Tutti gli individui", "Solo morfotipo noto"),
  n_denominatore = c(nrow(copia), n_noti),
  percentuale_Spiky = 100 * n_spiky / c(nrow(copia), n_noti))


# Preparazione: Una tabella a doppia entrata
d <- leggi_dati("campioni_modulo1.csv")
tab <- table(Affioramento = d$affioramento, Alterazione = d$alterazione)
tab
percentuali_riga <- 100 * prop.table(tab, margin = 1)
percentuali_colonna <- 100 * prop.table(tab, margin = 2)
round(percentuali_riga, 1)
round(percentuali_colonna, 1)
stopifnot(all(abs(rowSums(percentuali_riga) - 100) < 1e-10))


# Preparazione: Media e mediana: due domande differenti
x_demo <- c(3, 4, 5, 100)
media_manuale <- sum(x_demo) / length(x_demo)
ordinati <- sort(x_demo)
mediana_manuale <- mean(ordinati[2:3])
c(media = media_manuale, mediana = mediana_manuale)
stopifnot(media_manuale == mean(x_demo), mediana_manuale == median(x_demo))
x <- f$diametro_tot_um
c(media_um = mean(x), mediana_um = median(x))


# Preparazione: Dispersione: la media non basta
scarti <- x - mean(x)
sum(scarti)
varianza_manual <- sum(scarti^2) / (length(x) - 1)
sd_manual <- sqrt(varianza_manual)
stopifnot(isTRUE(all.equal(varianza_manual, var(x))))
stopifnot(isTRUE(all.equal(sd_manual, sd(x))))
data.frame(n = length(x), media_um = mean(x), sd_um = sd(x),
           varianza_um2 = var(x), ampiezza_um = diff(range(x)))


# Preparazione: Quantili e intervallo interquartile
q <- quantile(x, probs = c(0, 0.25, 0.5, 0.75, 1), type = 7)
q
IQR(x, type = 7)
stopifnot(abs(IQR(x) - unname(q[4] - q[2])) < 1e-12)
# Introduciamo un estremo solo in una copia per confrontare la sensibilità.
x_estremo <- x
x_estremo[1] <- 30
confronto <- data.frame(
  versione = c("Originale simulata", "Copia con un valore a 30"),
  media = c(mean(x), mean(x_estremo)),
  mediana = c(median(x), median(x_estremo)),
  sd = c(sd(x), sd(x_estremo)),
  IQR = c(IQR(x), IQR(x_estremo)))
confronto


# Preparazione: Una tabella completa per morfotipo
descrivi <- function(v) {
  stopifnot(is.numeric(v), all(is.finite(v)))
  c(n = length(v), media = mean(v), mediana = median(v), sd = sd(v),
    Q1 = unname(quantile(v, .25)), Q3 = unname(quantile(v, .75)),
    minimo = min(v), massimo = max(v))
}
gruppi <- split(f$diametro_tot_um, f$morfotipo)
riassunto <- as.data.frame(do.call(rbind, lapply(gruppi, descrivi)))
riassunto$morfotipo <- rownames(riassunto)
rownames(riassunto) <- NULL
riassunto
stopifnot(sum(riassunto$n) == nrow(f))


# Preparazione: Media di individui o media di gruppi?
medie_gruppi <- c(A = 2.5, B = 2.8)
n_gruppi <- c(A = 10, B = 30)
media_gruppi <- mean(medie_gruppi)
media_individui <- weighted.mean(medie_gruppi, w = n_gruppi)
c(uguale_peso_gruppi = media_gruppi, peso_per_n = media_individui)
# Verifica del calcolo ponderato.
stopifnot(abs(media_individui - sum(medie_gruppi * n_gruppi) / sum(n_gruppi)) < 1e-12)


# Analisi principale: Scrivere una descrizione che rispetti i dati
salva_tabella(frequenze, "frequenze_morfotipi.csv", ctx$out)
salva_tabella(riassunto, "diametro_per_morfotipo.csv", ctx$out)
salva_tabella(confronto, "sensibilita_estremo_artificiale.csv", ctx$out)
nota <- c("160 fossili simulati: quote 80 Rounded e 80 Spiky fissate dal generatore.",
          sprintf("Diametro totale: media %.3f, mediana %.3f, SD %.3f micrometri.",
                  mean(x), median(x), sd(x)),
          "Le quote non stimano una prevalenza naturale dei morfotipi.")
salva_testo(nota, "descrizione.txt", ctx$out)
nota
