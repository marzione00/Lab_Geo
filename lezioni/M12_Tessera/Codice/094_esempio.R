okZ <- with(d,!(riga %in% 4:7 &
                 colonna %in% 9:14))
table(d$unita[okZ])/table(d$unita)
