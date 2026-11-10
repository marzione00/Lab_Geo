tab <- matrix(c(18,12,9,21),nrow=2,byrow=TRUE,
 dimnames=list(sito=c('A','B'),
 esito=c('Presenza','Assenza')))
prop.table(tab,1)
q <- chisq.test(tab,correct=FALSE)
q$expected
q
fisher.test(tab)
