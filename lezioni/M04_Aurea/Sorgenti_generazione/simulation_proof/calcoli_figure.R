# Aurea M04: coordinate delle figure 50-76.
# Eseguire nella cartella di questo file. Solo R base.
dir.create("coordinate", showWarnings = FALSE)
write_xy <- function(name, x, y) {
  write.csv(data.frame(x=x,y=y),
    file.path("coordinate", paste0(name, ".csv")), row.names=FALSE)
}
# Frequenza progressiva dell'evento Bernoulli: stesso codice di slide 60.
set.seed(17)
b <- 2000
z <- rbinom(b, 1, .1)
k <- seq_len(b)
write_xy("mc_progressivo", k, cumsum(z)/k)
# Densita' fisica: medie e SD degli ingressi in g e cm^3.
rpos <- function(n, mu, s) {
  v <- log1p((s/mu)^2)
  rlnorm(n, log(mu)-v/2, sqrt(v))
}
set.seed(17)
b <- 20000
m <- rpos(b, 106, 1)
v <- rpos(b, 40, .6)
d <- m/v
h <- hist(d, breaks=seq(2.40,2.95,.02), plot=FALSE)
write.csv(data.frame(left=head(h$breaks,-1),right=tail(h$breaks,-1),
                    density=h$density,count=h$counts),
          "coordinate/densita_fisica_hist.csv",row.names=FALSE)
write.csv(data.frame(media=mean(d),sd=sd(d),
                    q025=unname(quantile(d,.025)),
                    q975=unname(quantile(d,.975))),
          "coordinate/densita_fisica_riepilogo.csv",row.names=FALSE)
# Tre dipendenze gaussiane standard per il diagramma concettuale.
set.seed(17)
z <- matrix(rnorm(160),ncol=2)
for (co in c(-.7,0,.7)) {
  write_xy(paste0("correlazione_",co), z[,1],
           co*z[,1]+sqrt(1-co^2)*z[,2])
}
# Confronti analitici e numerici di controllo.
s <- c(.02,.1,.2,.3)
t2 <- 2*s^2
write.csv(data.frame(sdlog=s,approssimata=2*sqrt(t2),
                    esatta=2*sqrt(expm1(t2)*exp(t2))),
          "coordinate/rapporto_sd.csv",row.names=FALSE)
print(data.frame(media=mean(d),sd=sd(d),
                 q025=unname(quantile(d,.025)),
                 q975=unname(quantile(d,.975))))
print(data.frame(sdlog=s,CV=sqrt(expm1(s^2))))
print(2.65*sqrt((1/106)^2+(.6/40)^2))
