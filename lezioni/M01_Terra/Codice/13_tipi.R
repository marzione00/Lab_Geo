# Le stazioni sono categorie
g <- factor(c("A", "A", "B", "C"))
levels(g)
table(g)  # Frequenze per categoria

# Le concentrazioni sono numeriche
x <- c(2.9, 3.2, 7.1, 10.0)
is.numeric(x)
