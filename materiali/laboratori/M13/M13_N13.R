# Una lacuna di sedimentazione come scenario
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Nessuna installazione automatica durante l'analisi.
find_root <- function(start=getwd()) {
  p<-normalizePath(start,mustWork=TRUE)
  repeat {
    if(file.exists(file.path(p,'.geologia-v3'))) return(p)
    q<-dirname(p);if(identical(p,q)) stop('Aprire il progetto Corso_Geologia.Rproj.');p<-q
  }
}
root<-find_root();out<-file.path(root,'risultati','R','M13_N13')
dir.create(out,recursive=TRUE,showWarnings=FALSE)
need<-function(pkg) {if(!requireNamespace(pkg,quietly=TRUE)) stop(paste('Installare prima il pacchetto',pkg))}
read_data<-function(name) read.csv(file.path(root,'dati',name),stringsAsFactors=FALSE,check.names=FALSE)
d<-read_data('cronologia_v3.csv')
casuali<-read_data('casuali_comuni_v3.csv');u<-casuali$u;z<-casuali$z
set.seed(20261104)
cat('Input:',file.path(root,'dati','cronologia_v3.csv'),'\nOutput:',out,'\n')



# Analisi principale: Una lacuna di sedimentazione come scenario
p<-read_data('proxy_v3.csv');a<-approx(d$profondita_cm,d$eta_cal_BP,xout=p$profondita_cm)$y;h<-a+ifelse(p$profondita_cm>80,400,0)
risultato<-data.frame(profondita=p$profondita_cm,base=a,hiatus=h);stopifnot(all(diff(h)>0));plot(h,p$profondita_cm,type='l',ylim=c(160,0),xlab='Età',ylab='Profondità')


print(risultato)
write.csv(risultato,file.path(out,'risultato.csv'),row.names=FALSE,na='')


writeLines(capture.output(sessionInfo()),file.path(out,'sessione_R.txt'))
