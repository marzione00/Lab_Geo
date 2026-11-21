# Lista incompleta: esempio costruito
u16 <- data.frame(
 valore=c(4,5,5,6,8,9,10,11),
 accessibile=c(rep(TRUE,4),
               rep(FALSE,4)))
mean(u16$valore)
mean(u16$valore[u16$accessibile])
