# M05. Calcoli didattici; eseguire dalla radice del corso.
# I CSV originali sono letti senza modifiche. Ogni simulazione ha un seme proprio.
options(warn=2)
suppressPackageStartupMessages(library(ggplot2))
suppressPackageStartupMessages(library(jsonlite))
for (p in c('figure/M05','risultati/M05','verifiche/M05')) dir.create(p,showWarnings=FALSE)
RNGkind('Mersenne-Twister','Inversion','Rejection')
d <- read.csv('dati/campioni_modulo1.csv',stringsAsFactors=FALSE)
f <- read.csv('dati/fossili_simulati.csv',stringsAsFactors=FALSE)
d$densita <- d$massa_g/d$volume_cm3
st <- aggregate(densita~affioramento+stazione,d,mean)
g <- split(f$diametro_tot_um,f$morfotipo)
x <- g$Rounded; y <- g$Spiky
B <- 10000L
boot_media <- function(v,b=B) replicate(b,mean(sample(v,length(v),replace=TRUE)))
q95 <- function(v) unname(quantile(v,c(.025,.975),type=7))
V <- list()
# @@ N01
parametro <- 1
set.seed(301); campione <- rexp(40,rate=1)
stima <- mean(campione)
V$media_R <- mean(x); V$media_S <- mean(y); V$media_st <- mean(st$densita)
# @@ fine
# @@ N02
set.seed(302); percorsi <- replicate(4,cumsum(rexp(1500))/seq_len(1500))
lln <- data.frame(n=rep(seq_len(1500),4),media=as.vector(percorsi),
                  percorso=factor(rep(seq_len(4),each=1500)))
# @@ fine
# @@ N03
set.seed(303); M <- 6000L
medie5 <- replicate(M,mean(rexp(5)))
medie40 <- replicate(M,mean(rexp(40)))
campionarie <- data.frame(media=c(medie5,medie40),
                          n=factor(rep(c('n = 5','n = 40'),each=M)))
V$sd_medie5 <- sd(medie5); V$sd_medie40 <- sd(medie40)
# @@ fine
# @@ N04
standardizzate <- data.frame(z=c(sqrt(5)*(medie5-1),sqrt(40)*(medie40-1)),
                            n=campionarie$n)
# Modello equicorrelato entro stazione: G = 6, m = 4, sigma = 1, ICC = 0.6.
G <- 6L; m <- 4L; eta <- .6
Sigma <- kronecker(diag(G),(1-eta)*diag(m)+eta*matrix(1,m,m))
var_media <- sum(Sigma)/(G*m)^2
V$deff <- 1+(m-1)*eta; V$neff <- G*m/V$deff
V$var_cluster <- var_media
# @@ fine
# @@ N05
n <- length(x); xb <- mean(x); s <- sd(x); se <- s/sqrt(n)
V$sd_R <- s; V$se_R <- se
V$var_R <- var(x)
# @@ fine
# @@ N06
critico <- qt(.975,n-1)
ic_t <- xb+c(-1,1)*critico*se
ip_t <- xb+c(-1,1)*critico*s*sqrt(1+1/n)
ic_welch <- unname(t.test(y,x)$conf.int)
pa <- subset(f,morfotipo=='Rounded')
diff_coppie <- pa$diametro_tot_um-pa$diametro_int_um
ic_coppie <- unname(t.test(diff_coppie)$conf.int)
V$tcrit <- critico; V$t_lo <- ic_t[1]; V$t_hi <- ic_t[2]
V$pred_lo <- ip_t[1]; V$pred_hi <- ip_t[2]
V$welch_lo <- ic_welch[1]; V$welch_hi <- ic_welch[2]
V$paired_media <- mean(diff_coppie); V$paired_se <- sd(diff_coppie)/sqrt(n)
V$paired_lo <- ic_coppie[1]; V$paired_hi <- ic_coppie[2]
# @@ fine
# @@ N07
set.seed(307); K <- 2000L; n_cov <- 20L
campioni <- matrix(rnorm(K*n_cov,5,2),nrow=K)
centri <- rowMeans(campioni)
margini <- qt(.975,n_cov-1)*apply(campioni,1,sd)/sqrt(n_cov)
copre <- abs(centri-5)<=margini
copertura <- data.frame(replica=seq_len(K),media=centri,
                        basso=centri-margini,alto=centri+margini,copre=copre)
