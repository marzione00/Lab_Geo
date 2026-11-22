# Medie e numerosita per stazione
m <- tapply(terra_sim$valore,
            terra_sim$stazione, mean)
n <- table(terra_sim$stazione)
n <- n[names(m)]  # Stesso ordine dei gruppi

mean(terra_sim$valore)  # Circa 5.75 mg/L
mean(m)                # Circa 6.61 mg/L
weighted.mean(m, n)     # Controllo: circa 5.75
