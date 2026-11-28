# Isocrona (M19): figure e valori della lezione sulla datazione radiometrica.
# Uso: LC_ALL=C.UTF-8 Rscript R/M19_figure.R dalla cartella della lezione. Scrive figure/M19 e risultati/M19.
# Codice: PolyForm Noncommercial 1.0.0. Required Notice: Copyright 2026 Marzio De Corato.
source('R/stile.R'); source('R/york.R')
out <- 'risultati/M19'; dir.create(out, recursive = TRUE, showWarnings = FALSE)
v <- list()
lambda <- 1.3972e-11; s_lambda <- 0.0045e-11 / 2   # Villa e colleghi (2015): incertezza con fattore di copertura 2.
eta <- function(b) log(1 + b) / lambda / 1e6
s_eta <- function(b, sb) sb / (lambda * (1 + b)) / 1e6

# 0. Controlli dell'implementazione di York.
px <- c(0, .9, 1.8, 2.6, 3.3, 4.4, 5.2, 6.1, 6.5, 7.4); py <- c(5.9, 5.4, 4.4, 4.6, 3.5, 3.7, 2.8, 2.8, 2.4, 1.5)
pwx <- c(1000, 1000, 500, 800, 200, 80, 60, 20, 1.8, 1); pwy <- c(1, 1.8, 4, 8, 20, 20, 70, 70, 100, 500)
yp <- york(px, 1 / sqrt(pwx), py, 1 / sqrt(pwy))
v$pearson_york <- yp
verifica('dati di Pearson con i pesi di York: b = -0,4805 e a = 5,4799', abs(yp[['b']] + .48053) < 1e-4 && abs(yp[['a']] - 5.47991) < 1e-4)
yw <- york(px, rep(1e-9, 10), py, 1 / sqrt(pwy)); lw <- coef(lm(py ~ px, weights = pwy))
verifica('con errori trascurabili su x York coincide con i minimi quadrati pesati', abs(yw[['b']] - lw[[2]]) < 1e-8)

# 1. Costante di decadimento, tempo di dimezzamento, età di un rapporto.
v$dimezzamento_Ga <- log(2) / lambda / 1e9
verifica('tempo di dimezzamento 49,61 Ga', abs(v$dimezzamento_Ga - 49.61) < .01)
v$eta_rapporto <- eta(0.0042)
v$frazione_decaduta_300 <- 1 - exp(-lambda * 300e6)

# 2. Granito: età modello con rapporto iniziale assunto 0,704, minimi quadrati ordinari e York.
d <- leggi('isocrone_v1.csv'); g <- d[d$suite == 'granito', ]; f <- d[d$suite == 'filone', ]
mod <- function(x, y, r0) log(1 + (y - r0) / x) / lambda / 1e6
v$eta_modello <- setNames(mod(g$Rb87Sr86, g$Sr87Sr86, .704), g$campione)
ols <- coef(lm(Sr87Sr86 ~ Rb87Sr86, data = g))
v$ols <- c(a = ols[[1]], b = ols[[2]], eta = eta(ols[[2]]))
yg <- with(g, york(Rb87Sr86, sRb, Sr87Sr86, sSr))
v$york_granito <- c(yg, eta = eta(yg[['b']]), s_eta = s_eta(yg[['b']], yg[['sb']]))
fg <- nrow(g) - 2; v$soglia_granito <- 1 + 2 * sqrt(2 / fg); v$p_granito <- pchisq(yg[['mswd']] * fg, fg, lower.tail = FALSE)
verifica('granito: età entro tre deviazioni standard da 300 Ma', abs(v$york_granito[['eta']] - 300) < 3 * v$york_granito[['s_eta']])
verifica('granito: MSWD sotto la soglia di Wendt e Carl', yg[['mswd']] < v$soglia_granito)
# Simulazione: la deviazione standard delle pendenze di York riproduce l'errore standard calcolato.
set.seed(11)
bt <- exp(lambda * 300e6) - 1
bs <- replicate(2000, { x <- g$Rb87Sr86 + rnorm(10, 0, g$sRb); y <- .7085 + bt * g$Rb87Sr86 + rnorm(10, 0, g$sSr)
  york(x, g$sRb, y, g$sSr)[['b']] })
