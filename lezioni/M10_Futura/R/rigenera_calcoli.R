# Futura M10: rigenerazione completa di numeri e figure.
# Usare source("R/rigenera_calcoli.R") dalla cartella del modulo.
# Tutti i modelli seguono il protocollo dichiarato prima dell'apertura del test.
source("setup.R",encoding="UTF-8")
for(p in c("Calcoli","Risultati/Figure","Verifiche")) dir.create(p,recursive=TRUE,showWarnings=FALSE)
set.seed(1010)
write_csv<-function(x,n)write.csv(x,file.path("Calcoli",paste0(n,".csv")),row.names=FALSE,na="")
# Serializzatore del solo riepilogo: nessuna dipendenza da jsonlite.
to_json<-function(x){
 if(is.list(x))return(paste0("{",paste(paste0(encodeString(names(x),quote='"'),":",vapply(x,to_json,"")),collapse=","),"}"))
 if(length(x)>1)return(paste0("[",paste(vapply(as.list(x),to_json,""),collapse=","),"]"))
 if(is.character(x))return(encodeString(x,quote='"'))
 if(is.logical(x))return(ifelse(is.na(x),"null",ifelse(x,"true","false")))
 if(!length(x)||!is.finite(x))return("null")
 format(x,digits=16,scientific=FALSE,trim=TRUE)
}
# CO2: train 1985-1998; verifica finale 1999-2001, origine fissa dicembre 1998.
h<-length(test);fit<-stima_sarima(train);fc<-previsione_sarima(fit,h)
b<-baseline(train,h);predizioni<-c(b,list(SARIMA=fc$previsto))
met<-as.data.frame(do.call(rbind,lapply(predizioni,function(p)metriche(as.numeric(test),p))))
met$modello<-rownames(met);rownames(met)<-NULL;met<-met[,c("modello","MAE","RMSE","bias")]
forecast<-data.frame(data=co2$data[169:204],fc,osservato=as.numeric(test),
                    ultimo=b$Ultimo,stagionale=b$Stagionale,deriva=b$Deriva,media=b$Media)
forecast$errore<-forecast$osservato-forecast$previsto
forecast$coperto95<-forecast$osservato>=forecast$inferiore&forecast$osservato<=forecast$superiore
forecast$blocco<-factor(rep(c("01-12","13-24","25-36"),each=12),levels=c("01-12","13-24","25-36"))
forecast$ampiezza95<-forecast$superiore-forecast$inferiore
write_csv(forecast,"previsioni_CO2");write_csv(met,"metriche_CO2")
cf<-data.frame(termine=names(coef(fit)),stima=as.numeric(coef(fit)),se=sqrt(diag(fit$var.coef)))
write_csv(cf,"coefficienti_SARIMA")
# I residui iniziali risentono dell'inizializzazione diffusa: convenzione del sito, da indice14.
res<-as.numeric(residuals(fit))[14:168];stopifnot(all(is.finite(res)))
lj<-Box.test(res,lag=24,type="Ljung-Box",fitdf=2)
write_csv(data.frame(indice=14:168,data=co2$data[14:168],residuo=res),"residui_SARIMA")
write_csv(data.frame(test="Ljung-Box",lag=24,fitdf=2,df=unname(lj$parameter),statistica=unname(lj$statistic),p=lj$p.value),"diagnostica_SARIMA")
cv<-valida_origini(train);write_csv(cv,"validazione_interna_dettaglio")
cvmet<-do.call(rbind,lapply(split(cv,cv$origine),function(x)data.frame(origine=x$origine[1],
 RMSE_SARIMA=metriche(x$osservato,x$SARIMA)[2],RMSE_stagionale=metriche(x$osservato,x$Stagionale)[2],
 RMSE_deriva=metriche(x$osservato,x$Deriva)[2])))
