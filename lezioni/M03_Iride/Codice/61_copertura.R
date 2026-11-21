# Posizioni deterministiche in metri
s_est <- seq(0,100,length.out=30)
s_nord <- 50 + 5*sin(s_est/8)
plot(s_est,s_nord,pch=16,asp=1,
     xlim=c(0,100),ylim=c(0,100),
     xlab="Est [m]",ylab="Nord [m]")
