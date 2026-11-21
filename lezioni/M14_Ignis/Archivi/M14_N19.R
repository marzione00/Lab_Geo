# Pericolosità ed esposizione: perdita attesa di scenario
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Nessuna installazione automatica durante l'analisi.
find_root <- function(start=getwd()) {
  p<-normalizePath(start,mustWork=TRUE)
  repeat {
    if(file.exists(file.path(p,'.geologia-v3'))) return(p)
    q<-dirname(p);if(identical(p,q)) stop('Aprire il progetto Corso_Geologia.Rproj.');p<-q
  }
}
root<-find_root();out<-file.path(root,'risultati','R','M14_N19')
dir.create(out,recursive=TRUE,showWarnings=FALSE)
need<-function(pkg) {if(!requireNamespace(pkg,quietly=TRUE)) stop(paste('Installare prima il pacchetto',pkg))}
read_data<-function(name) read.csv(file.path(root,'dati',name),stringsAsFactors=FALSE,check.names=FALSE)
d<-read_data('estremi_v3.csv')
casuali<-read_data('casuali_comuni_v3.csv');u<-casuali$u;z<-casuali$z
set.seed(20261104)
cat('Input:',file.path(root,'dati','estremi_v3.csv'),'\nOutput:',out,'\n')



# Analisi principale: Pericolosità ed esposizione: perdita attesa di scenario
p<-c(.08,.015,.005);danno<-c(1e4,1e5,1e6);risultato<-data.frame(classe=c('moderata','alta','molto_alta'),p=p,danno=danno,contributo=p*danno);cat('Perdita attesa',sum(risultato$contributo));stopifnot(sum(p)<=1)


print(risultato)
write.csv(risultato,file.path(out,'risultato.csv'),row.names=FALSE,na='')


writeLines(capture.output(sessionInfo()),file.path(out,'sessione_R.txt'))
