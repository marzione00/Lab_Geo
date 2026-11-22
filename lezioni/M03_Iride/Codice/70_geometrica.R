# Misure in mm; riferimento 1 mm
l_es <- c(1,4,16)
c(aritmetica=mean(l_es),
  geometrica=l_ref*
    exp(mean(log(l_es/l_ref))))
