coinvolte <- coppie$i==1L | coppie$j==1L
data.frame(coppie_con_S01=sum(coinvolte),coppie_restanti=sum(!coinvolte),
  attese_dopo_rimozione=choose(63,2))
table(coppie$classe[coinvolte])
stopifnot(sum(coinvolte)==63L,sum(!coinvolte)==choose(63,2))
