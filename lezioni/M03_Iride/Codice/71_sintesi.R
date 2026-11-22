# Riferimento delle misure: 1 mm
l_a <- c(1,4,16)
l_b <- c(7,7,7)
l_medie <- function(v) {
  c(aritmetica=mean(v),
    geometrica=exp(mean(log(v/1))))
}
rbind(A=l_medie(l_a),B=l_medie(l_b))
