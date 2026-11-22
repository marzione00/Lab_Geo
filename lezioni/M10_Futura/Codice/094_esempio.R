v <- processi[1:250,
  c("x_VAR","y_VAR")]
varfit <- stima_VAR1(v)
varfit$A
