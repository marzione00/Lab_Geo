riassumi_f <- function(v) {
  c(n = length(v), media = mean(v),
    mediana = median(v), sd = sd(v),
    IQR = IQR(v, type = 7))
}
# gr_f e' la lista della slide 48
round(t(sapply(gr_f, riassumi_f)), 3)
