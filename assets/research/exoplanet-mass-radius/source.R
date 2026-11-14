# Richiede entrambi gli errori asimmetrici: i mancanti non vengono sostituiti con zero.
mass_err <- pmax(abs(observations$pl_bmasseerr1), abs(observations$pl_bmasseerr2)) / observations$pl_bmasse
radius_err <- pmax(abs(observations$pl_radeerr1), abs(observations$pl_radeerr2)) / observations$pl_rade
keep <- is.finite(mass_err) & is.finite(radius_err) &
  mass_err > 0 & radius_err > 0 &
  mass_err <= p$max_relative_error & radius_err <= p$max_relative_error &
  observations$pl_rade >= 0.5 & observations$pl_rade <= p$max_radius
keep[is.na(keep)] <- FALSE
data <- observations[keep, , drop = FALSE]
stopifnot(nrow(data) >= 20)

# Divide per stella: tutti i pianeti dello stesso sistema rimangono nello stesso insieme.
# L’ordine dei nomi è fissato byte per byte, indipendentemente dalla lingua del sistema.
hosts <- sort(unique(data$hostname), method="radix")
stopifnot(length(hosts) >= 10)
train_hosts <- sample(hosts, size = floor(length(hosts) * p$train_fraction))
data$insieme <- ifelse(data$hostname %in% train_hosts, "Stima", "Verifica")
data$log_radius <- log10(data$pl_rade)
data$log_mass <- log10(data$pl_bmasse)
train <- data[data$insieme == "Stima", , drop = FALSE]
test <- data[data$insieme == "Verifica", , drop = FALSE]

# Stima il modello soltanto sui sistemi assegnati all’insieme di addestramento.
fit <- lm(log_mass ~ log_radius, data = train)
data$predicted_log_mass <- as.numeric(predict(fit, newdata = data))
data$residuo_log <- data$log_mass - data$predicted_log_mass
test_prediction <- as.numeric(predict(fit, newdata = test))
rmse <- sqrt(mean((test$log_mass - test_prediction)^2))
baseline_rmse <- sqrt(mean((test$log_mass - mean(train$log_mass))^2))
metrics <- metric(
  "Pianeti dopo i filtri" = nrow(data),
  "Sistemi di stima" = length(train_hosts),
  "Sistemi di verifica" = length(hosts) - length(train_hosts),
  "Pendenza beta" = f(unname(coef(fit)[2])),
  "RMSE verifica [dex]" = f(rmse),
  "RMSE previsione costante [dex]" = f(baseline_rmse)
)

# Disegna il modello di stima sull’intervallo osservato; i punti di verifica restano distinguibili.
grid <- data.frame(log_radius = seq(min(data$log_radius), max(data$log_radius), length.out = 100))
grid$log_mass <- as.numeric(predict(fit, newdata = grid))
g1 <- ggplot(data, aes(x = log_radius, y = log_mass, colour = insieme)) +
  geom_point(size = 2.3, alpha = 0.65) +
  geom_line(data = grid, aes(x = log_radius, y = log_mass), inherit.aes = FALSE,
            colour = "#172F42", linewidth = 1) +
  scale_colour_manual(values = c("Stima" = col_geo[1], "Verifica" = col_geo[2])) +
  labs(title = "Relazione massa–raggio: modello di riferimento",
       subtitle = "NASA Exoplanet Archive · partizione per sistema stellare",
       x = "log10 del raggio [R/R⊕]", y = "log10 della massa [M/M⊕]")

# La struttura dei residui suggerisce quali aspetti il modello lineare non descrive.
g2 <- ggplot(data, aes(x = predicted_log_mass, y = residuo_log, colour = insieme)) +
  geom_hline(yintercept = 0, colour = "#64748B", linetype = 2) +
  geom_point(size = 2.3, alpha = 0.65) +
  scale_colour_manual(values = c("Stima" = col_geo[1], "Verifica" = col_geo[2])) +
  labs(title = "Residui e valori previsti", subtitle = "Un residuo è osservato meno previsto, in scala logaritmica",
       x = "log10 della massa prevista [M/M⊕]", y = "Residuo [dex]")
plots <- list(g1, g2)
