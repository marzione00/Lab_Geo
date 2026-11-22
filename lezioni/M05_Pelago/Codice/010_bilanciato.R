# Riprendiamo i gruppi di slide 5.
m10 <- tapply(d05$misura,
  d05$stazione,mean)
c(righe=mean(d05$misura),
  stazioni=mean(m10))
table(d05$stazione)  # 4,4,4
# L'uguaglianza deriva dai pesi.
