v <- z-mean(z)
I_A <- n/sum(A)*sum(A*outer(v,v))/
       sum(v^2)
I_W <- drop(t(v)%*%W%*%v)/sum(v^2)
c(binaria=I_A,riga=I_W)
