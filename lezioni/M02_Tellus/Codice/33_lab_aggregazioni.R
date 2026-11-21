# Versione locale del modello del sito
source("Tellus_laboratori.R")
ris <- lab_aggregazioni(nA = 50,
                        seed = 17)
ris$indicatori    # Medie campionarie
ris$attese        # Valori del modello
