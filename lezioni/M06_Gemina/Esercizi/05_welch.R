# Gemina M06 - Separare le due varianze
# Aprire Gemina_M06.Rproj; eseguire dalla cartella del progetto.
# https://marzione00.github.io/Lab_Geo/#laboratorio/m06-welch
source("setup.R", encoding = "UTF-8")

# La base usa esattamente i valori iniziali del sito.
rA <- lab_welch()
# La variante cambia un solo parametro, mantenendo seed = 17.
rB <- lab_welch(ratio = 1)

# $metrics estrae le statistiche; rbind le mette in due righe.
confronto <- rbind(base = rA$metrics, variante = rB$metrics)
print(confronto)
# $data contiene i dati del grafico, senza arrotondamento.
head(rA$data)
grafico_lab(rA)
grafico_lab(rB)
# Condizioni e limiti del confronto sono descritti nel quaderno.
