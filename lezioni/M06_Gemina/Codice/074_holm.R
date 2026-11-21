p74 <- c(.003,.018,.041,.2)
adj74 <- p.adjust(p74,method="holm")
# Calcolo sui p-value gia ordinati
manuale74 <- pmin(1,cummax(4:1*p74))
stopifnot(isTRUE(all.equal(
  adj74,manuale74)))
data.frame(p74,adj74,rifiuto=adj74<=.05)
