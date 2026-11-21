# La risposta compare a sinistra di ~.
m0 <- lm(diametro_int_um ~
           diametro_tot_um, data = f)
coef(m0)      # Intercetta e pendenza.
fitted(m0)    # Valori medi stimati.
residuals(m0) # Osservato - stimato.
summary(m0)
