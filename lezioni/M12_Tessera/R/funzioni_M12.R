# Tessera: funzioni esplicite, matrici con prima riga a Sud.
# Le quote e le distanze orizzontali sono entrambe in metri.
row_values <- function(M) as.vector(t(M))
gradiente_centrato <- function(Z,dx=30,dy=dx,centro_valido=TRUE) {
 stopifnot(is.matrix(Z),nrow(Z)>=3,ncol(Z)>=3,dx>0,dy>0)
 nr<-nrow(Z);nc<-ncol(Z)
 gx<-(Z[2:(nr-1),3:nc,drop=FALSE]-Z[2:(nr-1),1:(nc-2),drop=FALSE])/(2*dx)
 gy<-(Z[3:nr,2:(nc-1),drop=FALSE]-Z[1:(nr-2),2:(nc-1),drop=FALSE])/(2*dy)
 ok<-is.finite(gx)&is.finite(gy)
 if(centro_valido)ok<-ok&is.finite(Z[2:(nr-1),2:(nc-1),drop=FALSE])
 gx[!ok]<-NA_real_;gy[!ok]<-NA_real_
 list(gx=gx,gy=gy,valido=ok)
}
morfometria <- function(Z,dx=30,dy=dx,flat_tol=1e-12) {
 v<-gradiente_centrato(Z,dx,dy);g<-sqrt(v$gx^2+v$gy^2)
 asp<-(atan2(-v$gx,-v$gy)*180/pi)%%360;asp[!is.finite(g)|g<=flat_tol]<-NA_real_
 c(v,list(g=g,slope_deg=atan(g)*180/pi,slope_pct=100*g,aspect_deg=asp))
}
hillshade_normale <- function(gx,gy,az=315,altezza=45) {
 stopifnot(identical(dim(gx),dim(gy)),altezza>=0,altezza<=90)
 aa<-az*pi/180;hh<-altezza*pi/180
 raw<-(-gx*sin(aa)*cos(hh)-gy*cos(aa)*cos(hh)+sin(hh))/sqrt(1+gx^2+gy^2)
 pmax(raw,0) # La matrice prima dello scalare conserva dim e ordine.
}
media_circolare <- function(gradi,tol=1e-12) {
 a<-gradi[is.finite(gradi)]*pi/180
 if(!length(a))return(c(media_gradi=NA_real_,risultante=NA_real_,n=0))
 s<-mean(sin(a));cc<-mean(cos(a));r<-sqrt(s*s+cc*cc)
 mu<-if(r<=tol)NA_real_ else (atan2(s,cc)*180/pi)%%360
 if(is.finite(mu)&&abs(mu-360)<1e-10)mu<-0
 c(media_gradi=mu,risultante=r,n=length(a))
}
aggrega2 <- function(Z,na.rm=FALSE) {
 stopifnot(nrow(Z)%%2==0,ncol(Z)%%2==0)
 a<-matrix(NA_real_,nrow(Z)/2,ncol(Z)/2)
 for(i in seq_len(nrow(a)))for(j in seq_len(ncol(a)))a[i,j]<-mean(Z[(2*i-1):(2*i),(2*j-1):(2*j)],na.rm=na.rm)
 a
}
indice_normalizzato <- function(N,R,eps=1e-6) {
 stopifnot(length(N)==length(R),eps>=0)
 den<-N+R;ok<-is.finite(N)&is.finite(R)&den>eps
 v<-rep(NA_real_,length(N));v[ok]<-(N[ok]-R[ok])/den[ok]
 list(indice=v,denominatore=den,valido=ok)
}
matrice_df <- function(M,x,y,nome="valore") {
 stopifnot(ncol(M)==length(x),nrow(M)==length(y))
 d<-expand.grid(x_m=x,y_m=y);d[[nome]]<-row_values(M);d
}
raster_locale <- function(M,x,y,dx=30,dy=dx,offset=c(500015,4999295),crs="EPSG:32632") {
 stopifnot(ncol(M)==length(x),nrow(M)==length(y))
 r<-terra::rast(nrows=nrow(M),ncols=ncol(M),xmin=min(x)-dx/2+offset[1],xmax=max(x)+dx/2+offset[1],
  ymin=min(y)-dy/2+offset[2],ymax=max(y)+dy/2+offset[2],crs=crs)
 terra::values(r)<-row_values(M[nrow(M):1,,drop=FALSE]);r
}
matrice_locale <- function(r) {M<-as.matrix(r,wide=TRUE);M[nrow(M):1,,drop=FALSE]}
superficie_analitica <- function(x,y) 900+.12*x+.08*y+80*exp(-((x-450)^2+(y-300)^2)/(2*120^2))
gradiente_analitico <- function(x,y) {
 h<-80*exp(-((x-450)^2+(y-300)^2)/(2*120^2))
 list(gx=.12-(x-450)*h/120^2,gy=.08-(y-300)*h/120^2)
}
pesi_finestra <- function(x,y,h,lim=c(100,800,100,500)) {
 wx<-pmax(0,pmin(x+h/2,lim[2])-pmax(x-h/2,lim[1]));wy<-pmax(0,pmin(y+h/2,lim[4])-pmax(y-h/2,lim[3]));outer(wy,wx)
}
# JSON minimale base R: non richiede pacchetti aggiuntivi per i risultati.
to_json <- function(x) {
 if(is.data.frame(x))return(to_json(lapply(seq_len(nrow(x)),function(i)as.list(x[i,,drop=FALSE]))))
 if(is.list(x)){
  vals<-vapply(x,to_json,"");nm<-names(x)
  if(is.null(nm))return(paste0("[",paste(vals,collapse=","),"]"))
  return(paste0("{",paste(paste0(vapply(nm,to_json,""),":",vals),collapse=","),"}"))
 }
 if(length(x)==0)return("null")
 if(length(x)>1)return(paste0("[",paste(vapply(as.list(x),to_json,""),collapse=","),"]"))
 if(is.na(x)||is.numeric(x)&&!is.finite(x))return("null")
 if(is.logical(x))return(if(x)"true" else "false")
 if(is.numeric(x))return(format(x,digits=16,scientific=FALSE,trim=TRUE))
 encodeString(as.character(x),quote='"')
}
