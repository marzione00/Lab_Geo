# Introduzione a R e all'analisi dei dati
# Eseguire dalla cartella che contiene Terra01.Rproj.
# I frammenti seguono l'ordine delle slide.
# I dati meteorologici in demo sono simulati.
# Per vedere anche i valori: source("Lezione_completa.R", echo = TRUE)
source("setup.R")


# =======================================================
# 03_oggetti.R
# =======================================================
# Tre concentrazioni, in mg/L
x <- c(3, 7, 10)

# Salva la media in un nuovo oggetto
media <- mean(x)
media
# [1] 6.666667


# =======================================================
# 04_unita.R
# =======================================================
# Esempio didattico: temperature
temp_c <- c(12, 14, 13)

# Conversione da Celsius a kelvin
temp_k <- temp_c + 273.15
temp_k


# =======================================================
# 06_tabella.R
# =======================================================
# Tre misure, ciascuna con il suo id
misure <- data.frame(
  id = 1:3,
  stazione = factor(c("A", "A", "B")),
  valore = c(2.9, 3.2, 7.1)
)
str(misure)  # Tipi delle colonne
head(misure) # Prime righe


# =======================================================
# 07_avvio.R
# =======================================================
# Carica i due dataset della lezione
source("setup.R")
head(terra)

# Registra l'ambiente di esecuzione
sessionInfo()


# =======================================================
# 08_riepiloghi.R
# =======================================================
# Usa la tabella della slide 6
mean(misure$valore)  # 4.4
# Una media per ciascuna stazione
tapply(misure$valore,
       misure$stazione, mean)
# A: 3.05; B: 7.10


# =======================================================
# 09_schema.R
# =======================================================
# Dataset caricato da setup.R
names(terra)
nrow(terra)  # Numero di misure
ncol(terra)  # Numero di colonne


# =======================================================
# 13_tipi.R
# =======================================================
# Le stazioni sono categorie
g <- factor(c("A", "A", "B", "C"))
levels(g)
table(g)  # Frequenze per categoria

# Le concentrazioni sono numeriche
x <- c(2.9, 3.2, 7.1, 10.0)
is.numeric(x)


# =======================================================
# 15_posizione.R
# =======================================================
x <- c(2, 3, 3, 4, 9)
mean(x)    # Media: 4.2
median(x)  # Mediana: 3
sort(x)    # Dati in ordine crescente

# Trova la frequenza maggiore
table(x)   # La moda e 3


# =======================================================
# 16_calcolo.R
# =======================================================
x <- c(10, 3, 2, 5)
sum(x) / length(x)  # 20 / 4 = 5
mean(x)            # Stesso risultato

sort(x)            # 2, 3, 5, 10
median(x)          # (3 + 5) / 2 = 4


# =======================================================
# 18_conteggi.R
# =======================================================
# Dati dell'anteprima, dal file CSV
table(terra$stazione)
#  A  B  C
# 20 10 10

nlevels(terra$stazione) # 3 stazioni
nrow(terra)            # 40 misure


# =======================================================
# 21_attese.R
# =======================================================
# Medie teoriche A=3, B=7, C=10
n_A <- c(10, 20, 50, 100)
attesa_m <- (3*n_A + 170)/(n_A + 20)
attesa_s <- rep(20/3, length(n_A))

data.frame(n_A, attesa_m, attesa_s)
# Misure: 6.67, 5.75, 4.57, 3.92
# Stazioni: sempre 6.67 (circa)


# =======================================================
# 22_simulazione.R
# =======================================================
# Stessa sequenza con lo stesso seme
set.seed(17)
campione_A <- rnorm(20,
                    mean = 3,
                    sd = 0.4)
mean(campione_A)
sd(campione_A)


# =======================================================
# 23_costruzione.R
# =======================================================
n_A <- 20
set.seed(17)  # Seme iniziale del laboratorio
terra_sim <- data.frame(
  stazione = rep(c("A", "B", "C"),
                 c(n_A, 10, 10)),
  valore = c(rnorm(n_A, 3, 0.4),
             rnorm(10, 7, 0.4),
             rnorm(10, 10, 0.4))
)
table(terra_sim$stazione)


