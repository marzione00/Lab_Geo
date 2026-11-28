# Azimut (M18): figure e valori della lezione sui dati direzionali.
# Uso: LC_ALL=C.UTF-8 Rscript R/M18_figure.R dalla cartella della lezione. Scrive figure/M18 e risultati/M18.
# Codice: PolyForm Noncommercial 1.0.0. Required Notice: Copyright 2026 Marzio De Corato.
source('R/stile.R')
out <- 'risultati/M18'; dir.create(out, recursive = TRUE, showWarnings = FALSE)
gr <- pi / 180
v <- list()
media_circ <- function(a) c(dir = (atan2(mean(sin(a)), mean(cos(a))) / gr) %% 360, R = sqrt(mean(cos(a))^2 + mean(sin(a))^2))
A1 <- function(k) besselI(k, 1, TRUE) / besselI(k, 0, TRUE)
kappa_mv <- function(R) uniroot(function(k) A1(k) - R, c(1e-8, 1e3), tol = 1e-12)$root
# Approssimazione per piccoli campioni della probabilità di coda del test di Rayleigh.
p_rayleigh <- function(Z, n) pmin(1, exp(-Z) * (1 + (2 * Z - Z^2) / (4 * n) - (24 * Z - 132 * Z^2 + 76 * Z^3 - 9 * Z^4) / (288 * n^2)))
vett <- function(az, inc) cbind(cos(inc * gr) * cos(az * gr), cos(inc * gr) * sin(az * gr), sin(inc * gr))
angoli <- function(x) c(az = (atan2(x[2], x[1]) / gr) %% 360, inc = asin(x[3] / sqrt(sum(x^2))) / gr)
# Proiezione equivalente (Lambert, emisfero inferiore) su un cerchio primitivo di raggio unitario.
proietta <- function(V) {
  V <- V * sign(V[, 3]); inc <- asin(pmin(1, V[, 3])); az <- atan2(V[, 2], V[, 1])
  r <- sqrt(2) * sin((pi / 2 - inc) / 2); data.frame(x = r * sin(az), y = r * cos(az))
}
cerchio <- data.frame(x = sin(seq(0, 2 * pi, length.out = 361)), y = cos(seq(0, 2 * pi, length.out = 361)))
rete <- function() list(geom_path(data = cerchio, aes(x, y), colour = ink, linewidth = .5),
  annotate('segment', x = 0, xend = 0, y = 1, yend = 1.06, colour = ink, linewidth = .5),
  annotate('text', x = 0, y = 1.13, label = 'N', size = 6, colour = ink),
  annotate('point', x = 0, y = 0, shape = 3, size = 2.5, colour = ink),
  coord_equal(xlim = c(-1.08, 1.08), ylim = c(-1.08, 1.18), clip = 'off'),
  theme_void(base_size = 18, base_family = 'Nimbus Sans'),
  theme(plot.background = element_rect(fill = paper, colour = NA), legend.position = 'right',
        legend.title = element_blank(), legend.text = element_text(size = 15), plot.margin = margin(9, 9, 9, 9)))

# 1. Paleocorrenti: media aritmetica, direzione media, lunghezza media risultante, per stazione.
d <- leggi('correnti_v1.csv'); a <- d$azimut * gr
v$n_correnti <- nrow(d)
v$media_aritmetica <- mean(d$azimut)
v$media_circolare <- media_circ(a)
v$varianza_circolare <- 1 - v$media_circolare[['R']]
v$sd_circolare <- sqrt(-2 * log(v$media_circolare[['R']])) / gr
dd <- function(x, y) abs(((x - y + 180) %% 360) - 180)
verifica('la media aritmetica degli azimut dista più di 90 gradi dalla direzione media', dd(v$media_aritmetica, v$media_circolare[['dir']]) > 90)
per <- t(sapply(split(a, d$stazione), function(x) {
  m <- media_circ(x); n <- length(x); Z <- n * m[['R']]^2
  c(m, sd = sqrt(-2 * log(m[['R']])) / gr, kappa = kappa_mv(m[['R']]), Z = Z, p = p_rayleigh(Z, n))
}))
v$stazioni <- per
verifica('la stima di kappa soddisfa A1(kappa) = R', max(abs(A1(per[, 'kappa']) - per[, 'R'])) < 1e-9)
v$kappa_tutti <- kappa_mv(v$media_circolare[['R']])
# Controllo dell'approssimazione di Rayleigh con una simulazione sotto l'ipotesi di uniformità (n = 20).
set.seed(7)
Zs <- replicate(20000, { x <- runif(20, 0, 2 * pi); 20 * (mean(cos(x))^2 + mean(sin(x))^2) })
z95 <- unname(quantile(Zs, .95))
v$rayleigh_critico <- c(Z_simulato = z95, R_simulato = sqrt(z95 / 20), p_formula = p_rayleigh(z95, 20))
verifica('la formula di Rayleigh dà p vicino a 0,05 nel quantile simulato', abs(p_rayleigh(z95, 20) - .05) < .004)
Rcrit <- sqrt(uniroot(function(z) p_rayleigh(z, 20) - .05, c(1, 6))$root / 20)
v$R_critico_formula <- Rcrit

