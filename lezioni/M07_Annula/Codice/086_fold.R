# Cinque parti interne al solo training.
set.seed(714)
fold <- sample(rep(1:5,
  length.out = nrow(training)))
table(fold)
# Il test esterno non compare nei fold.
