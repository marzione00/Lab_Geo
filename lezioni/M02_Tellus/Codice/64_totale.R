ossidi <- c("SiO2", "MgO", "FeO",
            "CaO", "Al2O3", "Cr2O3")
totale <- rowSums(microsonda[ossidi])
# Tolleranza didattica: 2 punti %
qc_totale <- abs(totale - 100) <= 2
table(qc_totale)
range(totale)
max(abs(totale-microsonda$totale_wt))