# 2. Fratture: angoli registrati, angoli raddoppiati, asse medio per famiglia e insieme.
fr <- leggi('fratture_v1.csv')
ass <- function(x) { m <- media_circ(2 * x * gr); c(R = media_circ(x * gr)[['R']], R2 = m[['R']], asse = (m[['dir']] / 2) %% 180) }
v$fratture <- rbind(t(sapply(split(fr$direzione, fr$famiglia), ass)), tutte = ass(fr$direzione))
verifica('raddoppiare gli angoli aumenta R per J1', v$fratture['J1', 'R2'] > 5 * v$fratture['J1', 'R'])
v$fratture_n <- table(fr$famiglia)
v$angolo_famiglie <- dd(2 * v$fratture['J1', 'asse'], 2 * v$fratture['J2', 'asse']) / 2

# 3. Paleomagnetismo: media di Fisher, k, alfa95 esatto e approssimato, confronto con il dipolo assiale.
pm <- leggi('paleomag_v1.csv'); X <- vett(pm$D, pm$I); N <- nrow(X)
s <- colSums(X); R <- sqrt(sum(s^2)); k <- (N - 1) / (N - R)
a95 <- acos(1 - (N - R) / R * (20^(1 / (N - 1)) - 1)) / gr
v$fisher <- c(angoli(s), N = N, R = R, k = k, a95 = a95, a95_approx = 140 / sqrt(k * N))
lat <- 42; Ig <- atan(2 * tan(lat * gr)) / gr
m <- s / R; g <- vett(0, Ig)[1, ]
psi <- acos(sum(m * g)) / gr
v$gad <- c(latitudine = lat, I_gad = Ig, distanza = psi, rotazione = ((v$fisher[['az']] + 180) %% 360) - 180)
verifica('la direzione del dipolo assiale cade fuori dal cono alfa95', psi > a95)
verifica('alfa95 esatto e approssimato concordano entro un grado', abs(a95 - 140 / sqrt(k * N)) < 1)

# 4. Stratificazione: tensore di orientazione dei poli, asse della piega, parametri di Woodcock.
st <- leggi('strati_v1.csv')
P <- vett((st$immersione + 180) %% 360, 90 - st$inclinazione)
e <- eigen(crossprod(P) / nrow(P), symmetric = TRUE)
ax <- e$vectors[, 3] * sign(e$vectors[3, 3])
v$tensore <- c(S = e$values, angoli(ax), K = log(e$values[1] / e$values[2]) / log(e$values[2] / e$values[3]),
               C = log(e$values[1] / e$values[3]))
verifica('autovalori a somma uno', abs(sum(e$values) - 1) < 1e-12)
verifica('asse stimato entro cinque gradi da 300/15', acos(abs(sum(ax * vett(300, 15)[1, ]))) / gr < 5)
verifica('distribuzione a cintura: K di Woodcock minore di 1', v$tensore[['K']] < 1)
pm_s <- colMeans(P); v$poli_R_medio <- sqrt(sum(pm_s^2))

# Figure.
# F01: rosa a settori di uguale area (raggio proporzionale alla radice della frequenza), frecce delle due medie.
cl <- cut(d$azimut, seq(0, 360, 15), right = FALSE, include.lowest = TRUE)
fq <- data.frame(c = seq(7.5, 352.5, 15), n = as.vector(table(cl)))
rmax <- sqrt(max(fq$n))
frecce <- data.frame(t = c(v$media_circolare[['dir']], v$media_aritmetica), y = 0, yend = rmax * 1.05,
                     tipo = c('Direzione media circolare', 'Media aritmetica degli azimut'))
