# Simplex (M17): figure e valori della lezione sui dati composizionali.
# Uso: Rscript R/M17_figure.R dalla cartella della lezione. Scrive figure/M17 e risultati/M17.
# Codice: PolyForm Noncommercial 1.0.0. Required Notice: Copyright 2026 Marzio De Corato.
source('R/stile.R')
out <- 'risultati/M17'; dir.create(out, recursive = TRUE, showWarnings = FALSE)
d <- leggi('composizioni_v1.csv')
parti <- c('SiO2', 'Al2O3', 'CaO', 'MgO', 'FeO', 'Altro')
X <- as.matrix(d[parti]); lit <- d$litologia; classi <- c('Arenaria', 'Basalto', 'Calcare')
chiudi <- function(x, k = 100) k * x / rowSums(x)
clr <- function(x) log(x) - rowMeans(log(x))
g <- function(x) exp(mean(log(x)))
centro <- function(x) { m <- exp(colMeans(log(x))); 100 * m / sum(m) }
bilancio <- function(x, num, den) {
  r <- length(num); s <- length(den)
  sqrt(r * s / (r + s)) * log(apply(x[, num, drop = FALSE], 1, g) / apply(x[, den, drop = FALSE], 1, g))
}
v <- list()

# 1. Chiusura e somma costante.
zeri <- rowSums(X == 0) > 0
verifica('somma 100 per le righe senza valori sotto il limite', max(abs(rowSums(X[!zeri, ]) - 100)) < .02)
verifica('quindici righe con una parte sotto il limite', sum(zeri) == 15)
v$righe <- nrow(X); v$zeri <- sum(zeri)
v$zeri_tabella <- table(lit[zeri], d$sotto_limite[zeri])
v$cor_si_ca <- cor(X[, 'SiO2'], X[, 'CaO'])
v$cor_si_ca_lit <- sapply(classi, function(k) cor(X[lit == k, 'SiO2'], X[lit == k, 'CaO']))
C <- cov(chiudi(X[!zeri, ]))
verifica('identità di Chayes: le covarianze di riga sommano a zero', max(abs(rowSums(C))) < 1e-8)
v$chayes_si <- c(var = C['SiO2', 'SiO2'], somma_altre = sum(C['SiO2', -1]))

# 2. Sottocomposizioni: correlazioni incoerenti, log-rapporti invarianti (Basalto).
b <- lit == 'Basalto'
sub <- chiudi(X[b, c('CaO', 'MgO', 'FeO')])
v$cor_mg_fe_intera <- cor(X[b, 'MgO'], X[b, 'FeO'])
v$cor_mg_fe_sotto <- cor(sub[, 'MgO'], sub[, 'FeO'])
v$var_lr_intera <- var(log(X[b, 'MgO'] / X[b, 'FeO']))
v$var_lr_sotto <- var(log(sub[, 'MgO'] / sub[, 'FeO']))
verifica('il log-rapporto non cambia nella sottocomposizione', abs(v$var_lr_intera - v$var_lr_sotto) < 1e-12)

# 3. Sostituzione moltiplicativa degli zeri (limite 0,1; delta = 0,65 del limite).
sostituisci <- function(x, delta) {
  z <- x == 0
  t(apply(cbind(x, z), 1, function(r) {
    y <- r[1:6]; zz <- as.logical(r[7:12])
    if (!any(zz)) return(y)
    y[zz] <- delta; y[!zz] <- y[!zz] * (100 - sum(y[zz])) / sum(y[!zz]); y
  }))
}
Y <- sostituisci(X, .065); colnames(Y) <- parti
verifica('dopo la sostituzione tutte le parti sono positive e la somma resta 100', all(Y > 0) && max(abs(rowSums(Y) - 100)) < .02)
nz <- which(zeri)[1]
v$rapporto_prima <- X[nz, 'SiO2'] / X[nz, 'Al2O3']; v$rapporto_dopo <- Y[nz, 'SiO2'] / Y[nz, 'Al2O3']
verifica('la sostituzione conserva i rapporti fra le parti presenti', abs(v$rapporto_prima - v$rapporto_dopo) < 1e-12)

