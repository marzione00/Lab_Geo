# E varia piu rapidamente di N
s_rete <- expand.grid(E=1:4,N=1:4)
s_rete$valore <- rep(1:4,4)
s_mat <- matrix(s_rete$valore,4,4)
s_pal <- colorRampPalette(
  c("#F0F4F3","#087C74"))(4)
image(1:4,1:4,s_mat,col=s_pal,
      xlab="Est [km]",
      ylab="Nord [km]",asp=1)
