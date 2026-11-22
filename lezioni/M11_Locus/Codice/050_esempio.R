A_200 <- 1*(D>0 & D<=200)
isolati <- rowSums(A_200)==0
stopifnot(sum(isolati)==64L)
sum(isolati)
