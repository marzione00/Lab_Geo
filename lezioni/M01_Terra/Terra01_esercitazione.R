# Terra 01: definire la quantità di interesse
# Materiale di accompagnamento alla presentazione.
# Fonte del modello: https://marzione00.github.io/Lab_Geo/#laboratorio/m01-estimando
# Codice del laboratorio:
# https://github.com/marzione00/Lab_Geo/blob/main/R/experiments/m01-estimando.R
#
# Richiede soltanto R. Non occorre installare pacchetti.
# In RStudio si possono eseguire poche righe alla volta con Ctrl+Invio.
# Le concentrazioni sono dati simulati, espressi in mg/L.


# 1. Generazione dei dati ---------------------------------------------------

# Modificare n_A ed eseguire di nuovo l'intero blocco.
# B e C hanno sempre 10 misure ciascuna.
n_A <- 20L
seed <- 17L

set.seed(seed)
dati <- data.frame(
  stazione = rep(c("A", "B", "C"), c(n_A, 10, 10)),
  valore = c(
    rnorm(n_A, mean = 3, sd = 0.4),
    rnorm(10, mean = 7, sd = 0.4),
    rnorm(10, mean = 10, sd = 0.4)
  )
)

# Ogni riga contiene una misura e il nome della sua stazione.
# rnorm(n, mean, sd) genera n valori da una distribuzione normale.
# Il modello assegna alle stazioni medie 3, 7 e 10 mg/L.
# La deviazione standard all'interno di ciascuna stazione è 0.4 mg/L.
head(dati)
str(dati)


# 2. Conteggi e medie per stazione -----------------------------------------

n <- table(dati$stazione)
medie <- tapply(dati$valore, dati$stazione, mean)

print(n)
print(medie)

# $ seleziona una colonna.
# tapply() suddivide i valori secondo stazione e applica mean() a ogni gruppo.
riepilogo <- data.frame(
  stazione = names(n),
  n_misure = as.integer(n),
  media_mg_L = as.numeric(medie[names(n)])
)
print(riepilogo, row.names = FALSE)


# 3. Le due sintesi --------------------------------------------------------

# Ogni riga ha lo stesso peso.
media_misure <- mean(dati$valore)

# Prima si calcola la media in ogni stazione.
# Poi si attribuisce a ciascuna delle tre stazioni lo stesso peso.
media_stazioni <- mean(medie)

risultati <- data.frame(
  indicatore = c("Media delle misure", "Media delle stazioni"),
  valore_mg_L = c(media_misure, media_stazioni)
)
print(risultati, row.names = FALSE)

# La media di tutte le righe equivale alla media delle medie di stazione
# ponderata con il numero delle rispettive misure.
# L'indicizzazione per nome allinea ogni media al conteggio corrispondente.
media_ponderata <- weighted.mean(medie, w = n[names(medie)])
print(media_ponderata)
print(all.equal(media_misure, unname(media_ponderata)))


# 4. Distribuzioni e medie -------------------------------------------------

# Il segmento interno a ciascuna scatola indica la mediana.
# I rombi aggiunti con points() indicano le medie di stazione.
# Il numero di misure compare sotto il nome della stazione.
# La larghezza delle scatole è fissa e non rappresenta il conteggio.
# Il grafico appare solo in una sessione interattiva. Da terminale questo
# blocco non crea automaticamente un file Rplots.pdf.
if (interactive()) {
  boxplot(
    valore ~ stazione,
    data = dati,
    names = paste0(names(n), "\nn = ", as.integer(n)),
    col = c("#C4E0DB", "#D8D2ED", "#D7DDE5"),
    border = "#253344",
    xlab = "Stazione",
    ylab = "Concentrazione [mg/L]",
    main = paste("Terra 01: misure nella stazione A =", n_A)
  )
  points(seq_along(medie), medie, pch = 18, col = "#15283E", cex = 1.5)
  legend(
    "topleft",
    legend = "Media della stazione",
    pch = 18,
    col = "#15283E",
    bty = "n"
  )
}


