# Calcoli riproducibili per le figure e i risultati di Borealis M09.
# Avviare dalla cartella del modulo LaTeX oppure fornire radice_modulo.
if (!exists("radice_modulo")) radice_modulo <- "."
D <- file.path(radice_modulo,"Dati")
O <- file.path(radice_modulo,"Calcoli")
dir.create(O,recursive=TRUE,showWarnings=FALSE)
source(file.path(radice_modulo,"R","funzioni_calcoli.R"))
stopifnot(requireNamespace("tseries",quietly=TRUE))
leggi <- function(n) read.csv(file.path(D,n),stringsAsFactors=FALSE)
salva <- function(x,n) write.csv(x,file.path(O,n),row.names=FALSE,na="")
w <- leggi("co2_settimanale_storica.csv");w$data <- as.Date(w$data)
m <- leggi("co2_mensile_derivata.csv");m$data <- as.Date(m$data)
d <- leggi("co2_1985_2001.csv");d$data <- as.Date(d$data)
t <- leggi("temperatura_simulata.csv");t$data <- as.Date(t$data)
p <- leggi("processi_simulati.csv")
stopifnot(!anyDuplicated(w$data),all(diff(w$data)==7),nrow(w)==2284,
 sum(is.na(w$co2))==59,identical(d$data,seq(as.Date("1985-01-01"),as.Date("2001-12-01"),by="month")),
 !anyNA(d),nrow(d)==204,all(d$n_settimane>=3),nrow(p)==300)
gruppi <- split(w$co2,format(w$data,"%Y-%m"))
ric <- do.call(rbind,lapply(names(gruppi),function(k) {
 z<-gruppi[[k]];n<-sum(!is.na(z))
 data.frame(data=as.Date(paste0(k,"-01")),co2_ppm=if(n)mean(z,na.rm=TRUE) else NA_real_,n_settimane=n)
}))
stopifnot(identical(ric$data,m$data),identical(is.na(ric$co2_ppm),is.na(m$co2_ppm)),
 all(ric$n_settimane==m$n_settimane),max(abs(ric$co2_ppm-m$co2_ppm),na.rm=TRUE)<1e-5)
salva(ric,"co2_mensile_ricostruita.csv")
salva(as.data.frame(table(n_settimane=m$n_settimane)),"copertura_mensile.csv")
x <- d$co2_ppm
serie_co2 <- data.frame(data=d$data,livello=x,diff1=c(NA,diff(x)),
 diff12=c(rep(NA,12),diff(x,lag=12)),diff1_12=c(rep(NA,13),diff(diff(x,lag=12))))
stopifnot(max(abs(diff(diff(x,lag=12))-diff(diff(x),lag=12)))<1e-12)
salva(serie_co2,"co2_trasformazioni.csv")
u <- t$temperatura_C;tempo <- seq_along(u);mese <- as.integer(format(t$data,"%m"))
base <- t$data>=as.Date("2000-01-01") & t$data<=as.Date("2004-12-01")
clima <- tapply(u[base],mese[base],mean)
anomalia <- u-as.numeric(clima[as.character(mese)])
dec <- stl(ts(u,start=c(2000,1),frequency=12),s.window="periodic",robust=TRUE)
ma3 <- as.numeric(filter(u,rep(1/3,3),sides=2))
ma13 <- as.numeric(filter(u,rep(1/13,13),sides=2))
tr13 <- as.numeric(filter(u,rep(1/13,13),sides=1))
l20 <- fitted(loess(u~tempo,span=.2));l60 <- fitted(loess(u~tempo,span=.6))
temp <- data.frame(data=t$data,osservata=u,trend_vero=t$trend_simulato,
 stagione_vera=t$stagione_simulata,residuo_vero=t$residuo_simulato,
 ma3=ma3,ma13=ma13,trailing13=tr13,loess20=l20,loess60=l60,
 riferimento_2000_2004=as.numeric(clima[as.character(mese)]),anomalia=anomalia,
 stl_trend=as.numeric(dec$time.series[,"trend"]),
 stl_stagione=as.numeric(dec$time.series[,"seasonal"]),
 stl_residuo=as.numeric(dec$time.series[,"remainder"]))
stopifnot(max(abs(u-t$trend_simulato-t$stagione_simulata-t$residuo_simulato))<2e-8,
 max(abs(rowSums(dec$time.series)-u))<1e-10)
salva(temp,"temperatura_componenti.csv")
salva(data.frame(mese=1:12,climatologia=as.numeric(clima)),"climatologia_base_2000_2004.csv")
serie <- c(as.list(p[c("rumore_bianco","ar1","random_walk")]),
 list(co2_livello=x,co2_diff1=diff(x),co2_diff12=diff(x,lag=12),
 co2_combinata=diff(diff(x,lag=12))))
