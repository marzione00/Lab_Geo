blocco <- interaction(d$x_m>=1000,
                      d$y_m>=1000)
nb <- table(blocco)
mb <- tapply(z,blocco,mean)
c(siti=mean(z),blocchi=mean(mb))
