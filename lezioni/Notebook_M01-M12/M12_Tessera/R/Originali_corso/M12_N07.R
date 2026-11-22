# Aggregazione 2×2 e conservazione della media
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Nessuna installazione automatica durante l'analisi.
find_root <- function(start=getwd()) {
  p<-normalizePath(start,mustWork=TRUE)
  repeat {
    if(file.exists(file.path(p,'.geologia-v3'))) return(p)
    q<-dirname(p);if(identical(p,q)) stop('Aprire il progetto Corso_Geologia.Rproj.');p<-q
  }
}
root<-find_root();out<-file.path(root,'risultati','R','M12_N07')
dir.create(out,recursive=TRUE,showWarnings=FALSE)
need<-function(pkg) {if(!requireNamespace(pkg,quietly=TRUE)) stop(paste('Installare prima il pacchetto',pkg))}
read_data<-function(name) read.csv(file.path(root,'dati',name),stringsAsFactors=FALSE,check.names=FALSE)
d<-read_data('raster_v3.csv')
casuali<-read_data('casuali_comuni_v3.csv');u<-casuali$u;z<-casuali$z
set.seed(20261104)
cat('Input:',file.path(root,'dati','raster_v3.csv'),'\nOutput:',out,'\n')



# Analisi principale: Aggregazione 2×2 e conservazione della media
Z<-matrix(d$quota_m,24,byrow=TRUE);A<-matrix(NA_real_,12,15)
for(i in 1:12)for(j in 1:15)A[i,j]<-mean(Z[(2*i-1):(2*i),(2*j-1):(2*j)])
risultato<-data.frame(griglia=c('30m','60m'),media=c(mean(Z),mean(A)),massimo=c(max(Z),max(A)));stopifnot(abs(mean(Z)-mean(A))<1e-10,max(A)<=max(Z))


print(risultato)
write.csv(risultato,file.path(out,'risultato.csv'),row.names=FALSE,na='')


writeLines(capture.output(sessionInfo()),file.path(out,'sessione_R.txt'))