v$sd_pendenze_simulate <- sd(bs)
verifica('errore standard della pendenza confermato dalla simulazione entro il 10%', abs(sd(bs) / yg[['sb']] - 1) < .1)

# 3. Filone: dispersione in eccesso.
yf <- with(f, york(Rb87Sr86, sRb, Sr87Sr86, sSr))
ff <- nrow(f) - 2
v$york_filone <- c(yf, eta = eta(yf[['b']]), s_eta = s_eta(yf[['b']], yf[['sb']]), s_eta_scalato = s_eta(yf[['b']], yf[['sb']]) * sqrt(yf[['mswd']]))
v$soglia_filone <- 1 + 2 * sqrt(2 / ff); v$p_filone <- pchisq(yf[['mswd']] * ff, ff, lower.tail = FALSE)
verifica('filone: MSWD oltre la soglia', yf[['mswd']] > v$soglia_filone)
wf <- with(f, 1 / sqrt(sRb^2 * yf[['b']]^2 + sSr^2))
v$residui_filone <- setNames(with(f, (Sr87Sr86 - yf[['a']] - yf[['b']] * Rb87Sr86) * wf), f$campione)

# 4. Incertezza dell'età del granito con la costante di decadimento.
t_g <- v$york_granito[['eta']]
v$incertezza <- c(analitica = v$york_granito[['s_eta']], costante = t_g * s_lambda / lambda,
                  totale = sqrt(v$york_granito[['s_eta']]^2 + (t_g * s_lambda / lambda)^2))

# 5. Zirconi: media pesata con e senza il granulo ereditato.
z <- leggi('date_v1.csv')
mp <- function(t, s) { w <- 1 / s^2; m <- sum(w * t) / sum(w); c(media = m, se = sqrt(1 / sum(w)), mswd = sum(w * (t - m)^2) / (length(t) - 1),
  soglia = 1 + 2 * sqrt(2 / (length(t) - 1))) }
v$zirconi_tutti <- mp(z$data_Ma, z$s_Ma); v$zirconi_14 <- mp(z$data_Ma[-15], z$s_Ma[-15])
verifica('con Z15 la MSWD supera la soglia, senza resta sotto', v$zirconi_tutti[['mswd']] > v$zirconi_tutti[['soglia']] && v$zirconi_14[['mswd']] < v$zirconi_14[['soglia']])
s_l238 <- 0.00333e-10 / 2 / 1.55125e-10   # incertezza relativa (1 sigma) della costante di 238U, Villa e colleghi (2022).
zt <- v$zirconi_14[['media']]
v$zirconi_totale <- sqrt(v$zirconi_14[['se']]^2 + (zt * s_l238)^2)
v$confronto <- c(differenza = t_g - zt, s_diff = sqrt(v$incertezza[['totale']]^2 + v$zirconi_totale^2))
v$confronto[['z']] <- v$confronto[['differenza']] / v$confronto[['s_diff']]

# Figure.
xs <- seq(0.05, 12, length.out = 300)
salva('M19', 'F01', ggplot(data.frame(x = xs, t = mod(xs, .7085 + bt * xs, .704)), aes(x, t)) + geom_line(colour = geo[1], linewidth = 1) +
  geom_hline(yintercept = 300, linetype = 2, colour = ink) +
  geom_point(data = data.frame(x = g$Rb87Sr86, t = v$eta_modello), colour = geo[3], size = 2.4) +
  scale_y_log10(breaks = c(300, 500, 1000, 2000, 5000), labels = fmt) + scale_x_continuous(labels = fmt) +
  labs(x = expression({}^87 * Rb / {}^86 * Sr), y = 'Età modello (Ma)'))
lg <- data.frame(x = c(0, 12)); lg$y <- yg[['a']] + yg[['b']] * lg$x
salva('M19', 'F02', ggplot(g, aes(Rb87Sr86, Sr87Sr86)) + geom_line(data = lg, aes(x, y), colour = geo[2], linewidth = .9) +
  geom_errorbarh(aes(xmin = Rb87Sr86 - 2 * sRb, xmax = Rb87Sr86 + 2 * sRb), height = .0012, colour = ink, linewidth = .5) +
  geom_point(colour = geo[1], size = 2.4) + scale_y_continuous(labels = fmt) + scale_x_continuous(labels = fmt) +
  labs(x = expression({}^87 * Rb / {}^86 * Sr), y = expression({}^87 * Sr / {}^86 * Sr)))
