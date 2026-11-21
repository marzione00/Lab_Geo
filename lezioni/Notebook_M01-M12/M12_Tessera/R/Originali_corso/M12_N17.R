# Bootstrap di blocchi: un’ipotesi esplicita
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Nessuna installazione automatica durante l'analisi.
find_root <- function(start=getwd()) {
  p<-normalizePath(start,mustWork=TRUE)
  repeat {
    if(file.exists(file.path(p,'.geologia-v3'))) return(p)
    q<-dirname(p);if(identical(p,q)) stop('Aprire il progetto Corso_Geologia.Rproj.');p<-q
  }
}
root<-find_root();out<-file.path(root,'risultati','R','M12_N17')
dir.create(out,recursive=TRUE,showWarnings=FALSE)
need<-function(pkg) {if(!requireNamespace(pkg,quietly=TRUE)) stop(paste('Installare prima il pacchetto',pkg))}
read_data<-function(name) read.csv(file.path(root,'dati',name),stringsAsFactors=FALSE,check.names=FALSE)
d<-read_data('raster_v3.csv')
casuali<-read_data('casuali_comuni_v3.csv');u<-casuali$u;z<-casuali$z
set.seed(20261104)
cat('Input:',file.path(root,'dati','raster_v3.csv'),'\nOutput:',out,'\n')



# Analisi principale: Bootstrap di blocchi: un’ipotesi esplicita
Z<-matrix(d$quota_m,24,byrow=TRUE);v<-numeric(12);k<-1
for(i in 1:4)for(j in 1:3){v[k]<-mean(Z[((i-1)*6+1):(i*6),((j-1)*10+1):(j*10)]);k<-k+1}
ix<-matrix(floor(u[1:3600]*12)+1,300,byrow=TRUE);b<-apply(ix,1,function(i)mean(v[i]));q<-quantile(b,c(.025,.975))
risultato<-data.frame(media=mean(v),basso=q[1],alto=q[2]);stopifnot(abs(mean(v)-mean(Z))<1e-10)


print(risultato)
write.csv(risultato,file.path(out,'risultato.csv'),row.names=FALSE,na='')


writeLines(capture.output(sessionInfo()),file.path(out,'sessione_R.txt'))
