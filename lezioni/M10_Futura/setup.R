# Avviare dalla cartella del progetto Futura_M10.Rproj.
stopifnot(file.exists("Dati/co2_1985_2001.csv"),file.exists("R/funzioni_M10.R"))
source("R/funzioni_M10.R",encoding="UTF-8")
co2 <- read.csv("Dati/co2_1985_2001.csv",stringsAsFactors=FALSE)
co2$data<-as.Date(co2$data)
stopifnot(identical(co2$data,seq(as.Date("1985-01-01"),as.Date("2001-12-01"),by="month")),
          nrow(co2)==204L,!anyNA(co2$co2_ppm))
y<-ts(co2$co2_ppm,start=c(1985,1),frequency=12)
train<-window(y,end=c(1998,12));test<-window(y,start=c(1999,1))
stopifnot(length(train)==168L,length(test)==36L)
fossili<-read.csv("Dati/fossili_simulati.csv",stringsAsFactors=FALSE)
processi<-read.csv("Dati/processi_simulati.csv",stringsAsFactors=FALSE)
options(width=96,digits=6)
