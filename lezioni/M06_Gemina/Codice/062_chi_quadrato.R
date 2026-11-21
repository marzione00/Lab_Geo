O62 <- matrix(c(18,12,9,21),2,
              byrow=TRUE)
q62 <- chisq.test(O62,correct=FALSE)
C62 <- (O62-q62$expected)^2/
        q62$expected
C62  # Contributi delle quattro celle
c(X2=sum(C62),p=q62$p.value)
