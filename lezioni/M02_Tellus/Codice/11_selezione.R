# Un criterio per ogni riga
sel <- campioni$affioramento == "A"
s <- campioni[sel, ]
nrow(s)

# Ordiniamo tutta la tabella
o <- order(s$volume_cm3)
s <- s[o, ]
head(s[c("id", "volume_cm3")])
