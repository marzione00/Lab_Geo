# Esempio deterministico positivo
r_a <- c(1, 2, 2, 5, 8)
r_b <- r_a^2
rank(r_a)
cor(r_a, r_b)
cor(r_a, r_b, method="spearman")
cor(rank(r_a), rank(r_b))
