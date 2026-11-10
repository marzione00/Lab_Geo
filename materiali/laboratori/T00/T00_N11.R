# Raggruppare cambia l’unità della tabella
# Laboratorio R autonomo; eseguire dalla radice del progetto.

root <- normalizePath(getwd())
while(!file.exists(file.path(root,'.geologia-v3'))) {
 parent <- dirname(root);if(identical(parent,root)) stop('Aprire Corso_Geologia.Rproj');root <- parent
}
setwd(root)
out <- file.path(root,'risultati','R','T00_N11');dir.create(out,recursive=TRUE,showWarnings=FALSE)
d <- read.csv(file.path(root,'dati/campioni_modulo1.csv'))
d$densita_g_cm3 <- d$massa_g/d$volume_cm3
medie <- aggregate(densita_g_cm3~affioramento,d,mean)
cat('Output:',out,'\n')


medie <- aggregate(
  densita_g_cm3 ~ affioramento,
  data = d, FUN = mean
)
print(medie)

