set.seed(17)
a46 <- rnorm(30)
b46 <- rnorm(30, mean = 0.5, sd = 2)
tt46 <- t.test(b46, a46)
mean(b46) - mean(a46)
tt46$conf.int
tt46$p.value
