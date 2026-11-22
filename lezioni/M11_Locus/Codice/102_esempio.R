lambda <- sol[1:3]
z_toy <- c(10,15,12)
c(lambda,previsione=sum(lambda*z_toy))
stopifnot(any(lambda<0))
