# Soglia decisionale: probabilità e scelta
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Nessuna installazione automatica durante l'analisi.
find_root <- function(start=getwd()) {
  p<-normalizePath(start,mustWork=TRUE)
  repeat {
    if(file.exists(file.path(p,'.geologia-v3'))) return(p)
    q<-dirname(p);if(identical(p,q)) stop('Aprire il progetto Corso_Geologia.Rproj.');p<-q
  }
}
root<-find_root();out<-file.path(root,'risultati','R','M16_N16')
dir.create(out,recursive=TRUE,showWarnings=FALSE)
need<-function(pkg) {if(!requireNamespace(pkg,quietly=TRUE)) stop(paste('Installare prima il pacchetto',pkg))}
read_data<-function(name) read.csv(file.path(root,'dati',name),stringsAsFactors=FALSE,check.names=FALSE)
d<-read_data('ml_v3.csv')
casuali<-read_data('casuali_comuni_v3.csv');u<-casuali$u;z<-casuali$z
set.seed(20261104)
cat('Input:',file.path(root,'dati','ml_v3.csv'),'\nOutput:',out,'\n')



# Analisi principale: Soglia decisionale: probabilità e scelta
features<-c('SiO2','CaO','MgO','FeO','densita')
tr<-d$split=='train';te<-d$split=='test';lev<-sort(unique(d$litologia))
ytr<-factor(d$litologia[tr],levels=lev);yte<-factor(d$litologia[te],levels=lev)
X<-as.matrix(d[features]);mu<-colMeans(X[tr,,drop=FALSE]);s<-apply(X[tr,,drop=FALSE],2,sd)
Ztr<-scale(X[tr,,drop=FALSE],center=mu,scale=s);Zte<-scale(X[te,,drop=FALSE],center=mu,scale=s)
centroid_predict<-function(A,y,B){lv<-sort(unique(as.character(y)));C<-t(sapply(lv,function(k)colMeans(A[as.character(y)==k,,drop=FALSE])));dist<-sapply(1:nrow(C),function(j)rowSums(sweep(B,2,C[j,],'-')^2));lv[max.col(-dist,ties.method='first')]}
a<-data.frame(y=as.integer(ytr=='Basalto'),dens=Ztr[,5]);f<-glm(y~dens,a,family=binomial());p<-predict(f,data.frame(dens=Zte[,5]),type='response');th<-c(.2,.5,.8);risultato<-data.frame(soglia=th,n_positivi=sapply(th,function(v)sum(p>=v)));stopifnot(all(diff(risultato$n_positivi)<=0))


print(risultato)
write.csv(risultato,file.path(out,'risultato.csv'),row.names=FALSE,na='')


writeLines(capture.output(sessionInfo()),file.path(out,'sessione_R.txt'))
