sed <- c("sabbia", "ghiaia",
         "sabbia", "fango")
freq <- table(sed)
# Categorie con frequenza massima
moda <- names(freq[freq==max(freq)])
moda
