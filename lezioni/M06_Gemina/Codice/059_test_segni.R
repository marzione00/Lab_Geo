D59 <- c(1,-2,3,-4,2,0,1)
z59 <- D59[D59!=0]
k59 <- sum(z59>0); n59 <- length(z59)
# Tra i cambiamenti non nulli
binom.test(k59,n59,p=.5)
# Si usano soltanto i segni;
# le ampiezze non entrano nel test.
