# Livelli espliciti anche se un conteggio e' 0.
tab78 <- table(
  osservato = factor(f$spiky, levels = 0:1),
  previsto = factor(classe77, levels = 0:1))
tab78
sum(diag(tab78)) / sum(tab78)
