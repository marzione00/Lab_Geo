O61 <- matrix(c(18,12,9,21),2,
              byrow=TRUE)
E61 <- outer(rowSums(O61),
             colSums(O61))/sum(O61)
E61  # 13.5 e 16.5 per riga
chisq.test(O61,correct=FALSE)$expected
