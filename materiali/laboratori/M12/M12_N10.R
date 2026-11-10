# Pendenza in gradi e in percentuale
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Nessuna installazione automatica durante l'analisi.
find_root <- function(start=getwd()) {
  p<-normalizePath(start,mustWork=TRUE)
  repeat {
    if(file.exists(file.path(p,'.geologia-v3'))) return(p)
    q<-dirname(p);if(identical(p,q)) stop('Aprire il progetto Corso_Geologia.Rproj.');p<-q
  }
}
root<-find_root();out<-file.path(root,'risultati','R','M12_N10')
dir.create(out,recursive=TRUE,showWarnings=FALSE)
need<-function(pkg) {if(!requireNamespace(pkg,quietly=TRUE)) stop(paste('Installare prima il pacchetto',pkg))}
read_data<-function(name) read.csv(file.path(root,'dati',name),stringsAsFactors=FALSE,check.names=FALSE)
d<-read_data('raster_v3.csv')
casuali<-read_data('casuali_comuni_v3.csv');u<-casuali$u;z<-casuali$z
set.seed(20261104)
cat('Input:',file.path(root,'dati','raster_v3.csv'),'\nOutput:',out,'\n')



# Analisi principale: Pendenza in gradi e in percentuale
Z<-matrix(d$quota_m,24,byrow=TRUE);gx<-(Z[2:23,3:30]-Z[2:23,1:28])/60;gy<-(Z[3:24,2:29]-Z[1:22,2:29])/60
g<-sqrt(gx^2+gy^2);ang<-atan(g)*180/pi;risultato<-data.frame(gradi=as.vector(t(ang)),percento=as.vector(t(100*g)))
hist(ang,xlab='Gradi',main='Pendenza simulata');stopifnot(all(ang>=0 & ang<90))


print(risultato)
write.csv(risultato,file.path(out,'risultato.csv'),row.names=FALSE,na='')


writeLines(capture.output(sessionInfo()),file.path(out,'sessione_R.txt'))
