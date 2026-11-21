# Alternativa convenzionale: eseguire gli Rmd con knitr e creare gli HTML.
# Aprire GeoStat_Lab_Notebooks.Rproj nella cartella M11_Locus.
# Il registro Verifiche è prodotto separatamente da esegui_notebook.R.
if(!requireNamespace("rmarkdown",quietly=TRUE))
  stop("Eseguire prima source('R/00_installazione.R') per installare rmarkdown e knitr.")
files <- sprintf("M11_N%02d.Rmd",1:20)
for(f in files) rmarkdown::render(f,encoding="UTF-8",envir=new.env(parent=globalenv()))
