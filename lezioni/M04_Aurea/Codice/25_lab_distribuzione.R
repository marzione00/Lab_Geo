a25 <- lab_distribuzione(cut=1)
a25$indicatori
# Probabilita' esatte della normale
pnorm(1)              # circa .8413
pnorm(1, lower.tail=FALSE)
b25 <- lab_distribuzione(cut=0)
b25$indicatori        # .5 e .5
