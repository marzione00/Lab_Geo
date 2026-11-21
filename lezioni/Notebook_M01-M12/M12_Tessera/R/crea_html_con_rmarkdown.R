# Alternativa convenzionale: eseguire gli Rmd con knitr e creare gli HTML.
if(!requireNamespace("rmarkdown",quietly=TRUE))
  stop("Eseguire prima source('R/00_installazione.R').")
for(f in sprintf("M12_N%02d.Rmd",1:20))
  rmarkdown::render(f,encoding="UTF-8",envir=new.env(parent=globalenv()))