# 5. Confronto da svolgere -------------------------------------------------

# Eseguire i blocchi 1-4 con n_A pari a 10, 20, 50 e 100.
# Mantenere seed = 17 durante questo confronto.
# Per ogni scenario annotare i conteggi e le due medie.
#
# Domande:
# - Per n_A = 10, perché le due medie coincidono?
# - Quale peso riceve A nella media di tutte le misure per n_A = 100?
# - Perché la media delle misure si avvicina ai valori della stazione A?
# - Quale sintesi risponde alla domanda sulla media delle tre stazioni,
#   quando ciascuna stazione deve avere lo stesso peso?
#
# A parità di codice, parametri e generatore, set.seed() riproduce i dati.
# Cambiare n_A cambia anche il punto della sequenza casuale dal quale
# iniziano le estrazioni di B e C. Perciò, con lo stesso seed, le medie
# osservate di B e C possono cambiare fra gli scenari.
# Il valore atteso della media delle stazioni rimane costante.
# La sua realizzazione numerica può variare.
#
# Per osservare la variabilità casuale, mantenere n_A = 20 e provare un
# altro seed. Tornare al seed 17 per riprodurre lo scenario iniziale.


# 6. Valori attesi del modello --------------------------------------------

# Questa tabella usa le medie delle popolazioni simulate.
# Non contiene le medie ricavate dal campione appena generato.
mu <- c(A = 3, B = 7, C = 10)
n_A_scenari <- c(10L, 20L, 50L, 100L)

teoria <- data.frame(
  n_A = n_A_scenari,
  n_B = 10L,
  n_C = 10L,
  peso_A_nella_media_misure = n_A_scenari / (n_A_scenari + 20),
  attesa_media_misure_mg_L =
    (n_A_scenari * mu["A"] + 10 * mu["B"] + 10 * mu["C"]) /
    (n_A_scenari + 20),
  attesa_media_stazioni_mg_L = mean(mu)
)
print(round(teoria, 4), row.names = FALSE)

# Per n_A = 20 i valori attesi sono 5.75 e 6.6667 mg/L.
# I risultati del singolo campione possono essere diversi.
# Con dieci misure in ciascuna stazione le due medie campionarie
# coincidono per qualunque campione, salvo arrotondamenti numerici.
# I pesi uguali tra stazioni non implicano pesi uguali per superficie,
# volume o popolazione. Un diverso obiettivo può richiedere altri pesi.


# 7. Raccolta automatica degli scenari -------------------------------------

# Questa funzione ripete la procedura già svolta nei blocchi 1-3.
# Tutti gli scenari ripartono dallo stesso seed.
simula_scenario <- function(n_A, seed = 17L) {
  set.seed(seed)
  d <- data.frame(
    stazione = rep(c("A", "B", "C"), c(n_A, 10, 10)),
    valore = c(
      rnorm(n_A, mean = 3, sd = 0.4),
      rnorm(10, mean = 7, sd = 0.4),
      rnorm(10, mean = 10, sd = 0.4)
    )
  )
  m <- tapply(d$valore, d$stazione, mean)
  data.frame(
    n_A = n_A,
    seed = seed,
    media_A_mg_L = unname(m["A"]),
    media_B_mg_L = unname(m["B"]),
    media_C_mg_L = unname(m["C"]),
    media_misure_mg_L = mean(d$valore),
    media_stazioni_mg_L = mean(m)
  )
}

scenari <- do.call(rbind, lapply(n_A_scenari, simula_scenario, seed = seed))
print(round(scenari, 4), row.names = FALSE)

# Esportazioni facoltative: togliere # solo se si desidera creare i file.
# write.csv(dati, "Terra01_dati.csv", row.names = FALSE)
# write.csv(scenari, "Terra01_scenari.csv", row.names = FALSE)
# write.csv(teoria, "Terra01_valori_attesi.csv", row.names = FALSE)
