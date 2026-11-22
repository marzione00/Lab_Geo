# Parabola simmetrica, senza rumore
r_u <- seq(-2, 2, by=.5)
r_v <- r_u^2
round(c(cor(r_u,r_v),
  cor(r_u,r_v,method="spearman")),8)
plot(r_u, r_v, pch=16,
     xlab="x", ylab="y = x^2")
