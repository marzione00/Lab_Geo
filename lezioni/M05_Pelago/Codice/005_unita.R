# Tre stazioni con quattro misure
d05 <- data.frame(
 stazione=rep(c("A","B","C"),each=4),
 misura=c(2.3,2.4,2.5,2.4,
          2.6,2.7,2.6,2.5,
          2.8,2.9,2.7,2.8))
G05 <- length(unique(d05$stazione))
c(righe=nrow(d05),stazioni=G05)
