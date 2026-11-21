# A: 15 su 50; B: count su 60
z85 <- lab_categorie(count=25)
w85 <- lab_categorie(count=18)
z85$tabella
z85$attesi
rbind(B25=z85$metrics,
      B18=w85$metrics)
