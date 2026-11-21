# Stato didattico leggero per eseguire i frammenti delle slide in sequenza.
# Eseguire dalla radice del progetto. Non scrive file e non genera figure.
source("setup.R",encoding="UTF-8")
d <- co2
h <- length(test)
fit <- stima_sarima(train)
fc <- previsione_sarima(fit,h)
b <- baseline(train,h)
res <- as.numeric(residuals(fit))[14:168]
cv <- valida_origini(train)
fossili_indice_test <- seq(5,nrow(fossili),by=5)
fossilitrain <- fossili[-fossili_indice_test,]
fossilitest <- fossili[fossili_indice_test,]
fossilifit <- lm(diametro_int_um~diametro_tot_um,data=fossilitrain)
v <- processi[1:250,c("x_VAR","y_VAR")]
varfit <- stima_VAR1(v)
varpred <- previsione_VAR1(varfit,tail(v,1),10L)
invisible(TRUE)
