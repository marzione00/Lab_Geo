# Confronto senza nomi dei gruppi.
A91 <- outer(km$cluster,
              km$cluster,"==")
B91 <- outer(ward,ward,"==")
sopra91 <- upper.tri(A91)
mean(A91[sopra91]==B91[sopra91])
# Confronto non sensibile ai nomi.
all(A91==B91)
