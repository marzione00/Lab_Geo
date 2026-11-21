# Valori del modulo Annula, ricalcolati dal CSV originale.
# Eseguire dalla radice del progetto Annula.
radice <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
while (!file.exists(file.path(radice,"Dati","fossili_simulati.csv"))) {
  padre <- dirname(radice)
  if (padre==radice) stop("Aprire il progetto Annula e riprovare.")
  radice <- padre
}
f <- read.csv(file.path(radice,"Dati","fossili_simulati.csv"))
f$morfotipo <- factor(f$morfotipo, levels=c("Rounded","Spiky"))
x <- f$diametro_tot_um; y <- f$diametro_int_um
m <- lm(diametro_int_um ~ diametro_tot_um, data=f)
mi <- lm(diametro_int_um ~ diametro_tot_um*morfotipo, data=f)
ma <- lm(diametro_int_um ~ diametro_tot_um+morfotipo, data=f)
out <- file.path(radice,"Calcoli")
dir.create(out,showWarnings=FALSE)
salva <- function(z,nome) write.csv(z,file.path(out,paste0(nome,".csv")),row.names=FALSE)
salva(data.frame(id=f$id,gruppo=f$morfotipo,x=x,y=y,
                fitted=fitted(m),residuo=resid(m),
                leverage=hatvalues(m),Cook=cooks.distance(m),
                residuo_standard=rstandard(m)),"osservazioni")
salva(data.frame(termine=names(coef(m)),stima=coef(m),confint(m),check.names=FALSE),"coefficienti_lineari")
salva(data.frame(termine=names(coef(mi)),stima=coef(mi),confint(mi),check.names=FALSE),"coefficienti_interazione")
salva(data.frame(termine=names(coef(ma)),stima=coef(ma),confint(ma),check.names=FALSE),"coefficienti_additivi")
val <- c(n=nrow(f),xmin=min(x),xmax=max(x),ymin=min(y),ymax=max(y),xmedio=mean(x),ymedio=mean(y),
         Pearson=cor(x,y),Spearman=cor(x,y,method="spearman"),
         intercetta=coef(m)[1],pendenza=coef(m)[2],R2=summary(m)$r.squared,
         SD_residua=summary(m)$sigma,RMSE_in_sample=sqrt(mean(resid(m)^2)),
         SSE=sum(resid(m)^2),SST=sum((y-mean(y))^2),df=df.residual(m),
         identita_max=max(abs(x-y-2*f$spessore_um)),
         pendenza_Rounded=coef(mi)[2],pendenza_Spiky=coef(mi)[2]+coef(mi)[4],
         contrasto_a_7=coef(mi)[3]+7*coef(mi)[4])
grid <- data.frame(diametro_tot_um=seq(min(x),max(x),length.out=121))
ic <- predict(m,grid,interval="confidence");ip <- predict(m,grid,interval="prediction")
salva(data.frame(x=grid$diametro_tot_um,fit=ic[,1],ic_lwr=ic[,2],ic_upr=ic[,3],
                 ip_lwr=ip[,2],ip_upr=ip[,3]),"intervalli_griglia")
x0 <- data.frame(diametro_tot_um=c(5,7,9,11))
ic0 <- predict(m,x0,interval="confidence");ip0 <- predict(m,x0,interval="prediction")
salva(data.frame(x=x0$diametro_tot_um,fit=ic0[,1],ic_lwr=ic0[,2],ic_upr=ic0[,3],
                 ip_lwr=ip0[,2],ip_upr=ip0[,3]),"intervalli_esempi")
is_test <- seq_len(nrow(f))%%5L==0L
train <- f[!is_test,]; test <- f[is_test,]
metriche <- function(y,p) c(MAE=mean(abs(y-p)),RMSE=sqrt(mean((y-p)^2)))
formule <- list(lineare=diametro_int_um~diametro_tot_um,
 con_morfotipo=diametro_int_um~diametro_tot_um+morfotipo,
 polinomio3=diametro_int_um~poly(diametro_tot_um,3))
set.seed(714);fold <- sample(rep(1:5,length.out=nrow(train)))
cv <- do.call(rbind,lapply(names(formule),function(nome) {
 do.call(rbind,lapply(1:5,function(k) {
  fit <- lm(formule[[nome]],data=train[fold!=k,])
  v <- metriche(train$diametro_int_um[fold==k],predict(fit,newdata=train[fold==k,]))
  data.frame(modello=nome,fold=k,MAE=unname(v[1]),RMSE=unname(v[2]))
 }))
}))
medie_cv <- aggregate(cbind(MAE,RMSE)~modello,cv,mean)
scelto <- medie_cv$modello[which.min(medie_cv$RMSE)]
finale <- lm(formule[[scelto]],data=train)
pred <- predict(finale,newdata=test)
base <- rep(mean(train$diametro_int_um),nrow(test))
mt <- metriche(test$diametro_int_um,pred); mb <- metriche(test$diametro_int_um,base)
salva(cv,"cv_fold");salva(medie_cv,"cv_modelli")
salva(data.frame(metodo=c("media_training",scelto),MAE=c(mb[1],mt[1]),RMSE=c(mb[2],mt[2])),"metriche_test")
salva(data.frame(id=test$id,y=test$diametro_int_um,previsto=pred,base=base),"previsioni_test")
salva(data.frame(id=f$id,insieme=ifelse(is_test,"test","train")),"partizione")
val <- c(val,n_train=nrow(train),n_test=nrow(test),media_training=mean(train$diametro_int_um),
         test_MAE=mt[1],test_RMSE=mt[2],test_base_MAE=mb[1],test_base_RMSE=mb[2])
train$spiky <- as.integer(train$morfotipo=="Spiky");test$spiky <- as.integer(test$morfotipo=="Spiky")
logit <- glm(spiky~diametro_tot_um+rapporto_int_tot,data=train,family=binomial())
stopifnot(logit$converged)
prob <- predict(logit,test,type="response")
salva(data.frame(termine=names(coef(logit)),stima=coef(logit),OR=exp(coef(logit))),"coefficienti_logistica")
salva(data.frame(id=test$id,osservato=test$spiky,probabilita=prob,classe=as.integer(prob>=.5)),"probabilita_test")
val <- c(val,Brier=mean((prob-test$spiky)^2),Brier_base=mean((mean(train$spiky)-test$spiky)^2),
         accuracy=mean((prob>=.5)==test$spiky),soglia=.5)
z <- data.frame(prob=prob,osservato=test$spiky,fascia=cut(prob,seq(0,1,.2),include.lowest=TRUE))
cal <- aggregate(cbind(prob,osservato)~fascia,z,mean)
nc <- aggregate(osservato~fascia,z,length);names(nc)[2]<-"n"
salva(merge(cal,nc,by="fascia"),"calibrazione")
salva(as.data.frame(table(osservato=factor(test$spiky,levels=0:1),previsto=factor(prob>=.5,levels=c(FALSE,TRUE)))),"confusione")
salva(data.frame(nome=names(val),valore=unname(val)),"valori")
writeLines(scelto,file.path(out,"modello_selezionato.txt"))
writeLines(R.version.string,file.path(out,"ambiente.txt"))
stopifnot(length(intersect(train$id,test$id))==0L,all(prob>=0 & prob<=1),
 max(abs(unname(coef(m))-c(mean(y)-cov(x,y)/var(x)*mean(x),cov(x,y)/var(x))))<1e-10,
 all(ip[,3]-ip[,2]>ic[,3]-ic[,2]),max(abs(crossprod(model.matrix(m),resid(m))))<1e-9)
print(val)
print(medie_cv)
