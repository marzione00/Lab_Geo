# Dipendenza: differenze a 30 e 300 metri
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Nessuna installazione automatica durante l'analisi.
find_root <- function(start=getwd()) {
  p<-normalizePath(start,mustWork=TRUE)
  repeat {
    if(file.exists(file.path(p,'.geologia-v3'))) return(p)
    q<-dirname(p);if(identical(p,q)) stop('Aprire il progetto Corso_Geologia.Rproj.');p<-q
  }
}
root<-find_root();out<-file.path(root,'risultati','R','M12_N16')
dir.create(out,recursive=TRUE,showWarnings=FALSE)
need<-function(pkg) {if(!requireNamespace(pkg,quietly=TRUE)) stop(paste('Installare prima il pacchetto',pkg))}
read_data<-function(name) read.csv(file.path(root,'dati',name),stringsAsFactors=FALSE,check.names=FALSE)
d<-read_data('raster_v3.csv')
casuali<-read_data('casuali_comuni_v3.csv');u<-casuali$u;z<-casuali$z
set.seed(20261104)
cat('Input:',file.path(root,'dati','raster_v3.csv'),'\nOutput:',out,'\n')



# Analisi principale: Dipendenza: differenze a 30 e 300 metri
Z<-matrix(d$quota_m,24,byrow=TRUE);v<-as.vector(Z[,2:30]-Z[,1:29]);l<-as.vector(Z[,11:30]-Z[,1:20])
risultato<-data.frame(distanza=c(30,300),media_abs=c(mean(abs(v)),mean(abs(l))));stopifnot(length(v)==696,length(l)==480)


print(risultato)
write.csv(risultato,file.path(out,'risultato.csv'),row.names=FALSE,na='')


writeLines(capture.output(sessionInfo()),file.path(out,'sessione_R.txt'))
