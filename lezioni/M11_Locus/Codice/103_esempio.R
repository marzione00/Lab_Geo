varK <- 4-2*sum(lambda*c0)+
 drop(t(lambda)%*%C%*%lambda)
stopifnot(abs(varK-
 (4-sum(lambda*c0)-sol[4]))<1e-10,
 varK>=0)
varK
