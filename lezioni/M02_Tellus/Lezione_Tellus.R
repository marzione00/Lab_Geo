# Tellus - R e gestione dei dati
# Eseguire dalla cartella di Tellus_M02.Rproj.
# Per mostrare il codice: source("Lezione_Tellus.R", echo = TRUE)
source("setup.R", encoding = "UTF-8")


# ======================================================
# 04_progetto.R
# ======================================================
# Aprire prima Tellus_M02.Rproj.
getwd()  # Cartella del progetto
source("setup.R")

# Oggetti preparati dai CSV locali
dim(campioni)
names(campioni)
head(campioni, 3)


# ======================================================
# 05_stato.R
# ======================================================
# Una dipendenza da ricalcolare
x <- 1:3
a <- 2
z <- a * x
a <- 3
z                 # Ancora 2, 4, 6
z <- a * x        # Ricalcolo
z                 # Ora 3, 6, 9


# ======================================================
# 06_procedura.R
# ======================================================
# Ingressi e parametri dichiarati
x <- 1:10
a <- 1.5
b <- -1
# Trasformazione e sintesi
z <- a * x + b
mean(z)           # 7.25


# ======================================================
# 07_percorsi.R
# ======================================================
# Percorso relativo alla radice
f <- file.path("Dati",
               "campioni_modulo1.csv")
stopifnot(file.exists(f))

# Controlli dopo la lettura
campioni <- read.csv(f)
stopifnot(nrow(campioni) == 24L)
str(campioni)


# ======================================================
# 09_tipi.R
# ======================================================
# Stesso aspetto, tipi differenti
numeri <- c(4, 5, 6)
testo <- c(4, "5", "ND")
typeof(numeri)    # double
typeof(testo)     # character
is.numeric(testo)


# ======================================================
# 10_posizioni.R
# ======================================================
# Indici di un vettore
x <- c(10, 20, 30, 40)
x[c(1, 3)]       # Posizioni 1 e 3
x[-2]            # Esclude la seconda

# La tabella conserva righe e colonne
campioni[1:3, c("id", "massa_g")]
campioni["massa_g"]  # Una tabella
campioni$massa_g     # Un vettore


# ======================================================
# 11_selezione.R
# ======================================================
# Un criterio per ogni riga
sel <- campioni$affioramento == "A"
s <- campioni[sel, ]
nrow(s)

# Ordiniamo tutta la tabella
o <- order(s$volume_cm3)
s <- s[o, ]
head(s[c("id", "volume_cm3")])


# ======================================================
# 12_logica.R
# ======================================================
# Intersezione di due condizioni
in_A <- campioni$affioramento == "A"
volume_ok <- campioni$volume_cm3 >= 40
sel <- in_A & volume_ok
sum(sel)           # Righe incluse
# Appartenenza a un insieme di nomi
liv <- c("bassa", "media")
table(campioni$alterazione %in% liv)


# ======================================================
# 13_na_logici.R
# ======================================================
# Un confronto puo' essere ignoto
x <- c(2, NA, 5)
x >= 3             # FALSE NA TRUE

# Qui escludiamo il valore assente
ok <- !is.na(x) & x >= 3
stopifnot(!anyNA(ok))
x[ok]              # 5


# ======================================================
# 14_categorie_date.R
# ======================================================
# Ordine della scala di alterazione
livelli <- c("bassa", "media", "alta")
grado <- factor(campioni$alterazione,
  levels = livelli, ordered = TRUE)
table(grado)

# Date di un esempio separato
giorni <- as.Date(c("2024-02-28",
                    "2024-03-01"))
diff(giorni)        # Due giorni


# ======================================================
# 15_lab_selezioni.R
# ======================================================
# La griglia del laboratorio
x <- seq(0, 10, by = 0.5)
lo <- 3; hi <- 8
a <- min(lo, hi); b <- max(lo, hi)
incluso <- x >= a & x <= b
c(inclusi = sum(incluso),
  esclusi = sum(!incluso))
x[incluso]         # Estremi inclusi


# ======================================================
# 16_file_testuale.R
# ======================================================
# Prima di interpretare le colonne
f <- file.path("Dati",
 "fossili_da_controllare.csv")
readLines(f, n = 4)


