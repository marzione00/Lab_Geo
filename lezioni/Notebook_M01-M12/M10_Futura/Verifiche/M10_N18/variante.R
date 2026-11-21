files <- list.files(dirname(percorso_risultati("scheda_modello.txt")),full.names=TRUE)
data.frame(file=basename(files),bytes=file.info(files)$size)
