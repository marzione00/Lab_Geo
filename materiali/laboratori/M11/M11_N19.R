# Validazione spaziale: lasciare fuori Est
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Nessuna installazione automatica durante l'analisi.
find_root <- function(start=getwd()) {
  p<-normalizePath(start,mustWork=TRUE)
  repeat {
    if(file.exists(file.path(p,'.geologia-v3'))) return(p)
    q<-dirname(p);if(identical(p,q)) stop('Aprire il progetto Corso_Geologia.Rproj.');p<-q
  }
}
root<-find_root();out<-file.path(root,'risultati','R','M11_N19')
dir.create(out,recursive=TRUE,showWarnings=FALSE)
need<-function(pkg) {if(!requireNamespace(pkg,quietly=TRUE)) stop(paste('Installare prima il pacchetto',pkg))}
read_data<-function(name) read.csv(file.path(root,'dati',name),stringsAsFactors=FALSE,check.names=FALSE)
d<-read_data('spazio_v3.csv')
casuali<-read_data('casuali_comuni_v3.csv');u<-casuali$u;z<-casuali$z
set.seed(20261104)
cat('Input:',file.path(root,'dati','spazio_v3.csv'),'\nOutput:',out,'\n')



# Analisi principale: Validazione spaziale: lasciare fuori Est
tr<-d$x_m<1250;te<-!tr
q<-sapply(which(te),function(i){r<-sqrt((d$x_m[tr]-d$x_m[i])^2+(d$y_m[tr]-d$y_m[i])^2);w<-r^-2;sum(w*d$concentrazione[tr])/sum(w)})
e<-d$concentrazione[te]-q;risultato<-data.frame(n_train=sum(tr),n_test=sum(te),MAE=mean(abs(e)),RMSE=sqrt(mean(e^2)))
stopifnot(all(is.finite(q)),!any(tr&te))


print(risultato)
write.csv(risultato,file.path(out,'risultato.csv'),row.names=FALSE,na='')


writeLines(capture.output(sessionInfo()),file.path(out,'sessione_R.txt'))
