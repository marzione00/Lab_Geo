# Generatore iniziale: quattro gruppi
set.seed(17); n65 <- 30
g65 <- factor(rep(LETTERS[1:4],
                  each=n65))
mu65 <- rep((0:3)*.5,each=n65)
s65 <- rep(seq(1,2,length.out=4),
            each=n65)
y65 <- rnorm(4*n65,mu65,s65)
tapply(y65,g65,mean)