# ======================================================
# 17_separatori.R
# ======================================================
# Un piccolo file scritto nel codice
csv <- "id;valore\nA;1,25\nB;2,50"
d <- read.csv(text = csv,
              sep = ";", dec = ",")
str(d)
mean(d$valore)       # 1.875


# ======================================================
# 18_importazione.R
# ======================================================
# Conserviamo tutte le scritture
fossili_raw <- read.csv(
 "Dati/fossili_da_controllare.csv",
 sep = ";", colClasses = "character",
 na.strings = character())
fossili_raw$riga_origine <-
 seq_len(nrow(fossili_raw))
head(fossili_raw, 3)


# ======================================================
# 19_numeri.R
# ======================================================
# Esempio ridotto con tre scritture
originale <- c("6,40", " 5.40 ", "ND")
t <- trimws(originale)
assente <- t %in% c("", "ND", "NA")
t[assente] <- NA_character_
t <- sub(",", ".", t, fixed = TRUE)
valore <- as.numeric(t)
data.frame(originale, valore)


# ======================================================
# 20_mancanti_dichiarati.R
# ======================================================
# Riconoscere il codice nella colonna
raw <- fossili_raw$diametro_tot_um
t <- trimws(raw)
assente <- t %in% c("", "NA", "ND")
sum(assente)      # Un esterno assente
fossili_raw$id[assente]

# Lo zero e' un valore numerico
is.na(0)           # FALSE


# ======================================================
# 21_esiti_conversione.R
# ======================================================
# Aggiungiamo un errore intenzionale
testi <- c("6,4", "errore",
           "ND", "Inf")
z <- converti_misura(testi)
data.frame(testo = testi,
           valore = z$valore,
           stato = z$stato)


# ======================================================
# 22_limiti.R
# ======================================================
# Un'informazione espressa come limite
t <- c("<0,05", "0,12", "ND")
z <- converti_misura(t)
data.frame(testo = t,
           valore = z$valore,
           limite = z$limite,
           stato = z$stato)


# ======================================================
# 23_dizionario.R
# ======================================================
# Controlliamo i nomi attesi
richieste <- c("id", "morfotipo",
 "diametro_tot_um", "diametro_int_um",
 "diaframma_um", "riga_origine")
stopifnot(all(richieste %in%
              names(fossili_raw)))
vapply(fossili_raw, is.character,
       logical(1))


# ======================================================
# 24_riepilogo_conversioni.R
# ======================================================
# Esiti della preparazione documentata
v <- "diametro_tot_um_stato"
table(fossili[[v]], useNA = "ifany")
bad <- fossili$conversione_fallita
sum(bad)            # Zero nel CSV

# Nessuna riga eliminata dal setup
stopifnot(nrow(fossili) ==
          nrow(fossili_raw))


# ======================================================
# 25_lab_importazione.R
# ======================================================
# Cinque stringhe del laboratorio
testi <- c("1,2", "2,4", "3,1",
           "4,8", "ND")
z <- converti_misura(testi)
sum(!is.na(z$valore)) # Quattro numeri
mean(z$valore, na.rm = TRUE)
# 2.875: media delle quattro misure


# ======================================================
# 26_densita.R
# ======================================================
# Una nuova grandezza per ogni provino
stopifnot(all(campioni$volume_cm3>0))
campioni$densita <-
 campioni$massa_g/campioni$volume_cm3
head(campioni[c("id", "densita")], 4)
# Unita' del rapporto: g/cm^3


# ======================================================
# 27_riciclo.R
# ======================================================
# Esempio con due volumi mancanti
massa <- c(10, 20, 30, 40)
volume <- c(2, 5)
massa / volume      # 5, 4, 15, 8
length(massa) == length(volume)
# FALSE: mancano due volumi associati

# Nei provini le lunghezze coincidono
stopifnot(length(campioni$massa_g) ==
          length(campioni$volume_cm3))


# ======================================================
# 28_aggregare.R
# ======================================================
# Una riga per stazione
medie <- aggregate(densita ~ stazione,
                   data = campioni,
                   FUN = mean)
medie
nrow(medie)         # Sei stazioni


# ======================================================
# 29_denominatore.R
# ======================================================
# Contare dati raccolti e usati
x <- c(2, NA, 4)
ok <- is.finite(x)
c(totali = length(x),
  disponibili = sum(ok),
  media = mean(x[ok]))
