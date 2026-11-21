# Colonne scelte nella slide 43
diametri <- fossili[due]
completi <- complete.cases(diametri)
finiti <- Reduce(`&`,
  lapply(diametri, is.finite))
table(completi, finiti)
