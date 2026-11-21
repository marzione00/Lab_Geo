q13 <- quantile(x_q, c(.25, .75),
                type = 7)
diff(q13)                   # 5.75
IQR(x_q, type = 7)          # 5.75
# La mediana e' 7.5 mm
median(x_q)