# Tre righe, due valori: media 3


# ======================================================
# 30_pesi.R
# ======================================================
# Medie e conteggi allineati per nome
m <- tapply(campioni$densita,
            campioni$stazione, mean)
n <- table(campioni$stazione)
weighted.mean(m, n[names(m)])
mean(campioni$densita)
mean(m)  # Quattro misure per stazione


# ======================================================
# 31_formato_lungo.R
# ======================================================
# Due misure per ciascun provino
v <- c("massa_g", "volume_cm3")
lunga <- reshape(campioni[c("id", v)],
 varying = v, v.names = "valore",
 times = v, timevar = "variabile",
 idvar = "id", direction = "long")
rownames(lunga) <- NULL
head(lunga, 3)


# ======================================================
# 32_verificare_formato.R
# ======================================================
# Unita' esplicite nel formato lungo
lunga$unita <- ifelse(
 lunga$variabile == "massa_g",
 "g", "cm3")
stopifnot(nrow(lunga) ==
          2L * nrow(campioni))
k <- lunga[c("id", "variabile")]
stopifnot(!anyDuplicated(k))
table(lunga$variabile, lunga$unita)


# ======================================================
# 33_lab_aggregazioni.R
# ======================================================
# Versione locale del modello del sito
source("Tellus_laboratori.R")
ris <- lab_aggregazioni(nA = 50,
                        seed = 17)
ris$indicatori    # Medie campionarie
ris$attese        # Valori del modello


# ======================================================
# 34_tabelle.R
# ======================================================
# Tre provini, due siti
provini <- data.frame(
  id = c("p1", "p2", "p3"),
  sito = c("A", "A", "B"))
siti <- data.frame(
  sito = c("A", "B"),
  quota = c(10, 20))


# ======================================================
# 35_chiave.R
# ======================================================
# Chiave della tabella dei siti
chiave <- siti$sito
stopifnot(!anyNA(chiave))
stopifnot(all(nzchar(trimws(chiave))))
stopifnot(!anyDuplicated(chiave))
# La ripetizione e' attesa nei provini
table(provini$sito)


# ======================================================
# 37_join.R
# ======================================================
# Tabelle costruite nella slide 34
uniti <- merge(provini, siti,
  by = "sito", all.x = TRUE)
# Ogni provino deve restare presente
stopifnot(nrow(uniti) ==
          nrow(provini))
uniti


# ======================================================
# 38_molteplicita.R
# ======================================================
# Una seconda riga per il sito A
siti2 <- rbind(siti, siti[1, ])
siti2$quota[3] <- 12
j2 <- merge(provini, siti2,
            by = "sito")
nrow(j2)       # 5 righe
table(j2$sito) # A: 4; B: 1


# ======================================================
# 39_non_abbinati.R
# ======================================================
# Anagrafica incompleta di esempio
siti3 <- siti[siti$sito == "A", ]
setdiff(provini$sito, siti3$sito)
# Il provino B resta nel risultato
j3 <- merge(provini, siti3,
  by = "sito", all.x = TRUE)
j3


# ======================================================
# 40_duplicati.R
# ======================================================
cc <- setdiff(names(fossili_raw),
              "riga_origine")
esatti <- duplicated(fossili_raw[cc])
ids <- fossili_raw$id # Chiave
ripetuti <- duplicated(ids) |
  duplicated(ids, fromLast = TRUE)
c(esatti = sum(esatti),
  righe_id = sum(ripetuti))


# ======================================================
# 41_ordine.R
# ======================================================
p_ord <- provini[c(3, 1, 2), ]
p_ord$ordine <- seq_len(nrow(p_ord))
j_ord <- merge(p_ord, siti,
  by = "sito", all.x = TRUE,
  sort = FALSE)
j_ord <- j_ord[order(j_ord$ordine), ]
stopifnot(identical(j_ord$id,
                    p_ord$id))


# ======================================================
# 42_pesi_join.R
# ======================================================
# Misure dell'esperimento sul sito
valori_join <- c(2, 5, 9)
mean(valori_join) # 16/3
# La misura B compare due volte
mean(valori_join[c(1, 2, 2, 3)])
# Risultato: 21/4 = 5.25


# ======================================================
# 43_disponibilita.R
# ======================================================
due <- c("diametro_tot_um",
         "diametro_int_um")
