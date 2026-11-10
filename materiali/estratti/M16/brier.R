d <- read.csv('dati/ml_v3.csv')
tr <- d$split=='train'
mu <- mean(d$densita[tr]); s <- sd(d$densita[tr])
z <- (d$densita-mu)/s
y <- as.integer(d$litologia=='Basalto')
f <- glm(y~z,data=data.frame(y=y[tr],z=z[tr]),
 family=binomial())
p <- predict(f,data.frame(z=z[!tr]),
 type='response')
bs <- mean((p-y[!tr])^2)
stopifnot(abs(bs-0.04285672213432)<1e-10)
bs
