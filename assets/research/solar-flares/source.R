# I tempi sono UTC; la durata termina secondo la definizione operativa dell'archivio GOES.
data <- observations
start <- as.POSIXct(data$start_time, format = '%Y-%m-%d %H:%M:%S', tz = 'UTC')
end <- as.POSIXct(data$end_time, format = '%Y-%m-%d %H:%M:%S', tz = 'UTC')
data$duration_minutes <- as.numeric(difftime(end, start, units = 'mins'))
valid <- is.finite(data$duration_minutes) & data$duration_minutes > 0 &
  is.finite(data$xrsb_irrad) & data$xrsb_irrad > 0
missing_duration <- sum(!valid)

# La soglia di irradiamento seleziona un sottocampione; non corregge la completezza del catalogo.
threshold <- switch(p$minimum_class, B = 1e-7, C = 1e-6, M = 1e-5)
selection <- valid & data$xrsb_irrad >= threshold
if (p$sequence == 'first') selection <- selection & data$sequential_flare_num == 1
selected <- data[selection, ]

# I picchi saturati rimangono visibili nel conteggio ma sono sempre esclusi dalla regressione.
saturated <- selected[selected$peak_saturated == 1, ]
data <- selected[!is.na(selected$peak_saturated) & selected$peak_saturated == 0, ]
stopifnot(nrow(data) >= 10)
data$log_duration <- log10(data$duration_minutes)
data$log_irradiance <- log10(data$xrsb_irrad)

# La retta riassume l'associazione logaritmica; le osservazioni non identificano un rapporto causale.
fit <- lm(log_irradiance ~ log_duration, data = data)
data$fitted_log_irradiance <- as.numeric(predict(fit))
data$residual_log_irradiance <- resid(fit)
rho <- cor(data$duration_minutes, data$xrsb_irrad, method = 'spearman')
metrics <- metric('Eventi nel file originale' = nrow(observations),
  'Durata o intensità non utilizzabile' = missing_duration,
  'Eventi selezionati prima del controllo saturazione' = nrow(selected),
  'Picchi saturati esclusi dal modello' = nrow(saturated),
  'Eventi nel modello' = nrow(data),
  'Pendenza in scala log10' = f(unname(coef(fit)[2])),
  'Correlazione di Spearman' = f(rho))

# Assi logaritmici mantengono visibili eventi che differiscono per diversi ordini di grandezza.
g1 <- ggplot(data, aes(duration_minutes, xrsb_irrad)) +
  geom_point(colour = '#BC5B35', alpha = 0.5, size = 1.9) +
  geom_smooth(method = 'lm', formula = y ~ x, se = FALSE, colour = '#168B9C', linewidth = 1.1) +
  scale_x_log10() + scale_y_log10() +
  labs(title = 'Brillamenti solari · GOES 2003',
    subtitle = 'Soli picchi non saturati · regressione descrittiva in scala logaritmica',
    x = 'Durata [minuti; scala log10]', y = 'Irradiamento di picco [W/m2; scala log10]')

# Il grafico dei residui aiuta a riconoscere dispersione variabile e forme non lineari.
g2 <- ggplot(data, aes(fitted_log_irradiance, residual_log_irradiance)) +
  geom_hline(yintercept = 0, colour = '#64748B', linetype = 2) +
  geom_point(colour = '#7054A4', alpha = 0.5, size = 1.9) +
  labs(title = 'Diagnostica della relazione durata–irradiamento',
    subtitle = 'Confrontare soglie e primi eventi di sequenza prima di interpretare la pendenza',
    x = 'Valore stimato [log10 W/m2]', y = 'Residuo [log10 W/m2]')
plots <- list(g1, g2)
