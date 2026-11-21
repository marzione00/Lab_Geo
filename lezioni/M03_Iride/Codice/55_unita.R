# Da micrometri a millimetri
r_mm <- r_x / 1000
c(cor(r_x,r_y), cor(r_mm,r_y))
c(cov(r_x,r_y), cov(r_mm,r_y))
# Invertire un asse cambia il segno
cor(-r_x, r_y)