# =======================================================
# 24_medie.R
# =======================================================
# Medie e numerosita per stazione
m <- tapply(terra_sim$valore,
            terra_sim$stazione, mean)
n <- table(terra_sim$stazione)
n <- n[names(m)]  # Stesso ordine dei gruppi

mean(terra_sim$valore)  # Circa 5.75 mg/L
mean(m)                # Circa 6.61 mg/L
weighted.mean(m, n)     # Controllo: circa 5.75


# =======================================================
# 25_boxplot.R
# =======================================================
# Usa l'anteprima archiviata in terra
boxplot(valore ~ stazione, data = terra,
        ylab = "Concentrazione [mg/L]")
# Le medie non sono la linea nel box
tapply(terra$valore,
       terra$stazione, mean)


# =======================================================
# 29_campionamento.R
# =======================================================
# Sei siti in ciascuna fascia
set.seed(17)
bassa <- sample(1:6, 2)
media <- sample(7:12, 2)
alta <- sample(13:18, 2)
# Indici dei sei siti selezionati
c(bassa, media, alta)


# =======================================================
# 30_controlli.R
# =======================================================
d <- data.frame(
  stazione = c("A", "A", "B", "B"),
  valore = c(3.1, NA, 7, 7))
# Numero di valori mancanti
sum(is.na(d$valore))
# Righe uguali a una precedente
duplicated(d)
range(d$valore, na.rm = TRUE)


# =======================================================
# 31_integrazione.R
# =======================================================
misure <- data.frame(
  id = c("A", "B"), x = c(3.1, 7))
meta <- data.frame(
  id = c("A", "B"), quota = c(120, 280))
# Una sola riga per chiave in meta
stopifnot(!anyDuplicated(meta$id))
uniti <- merge(misure, meta,
  by = "id", all.x = TRUE)


# =======================================================
# 32_distribuzione.R
# =======================================================
# Esempio didattico, valori in mm
x <- c(0, 0, 0, 1, 2, 8, 24)
mean(x)
median(x)
# Frequenza relativa dei giorni secchi
mean(x == 0)
quantile(x, c(0.25, 0.75))


# =======================================================
# 34_previsione.R
# =======================================================
# Tre valori esclusi dal modello
osservati <- c(10, 12, 15)
previsti <- c(9, 13, 14)
errori <- osservati - previsti
# Unita uguale a quella dei dati
sqrt(mean(errori^2))


# =======================================================
# 35_gruppi.R
# =======================================================
# Sei campioni, due proprieta
x <- rbind(c(1, 2), c(2, 1),
  c(2, 2), c(8, 9), c(9, 8), c(9, 9))
z <- scale(x)
set.seed(17)
gruppi <- kmeans(z,
  centers = 2, nstart = 20)
gruppi$cluster


# =======================================================
# 36_dipendenza.R
# =======================================================
# Serie didattica a intervalli uguali
x <- c(1, 2, 3, 4, 4, 3,
       2, 1, 1, 2, 3, 4)
# Correlazione per ritardi crescenti
acf(x, lag.max = 5,
    main = "Serie didattica")


# =======================================================
# 37_segnale.R
# =======================================================
set.seed(17)
t <- 1:30
segnale <- 2 + 0.1 * t
# Scarti indipendenti simulati
x <- segnale + rnorm(30, sd = 0.6)
plot(t, x, xlab = "Tempo",
     ylab = "Valore simulato")
lines(t, segnale, col = "purple")


# =======================================================
# 38_calibrazione.R
# =======================================================
# Letture didattiche in gradi C
letture <- c(20.2, 20.3, 20.4)
riferimento <- 20
scarto <- mean(letture) - riferimento
sd(letture)  # Dispersione ripetizioni
# Correzione dello scarto accertato
corrette <- letture - scarto
mean(corrette)


# =======================================================
# 41_sensibilita.R
# =======================================================
x <- c(3, 4, 5, 6, 7, 8, 16)
confronto <- c(
  media = mean(x),
  mediana = median(x),
  senza_massimo = mean(x[x < 16]))
# Ultima riga: scenario di sensibilita
confronto


# =======================================================
# 42_residui.R
# =======================================================
# Dati didattici con curvatura
x <- 1:8
y <- c(1, 4, 8, 16, 24, 36, 49, 65)
fit <- lm(y ~ x)
plot(fitted(fit), resid(fit),
  xlab = "Stimati", ylab = "Residui")