# 4. clr, centri, matrice di variazione, biplot.
Z <- clr(Y)
verifica('le coordinate clr sommano a zero', max(abs(rowSums(Z))) < 1e-12)
v$centri <- t(sapply(classi, function(k) round(rbind(aritmetico = colMeans(Y[lit == k, ]), geometrico = centro(Y[lit == k, ]))[, c('MgO', 'FeO')], 3)))
v$centro_arenaria <- rbind(aritmetico = colMeans(Y[lit == 'Arenaria', ]), geometrico = centro(Y[lit == 'Arenaria', ]))
V <- outer(1:6, 1:6, Vectorize(function(a, b) var(log(Y[, a] / Y[, b])))); dimnames(V) <- list(parti, parti)
v$variazione <- V
v$variazione_totale <- sum(V) / (2 * 6)
verifica('variazione totale uguale alla traccia della covarianza clr', abs(v$variazione_totale - sum(diag(cov(Z)))) < 1e-10)
pc <- prcomp(Z)
v$pca_quota <- summary(pc)$importance[2, 1:3]

# 5. Bilanci e regressione della densità.
B <- cbind(b1 = bilancio(Y, c('CaO', 'Altro'), c('SiO2', 'Al2O3', 'MgO', 'FeO')),
           b2 = bilancio(Y, 'CaO', 'Altro'),
           b3 = bilancio(Y, c('SiO2', 'Al2O3'), c('MgO', 'FeO')),
           b4 = bilancio(Y, 'SiO2', 'Al2O3'),
           b5 = bilancio(Y, 'MgO', 'FeO'))
verifica('i bilanci sono coordinate ortonormali (stessa distanza di Aitchison)',
         abs(sum(dist(B)^2) - sum(dist(Z)^2)) < 1e-6)
m_bil <- lm(d$densita ~ B); m_ar <- lm(d$densita ~ Y[, 1:5])
v$r2_bilanci <- summary(m_bil)$r.squared; v$r2_percentuali <- summary(m_ar)$r.squared
v$coef_b3 <- coef(m_bil)['Bb3']

# 6. Distanze: stessa differenza assoluta, effetti diversi.
a1 <- c(50, 20, 15, .1, 9.9, 5); a2 <- a1; a2[4] <- .2; a2[1] <- 49.9
c1 <- c(50, 20, 15, 5, 5, 5); c2 <- c1; c2[1] <- 50.1; c2[2] <- 19.9
ait <- function(p, q) sqrt(sum((clr(rbind(p))[1, ] - clr(rbind(q))[1, ])^2))
v$dist <- c(eu_traccia = sqrt(sum((a1 - a2)^2)), ait_traccia = ait(a1, a2),
            eu_maggiore = sqrt(sum((c1 - c2)^2)), ait_maggiore = ait(c1, c2))

# 7. Sensibilità del centro clr di MgO (Arenaria) al valore sostitutivo.
deltas <- c(.01, .025, .05, .065, .08, .1)
sens <- data.frame(delta = deltas, clr_mg = sapply(deltas, function(dl) mean(clr(sostituisci(X, dl))[lit == 'Arenaria', 4])))
v$sensibilita <- sens
oss <- lit == 'Arenaria' & !zeri
v$clr_mg_osservati <- mean(clr(X[oss, ])[, 4])

# Figure.
tern <- function(a, b, c) { s <- a + b + c; data.frame(x = (b / s) + (c / s) / 2, y = (c / s) * sqrt(3) / 2) }
tt <- cbind(tern(Y[, 'SiO2'], Y[, 'CaO'], Y[, 'MgO'] + Y[, 'FeO']), classe = lit)
tri <- data.frame(x = c(0, 1, .5, 0), y = c(0, 0, sqrt(3) / 2, 0))
etich <- data.frame(x = c(-.02, 1.02, .5), y = c(-.06, -.06, sqrt(3) / 2 + .05), t = c('SiO[2]', 'CaO', 'MgO+FeO'))
salva('M17', 'F01', ggplot() + geom_path(data = tri, aes(x, y), colour = ink, linewidth = .5) +
  geom_point(data = tt, aes(x, y, colour = classe), size = 1.8, alpha = .8) +
  geom_text(data = etich, aes(x, y, label = t), size = 6, colour = ink, parse = TRUE) + scale_colour_manual(values = geo[1:3]) +
  coord_equal(clip = 'off') + theme_void(base_size = 18, base_family = 'Nimbus Sans') +
  theme(plot.background = element_rect(fill = paper, colour = NA), legend.position = 'top', legend.title = element_blank(),
        legend.text = element_text(size = 17), plot.margin = margin(9, 20, 18, 20)))
