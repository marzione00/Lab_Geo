# Famiglia prevista: tre confronti
set.seed(17)
g69 <- rep(LETTERS[1:4],each=30)
y69 <- rnorm(120,rep(0:3,each=30))
z69 <- split(y69,g69)
p69 <- sapply(z69[c("B","C","D")],
  function(z) t.test(z,z69$A)$p.value)
p.adjust(p69,method="holm")
