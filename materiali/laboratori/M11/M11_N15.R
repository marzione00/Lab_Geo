# Semivarianza e coppie non indipendenti
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Nessuna installazione automatica durante l'analisi.
find_root <- function(start=getwd()) {
  p<-normalizePath(start,mustWork=TRUE)
  repeat {
    if(file.exists(file.path(p,'.geologia-v3'))) return(p)
    q<-dirname(p);if(identical(p,q)) stop('Aprire il progetto Corso_Geologia.Rproj.');p<-q
  }
}
root<-find_root();out<-file.path(root,'risultati','R','M11_N15')
dir.create(out,recursive=TRUE,showWarnings=FALSE)
need<-function(pkg) {if(!requireNamespace(pkg,quietly=TRUE)) stop(paste('Installare prima il pacchetto',pkg))}
read_data<-function(name) read.csv(file.path(root,'dati',name),stringsAsFactors=FALSE,check.names=FALSE)
d<-read_data('spazio_v3.csv')
casuali<-read_data('casuali_comuni_v3.csv');u<-casuali$u;z<-casuali$z
set.seed(20261104)
cat('Input:',file.path(root,'dati','spazio_v3.csv'),'\nOutput:',out,'\n')



# Analisi principale: Semivarianza e coppie non indipendenti
D<-as.matrix(dist(d[c('x_m','y_m')]));G<-.5*outer(d$concentrazione,d$concentrazione,'-')^2;s<-upper.tri(D)
a<-data.frame(h=D[s],gamma=G[s]);a$classe<-cut(a$h,c(0,300,600,1000,2500))
risultato<-aggregate(cbind(h,gamma)~classe,a,mean);risultato$n<-as.numeric(table(a$classe))
stopifnot(sum(risultato$n)==choose(nrow(d),2));plot(risultato$h,risultato$gamma,type='b',xlab='Distanza (m)',ylab='Semivarianza')


print(risultato)
write.csv(risultato,file.path(out,'risultato.csv'),row.names=FALSE,na='')


writeLines(capture.output(sessionInfo()),file.path(out,'sessione_R.txt'))
