# Ordine della scala di alterazione
livelli <- c("bassa", "media", "alta")
grado <- factor(campioni$alterazione,
  levels = livelli, ordered = TRUE)
table(grado)

# Date di un esempio separato
giorni <- as.Date(c("2024-02-28",
                    "2024-03-01"))
diff(giorni)        # Due giorni
