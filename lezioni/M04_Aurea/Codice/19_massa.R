k19 <- 0:2
p19 <- c(.49, .42, .09)
sum(p19)             # 1
sum(p19[k19 >= 1])    # .51
sum(k19 * p19)        # atteso .6
barplot(p19, names.arg=k19,
  xlab="Successi", ylab="Probabilita'")