write_csv(cvmet,"validazione_interna")
# Approfondimento didattico: 37 origini mensili, tutte interne al train.
cvdense<-valida_origini(train,origini=120:156,h=12L);write_csv(cvdense,"origini_mensili_train")
cvh<-do.call(rbind,lapply(split(cvdense,cvdense$h),function(x)data.frame(h=x$h[1],
 MAE_SARIMA=metriche(x$osservato,x$SARIMA)[1],RMSE_SARIMA=metriche(x$osservato,x$SARIMA)[2],
 RMSE_stagionale=metriche(x$osservato,x$Stagionale)[2],copertura95=mean(x$osservato>=x$inferiore&x$osservato<=x$superiore),n_origini=nrow(x))))
cvh<-cvh[order(cvh$h),];write_csv(cvh,"metriche_per_orizzonte_train")
# Copertura descrittiva: i 36 eventi non costituiscono 36 repliche indipendenti.
blocchi<-do.call(rbind,lapply(split(forecast,forecast$blocco),function(x)data.frame(blocco=as.character(x$blocco[1]),
 n=nrow(x),MAE=mean(abs(x$errore)),RMSE=sqrt(mean(x$errore^2)),coperti=sum(x$coperto95),
 copertura=mean(x$coperto95),ampiezza_media=mean(x$ampiezza95))))
write_csv(blocchi,"copertura_blocchi")
# Confronti AIC solo tra specifiche con d,D uguali: esposizione, senza selezione sul test.
candidati<-list(SARIMA011011=c(0,1,1,0,1,1),SARIMA110011=c(1,1,0,0,1,1),SARIMA111011=c(1,1,1,0,1,1))
aic<-do.call(rbind,lapply(names(candidati),function(n){o<-candidati[[n]];f<-stima_sarima(train,o[1:3],o[4:6]);
 data.frame(modello=n,AIC=as.numeric(AIC(f)),BIC=as.numeric(BIC(f)),k=length(coef(f))+1,convergenza=f$code)}))
