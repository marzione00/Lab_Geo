# Contributi delle due varianze stimate
va38 <- var(a37) / length(a37)
vb38 <- var(b37) / length(b37)
se38 <- sqrt(va38 + vb38)
c(A = va38, B = vb38, SE = se38)
