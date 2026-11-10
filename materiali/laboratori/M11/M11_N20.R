# Consegna GeoJSON e verifica del contenuto
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Nessuna installazione automatica durante l'analisi.
find_root <- function(start=getwd()) {
  p<-normalizePath(start,mustWork=TRUE)
  repeat {
    if(file.exists(file.path(p,'.geologia-v3'))) return(p)
    q<-dirname(p);if(identical(p,q)) stop('Aprire il progetto Corso_Geologia.Rproj.');p<-q
  }
}
root<-find_root();out<-file.path(root,'risultati','R','M11_N20')
dir.create(out,recursive=TRUE,showWarnings=FALSE)
need<-function(pkg) {if(!requireNamespace(pkg,quietly=TRUE)) stop(paste('Installare prima il pacchetto',pkg))}
read_data<-function(name) read.csv(file.path(root,'dati',name),stringsAsFactors=FALSE,check.names=FALSE)
d<-read_data('spazio_v3.csv')
casuali<-read_data('casuali_comuni_v3.csv');u<-casuali$u;z<-casuali$z
set.seed(20261104)
cat('Input:',file.path(root,'dati','spazio_v3.csv'),'\nOutput:',out,'\n')



# Analisi principale: Consegna GeoJSON e verifica del contenuto
need('sf');p<-sf::st_as_sf(d,coords=c('lon','lat'),crs=4326);f<-file.path(out,'campioni.geojson')
sf::st_write(p,f,driver='GeoJSON',delete_dsn=TRUE,quiet=TRUE);q<-sf::st_read(f,quiet=TRUE)
risultato<-data.frame(n_scritti=nrow(p),n_riletti=nrow(q),ID_ok=setequal(p$id,q$id));stopifnot(nrow(q)==64,setequal(p$id,q$id))


print(risultato)
write.csv(risultato,file.path(out,'risultato.csv'),row.names=FALSE,na='')


writeLines(capture.output(sessionInfo()),file.path(out,'sessione_R.txt'))
