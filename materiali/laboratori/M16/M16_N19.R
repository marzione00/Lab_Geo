# Controesempio di leakage: copiare il target
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Nessuna installazione automatica durante l'analisi.
find_root <- function(start=getwd()) {
  p<-normalizePath(start,mustWork=TRUE)
  repeat {
    if(file.exists(file.path(p,'.geologia-v3'))) return(p)
    q<-dirname(p);if(identical(p,q)) stop('Aprire il progetto Corso_Geologia.Rproj.');p<-q
  }
}
root<-find_root();out<-file.path(root,'risultati','R','M16_N19')
dir.create(out,recursive=TRUE,showWarnings=FALSE)
need<-function(pkg) {if(!requireNamespace(pkg,quietly=TRUE)) stop(paste('Installare prima il pacchetto',pkg))}
read_data<-function(name) read.csv(file.path(root,'dati',name),stringsAsFactors=FALSE,check.names=FALSE)
d<-read_data('ml_v3.csv')
casuali<-read_data('casuali_comuni_v3.csv');u<-casuali$u;z<-casuali$z
set.seed(20261104)
cat('Input:',file.path(root,'dati','ml_v3.csv'),'\nOutput:',out,'\n')



# Analisi principale: Controesempio di leakage: copiare il target
features<-c('SiO2','CaO','MgO','FeO','densita')
tr<-d$split=='train';te<-d$split=='test';lev<-sort(unique(d$litologia))
ytr<-factor(d$litologia[tr],levels=lev);yte<-factor(d$litologia[te],levels=lev)
X<-as.matrix(d[features]);mu<-colMeans(X[tr,,drop=FALSE]);s<-apply(X[tr,,drop=FALSE],2,sd)
Ztr<-scale(X[tr,,drop=FALSE],center=mu,scale=s);Zte<-scale(X[te,,drop=FALSE],center=mu,scale=s)
centroid_predict<-function(A,y,B){lv<-sort(unique(as.character(y)));C<-t(sapply(lv,function(k)colMeans(A[as.character(y)==k,,drop=FALSE])));dist<-sapply(1:nrow(C),function(j)rowSums(sweep(B,2,C[j,],'-')^2));lv[max.col(-dist,ties.method='first')]}
leak<-match(d$litologia,lev);pred<-lev[leak[te]];risultato<-data.frame(caso='ERRATO: target tra le feature',accuracy=mean(pred==yte));stopifnot(risultato$accuracy==1)


print(risultato)
write.csv(risultato,file.path(out,'risultato.csv'),row.names=FALSE,na='')


writeLines(capture.output(sessionInfo()),file.path(out,'sessione_R.txt'))