tre <- c(due, "diaframma_um")
c(due_misure = sum(complete.cases(
    fossili[due])),
  tre_misure = sum(complete.cases(
    fossili[tre])))


# ======================================================
# 44_meccanismi.R
# ======================================================
set.seed(17)
x_miss <- rlnorm(200, 1, 0.5)
# Due regole, stesso campione
casuali <- runif(200) < 0.3
alti <- rank(x_miss) > 200 * 0.7
c(casuali = sum(casuali),
  selettivi = sum(alti))


# ======================================================
# 45_finiti.R
# ======================================================
# Colonne scelte nella slide 43
diametri <- fossili[due]
completi <- complete.cases(diametri)
finiti <- Reduce(`&`,
  lapply(diametri, is.finite))
table(completi, finiti)


# ======================================================
# 46_denominatore.R
# ======================================================
x_na <- c(4, NA, 6)
n_oss <- sum(!is.na(x_na))
media_oss <- if (n_oss > 0)
  mean(x_na, na.rm = TRUE) else NA
c(totali = length(x_na),
  disponibili = n_oss,
  media = media_oss)


# ======================================================
# 47_imputazione.R
# ======================================================
x_imp <- x_na # 4, NA, 6
x_imp[is.na(x_imp)] <- media_oss
c(media = mean(x_imp),
  var_disponibili = var(x_na,
                        na.rm = TRUE),
  var_imputati = var(x_imp))


# ======================================================
# 48_censura.R
# ======================================================
# Dataset caricato da setup.R
table(censura$stato)
sel_c <- censura$stato == "censurato"
censura[sel_c, c("testo_originale",
  "valore_osservato", "limite")]
stopifnot(all(is.na(
  censura$valore_osservato[sel_c])))


# ======================================================
# 49_limiti.R
# ======================================================
# Sottocaso: tre valori non negativi
osservati_c <- c(0.12, 0.08)
limite_c <- 0.05
c(inferiore = sum(osservati_c) / 3,
  superiore = (sum(osservati_c) +
               limite_c) / 3)


# ======================================================
# 50_lab_mancanti.R
# ======================================================
set.seed(17)
lab_x <- rlnorm(200, 1, 0.5)
lab_assenti <- rank(lab_x) > 140
c(mancanti = sum(lab_assenti),
  completa = mean(lab_x),
  disponibile = mean(
    lab_x[!lab_assenti]))


# ======================================================
# 53_flag.R
# ======================================================
est <- fossili$diametro_tot_um
int <- fossili$diametro_int_um
pres <- is.finite(est) &
        is.finite(int)
viol <- pres & (est <= 0 |
               int < 0 | int > est)
stopifnot(!anyNA(viol))
table(presente = pres,
      violazione = viol)


# ======================================================
# 54_sovrapposizioni.R
# ======================================================
nomi_flag <- c("misura_mancante",
  "non_positivo", "interno_superiore")
flags <- fossili[nomi_flag]
colSums(flags) # 2, 1, 2
coinvolte <- rowSums(flags) > 0
sum(coinvolte) # 4 righe


# ======================================================
# 56_grafico_geometria.R
# ======================================================
x_g <- fossili$diametro_tot_um
y_g <- fossili$diametro_int_um
ok_g <- is.finite(x_g) &
        is.finite(y_g)
col_g <- ifelse(viol,
  "firebrick", "steelblue")
plot(x_g[ok_g], y_g[ok_g], asp = 1,
  pch = 19, col = col_g[ok_g],
  xlab = "D esterno [um]",
  ylab = "D interno [um]")
abline(0, 1, lty = 2)


# ======================================================
# 57_sensibilita.R
# ======================================================
g <- fossili$usabile_geometria
geo <- fossili[g, ]
rapporto <- geo$diametro_int_um /
            geo$diametro_tot_um
soglie <- c(0.8, 0.85, 0.9)
n_soglia <- sapply(soglie,
  function(s) sum(rapporto <= s))
data.frame(soglia = soglie,
           mantenute = n_soglia)


# ======================================================
# 58_lab_controlli.R
# ======================================================
set.seed(17)
temp_lab <- c(rnorm(29, 15, 3), 250)
valido_lab <- temp_lab >= -50 &
              temp_lab <= 60
c(segnalate = sum(!valido_lab),
  media = mean(temp_lab))
