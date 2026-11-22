# Base didattica: 40 g MgO, 10 g FeO
mgo <- 40
feo <- 10
rapporto_massa <- mgo / (mgo + feo)
a_mg <- mgo / 40.304
b_fe <- feo / 71.844
rapporto_moli <- a_mg / (a_mg + b_fe)
c(massa = rapporto_massa,
  molare = rapporto_moli)
