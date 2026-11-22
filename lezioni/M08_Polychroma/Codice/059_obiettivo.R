# Sei punti illustrativi, due gruppi.
u59 <- rbind(c(1,1), c(1.2,2.1),
 c(2.2,1.35), c(5.3,2.4),
 c(6.7,2.9), c(6,1.6))
g59 <- rep(1:2, each = 3)
cent59 <- rowsum(u59, g59) / 3
# Somma dei quadrati delle distanze.
sum((u59 - cent59[g59, ])^2)
