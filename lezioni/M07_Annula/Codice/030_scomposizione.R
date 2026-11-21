SST <- sum((y - mean(y))^2)
SSE <- sum(residuals(m0)^2)
SSR <- sum((fitted(m0) - mean(y))^2)
c(totale = SST, modello = SSR,
  residua = SSE)
all.equal(SST, SSR + SSE)
