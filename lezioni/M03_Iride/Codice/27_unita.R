# Da millimetri a micrometri
y_um <- 1000 * x_disp
sd(y_um)                    # 1000
var(y_um)                   # 1e6
# Traslazione nella stessa unita
sd(x_disp + 20)             # 1