# La media usa ancora tutte le righe


# ======================================================
# 59_derivata.R
# ======================================================
# F001: due diametri in micrometri
f1 <- fossili[fossili$id == "F001", ]
d_est <- f1$diametro_tot_um
d_int <- f1$diametro_int_um
spessore <- (d_est - d_int) / 2
spessore                   # 0.5
# Residuo dell'identita geometrica
d_est - d_int - 2 * spessore


# ======================================================
# 60_geometria.R
# ======================================================
# Flag documentato in setup.R
ok_geo <- fossili$usabile_geometria
geometria <- fossili[ok_geo, ]
geometria$spessore_um <- with(
  geometria,
  (diametro_tot_um-diametro_int_um)/2)
geometria$rapporto_int_tot <- with(
  geometria,
  diametro_int_um/diametro_tot_um)
nrow(geometria)              # 21


# ======================================================
# 61_chiusura.R
# ======================================================
# Tre parti nelle stesse unita
comp <- c(A = 40, B = 35, C = 25)
tot_comp <- sum(comp)
stopifnot(all(comp >= 0),
          tot_comp > 0)
chiusa <- 100 * comp / tot_comp
chiusa
sum(chiusa)                 # 100


# ======================================================
# 63_denominatore.R
# ======================================================
comp2 <- comp
comp2["A"] <- 80
chiusa2 <- 100 * comp2 / sum(comp2)
# Confronto di scenari deterministici
rbind(prima = chiusa,
      dopo = chiusa2)
chiusa2["B"] / chiusa2["C"]  # 1.4


# ======================================================
# 64_totale.R
# ======================================================
ossidi <- c("SiO2", "MgO", "FeO",
            "CaO", "Al2O3", "Cr2O3")
totale <- rowSums(microsonda[ossidi])
# Tolleranza didattica: 2 punti %
qc_totale <- abs(totale - 100) <= 2
table(qc_totale)
range(totale)
max(abs(totale-microsonda$totale_wt))


# ======================================================
# 65_normalizzazione.R
# ======================================================
stopifnot(all(is.finite(totale)),
          all(totale > 0))
normalizzati <- 100 * sweep(
  microsonda[ossidi], 1, totale, "/")
# Ora la somma e imposta a 100
range(rowSums(normalizzati))
# Il totale originale resta distinto
head(data.frame(totale, qc_totale))


# ======================================================
# 66_moli.R
# ======================================================
# Percentuali: grammi su 100 g
n_mg <- microsonda$MgO / 40.304
n_fe <- microsonda$FeO / 71.844
x_mg <- n_mg / (n_mg + n_fe)
head(x_mg)
# Nel CSV mg_num e una frazione
max(abs(x_mg-microsonda$mg_num))
mg_percento <- 100 * x_mg


# ======================================================
# 67_masse_moli.R
# ======================================================
# Base didattica: 40 g MgO, 10 g FeO
mgo <- 40
feo <- 10
rapporto_massa <- mgo / (mgo + feo)
a_mg <- mgo / 40.304
b_fe <- feo / 71.844
rapporto_moli <- a_mg / (a_mg + b_fe)
c(massa = rapporto_massa,
  molare = rapporto_moli)


# ======================================================
# 68_lab_composizione.R
# ======================================================
# Stesso modello del laboratorio
scenari <- c(40, 80)
percentuali <- sapply(scenari,
  function(a) {
    v <- c(A = a, B = 35, C = 25)
    100 * v / sum(v)
  })
colnames(percentuali) <- scenari
percentuali


# ======================================================
# 69_funzione.R
# ======================================================
densita <- function(massa, volume) {
  massa / volume
}
# Chiamata sul dataset dei provini
rho <- densita(campioni$massa_g,
               campioni$volume_cm3)
head(rho)
length(rho)                  # 24


# ======================================================
# 70_argomenti.R
# ======================================================
scarto <- function(x,
                   riferimento=100) {
  x - riferimento
}
# Riferimento esplicito
delta_tot <- scarto(
  x = totale, riferimento = 100)
head(delta_tot)
# Stesso risultato col valore previsto
head(scarto(totale))


# ======================================================
# 71_contratto.R
# ======================================================
densita_controllata <- function(m,v) {
  stopifnot(is.numeric(m),
    is.numeric(v), length(m)>0,
    length(m)==length(v))
  stopifnot(all(is.finite(m)),
    all(is.finite(v)))
  stopifnot(all(m>0), all(v>0))
  m / v
}


