A <- 315*pi/180; h <- 45*pi/180
luce <- c(cos(h)*sin(A),
 cos(h)*cos(A),sin(h))
L315 <- pmax((-gx*luce[1]-gy*luce[2]+
 luce[3])/sqrt(1+gx^2+gy^2),0)
stopifnot(identical(dim(L315),dim(gx)))
