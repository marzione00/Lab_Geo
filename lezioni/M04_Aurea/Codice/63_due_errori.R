set.seed(17)
B63 <- 2000
y63 <- rlnorm(B63, 0, .6)
s63 <- sd(y63)
c(SD_uscita = s63,
  SE_media_MC = s63/sqrt(B63))
