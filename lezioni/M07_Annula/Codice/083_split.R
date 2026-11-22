# Regola fissata prima della selezione.
is_test <- seq_len(nrow(f)) %% 5L == 0L
training <- f[!is_test, ]
test <- f[is_test, ]
c(training = nrow(training),
  test = nrow(test))
stopifnot(length(intersect(training$id,
                         test$id)) == 0L)
