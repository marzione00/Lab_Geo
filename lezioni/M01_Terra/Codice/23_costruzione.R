n_A <- 20
set.seed(17)  # Seme iniziale del laboratorio
terra_sim <- data.frame(
  stazione = rep(c("A", "B", "C"),
                 c(n_A, 10, 10)),
  valore = c(rnorm(n_A, 3, 0.4),
             rnorm(10, 7, 0.4),
             rnorm(10, 10, 0.4))
)
table(terra_sim$stazione)
