# Valutazione progressiva interna al train
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
ctx <- inizia_notebook("M10_N05")
set.seed(1019)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Preparazione: Fissare l’origine della previsione
d <- leggi_dati("co2_1985_2001.csv")
d$data <- as.Date(d$data)
stopifnot(identical(d$data,seq(as.Date("1985-01-01"),as.Date("2001-12-01"),by="month")))
y <- ts(d$co2_ppm,start=c(1985,1),frequency=12)
train <- window(y,end=c(1998,12))
test <- window(y,start=c(1999,1))
h <- length(test)
stopifnot(length(train)==168,h==36,!anyNA(y))
data.frame(insieme=c("Train","Test"),n=c(length(train),length(test)))


# Preparazione: Modelli di riferimento disponibili all’origine
pred_naive <- rep(as.numeric(tail(train,1)),h)
pred_stagionale <- rep(as.numeric(tail(train,12)),length.out=h)
deriva <- (as.numeric(tail(train,1))-as.numeric(head(train,1)))/(length(train)-1)
pred_deriva <- as.numeric(tail(train,1))+seq_len(h)*deriva
head(data.frame(passo=1:h,naive=pred_naive,stagionale=pred_stagionale,deriva=pred_deriva))


# Preparazione: Stimare il modello sui livelli, non sulle differenze già calcolate
fit <- stats::arima(train,order=c(0,1,1),
                    seasonal=list(order=c(0,1,1),period=12),
                    include.mean=FALSE,method="ML")
if(!is.null(fit$code) && fit$code!=0) stop("Ottimizzazione non convergente: controllare il modello.")
fit
coef(fit)
sqrt(diag(fit$var.coef))
# Un controllo formale dell'ordine indicato resta distinto dalla bontà del modello.
stopifnot(length(coef(fit))==2)


# Preparazione: Residui: controlli prima della previsione
res <- as.numeric(residuals(fit))
res <- res[seq.int(14,length(res))]
res <- res[is.finite(res)]
stile_grafico()
plot(res,type="l",xlab="Indice residuo",ylab="Residuo (ppm)",main="Residui del solo train")
abline(h=0,lty=2)
acf(res,lag.max=36,main="ACF residui del train")
# 24 ritardi, due coefficienti MA stimati: df = 24 - 2.
ljung <- Box.test(res,lag=24,type="Ljung-Box",fitdf=2)
ljung
qqnorm(res,main="Residui: verifica grafica della distribuzione")
qqline(res,col=palette_geo[2])


# Analisi principale: Valutazione progressiva interna al train
origini <- c(120,132,144)
cv <- do.call(rbind,lapply(origini,function(o) {
  tr <- ts(as.numeric(train)[1:o],start=c(1985,1),frequency=12)
  obs <- as.numeric(train)[(o+1):(o+12)]
  mod <- stats::arima(tr,order=c(0,1,1),
                     seasonal=list(order=c(0,1,1),period=12),include.mean=FALSE,method="ML")
  if(!is.null(mod$code) && mod$code!=0) stop("Non convergenza nella validazione interna.")
  pr <- as.numeric(predict(mod,n.ahead=12)$pred)
  sn <- as.numeric(tail(tr,12))
  data.frame(origine=o,RMSE_SARIMA=sqrt(mean((obs-pr)^2)),
             RMSE_stagionale=sqrt(mean((obs-sn)^2)))
}))
cv
