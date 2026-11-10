# Poisson: conteggi con esposizione dichiarata
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
ctx <- inizia_notebook("M04_N08")
set.seed(1007)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Preparazione: Evento e probabilità: una regola dichiarata
set.seed(407)
p <- .30
estrazioni <- rbinom(n = 20, size = 1, prob = p)
estrazioni
c(successi = sum(estrazioni), prove = length(estrazioni),
  frequenza_relativa = mean(estrazioni), probabilita_modello = p)


# Preparazione: Eventi complementari e soglie
conteggi_demo <- c(0,1,2,3,4,5)
data.frame(conteggio = conteggi_demo,
           almeno_3 = conteggi_demo >= 3,
           piu_di_3 = conteggi_demo > 3,
           al_massimo_3 = conteggi_demo <= 3,
           esattamente_3 = conteggi_demo == 3)
1 - p


# Preparazione: Una tabella per la probabilità condizionata
tab <- matrix(c(18,12,9,21), nrow = 2, byrow = TRUE,
              dimnames = list(gruppo = c("A","B"), carattere = c("Presente","Assente")))
tab
p_presente_dato_A <- tab["A","Presente"] / sum(tab["A",])
p_A_dato_presente <- tab["A","Presente"] / sum(tab[,"Presente"])
c(P_presente_dato_A = p_presente_dato_A,
  P_A_dato_presente = p_A_dato_presente)
prop.table(tab, 1)
prop.table(tab, 2)


# Preparazione: Indipendenza: non basta una somiglianza visiva
P <- tab / sum(tab)
p_A <- sum(P["A",])
p_presente <- sum(P[,"Presente"])
c(congiunta_osservata = P["A","Presente"],
  prodotto_marginali = p_A * p_presente)
attese <- outer(rowSums(tab), colSums(tab)) / sum(tab)
dimnames(attese) <- dimnames(tab)
attese


# Preparazione: La binomiale: numero di successi in n prove
n <- 10L
k <- 0:n
prob <- dbinom(k, size = n, prob = p)
binomiale <- data.frame(k = k, probabilita = prob)
binomiale
stopifnot(abs(sum(prob) - 1) < 1e-12)
c(media_teorica = n*p, varianza_teorica = n*p*(1-p))
stile_grafico()
plot(k, prob, type = "h", lwd = 6, col = palette_geo[1],
     xlab = "Successi in 10 prove", ylab = "Probabilità",
     main = "Modello binomiale: n=10, p=0,30")


# Preparazione: Calcolare probabilità di eventi composti
p_almeno_uno <- 1 - dbinom(0, size = n, prob = p)
p_almeno_quattro <- pbinom(3, size = n, prob = p, lower.tail = FALSE)
p_somma <- sum(dbinom(4:n, size = n, prob = p))
c(almeno_uno = p_almeno_uno, almeno_quattro = p_almeno_quattro)
stopifnot(abs(p_almeno_quattro - p_somma) < 1e-12)
# Probabilità tra 2 e 5 inclusi.
pbinom(5,n,p) - pbinom(1,n,p)


# Preparazione: Verificare una probabilità con simulazioni
set.seed(408)
B <- 10000L
sim <- rbinom(B, size = n, prob = p)
freq <- mean(sim >= 4)
se_MC <- sqrt(freq * (1 - freq) / B)
data.frame(probabilita_teorica = p_almeno_quattro,
           frequenza_simulata = freq,
           errore_standard_MonteCarlo = se_MC,
           repliche = B)
# Confronto tra frequenze e probabilità per tutti i conteggi.
osservate <- tabulate(sim + 1L, nbins = n + 1L) / B
head(data.frame(k = k, teorica = prob, simulata = osservate), 11)


# Analisi principale: Poisson: conteggi con esposizione dichiarata
lambda_ora <- 3
kP <- 0:15
probP <- dpois(kP, lambda = lambda_ora)
c(almeno_uno_in_un_ora = 1 - dpois(0,lambda_ora),
  almeno_uno_in_due_ore = 1 - dpois(0,2*lambda_ora))
set.seed(409)
simP <- rpois(10000, lambda_ora)
c(media = mean(simP), varianza = var(simP), lambda = lambda_ora)
stile_grafico()
plot(kP, probP, type = "h", lwd = 6, col = palette_geo[2],
     xlab = "Conteggio per intervallo", ylab = "Probabilità",
     main = "Esempio teorico Poisson: lambda=3")