salva('M18', 'F01', ggplot(fq) + geom_col(aes(c, sqrt(n)), width = 15, fill = '#8FC7BE', colour = paper, linewidth = .4) +
  geom_segment(data = frecce, aes(x = t, xend = t, y = y, yend = yend, colour = tipo, linetype = tipo), linewidth = 1.2,
               arrow = arrow(length = unit(3, 'mm'))) +
  scale_colour_manual(values = c(geo[2], geo[3])) + scale_linetype_manual(values = c(1, 2)) +
  scale_x_continuous(limits = c(0, 360), breaks = seq(0, 315, 45), labels = c('N', '45', 'E', '135', 'S', '225', 'O', '315')) +
  scale_y_continuous(breaks = NULL) + coord_polar(start = 0, direction = 1) + labs(x = NULL, y = NULL) +
  theme(legend.position = 'bottom', legend.direction = 'vertical', axis.text = element_text(size = 16)), w = 5.0, h = 5.2)
# F02: densità di von Mises per tre concentrazioni.
th <- seq(-180, 180, 1)
dv <- do.call(rbind, lapply(c(.5, 2, 8), function(k) data.frame(t = th, f = exp(k * cos(th * gr)) / (2 * pi * besselI(k, 0)) * gr,
                                                                  k = paste0('κ = ', fmt(k)))))
dv$k <- factor(dv$k, levels = paste0('κ = ', sapply(c(.5, 2, 8), fmt)))
salva('M18', 'F02', ggplot(dv, aes(t, f, colour = k)) + geom_line(linewidth = 1.1) + scale_colour_manual(values = geo[c(6, 1, 2)]) +
  scale_x_continuous(breaks = seq(-180, 180, 90)) + scale_y_continuous(labels = fmt) +
  labs(x = 'Scarto dalla direzione media (gradi)', y = 'Densità per grado'))
# F03: R per stazione con il valore critico del test di Rayleigh (n = 20, livello 5 %).
pr <- data.frame(stazione = rownames(per), R = per[, 'R'], sig = ifelse(per[, 'p'] < .05, 'p < 0,05', 'p ≥ 0,05'))
salva('M18', 'F03', ggplot(pr, aes(stazione, R, fill = sig)) + geom_col(width = .62) +
  geom_hline(yintercept = Rcrit, linetype = 2, colour = ink, linewidth = .7) +
  scale_fill_manual(values = c(geo[1], geo[3])) + scale_y_continuous(limits = c(0, 1), labels = fmt) +
  labs(x = 'Stazione', y = expression('Lunghezza media risultante ' * bar(R))))
# F04: rosa assiale delle fratture, ogni misura riportata alle due estremità, per famiglia.
fa <- rbind(data.frame(t = fr$direzione %% 180, f = fr$famiglia), data.frame(t = fr$direzione %% 180 + 180, f = fr$famiglia))
fa$c <- cut(fa$t, seq(0, 360, 10), right = FALSE, labels = seq(5, 355, 10))
ff <- aggregate(list(n = rep(1, nrow(fa))), list(c = fa$c, f = fa$f), sum); ff$c <- as.numeric(as.character(ff$c))
ff <- ff[order(ff$c, ff$f), ]
ff$r1 <- ave(ff$n, ff$c, FUN = function(x) sqrt(cumsum(x))); ff$r0 <- ave(ff$n, ff$c, FUN = function(x) sqrt(cumsum(x) - x))
salva('M18', 'F04', ggplot(ff) + geom_rect(aes(xmin = c - 5, xmax = c + 5, ymin = r0, ymax = r1, fill = f), colour = paper, linewidth = .3) +
  scale_fill_manual(values = geo[c(1, 2)]) +
  scale_x_continuous(limits = c(0, 360), breaks = seq(0, 315, 45), labels = c('N', '45', 'E', '135', 'S', '225', 'O', '315')) +
  scale_y_continuous(breaks = NULL) + coord_polar(start = 0, direction = 1) + labs(x = NULL, y = NULL) +
  theme(legend.position = 'right', axis.text = element_text(size = 16)), w = 5.4, h = 4.8)
# F05: proiezione equivalente delle direzioni paleomagnetiche con media, cono alfa95 e direzione del dipolo assiale.
base <- function(mm) { u <- if (abs(mm[3]) < .9) c(0, 0, 1) else c(1, 0, 0); e1 <- u - sum(u * mm) * mm; e1 <- e1 / sqrt(sum(e1^2))
  list(e1, c(mm[2] * e1[3] - mm[3] * e1[2], mm[3] * e1[1] - mm[1] * e1[3], mm[1] * e1[2] - mm[2] * e1[1])) }
