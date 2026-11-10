# Durata di un intervallo e dipendenza delle età
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Nessuna installazione automatica durante l'analisi.
find_root <- function(start=getwd()) {
  p<-normalizePath(start,mustWork=TRUE)
  repeat {
    if(file.exists(file.path(p,'.geologia-v3'))) return(p)
    q<-dirname(p);if(identical(p,q)) stop('Aprire il progetto Corso_Geologia.Rproj.');p<-q
  }
}
root<-find_root();out<-file.path(root,'risultati','R','M13_N18')
dir.create(out,recursive=TRUE,showWarnings=FALSE)
need<-function(pkg) {if(!requireNamespace(pkg,quietly=TRUE)) stop(paste('Installare prima il pacchetto',pkg))}
read_data<-function(name) read.csv(file.path(root,'dati',name),stringsAsFactors=FALSE,check.names=FALSE)
d<-read_data('cronologia_v3.csv')
casuali<-read_data('casuali_comuni_v3.csv');u<-casuali$u;z<-casuali$z
set.seed(20261104)
cat('Input:',file.path(root,'dati','cronologia_v3.csv'),'\nOutput:',out,'\n')



# Analisi principale: Durata di un intervallo e dipendenza delle età
A<-sweep(sweep(matrix(z[1:3000],500,6,byrow=TRUE),2,d$sd_scenario_anni,'*'),2,d$eta_cal_BP,'+');A<-A[apply(A,1,function(a)all(diff(a)>0)),,drop=FALSE]
v<-t(apply(A,1,function(a)approx(d$profondita_cm,a,xout=c(60,100))$y));dur<-v[,2]-v[,1];q<-quantile(dur,c(.025,.5,.975))
risultato<-data.frame(prob=c(.025,.5,.975),durata=as.numeric(q));stopifnot(all(dur>0))


print(risultato)
write.csv(risultato,file.path(out,'risultato.csv'),row.names=FALSE,na='')


writeLines(capture.output(sessionInfo()),file.path(out,'sessione_R.txt'))
