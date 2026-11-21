# GeoStat Lab M12 Tessera. Funzioni di preparazione e calcolo esplicito.
.gs_prepara_notebook <- function(radice,id) {
  uscita <- file.path(radice,"Risultati",id)
  dir.create(uscita,recursive=TRUE,showWarnings=FALSE)
  list(carica_dati=function(nome,...) read.csv(file.path(radice,"Dati",nome),
      stringsAsFactors=FALSE,check.names=FALSE,...),
    percorso_dati=function(nome) file.path(radice,"Dati",nome),
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
audit_raster <- function(d) {
  req <- c("riga","colonna","x_m","y_m","quota_m","unita")
  stopifnot(all(req %in% names(d)),nrow(d)==720L,
    !anyDuplicated(d[c("riga","colonna")]),
    setequal(d$riga,0:23),setequal(d$colonna,0:29),
    all(d$x_m==30*d$colonna),all(d$y_m==30*d$riga),
    all(is.finite(as.matrix(d[c("x_m","y_m","quota_m")]))))
  invisible(d)
}
matrice_quote <- function(d,variabile="quota_m") {
  a<-d[order(d$riga,d$colonna),]
  matrix(a[[variabile]],nrow=24,ncol=30,byrow=TRUE)
}
richiedi_terra <- function() {
  if(!requireNamespace("terra",quietly=TRUE))
    stop("Questo notebook richiede terra reale. Installarlo prima dell'analisi con R/00_installazione.R.")
  suppressPackageStartupMessages(library(terra))
}
matrice_locale <- function(r) {
  M<-terra::as.matrix(r,wide=TRUE)
  M[nrow(M):1,,drop=FALSE]
}
raster_da_matrice <- function(Z,modello) {
  stopifnot(is.matrix(Z),nrow(Z)==nrow(modello),ncol(Z)==ncol(modello))
  r<-terra::rast(modello)
  terra::values(r)<-as.vector(t(Z[nrow(Z):1,,drop=FALSE]))
  r
}
gradienti_centrali <- function(Z,dx=30,dy=30) {
  nr<-nrow(Z);nc<-ncol(Z)
  stopifnot(nr>=3L,nc>=3L,dx>0,dy>0)
  gx<-(Z[2:(nr-1),3:nc]-Z[2:(nr-1),1:(nc-2)])/(2*dx)
  gy<-(Z[3:nr,2:(nc-1)]-Z[1:(nr-2),2:(nc-1)])/(2*dy)
  g<-sqrt(gx^2+gy^2)
  list(gx=gx,gy=gy,modulo=g,gradi=atan(g)*180/pi,percento=100*g,
    azimut_discesa=(atan2(-gx,-gy)*180/pi)%%360)
}
aggrega_blocchi <- function(Z,ny=2L,nx=2L) {
  stopifnot(nrow(Z)%%ny==0L,ncol(Z)%%nx==0L)
  nr<-nrow(Z)/ny;nc<-ncol(Z)/nx
  media<-matrix(NA_real_,nr,nc);numero<-matrix(0L,nr,nc)
  for(i in seq_len(nr)) for(j in seq_len(nc)) {
    b<-Z[((i-1)*ny+1):(i*ny),((j-1)*nx+1):(j*nx)]
    numero[i,j]<-sum(is.finite(b))
    if(numero[i,j]>0) media[i,j]<-mean(b[is.finite(b)])
  }
  list(media=media,numero=numero)
}
hillshade_esplicito <- function(gx,gy,azimut=315,altezza=45) {
  s<-atan(sqrt(gx^2+gy^2));a<-atan2(-gx,-gy)
  az<-azimut*pi/180;alt<-altezza*pi/180
  pmax(sin(alt)*cos(s)+cos(alt)*sin(s)*cos(az-a),0)
}
media_circolare <- function(gradi,tolleranza=1e-8) {
  r<-gradi*pi/180;s<-mean(sin(r));c<-mean(cos(r));rho<-sqrt(s*s+c*c)
  a<-(atan2(s,c)*180/pi)%%360
  if(min(a,360-a)<1e-10) a<-0
  c(media_gradi=if(rho<tolleranza) NA_real_ else a,risultante=rho)
}
mappa_matrice <- function(Z,x=seq(0,by=30,length.out=ncol(Z)),
    y=seq(0,by=30,length.out=nrow(Z)),titolo="Griglia sintetica",
    unita="Quota (m)",limiti=NULL,colori=NULL) {
  stopifnot(length(x)==ncol(Z),length(y)==nrow(Z))
  op<-par(no.readonly=TRUE);on.exit({layout(1);par(op)})
  if(is.null(limiti)) limiti<-range(Z,finite=TRUE)
  if(diff(limiti)==0) limiti<-limiti+c(-.5,.5)
  if(is.null(colori)) colori<-colorRampPalette(c("#E4EBC5","#44A68F","#244B68"))(40)
  br<-seq(limiti[1],limiti[2],length.out=length(colori)+1L)
  layout(matrix(1:2,nrow=1),widths=c(5,1))
  stile_grafico();par(mar=c(4.2,4.3,3,.3))
  image(x,y,t(Z),asp=1,col=colori,breaks=br,xlab="x locale (m)",
    ylab="y locale (m)",main=titolo,useRaster=TRUE)
  par(mar=c(4.2,.2,3,3.6));plot.new();plot.window(xlim=c(0,1),ylim=limiti)
  rect(0,head(br,-1),.4,tail(br,-1),col=colori,border=NA)
  axis(4,las=1);mtext(unita,side=3,line=.5,cex=.82)
}
