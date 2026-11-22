lag_v <- drop(W%*%v)
beta_scatter <- unname(coef(
 lm(lag_v~v))[2])
stopifnot(abs(beta_scatter-I_W)
          <1e-12)
