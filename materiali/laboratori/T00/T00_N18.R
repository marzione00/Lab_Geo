# Una copia in memoria non modifica il CSV
# Laboratorio R autonomo; eseguire dalla radice del progetto.

root <- normalizePath(getwd())
while(!file.exists(file.path(root,'.geologia-v3'))) {
 parent <- dirname(root);if(identical(parent,root)) stop('Aprire Corso_Geologia.Rproj');root <- parent
}
setwd(root)
out <- file.path(root,'risultati','R','T00_N18');dir.create(out,recursive=TRUE,showWarnings=FALSE)
d <- read.csv(file.path(root,'dati/campioni_modulo1.csv'))
d$densita_g_cm3 <- d$massa_g/d$volume_cm3
medie <- aggregate(densita_g_cm3~affioramento,d,mean)
cat('Output:',out,'\n')


p <- file.path(root,'dati/campioni_modulo1.csv')
a <- unname(tools::md5sum(p))
copia <- d;copia$nota <- 'solo RAM'
b <- unname(tools::md5sum(p))
stopifnot(identical(a,b))
print(identical(a,b))
