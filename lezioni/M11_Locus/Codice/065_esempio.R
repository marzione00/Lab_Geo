u <- casuali$u
I_null <- sapply(1:100,function(b) {
 ii <- ((b-1)*n+1):(b*n)
 moran_I(z[order(u[ii])],A)
})
p_MC <- (1+sum(I_null>=I_A))/101
