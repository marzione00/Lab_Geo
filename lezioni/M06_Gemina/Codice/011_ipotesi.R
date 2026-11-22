# Domanda fissata prima dei dati:
# H0: media_B-media_A = 0.
a11 <- c(3, 4, 6, 7, 9)
b11 <- c(4, 6, 7, 8, 10)
t.test(b11, a11, mu=0,
       alternative="two.sided")
# "greater" richiede H1: Delta>0.
