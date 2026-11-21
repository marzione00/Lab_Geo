# Futura M10. Funzioni numeriche riutilizzabili, R base + stats.
# Edizione 20 novembre 2026. Le funzioni non installano pacchetti.

metriche <- function(osservato, previsto) {
  stopifnot(length(osservato)==length(previsto),length(osservato)>0,
            all(is.finite(osservato)),all(is.finite(previsto)))
  e <- osservato-previsto
  c(MAE=mean(abs(e)),RMSE=sqrt(mean(e^2)),bias=mean(e))
}

baseline <- function(train,h,periodo=12L) {
  y<-as.numeric(train);n<-length(y)
  stopifnot(n>=max(2L,periodo),h>=1L,all(is.finite(y)))
  deriva<-(tail(y,1)-head(y,1))/(n-1)
  list(Media=rep(mean(y),h),Ultimo=rep(tail(y,1),h),
       Stagionale=rep(tail(y,periodo),length.out=h),
       Deriva=tail(y,1)+seq_len(h)*deriva)
}

stima_sarima <- function(y,order=c(0L,1L,1L),seasonal=c(0L,1L,1L),periodo=12L) {
  f<-stats::arima(y,order=order,seasonal=list(order=seasonal,period=periodo),
                  include.mean=FALSE,method="ML")
  if(!is.null(f$code)&&f$code!=0L) stop("Ottimizzazione SARIMA non convergente.")
  f
}

previsione_sarima <- function(fit,h,livello=.95) {
  p<-predict(fit,n.ahead=h);z<-qnorm((1+livello)/2)
  data.frame(h=seq_len(h),previsto=as.numeric(p$pred),se=as.numeric(p$se),
             inferiore=as.numeric(p$pred-z*p$se),superiore=as.numeric(p$pred+z*p$se))
}

valida_origini <- function(train,origini=c(120L,132L,144L),h=12L) {
  stopifnot(all(origini>=24L),all(origini+h<=length(train)))
  do.call(rbind,lapply(origini,function(o){
    tr<-ts(as.numeric(train)[seq_len(o)],start=start(train),frequency=frequency(train))
    obs<-as.numeric(train)[o+seq_len(h)]
    f<-stima_sarima(tr);pr<-previsione_sarima(f,h)
    b<-baseline(tr,h)
    data.frame(origine=o,h=seq_len(h),osservato=obs,SARIMA=pr$previsto,
               Stagionale=b$Stagionale,Deriva=b$Deriva,Ultimo=b$Ultimo,
               inferiore=pr$inferiore,superiore=pr$superiore)
  }))
}

stima_VAR1 <- function(xy) {
  stopifnot(ncol(xy)==2,nrow(xy)>5,all(is.finite(as.matrix(xy))))
  x<-as.numeric(xy[,1]);y<-as.numeric(xy[,2])
  d<-data.frame(x=tail(x,-1),y=tail(y,-1),x_lag=head(x,-1),y_lag=head(y,-1))
  fx<-lm(x~x_lag+y_lag,data=d);fy<-lm(y~x_lag+y_lag,data=d)
  A<-rbind(coef(fx)[c("x_lag","y_lag")],coef(fy)[c("x_lag","y_lag")])
  c0<-c(coef(fx)[1],coef(fy)[1]);eg<-eigen(A,only.values=TRUE)$values
  list(A=A,c=c0,autovalori=eg,stabile=all(Mod(eg)<1),x=fx,y=fy,dati_ritardati=d)
}

previsione_VAR1 <- function(fit,ultimo,h) {
  s<-as.numeric(ultimo);p<-matrix(NA_real_,h,2,dimnames=list(NULL,c("X","Y")))
  for(k in seq_len(h)){s<-as.numeric(fit$c+fit$A%*%s);p[k,]<-s}
  p
}

ar1_teoria <- function(phi=.65,sigma=1,x0=2,mu=0,h=30L) {
  stopifnot(abs(phi)<1,sigma>0,h>=1)
  k<-seq_len(h);v<-sigma^2*(1-phi^(2*k))/(1-phi^2);m<-mu+phi^k*(x0-mu)
  data.frame(h=k,media=m,varianza=v,inferiore=m-qnorm(.975)*sqrt(v),
             superiore=m+qnorm(.975)*sqrt(v))
}
