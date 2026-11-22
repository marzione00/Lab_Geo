# Tellus M02 - esercizio 08
# Chiusura della composizione e denominatore comune
# Laboratorio: https://marzione00.github.io/Lab_Geo/#laboratorio/m02-composizione
# Aprire Tellus_M02.Rproj prima di eseguire questo file.
# Eseguire a righe oppure con source(..., echo = TRUE).

source("Tellus_laboratori.R", encoding = "UTF-8")
# Modifica solo A; B e C restano negli ingressi.
rA <- lab_composizione(a = 40)
rB <- lab_composizione(a = 80)
# Confronta quantita originarie e percentuali.
rA$dati
rB$dati
rbind(A = rA$indicatori, B = rB$indicatori)