V$coverage <- mean(copre); V$coverage_mcse <- sqrt(.95*.05/K)
V$coverage_first <- sum(copre[1:60]); V$coverage_success <- sum(copre)
# @@ fine
# @@ N08
set.seed(308)
bias_scenari <- do.call(rbind,lapply(c(10,40,160),function(nn) {
 data.frame(n=factor(nn,levels=c(10,40,160)),
 stima=c(rnorm(4000,0,1/sqrt(nn)),rnorm(4000,1,1/sqrt(nn))),
 base=rep(c('Dominio completo','Settore accessibile'),each=4000))
}))
# Campionamento casuale semplice senza reinserimento: verifica enumerativa.
pop <- c(2,4,6,8,10); nc <- 2L
combinazioni <- combn(pop,nc)
medie_srs <- colMeans(combinazioni)
var_design <- mean((medie_srs-mean(pop))^2)
var_fpc <- (1-nc/length(pop))*var(pop)/nc
V$fpc_var <- var_fpc
# @@ fine
# @@ N09
w <- ifelse(d$stazione=='A1',4,1)
V$media_pesata <- weighted.mean(d$densita,w)
V$n_progetto <- ceiling((qnorm(.975)*.8/.2)^2)
V$se25 <- 1/sqrt(25); V$se100 <- 1/sqrt(100)
# @@ fine
# @@ N10
empirica <- data.frame(valore=sort(x),probabilita=seq_along(x)/length(x))
V$unici_attesi <- n*(1-(1-1/n)^n)
# @@ fine
# @@ N11
set.seed(311)
indici <- sample.int(n,n,replace=TRUE)
replica <- x[indici]
frequenze <- tabulate(indici,nbins=n)
V$unici_replica <- length(unique(indici)); V$media_replica <- mean(replica)
# @@ fine
# @@ N12
set.seed(312)
b_R <- boot_media(x)
V$boot_R_se <- sd(b_R); V$boot_R_lo <- q95(b_R)[1]; V$boot_R_hi <- q95(b_R)[2]
V$boot_R_bias <- mean(b_R)-mean(x)
V$boot_R_se_esatto <- sqrt((n-1)*var(x)/n^2)
# @@ fine
# @@ N13
set.seed(313)
b_pool <- replicate(B,{
 id <- sample.int(nrow(f),nrow(f),replace=TRUE)
 c(media=mean(f$diametro_tot_um[id]),quota=sum(f$morfotipo[id]=='Spiky'))
})
V$pool_se <- sd(b_pool['media',]); V$pool_lo <- q95(b_pool['media',])[1]
V$pool_hi <- q95(b_pool['media',])[2]
# @@ fine
# @@ N14
set.seed(314)
b_strat <- replicate(B,.5*mean(sample(x,80,TRUE))+.5*mean(sample(y,80,TRUE)))
se_strat <- sqrt(.25*var(x)/80+.25*var(y)/80)
V$strat_se <- sd(b_strat); V$strat_se_formula <- se_strat
V$strat_lo <- q95(b_strat)[1]; V$strat_hi <- q95(b_strat)[2]
V$media_mix <- .5*mean(x)+.5*mean(y)
# @@ fine
# @@ N15
set.seed(315)
b_delta <- replicate(B,mean(sample(y,80,TRUE))-mean(sample(x,80,TRUE)))
V$delta <- mean(y)-mean(x); V$delta_se <- sd(b_delta)
V$delta_lo <- q95(b_delta)[1]; V$delta_hi <- q95(b_delta)[2]
set.seed(1315)
b_paired <- boot_media(diff_coppie)
V$paired_boot_se <- sd(b_paired)
# @@ fine
# @@ N16
set.seed(316)
b_righe <- boot_media(d$densita)
b_stazioni <- boot_media(st$densita)
V$righe_se <- sd(b_righe); V$stazioni_se <- sd(b_stazioni)
V$stazioni_lo <- q95(b_stazioni)[1]; V$stazioni_hi <- q95(b_stazioni)[2]
V$stazioni_t_lo <- unname(t.test(st$densita)$conf.int[1])
V$stazioni_t_hi <- unname(t.test(st$densita)$conf.int[2])
# @@ fine
# @@ N17
st_A <- st$densita[st$affioramento=='A']
st_B <- st$densita[st$affioramento=='B']
set.seed(317)
b_AB <- replicate(B,mean(sample(st_A,3,TRUE))-mean(sample(st_B,3,TRUE)))
V$AB <- mean(st_A)-mean(st_B); V$AB_lo <- q95(b_AB)[1]; V$AB_hi <- q95(b_AB)[2]
# @@ fine
# @@ N18
set.seed(318)
mc <- do.call(rbind,lapply(c(200L,1000L,5000L),function(bb) {
 do.call(rbind,lapply(seq_len(12),function(rr) {
  z <- boot_media(x,bb)
  data.frame(B=bb,corsa=rr,se=sd(z),basso=q95(z)[1],alto=q95(z)[2])
 }))
}))
# @@ fine
# @@ N19
piccolo <- c(4,5,7,8)
# Tutte le 4^4 = 256 sequenze ordinate, equiprobabili con reinserimento.
indici_esatti <- as.matrix(expand.grid(rep(list(seq_len(4)),4)))
medie_esatte <- apply(indici_esatti,1,function(ii)mean(piccolo[ii]))
V$toy_mean <- mean(medie_esatte)
V$toy_var <- mean((medie_esatte-mean(medie_esatte))^2)
# @@ fine
# @@ N20
set.seed(320)
b_mediana <- replicate(B,median(sample(x,length(x),replace=TRUE)))
V$mediana_R <- median(x); V$mediana_lo <- q95(b_mediana)[1]
V$mediana_hi <- q95(b_mediana)[2]
# @@ fine
# Dipendenza temporale: anticipazione al modulo M09.
set.seed(321); n_ar <- 160L; phi <- .7
serie <- as.numeric(arima.sim(model=list(ar=phi),n=n_ar,sd=sqrt(1-phi^2)))
blocco <- function(z,l) {
 starts <- sample.int(length(z)-l+1,ceiling(length(z)/l),replace=TRUE)
 unlist(lapply(starts,function(a)z[a:(a+l-1)]),use.names=FALSE)[seq_along(z)]
}
set.seed(322); b_ar_iid <- boot_media(serie,3000)
b_ar_blocchi <- replicate(3000,mean(blocco(serie,8)))
V$ar_se_iid <- sd(b_ar_iid); V$ar_se_blocchi <- sd(b_ar_blocchi)
V$ar_se_teorico <- sqrt((n_ar+2*sum((n_ar-seq_len(n_ar-1))*phi^seq_len(n_ar-1)))/n_ar^2)
# Salvataggi numerici comuni alle slide e ai laboratori.
write_json(V,'risultati/M05/valori.json',auto_unbox=TRUE,pretty=TRUE,digits=16)
write.csv(st,'risultati/M05/medie_stazioni.csv',row.names=FALSE)
write.csv(copertura,'risultati/M05/copertura.csv',row.names=FALSE)
write.csv(mc,'risultati/M05/stabilita_MC.csv',row.names=FALSE)
riepilogo <- data.frame(metodo=c('Rounded: t','Rounded: bootstrap','Miscela: pooled','Miscela: stratificato','Differenza S-R','Stazioni','Affioramenti A-B'),
 stima=c(xb,xb,V$media_mix,V$media_mix,V$delta,V$media_st,V$AB),
 basso=c(ic_t[1],V$boot_R_lo,V$pool_lo,V$strat_lo,V$delta_lo,V$stazioni_lo,V$AB_lo),
 alto=c(ic_t[2],V$boot_R_hi,V$pool_hi,V$strat_hi,V$delta_hi,V$stazioni_hi,V$AB_hi))
write.csv(riepilogo,'risultati/M05/intervalli.csv',row.names=FALSE)
