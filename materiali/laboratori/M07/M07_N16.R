# Approfondimento: risposta binaria e regressione logistica
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
ctx <- inizia_notebook("M07_N16")
set.seed(1014)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Preparazione: Il protocollo prima di guardare gli errori
f <- leggi_dati("fossili_simulati.csv")
f$morfotipo <- factor(f$morfotipo,levels=c("Rounded","Spiky"))
is_test <- seq_len(nrow(f))%%5L==0L
train <- f[!is_test,]
test <- f[is_test,]
stopifnot(nrow(train)==128L,nrow(test)==32L)
stopifnot(length(intersect(train$id,test$id))==0L)
table(insieme=ifelse(is_test,"test","train"),morfotipo=f$morfotipo)


# Preparazione: Una previsione di riferimento
metriche <- function(osservato,previsto) {
  stopifnot(length(osservato)==length(previsto),
            all(is.finite(osservato)),all(is.finite(previsto)))
  c(MAE=mean(abs(osservato-previsto)),
    RMSE=sqrt(mean((osservato-previsto)^2)))
}
media_training <- mean(train$diametro_int_um)
media_training
# Per ora definiamo la regola; il test sarà valutato dopo la scelta.
formule <- list(
  lineare=diametro_int_um~diametro_tot_um,
  con_morfotipo=diametro_int_um~diametro_tot_um+morfotipo,
  polinomio3=diametro_int_um~poly(diametro_tot_um,3))
names(formule)


# Preparazione: Validazione interna: dividere soltanto il training
set.seed(714)
fold <- sample(rep(1:5,length.out=nrow(train)))
cv <- do.call(rbind,lapply(names(formule),function(nome){
  do.call(rbind,lapply(1:5,function(k){
    tr <- train[fold!=k,]
    va <- train[fold==k,]
    m <- lm(formule[[nome]],data=tr)
    pr <- predict(m,newdata=va)
    met <- metriche(va$diametro_int_um,pr)
    data.frame(modello=nome,fold=k,MAE=met["MAE"],RMSE=met["RMSE"])
  }))
}))
media_cv <- aggregate(cbind(MAE,RMSE)~modello,cv,mean)
media_cv
scelto <- media_cv$modello[which.min(media_cv$RMSE)]
scelto


# Preparazione: Ristimare e valutare una volta sul test
finale <- lm(formule[[scelto]],data=train)
p_modello <- as.numeric(predict(finale,newdata=test))
p_base <- rep(media_training,nrow(test))
errori_test <- as.data.frame(rbind(
  media_training=metriche(test$diametro_int_um,p_base),
  modello_selezionato=metriche(test$diametro_int_um,p_modello)))
errori_test$metodo <- rownames(errori_test)
rownames(errori_test) <- NULL
errori_test
previsioni <- data.frame(id=test$id,osservato=test$diametro_int_um,
                         base=p_base,modello=p_modello,
                         errore=test$diametro_int_um-p_modello)
head(previsioni)


# Preparazione: Errore di training e generalizzazione
met_train <- metriche(train$diametro_int_um,predict(finale,newdata=train))
met_test <- metriche(test$diametro_int_um,p_modello)
rbind(training=met_train,test=met_test)
stile_grafico()
plot(test$diametro_int_um,p_modello,pch=19,col=palette_geo[1],
     xlab="Osservato nel test (micrometri)",ylab="Previsto (micrometri)",
     main=paste("Test separato; modello:",scelto))
abline(0,1,lty=2)


# Preparazione: Trasformazioni stimate sul training
mu_x <- mean(train$diametro_tot_um)
sd_x <- sd(train$diametro_tot_um)
stopifnot(sd_x>0)
z_train <- (train$diametro_tot_um-mu_x)/sd_x
z_test <- (test$diametro_tot_um-mu_x)/sd_x
c(media_train=mean(z_train),sd_train=sd(z_train),media_test=mean(z_test))
# Non ricalcoliamo mu e sd sul test. Questo blocco illustra la regola di preprocessing.


# Analisi principale: Approfondimento: risposta binaria e regressione logistica
train$spiky <- as.integer(train$morfotipo=="Spiky")
test$spiky <- as.integer(test$morfotipo=="Spiky")
logit <- glm(spiky~diametro_tot_um+rapporto_int_tot,data=train,family=binomial())
if (!isTRUE(logit$converged)) stop("Logistica non convergente: verificare prima di interpretare.")
prob <- as.numeric(predict(logit,newdata=test,type="response"))
stopifnot(all(is.finite(prob)),all(prob>=0 & prob<=1))
head(data.frame(id=test$id,osservato=test$spiky,probabilita=prob))
coef(logit)
