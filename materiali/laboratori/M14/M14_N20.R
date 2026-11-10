# Relazione finale: livello, metodo e condizioni
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Nessuna installazione automatica durante l'analisi.
find_root <- function(start=getwd()) {
  p<-normalizePath(start,mustWork=TRUE)
  repeat {
    if(file.exists(file.path(p,'.geologia-v3'))) return(p)
    q<-dirname(p);if(identical(p,q)) stop('Aprire il progetto Corso_Geologia.Rproj.');p<-q
  }
}
root<-find_root();out<-file.path(root,'risultati','R','M14_N20')
dir.create(out,recursive=TRUE,showWarnings=FALSE)
need<-function(pkg) {if(!requireNamespace(pkg,quietly=TRUE)) stop(paste('Installare prima il pacchetto',pkg))}
read_data<-function(name) read.csv(file.path(root,'dati',name),stringsAsFactors=FALSE,check.names=FALSE)
d<-read_data('estremi_v3.csv')
casuali<-read_data('casuali_comuni_v3.csv');u<-casuali$u;z<-casuali$z
set.seed(20261104)
cat('Input:',file.path(root,'dati','estremi_v3.csv'),'\nOutput:',out,'\n')



# Analisi principale: Relazione finale: livello, metodo e condizioni
x<-d$portata_massima_m3s;b<-sd(x)*sqrt(6)/pi;a<-mean(x)-.5772156649015329*b;T<-c(10,50,100);risultato<-data.frame(T=T,portata_m3_s=a-b*log(-log1p(-1/T)),metodo='Gumbel momenti',origine='simulazione v3');writeLines(c('100 massimi annuali simulati','Ipotesi: indipendenza e stazionarieta','Non usare per progettazione o allerta'),file.path(out,'LIMITI.txt'));stopifnot(all(is.finite(risultato$portata_m3_s)))


print(risultato)
write.csv(risultato,file.path(out,'risultato.csv'),row.names=FALSE,na='')


writeLines(capture.output(sessionInfo()),file.path(out,'sessione_R.txt'))