write_csv(aic,"candidati_train_AIC")
# Fossili: progetto osservazionale su dati simulati.
f<-fossili;stopifnot(nrow(f)==160,!anyDuplicated(f$id),!anyNA(f[c("diametro_tot_um","diametro_int_um")]))
ind_test<-seq(5,nrow(f),by=5);tr<-f[-ind_test,];te<-f[ind_test,]
mod<-lm(diametro_int_um~diametro_tot_um,data=tr)
pf<-as.numeric(predict(mod,newdata=te));bf<-rep(mean(tr$diametro_int_um),nrow(te))
fmet<-data.frame(modello=c("Media_train","Retta"),rbind(metriche(te$diametro_int_um,bf),metriche(te$diametro_int_um,pf)))
write_csv(fmet,"metriche_fossili")
write_csv(data.frame(id=te$id,totale=te$diametro_tot_um,osservato=te$diametro_int_um,previsto=pf,baseline=bf),"previsioni_fossili")
write_csv(data.frame(termine=names(coef(mod)),stima=coef(mod)),"coefficienti_fossili")
ferr<-max(abs(f$diametro_int_um-(f$diametro_tot_um-2*f$spessore_um)))
# VAR(1): stessa finestra e specificazione degli script online.
v<-processi[1:250,c("x_VAR","y_VAR")];vf<-stima_VAR1(v)
vp<-previsione_VAR1(vf,v[nrow(v),],10);vo<-as.matrix(processi[251:260,c("x_VAR","y_VAR")])
vb<-matrix(rep(as.numeric(v[nrow(v),]),each=10),ncol=2)
vmet<-data.frame(variabile=c("X","Y"),RMSE_VAR=sqrt(colMeans((vo-vp)^2)),RMSE_ultimo=sqrt(colMeans((vo-vb)^2)))
gxy<-anova(lm(y~y_lag,data=vf$dati_ritardati),vf$y)
gyx<-anova(lm(x~x_lag,data=vf$dati_ritardati),vf$x)
gp<-c(gxy$`Pr(>F)`[2],gyx$`Pr(>F)`[2]);gf<-c(gxy$F[2],gyx$F[2])
g<-data.frame(direzione=c("X verso Y","Y verso X"),F=gf,df1=1,df2=df.residual(vf$y),p=gp,p_Holm=p.adjust(gp,"holm"))
write_csv(g,"Granger");write_csv(vmet,"metriche_VAR")
write_csv(data.frame(passo=251:260,X_osservata=vo[,1],Y_osservata=vo[,2],X_prevista=vp[,1],Y_prevista=vp[,2],X_ultimo=vb[,1],Y_ultimo=vb[,2]),"previsioni_VAR")
write_csv(data.frame(equazione=c("X","Y"),intercetta=vf$c,coeff_X_lag1=vf$A[,1],coeff_Y_lag1=vf$A[,2]),"coefficienti_VAR")
write_csv(data.frame(reale=Re(vf$autovalori),immaginaria=Im(vf$autovalori),modulo=Mod(vf$autovalori)),"autovalori_VAR")
# Processi teorici e simulazioni: convenzione MA di R con segno positivo.
set.seed(101001);n<-240
arsim<-sapply(c(.2,.65,.95,-.6),function(p)as.numeric(arima.sim(list(ar=p),n=n,n.start=500)))
colnames(arsim)<-c("phi020","phi065","phi095","phim060");write_csv(data.frame(t=1:n,arsim),"AR1_simulazioni")
kat<-0:30;acf_theory<-data.frame(lag=kat,sapply(c(.2,.65,.95,-.6),function(p)p^kat));names(acf_theory)[-1]<-colnames(arsim)
write_csv(acf_theory,"AR1_ACF_teorica")
arfc<-ar1_teoria();write_csv(arfc,"AR1_previsione_teorica")
set.seed(101002);masim<-as.numeric(arima.sim(list(ma=.6),n=n,n.start=500))
armax<-as.numeric(arima.sim(list(ar=.65,ma=.4),n=n,n.start=500))
write_csv(data.frame(t=1:n,MA1=masim,ARMA11=armax),"MA_ARMA_simulazioni")
imp<-data.frame(lag=0:20,AR1=.65^(0:20),MA1=c(1,.6,rep(0,19)),ARMA11=c(1,ARMAtoMA(ar=.65,ma=.4,lag.max=20)))
write_csv(imp,"risposte_impulso")
# Copertura Monte Carlo con parametri noti e origine x0=2: 2000 traiettorie indipendenti.
set.seed(101003);B<-2000L;H<-30L;phi<-.65;x0<-2
paths<-matrix(NA_real_,B,H);st<-rep(x0,B)
for(k in 1:H){st<-phi*st+rnorm(B);paths[,k]<-st}
th<-ar1_teoria(phi=phi,x0=x0,h=H)
mc<-data.frame(h=1:H,media_MC=colMeans(paths),media_teorica=th$media,varianza_MC=apply(paths,2,var),varianza_teorica=th$varianza,
 copertura95=colMeans(sweep(paths,2,th$inferiore,">=")&sweep(paths,2,th$superiore,"<=")),B=B)
write_csv(mc,"AR1_MonteCarlo")
# Verifiche matematiche deterministiche e casi noti.
# Separazione effettiva: alterare l'intero test non cambia il train estratto
# per calendario, le baseline, i coefficienti o la previsione dal dicembre1998.
co2_perturbato<-co2
co2_perturbato$co2_ppm[co2_perturbato$data>=as.Date("1999-01-01")]<-
 co2_perturbato$co2_ppm[co2_perturbato$data>=as.Date("1999-01-01")]+seq_len(36)*1000
train_perturbato<-ts(co2_perturbato$co2_ppm[co2_perturbato$data<as.Date("1999-01-01")],
 start=c(1985,1),frequency=12)
