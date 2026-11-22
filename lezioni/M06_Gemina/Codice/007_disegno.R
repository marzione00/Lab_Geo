# Esempio di misure ripetute
d07 <- data.frame(
  provino=rep(1:4, each=2),
  tempo=rep(c("prima","dopo"),4))
nrow(d07)                  # 8 righe
length(unique(d07$provino)) # 4 coppie
table(d07$provino, d07$tempo)
