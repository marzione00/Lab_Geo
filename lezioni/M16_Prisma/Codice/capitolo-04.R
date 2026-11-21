gini <- function(p) 1-sum(p^2)
prima <- gini(c(.5,.5))
dopo <- gini(c(.75,.25))
c(prima=prima,dopo=dopo,riduzione=prima-dopo)
