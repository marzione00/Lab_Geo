P <- outer((0:23)*30,(0:29)*30,
 function(y,x)900+0.12*x+0.08*y)
g_atteso <- sqrt(0.12^2+0.08^2)
atan(g_atteso)*180/pi
