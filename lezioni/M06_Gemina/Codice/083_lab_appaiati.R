# Varia la componente individuale.
z83 <- lab_appaiati(tau=3)
w83 <- lab_appaiati(tau=5)
rbind(tau3=z83$metrics,
      tau5=w83$metrics)
all.equal(z83$differenze,
          w83$differenze)
