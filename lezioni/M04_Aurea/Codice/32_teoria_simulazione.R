# 400 repliche, 20 prove ciascuna
set.seed(17)
s32 <- rbinom(400, size=20, prob=.3)
f32 <- tabulate(s32+1, nbins=21)/400
plot(0:20, dbinom(0:20,20,.3),
     type="h", xlab="k", ylab="P")
points(0:20, f32, col="orange",pch=16)
mean(s32)  # 5.9375; teoria: 6
