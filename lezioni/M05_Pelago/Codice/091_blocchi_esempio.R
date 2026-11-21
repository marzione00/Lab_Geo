n91 <- 8
L91 <- 3
inizi91 <- c(7, 3, 5)
j91 <- unlist(lapply(inizi91,
  function(s)
    ((s-1+0:(L91-1)) %% n91)+1))
j91             # 9 indici
j91[1:n91]      # Troncamento a 8
