# Il primo argomento definisce B - A.
tt42 <- t.test(b37, a37,
  mu = 0, alternative = "two.sided",
  var.equal = FALSE, conf.level = 0.95)
tt42$estimate
tt42$conf.int
tt42$p.value
