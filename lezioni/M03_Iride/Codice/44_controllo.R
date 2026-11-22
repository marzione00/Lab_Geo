check_b <- data.frame(
  id = paste0("P", seq_along(x_b)),
  valore = x_b)
check_b$oltre <- x_b %in% bx$out
# Selezione per ispezione
check_b[check_b$oltre, ]
