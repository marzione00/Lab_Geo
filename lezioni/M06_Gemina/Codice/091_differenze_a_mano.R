# Cinque coppie costruite, unita u.c.
a91 <- c(10,12,9,11,13)
b91 <- c(10.4,12.1,9.7,10.8,13.5)
d91 <- b91-a91
c(media=mean(d91), SE=sd(d91)/sqrt(5))
all.equal(mean(d91),
          mean(b91)-mean(a91))
