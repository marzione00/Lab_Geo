# Bootstrap dei massimi annuali
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Nessuna installazione automatica durante l'analisi.
find_root <- function(start=getwd()) {
  p<-normalizePath(start,mustWork=TRUE)
  repeat {
    if(file.exists(file.path(p,'.geologia-v3'))) return(p)
    q<-dirname(p);if(identical(p,q)) stop('Aprire il progetto Corso_Geologia.Rproj.');p<-q
  }
}
root<-find_root();out<-file.path(root,'risultati','R','M14_N12')
dir.create(out,recursive=TRUE,showWarnings=FALSE)
need<-function(pkg) {if(!requireNamespace(pkg,quietly=TRUE)) stop(paste('Installare prima il pacchetto',pkg))}
read_data<-function(name) read.csv(file.path(root,'dati',name),stringsAsFactors=FALSE,check.names=FALSE)
d<-read_data('estremi_v3.csv')
casuali<-read_data('casuali_comuni_v3.csv');u<-casuali$u;z<-casuali$z
set.seed(20261104)
cat('Input:',file.path(root,'dati','estremi_v3.csv'),'\nOutput:',out,'\n')



# Analisi principale: Bootstrap dei massimi annuali
x<-d$portata_massima_m3s;ix<-matrix(floor(u[1:10000]*100)+1,100,byrow=TRUE);f<-function(y){b<-sd(y)*sqrt(6)/pi;a<-mean(y)-.5772156649015329*b;a-b*log(-log(.99))};v<-apply(ix,1,function(i)f(x[i]));q<-quantile(v,c(.025,.5,.975));risultato<-data.frame(prob=c(.025,.5,.975),livello100=as.numeric(q));stopifnot(all(is.finite(v)))


print(risultato)
write.csv(risultato,file.path(out,'risultato.csv'),row.names=FALSE,na='')


writeLines(capture.output(sessionInfo()),file.path(out,'sessione_R.txt'))
