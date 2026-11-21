tp <- 0; fn <- 10; tn <- 90; fp <- 0
c(accuracy=(tp+tn)/(tp+tn+fp+fn),
  bilanciata=mean(c(tp/(tp+fn),tn/(tn+fp))))
