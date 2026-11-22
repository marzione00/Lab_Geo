# M11 Locus — funzioni verificabili, R standard; sf serve solo alla geometria CRS.
metriche <- function(osservato, previsto) {
 stopifnot(length(osservato)==length(previsto),length(osservato)>0,
           all(is.finite(osservato)),all(is.finite(previsto)))
 e<-osservato-previsto;c(MAE=mean(abs(e)),RMSE=sqrt(mean(e^2)),bias=mean(e))
}
dist_cross <- function(xy,newxy) {
 xy<-as.matrix(xy);newxy<-as.matrix(newxy)
 stopifnot(ncol(xy)==2,ncol(newxy)==2,all(is.finite(xy)),all(is.finite(newxy)))
 sqrt(outer(newxy[,1],xy[,1],"-")^2+outer(newxy[,2],xy[,2],"-")^2)
}
normalizza_righe <- function(A,isolati=c("errore","zero")) {
 isolati<-match.arg(isolati);nv<-rowSums(A)
 if(any(nv==0)&&isolati=="errore")stop("Siti isolati: dichiarare una politica prima di normalizzare.")
 W<-A/pmax(nv,1);W
}
moran_I <- function(z,W) {
 z<-as.numeric(z);W<-as.matrix(W);v<-z-mean(z);n<-length(z)
 stopifnot(all(dim(W)==c(n,n)),all(is.finite(W)),all(is.finite(z)),
           all(diag(W)==0),sum(W)>0,sum(v^2)>0)
 n/sum(W)*sum(W*outer(v,v))/sum(v^2)
}
moran_centrato <- function(v,W)length(v)/sum(W)*sum(W*outer(v,v))/sum(v^2)
haversine <- function(lon1,lat1,lon2,lat2,R=6371000) {
 # Input in gradi, risultato in metri. R=6371km segue M11_N04.
 stopifnot(R>0);a<-pi/180
 h<-sin((lat2-lat1)*a/2)^2+cos(lat1*a)*cos(lat2*a)*sin((lon2-lon1)*a/2)^2
 2*R*asin(sqrt(pmax(0,pmin(1,h))))
}
idw_weights <- function(xy,pos,p=2,tol=1e-10) {
 xy<-as.matrix(xy);stopifnot(ncol(xy)==2,length(pos)==2,p>0,all(is.finite(xy)),all(is.finite(pos)))
 rr<-sqrt(rowSums(sweep(xy,2,pos,"-")^2));same<-rr<=tol
 if(any(same))return(as.numeric(same)/sum(same))
 # Scalare per la distanza minima evita overflow senza cambiare i pesi.
 w<-(rr/min(rr))^(-p);w/sum(w)
}
idw_pred <- function(xy,z,newxy,p=2) {
 newxy<-as.matrix(newxy);stopifnot(length(z)==nrow(xy),all(is.finite(z)),ncol(newxy)==2)
 apply(newxy,1,function(pos)sum(idw_weights(xy,pos,p)*z))
}
nn_pred <- function(xy,z,newxy,tol=1e-10) {
 rr<-dist_cross(xy,newxy)
 apply(rr,1,function(a)mean(z[abs(a-min(a))<=tol]))
}
coppie_spaziali <- function(xy,z,breaks=c(0,300,600,1000,2500)) {
 D<-as.matrix(dist(xy));ij<-which(upper.tri(D),arr.ind=TRUE)
 dx<-abs(xy[ij[,2],1]-xy[ij[,1],1]);dy<-abs(xy[ij[,2],2]-xy[ij[,1],2])
 data.frame(i=ij[,1],j=ij[,2],h=D[ij],gamma=.5*(z[ij[,1]]-z[ij[,2]])^2,
            dx=dx,dy=dy,angolo=atan2(dy,dx)*180/pi,classe=cut(D[ij],breaks,right=TRUE))
}
variogramma_bin <- function(coppie) {
 a<-aggregate(cbind(h,gamma)~classe,coppie,mean)
 a$n<-as.integer(table(coppie$classe)[as.character(a$classe)]);a
}
ok_solve <- function(C,c0,C00,z) {
 C<-as.matrix(C);n<-length(z);c0<-as.numeric(c0)
 stopifnot(all(dim(C)==c(n,n)),length(c0)==n,max(abs(C-t(C)))<1e-10,
           all(is.finite(C)),all(is.finite(z)),C00>0,min(eigen(C,symmetric=TRUE,only.values=TRUE)$values)>0)
 K<-rbind(cbind(C,1),c(rep(1,n),0));sol<-solve(K,c(c0,1))
 lambda<-sol[1:n];mu<-sol[n+1]
 vd<-as.numeric(C00-2*sum(lambda*c0)+t(lambda)%*%C%*%lambda)
 vs<-C00-sum(lambda*c0)-mu
 stopifnot(abs(sum(lambda)-1)<1e-10,abs(vd-vs)<1e-10,vd>=-1e-10)
 list(weights=lambda,mu=mu,prediction=sum(lambda*z),variance=vd,
      variance_direct=vd,variance_system=vs,K=K,c0=c0,C00=C00,C=C)
}
ok_esempio <- function() {
 xy<-cbind(c(0,500,1000),0);target<-c(250,0);z<-c(10,15,12);scala<-800;sigma2<-4
 C<-sigma2*exp(-(as.matrix(dist(xy))/scala)^2)
 c0<-sigma2*exp(-rowSums(sweep(xy,2,target,"-")^2)/scala^2)
 list(xy=xy,target=target,z=z,scala=scala,sigma2=sigma2,C=C,c0=c0,
      fit=ok_solve(C,c0,sigma2,z))
}
to_json <- function(x) {
 if(is.null(x))return("null")
 if(is.list(x)){
  vals<-vapply(x,to_json,"");nm<-names(x)
  if(!is.null(nm)&&all(nzchar(nm)))return(paste0("{",paste(paste0(encodeString(nm,quote='"'),":",vals),collapse=","),"}"))
  return(paste0("[",paste(vals,collapse=","),"]"))
 }
 if(length(x)>1)return(paste0("[",paste(vapply(as.list(x),to_json,""),collapse=","),"]"))
 if(!length(x)||is.na(x))return("null")
 if(is.character(x))return(encodeString(x,quote='"'))
 if(is.logical(x))return(if(x)"true" else "false")
 if(!is.finite(x))return("null")
 format(x,digits=16,scientific=FALSE,trim=TRUE)
}