abline(h = 0, lty = 2)


# =======================================================
# 43_intervalli.R
# =======================================================
x <- c(3.1, 3.4, 2.8, 3, 3.2)
n <- length(x)
errore_std <- sd(x) / sqrt(n)
q <- qt(0.975, df = n - 1)
# Estremi inferiore e superiore
mean(x) + c(-1, 1) * q * errore_std


# =======================================================
# 45_media_cumulativa.R
# =======================================================
set.seed(17)
x <- rexp(1000, rate = 1)
# Medie delle prime 1, 2, ..., 1000 misure
m <- cumsum(x) / seq_along(x)


# =======================================================
# 47_medie_replicate.R
# =======================================================
set.seed(17)
n <- 30  # Valori in ogni campione
medie <- replicate(3000, mean(rexp(n)))
z <- sqrt(n) * (medie - 1)


# =======================================================
# 49_livello_relativo.R
# =======================================================
# Variazioni simulate in mm
tempo <- 0:2
mare <- c(0, 3, 6)
suolo <- c(0, -1, -2)
relativo <- mare - suolo
data.frame(tempo, mare,
           suolo, relativo)


# =======================================================
# 50_piano_permafrost.R
# =======================================================
# Piano didattico, senza misure reali
piano <- data.frame(
  sito = rep(1:8, each = 5),
  anno = rep(2020:2024, times = 8))
# Numero di righe per sito e anno
with(piano, table(sito, anno))


# =======================================================
# 52_posizione.R
# =======================================================
x <- c(3, 4, 5, 100)
mean(x)    # 28
median(x)  # 4.5
# Frequenza di ciascun valore
table(x)


# =======================================================
# 53_moda.R
# =======================================================
sed <- c("sabbia", "ghiaia",
         "sabbia", "fango")
freq <- table(sed)
# Categorie con frequenza massima
moda <- names(freq[freq==max(freq)])
moda


# =======================================================
# 54_dispersione.R
# =======================================================
# Esempio in mg/L: cinque misure.
x <- c(1, 2, 2, 3, 7)
diff(range(x))   # ampiezza: 6
sd(x)           # circa 2.35 mg/L
quantile(x)     # quartili e estremi
IQR(x)          # Q3 - Q1: 1 mg/L


# =======================================================
# 55_posizione_dispersione.R
# =======================================================
# Traslare conserva la dispersione.
a <- 1:5
b <- a + 5
centrati <- a - mean(a)
dilatati <- 2 * centrati + mean(a)
gruppi <- list(A=a, B=b, C=dilatati)
sapply(gruppi, mean) # posizione
sapply(gruppi, sd)   # dispersione


# =======================================================
# 56_media_mediana_mese.R
# =======================================================
# demo contiene dati simulati.
mese <- format(demo$data, "%m")
p <- demo$pioggia
tapply(p, mese, mean)   # medie
tapply(p, mese, median) # mediane
mean(p == 0)          # quota asciutti


# =======================================================
# 57_correlazione.R
# =======================================================
# Coppie con entrambi i valori.
z <- demo[c("tmin", "tmax")]
ok <- complete.cases(z)
sum(ok)                # n coppie
cor(z$tmin[ok], z$tmax[ok])
plot(z$tmin, z$tmax,
     xlab = "Tmin [C]",
     ylab = "Tmax [C]")


# =======================================================
# 59_relazione_curva.R
# =======================================================
# Una relazione esatta, ma curva.
x <- -3:3
y <- x^2
cor(x, y)              # zero
plot(x, y, pch = 19)
# Rimuovere un punto cambia r:
cor(x[-1], y[-1])


# =======================================================
# 60_regressione.R
# =======================================================
# Esempio didattico simulato.
mod <- lm(tmax ~ tmin, data = demo)
coef(mod)              # coefficienti
residui <- residuals(mod)
plot(demo$tmin, demo$tmax,
     xlab = "Tmin [C]",
     ylab = "Tmax [C]")
abline(mod, col = "steelblue")


