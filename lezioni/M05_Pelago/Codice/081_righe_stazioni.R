set.seed(17)
br81 <- replicate(2000,
  mean(sample(provini$densita,
              replace = TRUE)))
set.seed(17)
bs81 <- replicate(2000,
  mean(sample(stazioni$densita,
              replace = TRUE)))
c(righe = sd(br81), siti = sd(bs81))
