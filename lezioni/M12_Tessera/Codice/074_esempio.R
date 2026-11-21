stopifnot(all(L315>=0 & L315<=1))
L_piano <- sin(45*pi/180)
stopifnot(
 abs(L_piano-sqrt(0.5))<1e-12)
