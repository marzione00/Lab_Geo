dist0 <- sqrt((d$x_m-750)^2+
              (d$y_m-750)^2)
raggi <- c(300,600,900)
sapply(raggi,function(r)
 sum(dist0<=r))
