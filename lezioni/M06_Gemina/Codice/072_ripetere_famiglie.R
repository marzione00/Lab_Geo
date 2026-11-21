set.seed(17)
v72 <- replicate(2000, {
  p72 <- runif(20) # Ipotesi nulle
  h72 <- p.adjust(p72,"holm")
  c(grezzi=any(p72<.05),
    Holm=any(h72<.05))
})
rowMeans(v72) # Quote di famiglie
# 2000 famiglie, 20 test per famiglia
