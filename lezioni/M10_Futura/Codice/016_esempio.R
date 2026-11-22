yy <- as.numeric(train)
delta <- (tail(yy,1)-yy[1])/
         (length(yy)-1)
p_deriva <- tail(yy,1)+(1:36)*delta
