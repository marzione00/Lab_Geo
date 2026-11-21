n48 <- 20
q48 <- qt(.975, df = n48-1)
q48  # Circa 2.093
# Area centrale della Student
pt(q48, n48-1) - pt(-q48, n48-1)
