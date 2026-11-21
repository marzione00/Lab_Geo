ov <- d$x_m<1000
es <- !ov
stopifnot(!any(ov & es),
          all(ov | es))
c(Ovest=sum(ov),Est=sum(es))
