# Confronta lo stesso mese tra anni: marzo e settembre non vengono mescolati.
data <- observations[observations$month == as.integer(p$month) &
  observations$year >= p$start_year & is.finite(observations$extent_million_km2), ]
data <- data[order(data$year), ]
stopifnot(nrow(data) >= 20)

# La pendenza beta esprime milioni di km2 per anno; moltiplicarla per 10 dà il tasso decennale.
fit <- lm(extent_million_km2 ~ year, data = data)
data$fitted_million_km2 <- as.numeric(predict(fit))
data$residual_million_km2 <- resid(fit)
beta <- unname(coef(fit)['year'])

# Il riferimento 1981-2010 usa sempre il medesimo mese, anche quando cambia l'inizio del periodo.
reference <- observations[observations$month == as.integer(p$month) &
  observations$year >= 1981 & observations$year <= 2010, ]
baseline <- mean(reference$extent_million_km2, na.rm = TRUE)
percent_decade <- 100 * 10 * beta / baseline

# La correlazione al ritardo 1 segnala dipendenza residua; non costituisce una prova di indipendenza.
lag1 <- as.numeric(acf(data$residual_million_km2, lag.max = 1, plot = FALSE)$acf[2])
metrics <- metric('Anni osservati' = nrow(data),
  'Pendenza [milioni km2 / decennio]' = f(10 * beta),
  'Pendenza [% del riferimento / decennio]' = f(percent_decade),
  'Riferimento 1981-2010 [milioni km2]' = f(baseline),
  'Correlazione residua al ritardo 1' = f(lag1))
month_name <- if (p$month == '3') 'Marzo' else 'Settembre'

# Mostra osservazioni e retta stimata, limitando la rappresentazione all'intervallo studiato.
g1 <- ggplot(data, aes(year, extent_million_km2)) +
  geom_line(colour = '#A0ADB7', linewidth = 0.55) +
  geom_point(colour = '#168B9C', size = 2.6) +
  geom_line(aes(y = fitted_million_km2), colour = '#BC5B35', linewidth = 1.15) +
  labs(title = paste('Estensione artica ·', month_name),
    subtitle = 'NSIDC Sea Ice Index v4 · osservazioni e tendenza lineare',
    x = 'Anno', y = 'Estensione [milioni di km2]')

# I residui conservano l'ordine temporale, così eventuali sequenze rimangono visibili.
g2 <- ggplot(data, aes(year, residual_million_km2)) +
  geom_hline(yintercept = 0, colour = '#64748B', linetype = 2) +
  geom_line(colour = '#7054A4', linewidth = 0.75) +
  geom_point(colour = '#7054A4', size = 2.3) +
  labs(title = 'Scarti dalla tendenza lineare',
    subtitle = 'Diagnostica descrittiva: verificare struttura temporale e sensibilità al periodo',
    x = 'Anno', y = 'Residuo [milioni di km2]')
plots <- list(g1, g2)
