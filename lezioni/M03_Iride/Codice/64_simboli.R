# Le aree sono nel rapporto 1:4:9
s_v <- c(1,4,9)
symbols(1:3,rep(1,3),
  circles=sqrt(s_v),inches=.35,
  bg="#1D7890",fg="#1D7890",
  xlab="Posizione dimostrativa",
  ylab="",ylim=c(0,2))