# =======================================================
# 61_residui.R
# =======================================================
# Diagnosi del modello simulato.
mod <- lm(tmax ~ tmin, data = demo)
e <- residuals(mod)
plot(fitted(mod), e,
     xlab = "Valori stimati",
     ylab = "Residui [C]")
abline(h = 0, col = "grey50")
acf(e, main = "Residui nel tempo")


# =======================================================
# 62_intervalli_retta.R
# =======================================================
# Intervalli: esempio su demo.
mod <- lm(tmax ~ tmin, data = demo)
nuovo <- data.frame(tmin = 10)
predict(mod, nuovo,
        interval = "confidence")
predict(mod, nuovo,
        interval = "prediction")


# =======================================================
# 63_importazione.R
# =======================================================
# File didattico fornito nel progetto.
demo <- read.csv(
  "Dati/meteo_simulati.csv",
  na.strings = c("", "NA"))
demo$data <- as.Date(demo$data)
str(demo)               # tipi
stopifnot(!anyNA(demo$data))
range(demo$data)        # periodo


# =======================================================
# 64_chiavi_ordine.R
# =======================================================
# demo contiene una stazione fittizia.
anyDuplicated(demo$data) # atteso: 0
stopifnot(
  anyDuplicated(demo$data) == 0)
demo <- demo[order(demo$data), ]
head(demo[c("data", "tmax")])
dim(demo)             # righe, colonne


# =======================================================
# 65_mancanti.R
# =======================================================
# Esempio con mancante ed estremo.
x <- c(1.2, NA, 1.4, 12)
is.na(x)               # individua NA
sum(!is.na(x))         # disponibili
mean(x)                # risultato: NA
mean(x, na.rm = TRUE)  # usa 3 valori
x[which(x > 10)]       # da verificare


# =======================================================
# 66_unita.R
# =======================================================
# Conserva anche le colonne originali.
demo$pioggia_m <- demo$pioggia / 1000
demo$sole_ore <- demo$sole / 60
stopifnot(all(demo$pioggia >= 0))
stopifnot(all(demo$nubi >= 0),
          all(demo$nubi <= 100))
# In demo la nuvolosita e in %.


# =======================================================
# 67_grafici.R
# =======================================================
# Terra01: stessi dati, due domande.
hist(terra$valore,
     xlab = "Concentrazione [mg/L]",
     main = "Tutte le misure")
boxplot(valore ~ stazione,
        data = terra,
        ylab="Concentrazione [mg/L]")


# =======================================================
# 68_trasformazioni.R
# =======================================================
# x0 = 1 mm: rapporto senza unita.
x0 <- 1
demo$log_pioggia <-
  log1p(demo$pioggia / x0)
s <- sd(demo$tmax)
stopifnot(s > 0)
demo$z_tmax <-
  (demo$tmax - mean(demo$tmax)) / s


# =======================================================
# 71_componenti.R
# =======================================================
# Medie mensili dei dati simulati.
mese <- format(demo$data, "%Y-%m")
mensile <- tapply(demo$tmax,
                  mese, mean)
serie <- ts(mensile,
            start = c(2022, 1),
            frequency = 12)
scomp <- stl(serie,
             s.window = "periodic")
plot(scomp)


# =======================================================
# 72_riferimento.R
# =======================================================
# Riferimento didattico: 2022-2023.
mese <- format(demo$data, "%m")
inizio <- as.Date("2024-01-01")
base <- demo$data < inizio
rif <- tapply(demo$tmax[base],
              mese[base], mean)
scarti <- demo$tmax - rif[mese]
# Ciascun giorno usa il proprio mese.
head(scarti)


# =======================================================
# 73_boxplot_mese.R
# =======================================================
# Distribuzioni mensili simulate.
mese <- factor(
  format(demo$data, "%m"),
  levels = sprintf("%02d", 1:12))
boxplot(demo$pioggia ~ mese,
        xlab = "Mese",
        ylab = "Pioggia [mm/giorno]")
table(mese)            # numerosita


# =======================================================
# 74_totali_annui.R
# =======================================================
# Totali e copertura per anno.
anno <- format(demo$data, "%Y")
giorni <- table(anno)
totali <- tapply(demo$pioggia,
                 anno, sum)
cbind(giorni = giorni, mm = totali)


