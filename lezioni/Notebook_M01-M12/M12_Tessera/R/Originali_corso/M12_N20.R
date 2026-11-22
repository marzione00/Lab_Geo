# Consegna delle pendenze interne
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Nessuna installazione automatica durante l'analisi.
find_root <- function(start=getwd()) {
  p<-normalizePath(start,mustWork=TRUE)
  repeat {
    if(file.exists(file.path(p,'.geologia-v3'))) return(p)
    q<-dirname(p);if(identical(p,q)) stop('Aprire il progetto Corso_Geologia.Rproj.');p<-q
  }
}
root<-find_root();out<-file.path(root,'risultati','R','M12_N20')
dir.create(out,recursive=TRUE,showWarnings=FALSE)
need<-function(pkg) {if(!requireNamespace(pkg,quietly=TRUE)) stop(paste('Installare prima il pacchetto',pkg))}
read_data<-function(name) read.csv(file.path(root,'dati',name),stringsAsFactors=FALSE,check.names=FALSE)
d<-read_data('raster_v3.csv')
casuali<-read_data('casuali_comuni_v3.csv');u<-casuali$u;z<-casuali$z
set.seed(20261104)
cat('Input:',file.path(root,'dati','raster_v3.csv'),'\nOutput:',out,'\n')



# Analisi principale: Consegna delle pendenze interne
Z<-matrix(d$quota_m,24,byrow=TRUE);gx<-(Z[2:23,3:30]-Z[2:23,1:28])/60;gy<-(Z[3:24,2:29]-Z[1:22,2:29])/60
s<-atan(sqrt(gx^2+gy^2))*180/pi
risultato<-data.frame(x_m=rep((1:28)*30,22),y_m=rep((1:22)*30,each=28),pendenza_gradi=as.vector(t(s)))
f<-file.path(out,'pendenze.csv');write.csv(risultato,f,row.names=FALSE);a<-read.csv(f);stopifnot(nrow(a)==616,all(is.finite(a$pendenza_gradi)))


print(risultato)
write.csv(risultato,file.path(out,'risultato.csv'),row.names=FALSE,na='')


writeLines(capture.output(sessionInfo()),file.path(out,'sessione_R.txt'))
