# Gemina M06 - Leggere probabilità e ranghi
# Aprire Gemina_M06.Rproj; eseguire dalla cartella del progetto.
# https://marzione00.github.io/Lab_Geo/#laboratorio/m06-ranghi
source("setup.R", encoding = "UTF-8")

# TODO: scrivere una previsione prima di eseguire le chiamate.
# La base usa esattamente i valori iniziali del sito.
rA <- lab_ranghi()
# La variante cambia un solo parametro, mantenendo seed = 17.
rB <- lab_ranghi(ratio = 2)

# $metrics estrae le statistiche; rbind le mette in due righe.
confronto <- rbind(base = rA$metrics, variante = rB$metrics)
print(confronto)
# $data contiene i dati del grafico, senza arrotondamento.
head(rA$data)
grafico_lab(rA)
grafico_lab(rB)
# TODO: rispondere alla domanda nel quaderno e discutere il limite.
