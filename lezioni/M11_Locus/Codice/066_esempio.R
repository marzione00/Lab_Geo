set.seed(20261109)
I_999 <- replicate(999,
 moran_I(sample(z),A))
c(p_100=p_MC,
 p_999=(1+sum(I_999>=I_A))/1000)
