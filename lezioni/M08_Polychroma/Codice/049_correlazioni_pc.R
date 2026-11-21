cor_PC <- sweep(pc$rotation, 2,
                pc$sdev, "*")
round(cor_PC[, 1:2], 3)
max(abs(cor_PC - cor(Z, pc$x)))
