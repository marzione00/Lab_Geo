# t e df sono assegnati direttamente.
z80 <- lab_pvalue(t=2,df=20)
w80 <- lab_pvalue(t=2,df=5)
rbind(df20=z80$metrics,
      df5=w80$metrics)
2*pt(-abs(2), df=20)
