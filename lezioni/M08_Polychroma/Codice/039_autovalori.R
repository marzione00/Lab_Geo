lam <- pc$sdev^2
lam
sum(lam) # otto colonne di varianza 1
max(abs(lam - lambda_svd))
# Il confronto controlla la convenzione n-1.
