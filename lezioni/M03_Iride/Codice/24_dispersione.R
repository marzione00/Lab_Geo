# Esempi costruiti: misure in mm
x_disp <- c(4, 5, 6)
y_disp <- c(0, 5, 10)
rbind(A = c(media = mean(x_disp),
            sd = sd(x_disp)),
      B = c(media = mean(y_disp),
            sd = sd(y_disp)))