fit_perturbato<-stima_sarima(train_perturbato)
fc_perturbato<-previsione_sarima(fit_perturbato,36)
tests<-data.frame(controllo=c("metriche_caso_noto","AR1_media_h1","AR1_varianza_h1","AR1_varianza_somma",
 "baseline_stagionale_ripetuta","origini_interne_al_train","VAR_ricorsione_h1","SARIMA_36_date","geometria_fossili",
 "test_perturbato_train_identico","test_perturbato_baseline_identiche","test_perturbato_SARIMA_identico"),
 esito=c(isTRUE(all.equal(unname(metriche(c(1,2),c(0,4))),c(1.5,sqrt(2.5),-.5))),
 abs(arfc$media[1]-1.3)<1e-12,abs(arfc$varianza[1]-1)<1e-12,
 max(abs(arfc$varianza-vapply(1:30,function(k)sum(.65^(2*(0:(k-1)))),0)))<1e-12,
 identical(as.numeric(b$Stagionale),rep(as.numeric(tail(train,12)),3)),
 all(cvdense$origine+cvdense$h<=length(train)),
 max(abs(vp[1,]-as.numeric(vf$c+vf$A%*%as.numeric(tail(v,1)))))<1e-12,
 nrow(forecast)==36&&all(forecast$data==co2$data[169:204]),ferr<2e-8,
 identical(train,train_perturbato),identical(b,baseline(train_perturbato,36)),
 max(abs(unlist(fc)-unlist(fc_perturbato)))<1e-12))
stopifnot(all(tests$esito));write.csv(tests,"Verifiche/test_numerici.csv",row.names=FALSE)
# Esportazioni dei modelli e metadati dell'ambiente.
saveRDS(fit,"Risultati/modello_SARIMA.rds");saveRDS(mod,"Risultati/modello_fossili.rds");saveRDS(vf,"Risultati/modello_VAR.rds")
writeLines(capture.output(sessionInfo()),"Verifiche/SESSIONE_R.txt")
summary<-list(edizione="2026-11-20",R=as.character(getRversion()),
 co2=list(n=204,train_n=168,test_n=36,origine="1998-12",test_inizio="1999-01",test_fine="2001-12",formula="SARIMA(0,1,1)(0,1,1)[12] ML senza drift",ma1=unname(coef(fit)[1]),sma1=unname(coef(fit)[2]),sigma2=fit$sigma2,AIC=fit$aic,
 RMSE_SARIMA=met$RMSE[met$modello=="SARIMA"],RMSE_ultimo=met$RMSE[met$modello=="Ultimo"],RMSE_stagionale=met$RMSE[met$modello=="Stagionale"],RMSE_deriva=met$RMSE[met$modello=="Deriva"],
 MAE_SARIMA=met$MAE[met$modello=="SARIMA"],bias_SARIMA=met$bias[met$modello=="SARIMA"],coperti=sum(forecast$coperto95),copertura=mean(forecast$coperto95),LjungBox_Q=unname(lj$statistic),LjungBox_df=unname(lj$parameter),LjungBox_p=lj$p.value),
 fossili=list(n=160,train_n=nrow(tr),test_n=nrow(te),intercetta=unname(coef(mod)[1]),pendenza=unname(coef(mod)[2]),RMSE_retta=fmet$RMSE[2],RMSE_media=fmet$RMSE[1],identita_max_errore=ferr),
 VAR=list(ntrain=250,orizzonte=10,stabile=vf$stabile,raggio_spettrale=max(Mod(vf$autovalori)),RMSE_X=vmet$RMSE_VAR[1],RMSE_Y=vmet$RMSE_VAR[2],RMSE_ultimo_X=vmet$RMSE_ultimo[1],RMSE_ultimo_Y=vmet$RMSE_ultimo[2],Granger_XY_p=g$p[1],Granger_YX_p=g$p[2],Granger_XY_Holm=g$p_Holm[1],Granger_YX_Holm=g$p_Holm[2]),
 verifiche=list(test_n=nrow(tests),tutti_superati=all(tests$esito),origini_protocollo=3,origini_approfondimento=37,repliche_MC=B))
writeLines(to_json(summary),"Calcoli/riassunto.json")
# Figure vettoriali originali: testo ASCII per il font PDF standard.
source("R/genera_figure.R",encoding="UTF-8")
cat("M10: calcoli e figure completati.\n");print(met);print(cvmet);print(fmet);print(vmet);print(g)
