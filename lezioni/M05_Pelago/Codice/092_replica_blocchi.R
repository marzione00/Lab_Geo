n92 <- length(x88)
L92 <- 8
set.seed(17)
s92 <- sample.int(n92,
  ceiling(n92/L92), replace = TRUE)
j92 <- unlist(lapply(s92,
  function(s)
    ((s-1+0:(L92-1)) %% n92)+1))
mean(x88[j92[1:n92]])