# ======================================================
# 72_riciclo.R
# ======================================================
m_test <- c(10, 20, 30, 40)
v_corto <- c(2, 4)
m_test / v_corto       # 5, 5, 15, 10
# La funzione controllata si ferma
tryCatch(
  densita_controllata(m_test,v_corto),
  error = function(e)
    message("Errore atteso: ",
            conditionMessage(e)))


# ======================================================
# 73_caso_noto.R
# ======================================================
frazione_mg <- function(mgo,feo) {
  stopifnot(length(mgo)==length(feo),
    all(is.finite(mgo)), all(mgo>=0),
    all(is.finite(feo)), all(feo>=0))
  a <- mgo/40.304; b <- feo/71.844
  stopifnot(all(a+b>0))
  a/(a+b)
}
stopifnot(
  frazione_mg(40.304,71.844)==0.5)


# ======================================================
# 74_parametri.R
# ======================================================
cfg <- list(tolleranza = 2, seme = 17)
qc_cfg <- abs(totale - 100) <=
  cfg$tolleranza
table(qc_cfg)
# Estrazione di quattro identificativi
set.seed(cfg$seme)
sample(campioni$id, size = 4)
sessionInfo()


# ======================================================
# 75_lab_funzioni.R
# ======================================================
ampiezza <- 1        # Ripetere con 0
x_lab <- 5 + ampiezza * (-2:2)
sd_lab <- sd(x_lab)
ok_lab <- sd_lab > 0
z_lab <- if (ok_lab) {
  as.vector(scale(x_lab))
} else {
  rep(NA_real_, length(x_lab))
}
c(sd = sd_lab, media_z = mean(z_lab))


# ======================================================
# 76_specifica.R
# ======================================================
n_geo <- nrow(geometria)
n_chiavi <- length(
  unique(geometria$id))
stopifnot(!anyNA(geometria$id),
          all(nzchar(geometria$id)),
          n_chiavi == n_geo)
c(righe = n_geo, chiavi = n_chiavi)


# ======================================================
# 77_registro.R
# ======================================================
stopifnot(identical(
  fossili$riga_origine,
  fossili_raw$riga_origine))
flag_geo <- c("duplicato_esatto",
  "misura_mancante",
  "interno_superiore",
  "non_positivo", "usabile_geometria")
registro <- cbind(fossili_raw,
                  fossili[flag_geo])
table(registro$usabile_geometria)


# ======================================================
# 78_analitica.R
# ======================================================
col_finali <- c("id", "morfotipo",
  "diametro_tot_um",
  "diametro_int_um",
  "spessore_um", "rapporto_int_tot")
analitica <- geometria[col_finali]
rownames(analitica) <- NULL
stopifnot(nrow(analitica) == 21,
          !anyNA(analitica))
head(analitica)


# ======================================================
# 79_esportazione.R
# ======================================================
dir.create("Risultati",
           showWarnings = FALSE)
percorso_tab <- file.path("Risultati",
  "fossili_analitici.csv")
write.csv(analitica, percorso_tab,
  row.names = FALSE, na = "NA")
write.csv(registro,
  "Risultati/registro_controlli.csv",
  row.names = FALSE, na = "NA")


# ======================================================
# 80_rilettura.R
# ======================================================
riletta <- read.csv(percorso_tab,
  stringsAsFactors = FALSE)
stopifnot(identical(names(riletta),
                    names(analitica)))
stopifnot(identical(riletta$id,
                    analitica$id))
stopifnot(isTRUE(all.equal(riletta,
  analitica, tolerance = 1e-10)))


# ======================================================
# 81_lab_tabella.R
# ======================================================
tab_lab <- data.frame(id = 1:8,
  lunghezza = c(1.1,1.3,1.2,1.5,
                1.4,1.1,1.6,1.2))
# Due modifiche come nel laboratorio
tab_lab$id[8] <- 7
tab_lab$lunghezza[8] <- 1200
c(righe = nrow(tab_lab),
  chiavi = length(unique(tab_lab$id)),
  duplicati =
    sum(duplicated(tab_lab$id)),
  fuori = sum(tab_lab$lunghezza > 10))
