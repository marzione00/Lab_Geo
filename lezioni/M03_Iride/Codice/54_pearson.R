# Due deviazioni standard positive
stopifnot(sd(r_x)>0, sd(r_y)>0)
r_p <- cor(r_x, r_y)
r_formula <- r_cov /
  (sd(r_x) * sd(r_y))
c(Pearson = r_p, formula = r_formula)
all.equal(r_p, r_formula)