# =======================================================
# 75_griglia_temporale.R
# =======================================================
# Una misura al giorno, senza salti.
date <- demo$data
passi <- as.integer(diff(date))
table(passi)
attese <- seq(min(date), max(date),
              by = "day")
setdiff(attese, date) # giorni assenti
stopifnot(all(passi == 1))


# =======================================================
# 76_medie_mobili.R
# =======================================================
# Dati giornalieri completi, ordinati.
x <- demo$tmax
media31 <- as.numeric(
  stats::filter(x, rep(1/31, 31),
                sides = 2))
mediana31 <- runmed(x, k = 31,
                  endrule="constant")
mediana31[c(1:15,
  (length(x)-14):length(x))] <- NA


# =======================================================
# 77_loess_locale.R
# =======================================================
# Giorni consecutivi, dati simulati.
demo$giorno <- seq_len(nrow(demo))
locale <- loess(tmax ~ giorno,
                data = demo,
                span=0.2, degree=1)
curva <- predict(locale)
plot(demo$data, curva, type = "l",
     xlab = "Data", ylab = "Tmax [C]")


# =======================================================
# 78_confrontare_span.R
# =======================================================
# Stessi dati e grado, due intorni.
demo$giorno <- seq_len(nrow(demo))
f1 <- loess(tmax ~ giorno, demo,
            span = .1, degree = 1)
f3 <- loess(tmax ~ giorno, demo,
            span = .3, degree = 1)
curve <- cbind(predict(f1),
               predict(f3))
matplot(curve, type = "l", lty = 1,
  xlab = "Giorno", ylab = "Tmax [C]")


# =======================================================
# 79_documentare_curva.R
# =======================================================
# Mostrare insieme dati e sintesi.
media31 <- stats::filter(demo$tmax,
  rep(1/31, 31), sides = 2)
plot(demo$data, demo$tmax, type = "l",
     col = "grey75", xlab = "Data",
     ylab = "Tmax [C]")
lines(demo$data, as.numeric(media31),
      col = "steelblue", lwd = 2)
etichette <- c("Dati", "Media 31 g")
legend("topleft", etichette,
       col = c("grey75", "steelblue"),
       lty = 1, bty = "n")


# =======================================================
# 80_scale_smussamento.R
# =======================================================
# Confronto dei numeri di punti.
n <- nrow(demo)
finestra <- 31
span <- 0.2
c(media_mobile = finestra,
  loess_circa = span * n)
# In demo: 31 contro circa 219 punti.


# =======================================================
# 81_scarti_mensili.R
# =======================================================
# Riferimento: tutti i 3 anni fittizi.
mese <- format(demo$data, "%m")
media_mese <- tapply(demo$tmax,
                     mese, mean)
anomalia <- demo$tmax -
  media_mese[mese]
plot(demo$data, anomalia, type = "l",
     xlab="Data", ylab="Scarto [C]")
abline(h = 0, col = "grey50")


# =======================================================
# 82_salto_strumento.R
# =======================================================
# Aggiunge un salto fittizio di 2 C.
cambio <- as.Date("2023-07-01")
con_salto <- demo$tmax +
  2 * (demo$data >= cambio)
plot(demo$data, con_salto, type = "l",
     xlab = "Data", ylab = "Tmax [C]")
abline(v = as.numeric(cambio),
       col = "firebrick", lty = 2)


# =======================================================
# 83_validazione_tempo.R
# =======================================================
# Separazione su dati simulati.
taglio <- as.Date("2024-01-01")
prima <- demo$data < taglio
addestramento <- demo[prima, ]
valutazione <- demo[!prima, ]
range(addestramento$data)
range(valutazione$data)
# Stima prima, verifica dopo.


# =======================================================
# 84_salvare_risultato.R
# =======================================================
# Sintesi per stazione di Terra01.
risultato <- aggregate(
  valore ~ stazione, terra, mean)
dir.create("Risultati",
           showWarnings = FALSE)
write.csv(risultato,
  "Risultati/medie_stazioni.csv",
  row.names = FALSE)
sessionInfo()          # versioni di R


# =======================================================
# 85_materiali.R
# =======================================================
source("setup.R")  # Carica i dati
# Guide delle funzioni
?tapply
?lm
?loess
