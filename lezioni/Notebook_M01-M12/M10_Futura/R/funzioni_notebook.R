# GeoStat Lab M10 Futura. Funzioni di servizio in R base e stats.
# Nessun download, installazione o modifica dei dati durante l'analisi.
.gs_prepara_notebook <- function(radice, id) {
  uscita <- file.path(radice, "Risultati", id)
  dir.create(uscita, recursive=TRUE, showWarnings=FALSE)
  list(carica_dati=function(nome, ...) {
    read.csv(file.path(radice, "Dati", nome), stringsAsFactors=FALSE,
             check.names=FALSE, ...)
  }, percorso_risultati=function(nome) {
    stopifnot(length(nome)==1L, !grepl("(^/|[.][.])", nome))
    destinazione <- file.path(uscita, nome)
    dir.create(dirname(destinazione), recursive=TRUE, showWarnings=FALSE)
    destinazione
  })
}
palette_geo <- c("#1D7890", "#C57E42", "#7363AA", "#657180")
stile_grafico <- function() {
  par(mar=c(4.2,4.4,3,1), mgp=c(2.7,.7,0), las=1, bty="l",
      col.axis="#253344", col.lab="#253344", col.main="#15283E",
      fg="#253344", bg="white", cex=.94)
}
prepara_co2 <- function(d) {
  d$data <- as.Date(d$data)
  stopifnot(identical(d$data,seq(as.Date("1985-01-01"),
                              as.Date("2001-12-01"),by="month")),
            all(is.finite(d$co2_ppm)), !anyDuplicated(d$data))
  y <- ts(d$co2_ppm,start=c(1985,1),frequency=12)
  list(dati=d, y=y, train=window(y,end=c(1998,12)),
       test=window(y,start=c(1999,1)), h=36L,
       date_test=d$data[169:204])
}
stima_sarima <- function(x) {
  fit <- stats::arima(x,order=c(0,1,1),
    seasonal=list(order=c(0,1,1),period=12),
    include.mean=FALSE,method="ML")
  if (!is.null(fit$code) && fit$code!=0L)
    stop("Ottimizzazione SARIMA non convergente.")
  fit
}
metriche <- function(osservato,previsto) {
  stopifnot(length(osservato)==length(previsto),length(osservato)>0L,
            all(is.finite(osservato)),all(is.finite(previsto)))
  e <- as.numeric(osservato)-as.numeric(previsto)
  c(MAE=mean(abs(e)),RMSE=sqrt(mean(e^2)),
    bias_osservato_meno_previsto=mean(e))
}
baseline_co2 <- function(train,h) {
  x <- as.numeric(train)
  stopifnot(length(x)>=12L,h>=1L,all(is.finite(x)))
  deriva <- (tail(x,1)-head(x,1))/(length(x)-1)
  list(Ultimo=rep(tail(x,1),h),
       Stagionale=rep(tail(x,12),length.out=h),
       Deriva=tail(x,1)+seq_len(h)*deriva,
       Media=rep(mean(x),h))
}
prepara_fossili <- function(f) {
  stopifnot(!anyDuplicated(f$id),nrow(f)==160L,
    all(is.finite(f$diametro_tot_um)),all(is.finite(f$diametro_int_um)),
    all(f$diametro_tot_um>0),all(f$diametro_int_um>0),
    all(f$diametro_int_um<=f$diametro_tot_um))
  test_idx <- seq(5L,nrow(f),by=5L)
  list(train=f[-test_idx,],test=f[test_idx,],test_idx=test_idx)
}
stima_var <- function(p,n_train=250L) {
  v <- p[seq_len(n_train),c("x_VAR","y_VAR")]
  stopifnot(nrow(v)>=4L,!anyNA(v))
  lagged <- data.frame(x=v$x_VAR[-1],y=v$y_VAR[-1],
    x_lag=head(v$x_VAR,-1),y_lag=head(v$y_VAR,-1))
  fit_x <- lm(x~x_lag+y_lag,data=lagged)
  fit_y <- lm(y~x_lag+y_lag,data=lagged)
  A <- rbind(coef(fit_x)[c("x_lag","y_lag")],
             coef(fit_y)[c("x_lag","y_lag")])
  rownames(A) <- c("X","Y"); colnames(A) <- c("X_lag","Y_lag")
  list(v=v,lagged=lagged,fit_x=fit_x,fit_y=fit_y,A=A,
       intercetta=c(coef(fit_x)[1],coef(fit_y)[1]))
}
prevedi_var <- function(mod,h) {
  stato <- as.numeric(tail(mod$v,1))
  out <- matrix(NA_real_,h,2,dimnames=list(NULL,c("X","Y")))
  for(k in seq_len(h)) {
    stato <- as.numeric(mod$intercetta+mod$A%*%stato)
    out[k,] <- stato
  }
  out
}
