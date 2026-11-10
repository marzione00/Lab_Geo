# Mostrare le coppie con segmenti
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Questo blocco prepara soltanto percorsi, funzioni di servizio e riproducibilità.
# Non scarica dati, non installa pacchetti, non elimina oggetti e non modifica i CSV.
trova_radice <- function() {
  p <- normalizePath(getwd(), winslash = "/", mustWork = TRUE)
  repeat {
    if (file.exists(file.path(p, "Notebook_R_Geologia.Rproj"))) return(p)
    genitore <- dirname(p)
    if (identical(p, genitore)) stop("Aprire Notebook_R_Geologia.Rproj e riprovare.")
    p <- genitore
  }
}
root <- trova_radice()
source(file.path(root, "R", "funzioni_comuni.R"), local = TRUE)
ctx <- inizia_notebook("M06_N11")
set.seed(1012)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Preparazione: La coppia è parte del dato
a <- leggi_dati("misure_appaiate_simulate.csv")
richiedi_colonne(a,c("id","prima","dopo"))
stopifnot(nrow(a)==24L,anyDuplicated(a$id)==0L)
stopifnot(all(complete.cases(a[c("prima","dopo")])) )
a$differenza <- a$dopo-a$prima
head(a)
c(media_prima=mean(a$prima),media_dopo=mean(a$dopo),
  media_differenze=mean(a$differenza))


# Analisi principale: Mostrare le coppie con segmenti
stile_grafico()
matplot(c(1,2),t(as.matrix(a[c("prima","dopo")])),type="b",
        pch=19,lty=1,col=adjustcolor(palette_geo[1],alpha.f=.55),xaxt="n",
        xlab="Condizione",ylab="Misura (unità convenzionali)",
        main="Stessi 24 ID prima e dopo")
axis(1,at=1:2,labels=c("Prima","Dopo"))
sum(a$differenza>0)
sum(a$differenza<0)
