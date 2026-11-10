x <- (0:29)*30; y <- (0:23)*30
Z <- outer(y,x,function(y,x)
 900+.12*x+.08*y)
gx <- (Z[2:23,3:30]-Z[2:23,1:28])/60
gy <- (Z[3:24,2:29]-Z[1:22,2:29])/60
stopifnot(max(abs(gx-.12)) < 1e-12,
 max(abs(gy-.08)) < 1e-12)
atan(sqrt(.12^2+.08^2))*180/pi
