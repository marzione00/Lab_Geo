# Scrivere una funzione riutilizzabile
# Laboratorio R autonomo; eseguire dalla radice del progetto.

root <- normalizePath(getwd())
while(!file.exists(file.path(root,'.geologia-v3'))) {
 parent <- dirname(root);if(identical(parent,root)) stop('Aprire Corso_Geologia.Rproj');root <- parent
}
setwd(root)
out <- file.path(root,'risultati','R','T00_N05');dir.create(out,recursive=TRUE,showWarnings=FALSE)
d <- read.csv(file.path(root,'dati/campioni_modulo1.csv'))
d$densita_g_cm3 <- d$massa_g/d$volume_cm3
medie <- aggregate(densita_g_cm3~affioramento,d,mean)
cat('Output:',out,'\n')


densita <- function(m, v) {
  if (v <= 0) stop("Controllare v")
  m / v
}
print(densita(107.2, 40))

