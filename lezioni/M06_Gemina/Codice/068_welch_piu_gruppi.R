r68 <- read.csv(
  "Dati/rocce_simulate.csv")
# Densita nelle litologie simulate
q68 <- oneway.test(
  densita~litologia_generatrice,
  data=r68,var.equal=FALSE)
q68
tapply(r68$densita,
       r68$litologia_generatrice,sd)
