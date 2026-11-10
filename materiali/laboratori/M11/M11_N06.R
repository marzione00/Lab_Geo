# Rietichettare non significa trasformare
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Nessuna installazione automatica durante l'analisi.
find_root <- function(start=getwd()) {
  p<-normalizePath(start,mustWork=TRUE)
  repeat {
    if(file.exists(file.path(p,'.geologia-v3'))) return(p)
    q<-dirname(p);if(identical(p,q)) stop('Aprire il progetto Corso_Geologia.Rproj.');p<-q
  }
}
root<-find_root();out<-file.path(root,'risultati','R','M11_N06')
dir.create(out,recursive=TRUE,showWarnings=FALSE)
need<-function(pkg) {if(!requireNamespace(pkg,quietly=TRUE)) stop(paste('Installare prima il pacchetto',pkg))}
read_data<-function(name) read.csv(file.path(root,'dati',name),stringsAsFactors=FALSE,check.names=FALSE)
d<-read_data('spazio_v3.csv')
casuali<-read_data('casuali_comuni_v3.csv');u<-casuali$u;z<-casuali$z
set.seed(20261104)
cat('Input:',file.path(root,'dati','spazio_v3.csv'),'\nOutput:',out,'\n')



# Analisi principale: Rietichettare non significa trasformare
need('sf');p<-sf::st_as_sf(d,coords=c('lon','lat'),crs=4326)
err<-sf::st_set_crs(sf::st_set_crs(p,NA),32632);ok<-sf::st_transform(p,32632)
risultato<-data.frame(caso=c('ERRATO','trasformato'),x=c(sf::st_coordinates(err)[1,1],sf::st_coordinates(ok)[1,1]))
stopifnot(abs(risultato$x[1]-d$lon[1])<1e-12)


print(risultato)
write.csv(risultato,file.path(out,'risultato.csv'),row.names=FALSE,na='')


writeLines(capture.output(sessionInfo()),file.path(out,'sessione_R.txt'))
