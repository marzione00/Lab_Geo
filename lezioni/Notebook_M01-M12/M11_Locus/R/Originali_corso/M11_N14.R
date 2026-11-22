# Un riferimento di permutazione spaziale
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Nessuna installazione automatica durante l'analisi.
find_root <- function(start=getwd()) {
  p<-normalizePath(start,mustWork=TRUE)
  repeat {
    if(file.exists(file.path(p,'.geologia-v3'))) return(p)
    q<-dirname(p);if(identical(p,q)) stop('Aprire il progetto Corso_Geologia.Rproj.');p<-q
  }
}
root<-find_root();out<-file.path(root,'risultati','R','M11_N14')
dir.create(out,recursive=TRUE,showWarnings=FALSE)
need<-function(pkg) {if(!requireNamespace(pkg,quietly=TRUE)) stop(paste('Installare prima il pacchetto',pkg))}
read_data<-function(name) read.csv(file.path(root,'dati',name),stringsAsFactors=FALSE,check.names=FALSE)
d<-read_data('spazio_v3.csv')
casuali<-read_data('casuali_comuni_v3.csv');u<-casuali$u;z<-casuali$z
set.seed(20261104)
cat('Input:',file.path(root,'dati','spazio_v3.csv'),'\nOutput:',out,'\n')



# Analisi principale: Un riferimento di permutazione spaziale
D<-as.matrix(dist(d[c('x_m','y_m')]));W<-1*(D>0&D<=260);v<-d$concentrazione-mean(d$concentrazione)
f<-function(a)length(a)/sum(W)*sum(W*outer(a,a))/sum(a^2)
obs<-f(v);B<-100;null<-sapply(1:B,function(b)f(v[order(u[((b-1)*64+1):(b*64)])]))
p<-(1+sum(null>=obs))/(B+1);risultato<-data.frame(I=obs,p_unilaterale=p,B=B)
hist(null,main='Permutazioni',xlab='Moran I');abline(v=obs,lty=2);stopifnot(p>=1/101)


print(risultato)
write.csv(risultato,file.path(out,'risultato.csv'),row.names=FALSE,na='')


writeLines(capture.output(sessionInfo()),file.path(out,'sessione_R.txt'))
