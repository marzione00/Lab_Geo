# Quote continue e classi discrete richiedono ricampionamenti diversi
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Nessuna installazione automatica durante l'analisi.
find_root <- function(start=getwd()) {
  p<-normalizePath(start,mustWork=TRUE)
  repeat {
    if(file.exists(file.path(p,'.geologia-v3'))) return(p)
    q<-dirname(p);if(identical(p,q)) stop('Aprire il progetto Corso_Geologia.Rproj.');p<-q
  }
}
root<-find_root();out<-file.path(root,'risultati','R','M12_N08')
dir.create(out,recursive=TRUE,showWarnings=FALSE)
need<-function(pkg) {if(!requireNamespace(pkg,quietly=TRUE)) stop(paste('Installare prima il pacchetto',pkg))}
read_data<-function(name) read.csv(file.path(root,'dati',name),stringsAsFactors=FALSE,check.names=FALSE)
d<-read_data('raster_v3.csv')
casuali<-read_data('casuali_comuni_v3.csv');u<-casuali$u;z<-casuali$z
set.seed(20261104)
cat('Input:',file.path(root,'dati','raster_v3.csv'),'\nOutput:',out,'\n')



# Analisi principale: Quote continue e classi discrete richiedono ricampionamenti diversi
x<-c(0,30,60,90);cl<-c(1,1,2,2);q<-seq(0,90,15);lin<-approx(x,cl,xout=q)$y;vic<-sapply(q,function(v)cl[which.min(abs(x-v))])
risultato<-data.frame(x=q,lineare_ERRATO=lin,vicino=vic);stopifnot(any(!lin %in% c(1,2)),all(vic %in% c(1,2)))


print(risultato)
write.csv(risultato,file.path(out,'risultato.csv'),row.names=FALSE,na='')


writeLines(capture.output(sessionInfo()),file.path(out,'sessione_R.txt'))
