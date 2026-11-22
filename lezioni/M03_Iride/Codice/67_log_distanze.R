# Riferimento esplicito: 1 mm
l_x <- c(1,2,5,10,20,50,100)
l_ref <- 1
cbind(mm=l_x,log10=log10(l_x/l_ref))
# Due rapporti pari a 10
diff(log10(c(1,10,100)/l_ref))
