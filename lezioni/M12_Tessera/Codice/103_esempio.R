nr <- 10000; nc <- 10000; nb <- 4
byte_valori <- nr*nc*nb*8
c(GB=byte_valori/1e9,
 GiB=byte_valori/1024^3)
