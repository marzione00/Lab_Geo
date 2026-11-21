# Gemina - verifica conclusiva della slide 93.
# Aprire Gemina_M06.Rproj ed eseguire dalla radice del progetto.
source("setup.R", encoding="UTF-8")
f <- read.csv("Dati/fossili_simulati.csv")
variabili <- c("diametro_tot_um","diametro_int_um")
table(f$morfotipo)
summary(f[variabili])

# 1. Motivare il disegno e dichiarare il contrasto Spiky meno Rounded.
# 2. Disegnare i valori dei due gruppi per ciascuna variabile.
# 3. Calcolare differenza media, SE, intervallo marginale 95% e p bilaterale.
# 4. Considerare le due ipotesi una famiglia pianificata e applicare Holm.
# 5. Scrivere una relazione di 120-180 parole.
#    Dichiarare unita, numerosita, indipendenza fra fossili,
#    dipendenza fra misure sullo stesso fossile e natura sintetica dei dati.
#    Gli IC marginali non diventano simultanei correggendo i soli p-value.