mm <- seq(0.01, 4, length.out = 400)
dens <- rbind(data.frame(m = mm, d = ff * dchisq(mm * ff, ff), f = paste('Filone, f =', ff)),
              data.frame(m = mm, d = fg * dchisq(mm * fg, fg), f = paste('Granito, f =', fg)))
oss <- data.frame(m = c(yg[['mswd']], min(yf[['mswd']], 3.9)), f = c(paste('Granito, f =', fg), paste('Filone, f =', ff)))
salva('M19', 'F03', ggplot(dens, aes(m, d, colour = f)) + geom_line(linewidth = 1) +
  geom_vline(data = data.frame(s = c(v$soglia_granito, v$soglia_filone), f = c(paste('Granito, f =', fg), paste('Filone, f =', ff))),
             aes(xintercept = s, colour = f), linetype = 2) +
  geom_point(data = oss, aes(m, 0, colour = f), size = 3.4, shape = 17) +
  scale_colour_manual(values = geo[c(3, 1)]) + scale_x_continuous(labels = fmt) + scale_y_continuous(labels = fmt) +
  labs(x = 'MSWD', y = 'Densità'))
salva('M19', 'F04', ggplot(data.frame(c = f$campione, r = v$residui_filone), aes(c, r)) +
  annotate('rect', xmin = -Inf, xmax = Inf, ymin = -2, ymax = 2, fill = '#DDEBE8') + geom_hline(yintercept = 0, colour = ink) +
  geom_point(colour = geo[3], size = 3) + scale_y_continuous(labels = fmt) +
  labs(x = 'Campione del filone', y = 'Residuo pesato') + theme(axis.text.x = element_text(size = 14)))
zz <- data.frame(z = z$zircone, t = z$data_Ma, s = z$s_Ma, ered = ifelse(z$zircone == 'Z15', 'Ereditato', 'Granito'))
zz <- zz[order(zz$t), ]; zz$k <- seq_len(nrow(zz))
salva('M19', 'F05', ggplot(zz, aes(k, t, colour = ered)) +
  annotate('rect', xmin = -Inf, xmax = Inf, ymin = zt - 2 * v$zirconi_14[['se']], ymax = zt + 2 * v$zirconi_14[['se']], fill = '#DDEBE8') +
  geom_hline(yintercept = zt, colour = ink, linewidth = .5) + geom_errorbar(aes(ymin = t - 2 * s, ymax = t + 2 * s), width = .3) +
  geom_point(size = 2.2) + scale_colour_manual(values = c(geo[3], geo[1])) + scale_y_continuous(labels = fmt) +
  labs(x = 'Zirconi ordinati per data', y = 'Data U-Pb (Ma)'))
ci <- data.frame(m = c('Rb-Sr, analitica', 'Rb-Sr, con costante', 'U-Pb, media pesata'),
                 t = c(t_g, t_g, zt), s = c(v$incertezza[['analitica']], v$incertezza[['totale']], v$zirconi_totale))
ci$m <- factor(ci$m, levels = rev(ci$m))
salva('M19', 'F06', ggplot(ci, aes(t, m)) + geom_errorbarh(aes(xmin = t - 2 * s, xmax = t + 2 * s), height = .25, colour = geo[1], linewidth = .8) +
  geom_point(colour = geo[2], size = 3) + scale_x_continuous(breaks = seq(298, 304, 1), labels = fmt) +
  labs(x = 'Età (Ma)', y = NULL) + theme(axis.text.y = element_text(size = 17)), w = 6.2, h = 3.8)

capture <- function(x) paste(capture.output(print(x)), collapse = '\n')
jsonlite::write_json(lapply(v, function(x) if (is.table(x) || is.matrix(x)) capture(x) else as.list(x)),
                     file.path(out, 'valori.json'), auto_unbox = TRUE, pretty = TRUE, digits = 8)
str(v)
