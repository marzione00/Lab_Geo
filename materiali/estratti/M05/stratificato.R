set.seed(314)
b_strat <- replicate(B,.5*mean(sample(x,80,TRUE))+.5*mean(sample(y,80,TRUE)))
