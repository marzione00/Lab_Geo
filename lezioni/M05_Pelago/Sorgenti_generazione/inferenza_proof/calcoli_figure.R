# Pelago M05, figure delle slide 26-59.
# Eseguire dalla cartella contenente questo file.
# I CSV qui prodotti forniscono le coordinate dei grafici TikZ.
dir.create("coordinate", showWarnings = FALSE)
salva <- function(x, nome) write.csv(x,
  file.path("coordinate", paste0(nome, ".csv")), row.names = FALSE)
f <- read.csv("fossili_simulati.csv", stringsAsFactors = FALSE)
x <- f$diametro_tot_um[f$morfotipo == "Rounded"]
y <- f$diametro_tot_um[f$morfotipo == "Spiky"]

grid <- seq(-2, 4.5, length.out = 261)
salva(data.frame(x = grid, normale = dnorm(grid,1,1),
                 esponenziale = dexp(grid)), "popolazioni")
grid <- seq(0, 2.3, length.out = 231)
salva(data.frame(x = grid, n12 = dgamma(grid,12,rate=12),
 n60 = dgamma(grid,60,rate=60)), "medie_esponenziali")
grid <- seq(-3.5, 4, length.out = 301)
salva(data.frame(z = grid, normale = dnorm(grid),
 n12 = dgamma(1+grid/sqrt(12),12,rate=12)/sqrt(12),
 n60 = dgamma(1+grid/sqrt(60),60,rate=60)/sqrt(60)),
 "standardizzate")
set.seed(17)
xx <- rexp(200)
salva(data.frame(n = seq_along(xx), media = cumsum(xx)/seq_along(xx)),
      "media_cumulativa")

# Nucleo dei laboratori del sito: ordine delle chiamate preservato.
set.seed(17)
means <- replicate(200, {
 u <- rnorm(1)
 mean(sqrt(.2)*u + sqrt(1-.2)*rnorm(60))
})
h <- hist(means, breaks = seq(-1.8,1.8,.15), plot = FALSE)
salva(data.frame(sinistra = head(h$breaks,-1),
 destra = tail(h$breaks,-1), densita = h$density), "dipendenza")
sim_ic <- function(rho) {
 set.seed(17)
 z <- t(replicate(200, {
  u <- rnorm(1)
  xx <- 10 + sqrt(rho)*u + sqrt(1-rho)*rnorm(30)
  c(mean(xx), sd(xx)/sqrt(30))
 }))
 q <- qt(.975,29)
 d <- data.frame(replica = 1:200, media = z[,1],
  inferiore = z[,1]-q*z[,2], superiore = z[,1]+q*z[,2])
 d$copre <- d$inferiore <= 10 & d$superiore >= 10
 d
}
d0 <- sim_ic(0); d2 <- sim_ic(.2)
salva(d0, "copertura_indipendente")
salva(d2, "copertura_correlata")
salva(data.frame(rho=c(0,.2), copertura=c(mean(d0$copre),mean(d2$copre)),
 se_mc=c(sqrt(mean(d0$copre)*(1-mean(d0$copre))/200),
 sqrt(mean(d2$copre)*(1-mean(d2$copre))/200))), "copertura_riepilogo")
grid <- seq(-4,4,length.out=321)
salva(data.frame(t=grid,normale=dnorm(grid), t19=dt(grid,19)), "student")
q <- qt(.975,length(x)-1)
ic <- mean(x)+c(-1,1)*q*sd(x)/sqrt(length(x))
ip <- mean(x)+c(-1,1)*q*sd(x)*sqrt(1+1/length(x))
welch <- t.test(y,x)
pa <- subset(f,morfotipo == "Rounded")
diff <- pa$diametro_tot_um-pa$diametro_int_um
cp <- t.test(diff)$conf.int
salva(data.frame(nome=c("n_R","media_R","sd_R","se_R","q_R","ic_inf",
 "ic_sup","ip_inf","ip_sup","media_S","sd_S","delta","se_delta",
 "nu_delta","delta_inf","delta_sup","coppie_media","coppie_sd",
 "coppie_se","coppie_inf","coppie_sup","cov_coppie"),
 valore=c(length(x),mean(x),sd(x),sd(x)/sqrt(length(x)),q,ic,ip,
 mean(y),sd(y),mean(y)-mean(x),welch$stderr,welch$parameter,
 welch$conf.int,mean(diff),sd(diff),sd(diff)/sqrt(length(diff)),cp,
 cov(pa$diametro_tot_um,pa$diametro_int_um))),"riepilogo_fossili")
salva(head(pa,8),"coppie")

# Controlli mirati: enumerazione del disegno e identita degli intervalli.
pop <- c(2,4,6,8,10)
medie <- colMeans(combn(pop,2))
v_enum <- mean((medie-mean(pop))^2)
v_fpc <- (1-2/length(pop))*var(pop)/2
stopifnot(abs(v_enum-v_fpc)<1e-12)
stopifnot(max(abs(ic-unname(t.test(x)$conf.int)))<1e-12)
stopifnot(abs(var(diff)-(var(pa$diametro_tot_um)+
 var(pa$diametro_int_um)-2*cov(pa$diametro_tot_um,pa$diametro_int_um)))<1e-12)
stopifnot(abs(60/(1+59*.2)-4.6875)<1e-12)
writeLines(capture.output(sessionInfo()),"sessionInfo_R.txt")
print(read.csv("coordinate/riepilogo_fossili.csv"))
print(read.csv("coordinate/copertura_riepilogo.csv"))
