# Quote note della popolazione
W13 <- c(.3,.7)
m13 <- c(5.2,8.4) # medie campionarie
n13 <- c(20,20)   # allocazione
sum(W13*m13)      # 7.44
weighted.mean(m13,n13) # 6.80
# I pesi W descrivono la popolazione.
