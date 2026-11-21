# GeoStat Lab M11 Locus. R base e sf per i soli notebook05,06,20.
.gs_prepara_notebook <- function(radice,id) {
  uscita <- file.path(radice,"Risultati",id)
  dir.create(uscita,recursive=TRUE,showWarnings=FALSE)
  list(carica_dati=function(nome,...) read.csv(file.path(radice,"Dati",nome),
      stringsAsFactors=FALSE,check.names=FALSE,...),
    percorso_risultati=function(nome) {
      stopifnot(length(nome)==1L,!grepl("(^/|[.][.])",nome))
      dest <- file.path(uscita,nome)
      dir.create(dirname(dest),recursive=TRUE,showWarnings=FALSE)
      dest
    })
}
palette_geo <- c("#1D7890","#C57E42","#7363AA","#2A8060","#657180")
stile_grafico <- function() par(mar=c(4.2,4.4,3,1),mgp=c(2.7,.7,0),las=1,
  bty="l",col.axis="#253344",col.lab="#253344",col.main="#15283E",
  fg="#253344",bg="white",cex=.94)
audit_spazio <- function(d) {
  req <- c("id","x_m","y_m","quota_m","concentrazione","area","lon","lat")
  stopifnot(all(req %in% names(d)),nrow(d)==64L,!anyDuplicated(d$id),
    !anyDuplicated(d[c("x_m","y_m")]),
    all(is.finite(as.matrix(d[c("x_m","y_m","lon","lat","concentrazione","quota_m")]))),
    identical(sort(unique(d$x_m)),seq(0,1750,250)),
    identical(sort(unique(d$y_m)),seq(0,1750,250)))
  invisible(d)
}
richiedi_sf <- function() {
  if(!requireNamespace("sf",quietly=TRUE))
    stop("Questo notebook richiede sf reale. Installarlo prima dell'analisi con R/00_installazione.R.")
}
distanze_incrociate <- function(a,b) {
  a<-as.matrix(a);b<-as.matrix(b)
  stopifnot(ncol(a)==2L,ncol(b)==2L,all(is.finite(a)),all(is.finite(b)))
  sqrt(outer(a[,1],b[,1],"-")^2+outer(a[,2],b[,2],"-")^2)
}
pesi_spaziali <- function(d,soglia=260) {
  D<-as.matrix(dist(d[c("x_m","y_m")]))
  A<-1*(D>0&D<=soglia);nv<-rowSums(A)
  W<-A
  W[nv>0,]<-A[nv>0,,drop=FALSE]/nv[nv>0]
  list(D=D,A=A,W=W,n_vicini=nv,isolati=which(nv==0))
}
moran_I <- function(z,W) {
  v<-as.numeric(z)-mean(z);n<-length(v);S0<-sum(W)
  stopifnot(nrow(W)==n,ncol(W)==n,S0>0,sum(v^2)>0,all(is.finite(W)))
  as.numeric(n/S0*crossprod(v,W%*%v)/sum(v^2))
}
haversine_km <- function(lon1,lat1,lon2,lat2,R=6371) {
  a<-lat1*pi/180;b<-lat2*pi/180;dlon<-(lon2-lon1)*pi/180
  h<-sin((b-a)/2)^2+cos(a)*cos(b)*sin(dlon/2)^2
  2*R*asin(sqrt(pmin(1,pmax(0,h))))
}
idw_pesi <- function(xy,pos,p=2,tol=1e-10) {
  stopifnot(length(pos)==2L,p>0,tol>=0)
  r<-as.numeric(distanze_incrociate(matrix(pos,nrow=1),xy))
  coincidenti<-r<=tol
  if(any(coincidenti)) return(as.numeric(coincidenti)/sum(coincidenti))
  w<-r^-p;w/sum(w)
}
idw_pred <- function(xy,z,newxy,p=2) {
  stopifnot(nrow(as.matrix(xy))==length(z),all(is.finite(z)))
  apply(as.matrix(newxy),1,function(pos) sum(idw_pesi(xy,pos,p)*z))
}
metriche <- function(obs,prev) {
  stopifnot(length(obs)==length(prev),length(obs)>0L,all(is.finite(obs)),all(is.finite(prev)))
  e<-obs-prev;c(MAE=mean(abs(e)),RMSE=sqrt(mean(e^2)),bias_osservato_meno_previsto=mean(e))
}
mappa_valori <- function(d,titolo="Concentrazione sui siti osservati") {
  op<-par(no.readonly=TRUE);on.exit({layout(1);par(op)})
  br<-seq(min(d$concentrazione),max(d$concentrazione),length.out=21)
  pal<-hcl.colors(20,"Viridis")
  layout(matrix(1:2,nrow=1),widths=c(5,1))
  stile_grafico();par(mar=c(4.2,4.3,3,0.3))
  plot(d$x_m,d$y_m,asp=1,pch=19,cex=1.1,
       col=pal[cut(d$concentrazione,br,include.lowest=TRUE,labels=FALSE)],
       xlab="x locale (m)",ylab="y locale (m)",main=titolo)
  par(mar=c(4.2,.2,3,3.4));plot.new();plot.window(xlim=c(0,1),ylim=range(br))
  rect(0,head(br,-1),.35,tail(br,-1),col=pal,border=NA)
  axis(4,las=1);mtext("u.a.",side=3,line=.5)
}
