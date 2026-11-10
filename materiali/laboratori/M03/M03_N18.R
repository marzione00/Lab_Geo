# Facoltativo: costruire una figura con ggplot2
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Questo blocco prepara soltanto percorsi, funzioni di servizio e riproducibilità.
# Non scarica dati, non installa pacchetti, non elimina oggetti e non modifica i CSV.
trova_radice <- function() {
  p <- normalizePath(getwd(), winslash = "/", mustWork = TRUE)
  repeat {
    if (file.exists(file.path(p, "Notebook_R_Geologia.Rproj"))) return(p)
    genitore <- dirname(p)
    if (identical(p, genitore)) stop("Aprire Notebook_R_Geologia.Rproj e riprovare.")
    p <- genitore
  }
}
root <- trova_radice()
source(file.path(root, "R", "funzioni_comuni.R"), local = TRUE)
ctx <- inizia_notebook("M03_N18")
set.seed(1006)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Preparazione: Dati e domanda prima del tipo di grafico
f <- leggi_dati("fossili_simulati.csv")
r <- leggi_dati("rocce_simulate.csv")
f$morfotipo <- factor(f$morfotipo, levels = c("Rounded", "Spiky"))
stopifnot(all(is.finite(f$diametro_tot_um)), all(r$grana_mm > 0))
x <- f$diametro_tot_um
table(f$morfotipo)


# Preparazione: Istogramma: il ruolo delle classi
stile_grafico()
hist(x, breaks = 8, col = palette_geo[1], border = "white",
     xlab = "Diametro totale (micrometri)", ylab = "Numero di individui",
     main = "Istogramma: richiesta di circa 8 classi")
stile_grafico()
hist(x, breaks = 25, col = palette_geo[2], border = "white",
     xlab = "Diametro totale (micrometri)", ylab = "Numero di individui",
     main = "Stessi 160 individui: più classi")


# Preparazione: Densità e area: non confondere altezza e frequenza
stile_grafico()
hist(x, breaks = 15, probability = TRUE, col = "grey90", border = "white",
     xlab = "Diametro totale (micrometri)", ylab = "Densità (1/micrometro)",
     main = "Istogramma normalizzato e densità stimata")
lines(density(x), col = palette_geo[1], lwd = 2)
# Controlliamo l'area dell'istogramma normalizzato.
h <- hist(x, breaks = 15, plot = FALSE)
sum(h$density * diff(h$breaks))


# Preparazione: Boxplot con punti: centro, dispersione e numerosità
set.seed(306)
stile_grafico()
boxplot(diametro_tot_um ~ morfotipo, f, outline = FALSE,
        col = c("grey92", "grey85"),
        xlab = "Morfotipo (80 individui ciascuno)", ylab = "Diametro totale (micrometri)",
        main = "Distribuzioni e osservazioni individuali")
stripchart(diametro_tot_um ~ morfotipo, f, vertical = TRUE,
           method = "jitter", jitter = .16, add = TRUE,
           pch = 19, cex = .5, col = palette_geo[1:2])


# Preparazione: La distribuzione cumulativa empirica
g <- split(f$diametro_tot_um, f$morfotipo)
F_round <- ecdf(g$Rounded)
F_spiky <- ecdf(g$Spiky)
data.frame(morfotipo = c("Rounded", "Spiky"),
           frazione_fino_a_6 = c(F_round(6), F_spiky(6)))
stile_grafico()
plot(F_round, xlim = range(x), verticals = TRUE, do.points = FALSE,
     col = palette_geo[1], xlab = "Diametro totale (micrometri)",
     ylab = "Frazione cumulativa", main = "ECDF per morfotipo")
lines(F_spiky, verticals = TRUE, do.points = FALSE, col = palette_geo[2])
legend("bottomright", c("Rounded", "Spiky"), col = palette_geo[1:2], lty = 1, bty = "n")


# Preparazione: Scatterplot: due misure dello stesso individuo
colore <- palette_geo[as.integer(f$morfotipo)]
simbolo <- c(16, 17)[as.integer(f$morfotipo)]
stile_grafico()
plot(f$diametro_tot_um, f$diametro_int_um, pch = simbolo,
     col = adjustcolor(colore, alpha.f = .65),
     xlab = "Diametro totale (micrometri)", ylab = "Diametro interno (micrometri)",
     main = "Relazione geometrica: dati simulati")
abline(0, 1, lty = 2)
legend("topleft", levels(f$morfotipo), col = palette_geo[1:2],
       pch = c(16,17), bty = "n")


# Preparazione: Trasformazione logaritmica e standardizzazione
grana <- r$grana_mm
log_grana <- log(grana)
z_grana <- as.numeric(scale(grana))
data.frame(variabile = c("grana_mm", "log_grana", "z_grana"),
           media = c(mean(grana), mean(log_grana), mean(z_grana)),
           sd = c(sd(grana), sd(log_grana), sd(z_grana)))
stile_grafico()
hist(log_grana, breaks = 15, col = palette_geo[1],
     xlab = "log(grana / 1 mm)", ylab = "Frequenza",
     main = "Trasformazione delle differenze relative")
stopifnot(abs(mean(z_grana)) < 1e-10, abs(sd(z_grana)-1) < 1e-10)


# Analisi principale: Facoltativo: costruire una figura con ggplot2
if (requireNamespace("ggplot2", quietly = TRUE)) {
  p <- ggplot2::ggplot(f, ggplot2::aes(x = morfotipo, y = diametro_tot_um)) +
    ggplot2::geom_boxplot(outlier.shape = NA, fill = "grey92") +
    ggplot2::geom_jitter(width = .15, height = 0, alpha = .5,
                         color = palette_geo[1]) +
    ggplot2::labs(title = "Diametro totale per morfotipo",
                  subtitle = "160 individui simulati; quote fissate 80/80",
                  x = "Morfotipo", y = "Diametro (micrometri)") +
    ggplot2::theme_minimal(base_size = 12)
  print(p)
  ggplot2::ggsave(file.path(ctx$out, "confronto_ggplot.png"), p,
                  width = 8, height = 5, dpi = 160)
} else {
  message("Figura ggplot2 non prodotta: pacchetto facoltativo assente.")
}
