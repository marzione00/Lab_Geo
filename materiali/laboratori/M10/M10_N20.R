# Laboratorio applicativo — Baseline stagionale
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
ctx <- inizia_notebook("M10_N20")
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


# Preparazione: Valutazione progressiva interna al train
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


# Preparazione: Previsione e intervallo condizionale
fc <- predict(fit,n.ahead=h)
pred_arima <- as.numeric(fc$pred)
se_arima <- as.numeric(fc$se)
limite_inf <- pred_arima-qnorm(.975)*se_arima
limite_sup <- pred_arima+qnorm(.975)*se_arima
date_test <- d$data[d$data>=as.Date("1999-01-01")]
stile_grafico()
plot(d$data,d$co2_ppm,type="n",ylim=range(d$co2_ppm,limite_inf,limite_sup),
     xlab="Data",ylab="CO2 (ppm)",main="Origine fissa: dicembre 1998")
polygon(c(date_test,rev(date_test)),c(limite_inf,rev(limite_sup)),
        col=adjustcolor(palette_geo[1],.18),border=NA)
lines(d$data,d$co2_ppm,col="grey45")
lines(date_test,pred_arima,col=palette_geo[1],lwd=2)
abline(v=as.numeric(as.Date("1999-01-01")),lty=2)
legend("topleft",c("Osservato","SARIMA","Intervallo 95% condizionale"),
       col=c("grey45",palette_geo[1],adjustcolor(palette_geo[1],.4)),lty=c(1,1,1),bty="n")


# Preparazione: Aprire il test e confrontare gli errori
metriche <- function(obs,prev) {
  stopifnot(length(obs)==length(prev),all(is.finite(obs)),all(is.finite(prev)))
  e <- obs-prev
  c(MAE=mean(abs(e)),RMSE=sqrt(mean(e^2)),bias_osservato_meno_previsto=mean(e))
}
predizioni <- list(Ingenuo=pred_naive,Stagionale=pred_stagionale,
                   Deriva=pred_deriva,SARIMA=pred_arima)
ris <- as.data.frame(do.call(rbind,lapply(predizioni,function(pr) metriche(as.numeric(test),pr))))
ris$modello <- rownames(ris); rownames(ris) <- NULL
ris <- ris[c("modello","MAE","RMSE","bias_osservato_meno_previsto")]
ris


# Preparazione: Orizzonte e copertura descrittiva
previsioni <- data.frame(data=date_test,orizzonte=1:h,osservato=as.numeric(test),
                         previsto=pred_arima,limite95_inf=limite_inf,limite95_sup=limite_sup)
previsioni$errore <- previsioni$osservato-previsioni$previsto
previsioni$dentro95 <- with(previsioni,osservato>=limite95_inf & osservato<=limite95_sup)
mean(previsioni$dentro95)
previsioni$blocco <- rep(c("1-12 mesi","13-24 mesi","25-36 mesi"),each=12)
aggregate(abs(errore)~blocco,data=previsioni,FUN=mean)
stile_grafico()
plot(previsioni$orizzonte,previsioni$errore,type="b",pch=19,
     xlab="Mesi dall'origine",ylab="Osservato - previsto (ppm)")
abline(h=0,lty=2)


# Preparazione: Esportare una previsione verificabile
salva_tabella(ris,"metriche_test.csv",ctx$out)
salva_tabella(cv,"validazione_interna_train.csv",ctx$out)
salva_tabella(previsioni,"previsioni_test.csv",ctx$out)
saveRDS(fit,file.path(ctx$out,"modello_SARIMA.rds"))
salva_testo(c("Train: 1985-01 / 1998-12; test: 1999-01 / 2001-12.",
              "Origine fissa dicembre 1998, orizzonte 36 mesi.",
              "SARIMA(0,1,1)(0,1,1)[12], ML, senza drift.",
              "Intervalli gaussiani condizionali; dati storici aggregati del corso.",
              capture.output(ris)),"report_previsione.txt",ctx$out)


# Analisi principale: Laboratorio applicativo — Baseline stagionale
d <- leggi_dati("co2_1985_2001.csv")
tr <- d$co2_ppm[1:168]
rep(tail(tr,12),length.out=18)
