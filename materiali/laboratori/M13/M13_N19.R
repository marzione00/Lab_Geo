# Una cronologia con metadati riproducibili
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Nessuna installazione automatica durante l'analisi.
find_root <- function(start=getwd()) {
  p<-normalizePath(start,mustWork=TRUE)
  repeat {
    if(file.exists(file.path(p,'.geologia-v3'))) return(p)
    q<-dirname(p);if(identical(p,q)) stop('Aprire il progetto Corso_Geologia.Rproj.');p<-q
  }
}
root<-find_root();out<-file.path(root,'risultati','R','M13_N19')
dir.create(out,recursive=TRUE,showWarnings=FALSE)
need<-function(pkg) {if(!requireNamespace(pkg,quietly=TRUE)) stop(paste('Installare prima il pacchetto',pkg))}
read_data<-function(name) read.csv(file.path(root,'dati',name),stringsAsFactors=FALSE,check.names=FALSE)
d<-read_data('cronologia_v3.csv')
casuali<-read_data('casuali_comuni_v3.csv');u<-casuali$u;z<-casuali$z
set.seed(20261104)
cat('Input:',file.path(root,'dati','cronologia_v3.csv'),'\nOutput:',out,'\n')



# Analisi principale: Una cronologia con metadati riproducibili
q<-seq(0,160,2);risultato<-data.frame(profondita_cm=q,eta_cal_BP=approx(d$profondita_cm,d$eta_cal_BP,xout=q)$y)
f<-file.path(out,'cronologia.csv');write.csv(risultato,f,row.names=FALSE);writeLines(c('Dati sintetici v3','BP: 1950','Metodo: lineare a tratti','Dominio: 0-160 cm','SD: scenario didattico, non datazioni pubblicate'),file.path(out,'METADATI.txt'))
stopifnot(nrow(read.csv(f))==81)


print(risultato)
write.csv(risultato,file.path(out,'risultato.csv'),row.names=FALSE,na='')


writeLines(capture.output(sessionInfo()),file.path(out,'sessione_R.txt'))
