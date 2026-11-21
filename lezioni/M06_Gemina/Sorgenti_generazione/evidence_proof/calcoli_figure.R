# Gemina M06, figure delle slide 20-46. Solo R base.
# Eseguire nella cartella contenente questo file e Dati/.
options(warn = 2)
dir.create("coordinate", showWarnings = FALSE)
wr <- function(x, name) write.csv(x, file.path("coordinate", paste0(name, ".csv")), row.names = FALSE)
x <- seq(-6,6,length.out=601)
wr(data.frame(x=x,t5=dt(x,5),t20=dt(x,20),normale=dnorm(x)), "riferimenti")
# Quantili e p esatti della distribuzione t.
wr(data.frame(nome=c("p20","p5","pz","q49","q51","crit20"),
  valore=c(2*pt(-2,20),2*pt(-2,5),2*pnorm(-2),qt(1-.049/2,20),qt(1-.051/2,20),qt(.975,20))),"pvalue")
# Calibrazione dei p sotto un riferimento continuo esatto.
set.seed(6029)
u <- 2*pnorm(-abs(rnorm(5000)))
zz <- seq(0,1,length.out=101)
wr(data.frame(u=zz,F=sapply(zz,function(v)mean(u<=v))),"calibrazione")
# Potenza normale nota: Z ha media delta/SE e varianza 1.
eta <- .5/sqrt(2/30)
wr(data.frame(x=x,H0=dnorm(x),H1=dnorm(x,eta)),"potenza_normale")
wr(data.frame(nome=c("eta","critico","power_normale"),
valore=c(eta,qnorm(.975),pnorm(-qnorm(.975),eta)+pnorm(qnorm(.975),eta,lower.tail=FALSE))),"potenza_normale_stats")
ns <- seq(5,300,5)
pow <- function(n,d)power.t.test(n=n,delta=d,sd=1,sig.level=.05,type="two.sample",alternative="two.sided",strict=TRUE)$power
wr(data.frame(n=ns,d02=sapply(ns,pow,d=.2),d05=sapply(ns,pow,d=.5),d08=sapply(ns,pow,d=.8)),"potenza_t")
np <- 2*(qnorm(.975)+qnorm(.8))^2/.5^2
nt <- power.t.test(delta=.5,sd=1,sig.level=.05,power=.8,type="two.sample",alternative="two.sided",strict=TRUE)$n
wr(data.frame(nome=c("n_normale","n_t","p30","p64"),valore=c(np,nt,pow(30,.5),pow(64,.5))),"pianificazione")
# Stopping non pianificato: test z a due code, sigma noto = 1.
set.seed(6035)
X <- matrix(rnorm(100*5000),nrow=100)
cs <- apply(X,2,cumsum)
looks <- seq(10,100,10)
Z <- cs[looks,,drop=FALSE]/sqrt(looks)
reject <- abs(Z)>qnorm(.975)
wr(data.frame(n=looks,finale=rowMeans(reject),qualsiasi=sapply(seq_along(looks),function(i)mean(colSums(reject[seq_len(i),,drop=FALSE])>0))),"arresto")
# Fossili sintetici: contrasto Spiky - Rounded.
f <- read.csv("Dati/fossili_simulati.csv")
a <- f$diametro_tot_um[f$morfotipo=="Rounded"]
b <- f$diametro_tot_um[f$morfotipo=="Spiky"]
na <- length(a); nb <- length(b); va <- var(a)/na; vb <- var(b)/nb
se <- sqrt(va+vb); est <- mean(b)-mean(a)
nu <- (va+vb)^2/(va^2/(na-1)+vb^2/(nb-1))
tt <- t.test(b,a)
wr(data.frame(nome=c("na","nb","mediaA","mediaB","sdA","sdB","varA","varB","contribA","contribB","se","delta","t","df","p","lo","hi","crit","pooled_sd","d","glassA"),
  valore=c(na,nb,mean(a),mean(b),sd(a),sd(b),var(a),var(b),va,vb,se,est,est/se,nu,tt$p.value,tt$conf.int,qt(.975,nu),sqrt(((na-1)*var(a)+(nb-1)*var(b))/(na+nb-2)),est/sqrt(((na-1)*var(a)+(nb-1)*var(b))/(na+nb-2)),est/sd(a))),"fossili_stats")
stopifnot(all.equal(unname(tt$statistic),est/se,tolerance=1e-13),all.equal(unname(tt$parameter),nu,tolerance=1e-13))
# Punti senza jitter casuale: ordinate cicliche per evitare sovrapposizioni.
wr(data.frame(valore=c(a,b),gruppo=rep(c("A","B"),c(na,nb)),offset=rep((seq_len(na) %% 7-3)/35,2)),"fossili_punti")
# Effetto del rapporto fra SD, con uguali n=30 e parametri del browser.
rat <- seq(.5,4,.05)
wr(data.frame(ratio=rat,df=(1+rat^2)^2/(1/29+rat^4/29)),"welch_df")
# Stessi campioni standardizzati per il browser Welch a diversi SD_B.
set.seed(17); wa <- rnorm(30); wb <- rnorm(30,.5,2)
w <- t.test(wb,wa)
wr(data.frame(gruppo=rep(c("A","B"),each=30),valore=c(wa,wb)),"welch_browser")
wr(data.frame(nome=c("delta","se","df","p","lo","hi"),valore=c(mean(wb)-mean(wa),sqrt(var(wa)/30+var(wb)/30),w$parameter,w$p.value,w$conf.int)),"welch_browser_stats")
cat("Figure e controlli numerici completati.\n")
