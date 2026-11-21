# Esempio: righe in ordine diverso
p48 <- data.frame(id=c(1,2,3),
                  prima=c(10,14,8))
d48 <- data.frame(id=c(3,1,2),
                 dopo=c(7,11,16))
j48 <- merge(p48,d48,by="id")
stopifnot(!anyDuplicated(j48$id))
j48$D <- j48$dopo-j48$prima
j48  # Differenze: 1, 2, -1
