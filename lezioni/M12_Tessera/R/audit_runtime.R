source("R/stato_lezione.R",encoding="UTF-8")
print(terra::gdal(lib="all"))
for(nm in c("pendenze_interne","pendenze_con_bordo_NA","quote_maschera")) {
 f<-file.path("Risultati",paste0(nm,".tif"))
 writeLines(terra::describe(f),file.path("Verifiche",paste0("GDAL_",nm,".txt")))
}
cat("RUNTIME E TAG TIFF VERIFICATI\n")