acfs <- do.call(rbind,lapply(names(serie),function(n){
 z<-serie[[n]];a<-as.numeric(acf(z,plot=FALSE,lag.max=36)$acf)
 data.frame(serie=n,lag=0:(length(a)-1),acf=a,n=length(z),banda_95=1.96/sqrt(length(z)))
}))
pacfs <- do.call(rbind,lapply(names(serie),function(n){
 z<-serie[[n]];a<-as.numeric(pacf(z,plot=FALSE,lag.max=36)$acf)
 data.frame(serie=n,lag=seq_along(a),pacf=a,n=length(z),banda_95=1.96/sqrt(length(z)))
}))
salva(acfs,"acf_processi.csv");salva(pacfs,"pacf_processi.csv")
tests <- do.call(rbind,lapply(names(serie),function(n)tabella_test(n,serie[[n]],k=4)))
salva(tests,"test_stazionarieta.csv")
set.seed(1909);B<-1000L;n<-150L;phi<-.7
ar <- replicate(B,simula_ar1(n,phi));rw <- replicate(B,cumsum(rnorm(n)))
salva(data.frame(passo=1:n,var_ar=apply(ar,1,var),var_rw=apply(rw,1,var),
 teoria_ar=1,teoria_rw=1:n),"processi_ensemble.csv")
salva(data.frame(passo=rep(1:n,12),processo=rep(c("AR1","RW"),each=6*n),
 traiettoria=rep(rep(1:6,each=n),2),valore=c(ar[,1:6],rw[,1:6])),"processi_traiettorie.csv")
set.seed(1805);e <- rnorm(3000);de <- diff(e)
salva(data.frame(lag=0:24,bianco=as.numeric(acf(e,plot=FALSE,lag.max=24)$acf),
 differenza=as.numeric(acf(de,plot=FALSE,lag.max=24)$acf),teoria_diff=c(1,-.5,rep(0,23))),"sovradifferenziazione.csv")
set.seed(1840);grande <- rnorm(10000)
# Detrending e differenze applicati alla medesima serie.
trend <- .03*p$passo+p$ar1
fit <- lm(trend~p$passo)
salva(data.frame(passo=p$passo,livello=trend,trend_stimato=fitted(fit),
 residuo=residuals(fit),differenza=c(NA,diff(trend))),"trend_deterministico.csv")
v <- p$ar1-mean(p$ar1)
acf_manuale <- sum(head(v,-1)*tail(v,-1))/sum(v^2)
stopifnot(abs(acf_manuale-as.numeric(acf(p$ar1,plot=FALSE,lag.max=1)$acf[2]))<1e-12)
metrics <- c(n_settimane=nrow(w),co2_osservate=sum(!is.na(w$co2)),co2_NA=sum(is.na(w$co2)),
 n_mesi=nrow(m),mesi_NA=sum(is.na(m$co2_ppm)),n_co2=nrow(d),n_temp=nrow(t),n_processi=nrow(p),
 n_diff1=length(diff(x)),n_diff12=length(diff(x,lag=12)),n_combinata=length(diff(diff(x,lag=12))),
 max_scarto_mensile=max(abs(ric$co2_ppm-m$co2_ppm),na.rm=TRUE),
 co2_prima=x[1],co2_ultima=tail(x,1),
 temperatura_ricostruzione=max(abs(rowSums(dec$time.series)-u)),
 acf_AR1=as.numeric(acf(p$ar1,plot=FALSE,lag.max=1)$acf[2]),
 cor_lag1_AR1=cor(head(p$ar1,-1),tail(p$ar1,-1)),acf_manuale=acf_manuale,
 acf_overdiff_3000=as.numeric(acf(de,plot=FALSE,lag.max=1)$acf[2]),
 acf_overdiff_10000=as.numeric(acf(diff(grande),plot=FALSE,lag.max=1)$acf[2]),
 media_pesata_esempio=weighted.mean(c(10,20),c(2,8)),media_periodi_esempio=mean(c(10,20)),
 ensemble_B=B,var_AR_fine=var(ar[n,]),var_RW_fine=var(rw[n,]))
salva(data.frame(nome=names(metrics),valore=unname(metrics)),"metrics.csv")
# JSON numerico semplice, senza dipendenze aggiuntive.
righe_json <- sprintf('  "%s": %.17g',names(metrics),as.numeric(metrics))
writeLines(paste0("{\n",paste(righe_json,collapse=",\n"),"\n}"),file.path(O,"metrics.json"))
writeLines(capture.output(sessionInfo()),file.path(O,"SESSIONE_R.txt"))
cat("Borealis: calcoli verificati;",nrow(tests),"esiti ADF/KPSS con avvisi conservati.\n")