set.seed(17)
W <- matrix(rlnorm(3 * 300, 0, .5), ncol = 3); Wc <- chiudi(W)
v$spuria <- c(grezze = cor(W[, 1], W[, 2]), chiuse = cor(Wc[, 1], Wc[, 2]))
salva('M17', 'F02', ggplot(data.frame(x = Wc[, 1], y = Wc[, 2]), aes(x, y)) + geom_point(colour = geo[1], alpha = .6, size = 1.6) +
  labs(x = 'Parte 1 dopo la chiusura (%)', y = 'Parte 2 (%)'))
salva('M17', 'F03', ggplot(data.frame(b3 = B[, 'b3'], rho = d$densita, classe = lit), aes(b3, rho, colour = classe)) +
  geom_point(size = 1.8, alpha = .8) + scale_colour_manual(values = geo[1:3]) +
  labs(x = expression('Bilancio silicati/femici ' * b[3]), y = expression('Densità (g/cm'^3 * ')')))
vl <- data.frame(expand.grid(r = parti, c = parti), val = as.vector(V)); vl$r <- factor(vl$r, levels = rev(parti))
nomi <- parse(text = c('SiO[2]', 'Al[2]*O[3]', 'CaO', 'MgO', 'FeO', 'Altro'))
nomit <- c('SiO[2]', 'Al[2]*O[3]', 'CaO', 'MgO', 'FeO', 'Altro')
salva('M17', 'F04', ggplot(vl, aes(c, r, fill = val)) + geom_tile(colour = paper, linewidth = .6) +
  geom_text(aes(label = fmt(round(val, 2))), size = 4.2, colour = ink) +
  scale_fill_gradient(low = paper, high = '#8FC7BE', guide = 'none') + scale_x_discrete(labels = nomi) +
  scale_y_discrete(labels = rev(nomi)) + labs(x = NULL, y = NULL) + theme(axis.text = element_text(size = 15)), w = 5.4, h = 4.2)
# Biplot di covarianza: punteggi standardizzati, raggi moltiplicati per le deviazioni standard delle componenti;
# la distanza fra le punte di due raggi approssima la deviazione standard del log-rapporto.
sc <- data.frame(sweep(pc$x[, 1:2], 2, pc$sdev[1:2], '/'), classe = lit)
G <- sweep(pc$rotation[, 1:2], 2, pc$sdev[1:2], '*'); ld <- data.frame(G, parte = nomit)
v$link <- c(CaO_FeO = sqrt(sum((G['CaO', ] - G['FeO', ])^2)), sd_CaO_FeO = sqrt(V['CaO', 'FeO']),
            SiO2_Al2O3 = sqrt(sum((G['SiO2', ] - G['Al2O3', ])^2)), sd_SiO2_Al2O3 = sqrt(V['SiO2', 'Al2O3']))
salva('M17', 'F05', ggplot(sc, aes(PC1, PC2)) + geom_point(aes(colour = classe), size = 1.6, alpha = .7) +
  geom_segment(data = ld, aes(x = 0, y = 0, xend = PC1, yend = PC2), colour = ink, linewidth = .5,
               arrow = arrow(length = unit(2, 'mm'))) +
  geom_label(data = ld, aes(PC1 * 1.16, PC2 * 1.16, label = parte), colour = ink, fill = paper, label.size = 0, size = 5, parse = TRUE) +
  scale_colour_manual(values = geo[1:3]) + coord_equal(clip = 'off') + labs(x = 'Prima componente clr', y = 'Seconda'))
salva('M17', 'F06', ggplot(sens, aes(delta, clr_mg)) + geom_line(colour = geo[1], linewidth = 1) +
  geom_point(colour = geo[1], size = 2.4) + geom_hline(yintercept = v$clr_mg_osservati, colour = geo[3], linetype = 2) +
  scale_x_continuous(labels = fmt) + scale_y_continuous(labels = fmt) +
  labs(x = expression('Valore sostitutivo ' * delta * ' (% in massa)'), y = 'clr medio di MgO'))

capture <- function(x) paste(capture.output(print(x)), collapse = '\n')
jsonlite::write_json(lapply(v, function(x) if (is.table(x) || is.matrix(x)) capture(x) else x),
                     file.path(out, 'valori.json'), auto_unbox = TRUE, pretty = TRUE, digits = 8)
str(v[c('cor_si_ca', 'cor_si_ca_lit', 'chayes_si', 'cor_mg_fe_intera', 'cor_mg_fe_sotto', 'var_lr_intera', 'rapporto_prima',
        'variazione_totale', 'pca_quota', 'link', 'r2_bilanci', 'r2_percentuali', 'coef_b3', 'dist', 'clr_mg_osservati', 'spuria')])
print(v$centri); print(v$centro_arenaria); print(round(V, 3)); print(sens)