b <- base(m); tt <- seq(0, 2 * pi, length.out = 181)
cono <- proietta(cos(a95 * gr) * matrix(m, 181, 3, byrow = TRUE) + sin(a95 * gr) * (outer(cos(tt), b[[1]]) + outer(sin(tt), b[[2]])))
pt <- cbind(proietta(X), tipo = 'Colate'); mp <- cbind(proietta(rbind(m)), tipo = 'Media di Fisher')
gp <- cbind(proietta(rbind(g)), tipo = 'Dipolo assiale')
# Particolare della proiezione attorno alla media, con cerchi di uguale inclinazione e linee di uguale declinazione.
grat <- rbind(do.call(rbind, lapply(c(40, 50, 60, 70, 80), function(i) cbind(proietta(vett(seq(300, 390, 1), i)), g = paste0('i', i)))),
              do.call(rbind, lapply(seq(300, 390, 15), function(az) cbind(proietta(vett(az, seq(30, 90, 1))), g = paste0('d', az)))))
et_i <- cbind(proietta(vett(rep(20, 4), c(40, 50, 60, 70))), t = paste0(c(40, 50, 60, 70), '°'))
et_d <- cbind(proietta(vett(c(330, 345, 0, 15), rep(36, 4))), t = paste0(c(330, 345, 0, 15), '°'))
salva('M18', 'F05', ggplot() + geom_path(data = grat, aes(x, y, group = g), colour = '#C9CFCD', linewidth = .35) +
  geom_text(data = et_i, aes(x, y, label = t), size = 4.2, colour = '#657180') +
  geom_text(data = et_d, aes(x, y, label = t), size = 4.2, colour = '#657180') +
  geom_path(data = cono, aes(x, y), colour = geo[2], linewidth = .8) +
  geom_point(data = pt, aes(x, y, colour = tipo, shape = tipo), size = 2.6) +
  geom_point(data = mp, aes(x, y, colour = tipo, shape = tipo), size = 3.6) +
  geom_point(data = gp, aes(x, y, colour = tipo, shape = tipo), size = 4.6, stroke = 1.2) +
  scale_colour_manual(values = c('Colate' = geo[1], 'Media di Fisher' = geo[2], 'Dipolo assiale' = geo[3])) +
  scale_shape_manual(values = c('Colate' = 16, 'Media di Fisher' = 15, 'Dipolo assiale' = 8)) +
  coord_equal(xlim = c(-.42, .2), ylim = c(.12, .66)) + theme_void(base_size = 18, base_family = 'Nimbus Sans') +
  theme(plot.background = element_rect(fill = paper, colour = NA), legend.position = 'bottom', legend.title = element_blank(),
        legend.text = element_text(size = 15), plot.margin = margin(9, 9, 9, 9)), w = 5.2, h = 4.8)
# F06: diagramma dei poli della stratificazione con il cerchio massimo meglio adattato e l'asse della piega.
hz <- c(-ax[2], ax[1], 0); hz <- hz / sqrt(sum(hz^2))
w2 <- c(ax[2] * hz[3] - ax[3] * hz[2], ax[3] * hz[1] - ax[1] * hz[3], ax[1] * hz[2] - ax[2] * hz[1]); w2 <- w2 * sign(w2[3])
gc <- proietta(outer(cos(seq(0, pi, length.out = 181)), hz) + outer(sin(seq(0, pi, length.out = 181)), w2))
pp <- cbind(proietta(P), tipo = 'Poli degli strati'); ap <- cbind(proietta(rbind(ax)), tipo = 'Asse della piega')
salva('M18', 'F06', ggplot() + rete() + geom_path(data = gc, aes(x, y), colour = geo[2], linewidth = .8) +
  geom_point(data = pp, aes(x, y, colour = tipo, shape = tipo), size = 2.2) +
  geom_point(data = ap, aes(x, y, colour = tipo, shape = tipo), size = 4.2, stroke = 1.2) +
  scale_colour_manual(values = c('Poli degli strati' = geo[1], 'Asse della piega' = geo[3])) +
  scale_shape_manual(values = c('Poli degli strati' = 16, 'Asse della piega' = 8)), w = 5.6, h = 4.4)

capture <- function(x) paste(capture.output(print(x)), collapse = '\n')
jsonlite::write_json(lapply(v, function(x) if (is.table(x) || is.matrix(x)) capture(x) else x),
                     file.path(out, 'valori.json'), auto_unbox = TRUE, pretty = TRUE, digits = 8)
str(v[c('media_aritmetica', 'media_circolare', 'varianza_circolare', 'sd_circolare', 'kappa_tutti', 'rayleigh_critico',
        'R_critico_formula', 'angolo_famiglie', 'fisher', 'gad', 'tensore', 'poli_R_medio')])
print(round(per, 4)); print(round(v$fratture, 4)); print(v$fratture_n)
