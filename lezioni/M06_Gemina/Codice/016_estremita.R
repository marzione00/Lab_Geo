# Oggetti della slide 15
soglia16 <- abs(obs15)
estremi16 <- abs(t15) >= soglia16
K16 <- sum(estremi16)
K16  # 66 dei 200 contrasti
sum(t15 <= -soglia16) +
  sum(t15 >= soglia16)
