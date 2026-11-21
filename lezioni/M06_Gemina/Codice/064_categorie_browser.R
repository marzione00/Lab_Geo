# Impostazione iniziale del browser
T64 <- matrix(c(15,35,25,35),2,
              byrow=TRUE)
q64 <- chisq.test(T64,correct=FALSE)
prop.table(T64,1)
c(atteso_min=min(q64$expected),
  p_chi=q64$p.value,
  p_fisher=fisher.test(T64)$p.value)
