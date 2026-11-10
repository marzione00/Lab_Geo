# Ignorare file locali: non condividere segreti
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Nessuna installazione automatica durante l'analisi.
find_root <- function(start=getwd()) {
  p<-normalizePath(start,mustWork=TRUE)
  repeat {
    if(file.exists(file.path(p,'.geologia-v3'))) return(p)
    q<-dirname(p);if(identical(p,q)) stop('Aprire il progetto Corso_Geologia.Rproj.');p<-q
  }
}
root<-find_root();out<-file.path(root,'risultati','R','M15_N17')
dir.create(out,recursive=TRUE,showWarnings=FALSE)
need<-function(pkg) {if(!requireNamespace(pkg,quietly=TRUE)) stop(paste('Installare prima il pacchetto',pkg))}
read_data<-function(name) read.csv(file.path(root,'dati',name),stringsAsFactors=FALSE,check.names=FALSE)
d<-read_data('campioni_modulo1.csv')
casuali<-read_data('casuali_comuni_v3.csv');u<-casuali$u;z<-casuali$z
set.seed(20261104)
cat('Input:',file.path(root,'dati','campioni_modulo1.csv'),'\nOutput:',out,'\n')



# Analisi principale: Ignorare file locali: non condividere segreti
p<-file.path(out,'repo_ignore');dir.create(p,showWarnings=FALSE);old<-getwd();setwd(p);stopifnot(nzchar(Sys.which('git')));system2('git',c('init','-q'));writeLines(c('.env','risultati/'),'.gitignore');writeLines('SEGNAPOSTO_NON_SEGRETO','.env');v<-system2('git',c('check-ignore','.env'),stdout=TRUE);setwd(old);risultato<-data.frame(file='.env',ignorato=any(v=='.env'));stopifnot(risultato$ignorato)


print(risultato)
write.csv(risultato,file.path(out,'risultato.csv'),row.names=FALSE,na='')


writeLines(capture.output(sessionInfo()),file.path(out,'sessione_R.txt'))
