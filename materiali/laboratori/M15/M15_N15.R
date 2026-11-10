# Git locale: creare un commit senza account
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Nessuna installazione automatica durante l'analisi.
find_root <- function(start=getwd()) {
  p<-normalizePath(start,mustWork=TRUE)
  repeat {
    if(file.exists(file.path(p,'.geologia-v3'))) return(p)
    q<-dirname(p);if(identical(p,q)) stop('Aprire il progetto Corso_Geologia.Rproj.');p<-q
  }
}
root<-find_root();out<-file.path(root,'risultati','R','M15_N15')
dir.create(out,recursive=TRUE,showWarnings=FALSE)
need<-function(pkg) {if(!requireNamespace(pkg,quietly=TRUE)) stop(paste('Installare prima il pacchetto',pkg))}
read_data<-function(name) read.csv(file.path(root,'dati',name),stringsAsFactors=FALSE,check.names=FALSE)
d<-read_data('campioni_modulo1.csv')
casuali<-read_data('casuali_comuni_v3.csv');u<-casuali$u;z<-casuali$z
set.seed(20261104)
cat('Input:',file.path(root,'dati','campioni_modulo1.csv'),'\nOutput:',out,'\n')



# Analisi principale: Git locale: creare un commit senza account
stopifnot(nzchar(Sys.which('git')));p<-file.path(out,'repo');dir.create(p,showWarnings=FALSE);old<-getwd();setwd(p);writeLines('Caso didattico v3','README.md');system2('git',c('init','-q'));system2('git',c('add','README.md'));system2('git',c('-c','user.name=Corso','-c','user.email=corso@example.invalid','commit','-q','--allow-empty','-m','inizio'));h<-system2('git',c('rev-parse','HEAD'),stdout=TRUE);setwd(old);risultato<-data.frame(commit=h);stopifnot(nchar(h[1])>=40)


print(risultato)
write.csv(risultato,file.path(out,'risultato.csv'),row.names=FALSE,na='')


writeLines(capture.output(sessionInfo()),file.path(out,'sessione_R.txt'))
