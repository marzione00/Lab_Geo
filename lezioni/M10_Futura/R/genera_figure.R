# Figure quantitative derivate dagli oggetti di rigenera_calcoli.R.
# Tutte le coordinate dipendono da dati o da formule dichiarate.
C<-c(blu="#1D7890",rame="#C57E42",viola="#7363AA",verde="#087C74",grigio="#657180",ink="#253344",paper="#F8F6F1")
files_fig<-character()
fig<-function(nome,expr,w=5.8,hh=3.1,ps=16){
 file<-file.path("Risultati/Figure",paste0(nome,".pdf"));files_fig<<-c(files_fig,file)
 pdf(file,width=w,height=hh,pointsize=ps,family="Helvetica",bg=C["paper"],useDingbats=FALSE)
 par(mar=c(4.1,4.4,1.25,1.0),mgp=c(2.5,.7,0),tcl=-.25,col=C["ink"],col.axis=C["grigio"],col.lab=C["ink"],fg=C["ink"],las=1,bty="l",cex.axis=.88,cex.lab=.92)
 eval.parent(substitute(expr));invisible(dev.off())
}
leg<-function(x="topleft",legend,col,lty=1,pch=NULL,cex=.8,...)
 legend(x,legend=legend,col=col,lty=lty,pch=pch,bty="n",cex=cex,inset=.01,...)
grid_y<-function()abline(h=axTicks(2),col=adjustcolor(C["grigio"],.17),lwd=.6)

fig("01_CO2_finestra",{
 plot(co2$data,co2$co2_ppm,type="n",xlab="Anno",ylab="CO2 (ppm)");grid_y()
 lines(co2$data[1:168],co2$co2_ppm[1:168],col=C["blu"],lwd=1.7)
 lines(co2$data[169:204],co2$co2_ppm[169:204],col=C["rame"],lwd=1.7)
 abline(v=as.numeric(as.Date("1999-01-01")),lty=3,col=C["ink"])
 leg(legend=c("Train: 168 mesi","Test: 36 mesi"),col=C[c("blu","rame")])
})
fig("02_baseline_CO2",{
 ix<-145:204;plot(co2$data[ix],co2$co2_ppm[ix],type="n",xlab="Anno",ylab="CO2 (ppm)",ylim=range(co2$co2_ppm[ix],b$Ultimo,b$Deriva,b$Stagionale)+c(0,3));grid_y()
 lines(co2$data[145:168],co2$co2_ppm[145:168],col=C["ink"],lwd=1.6)
 for(j in 1:3)lines(forecast$data,list(b$Ultimo,b$Stagionale,b$Deriva)[[j]],col=C[c("rame","viola","verde")][j],lwd=1.6,lty=j)
 abline(v=as.numeric(as.Date("1999-01-01")),lty=3)
 leg(legend=c("Ultimo","Stagionale","Deriva"),col=C[c("rame","viola","verde")],lty=1:3)
})
fig("03_previsione_CO2",{
 ix<-145:204;plot(co2$data[ix],co2$co2_ppm[ix],type="n",xlab="Anno",ylab="CO2 (ppm)",ylim=range(co2$co2_ppm[ix],fc$inferiore,fc$superiore)+c(0,2));grid_y()
 polygon(c(forecast$data,rev(forecast$data)),c(fc$inferiore,rev(fc$superiore)),col=adjustcolor(C["blu"],.19),border=NA)
 lines(co2$data[ix],co2$co2_ppm[ix],col=C["ink"],lwd=1.2)
 lines(forecast$data,forecast$previsto,col=C["blu"],lwd=2)
 abline(v=as.numeric(as.Date("1999-01-01")),lty=3)
 leg(legend=c("Osservato storico","SARIMA","Intervallo 95%"),col=c(C["ink"],C["blu"],adjustcolor(C["blu"],.4)),lty=c(1,1,1))
})
fig("04_errori_CO2",{
 plot(forecast$h,forecast$errore,type="o",pch=19,cex=.6,col=C["blu"],xlab="Mesi dall'origine",ylab="Errore (ppm)");abline(h=0,lty=2,col=C["rame"]);abline(v=c(12.5,24.5),lty=3,col=C["grigio"])
})
fig("05_metriche_CO2",{
 z<-met[met$modello!="Media",];vals<-rbind(z$MAE,z$RMSE)
 bx<-barplot(vals,beside=TRUE,names.arg=z$modello,col=C[c("blu","rame")],border=NA,ylab="Errore (ppm)",ylim=c(0,max(vals)*1.15),cex.names=.85)
 leg(x="topright",legend=c("MAE","RMSE"),col=C[c("blu","rame")],lty=1,lwd=6)
})
fig("06_cv_origini",{
 par(mar=c(4.1,2,1.2,1));plot(c(0,168),c(.5,4.3),type="n",xlab="Mese nel solo train (1985-1998)",ylab="",yaxt="n",xaxs="i")
 for(j in 1:3){o<-c(120,132,144)[j];segments(1,j,o,j,col=C["blu"],lwd=10);segments(o+1,j,o+12,j,col=C["rame"],lwd=10);text(o+6,j+.25,paste("+12"),cex=.7)}
 axis(2,at=1:3,labels=c("120","132","144"),las=1,cex.axis=.75)
 leg(x="top",legend=c("Stima","Valutazione interna"),col=C[c("blu","rame")],lty=1,lwd=6,horiz=TRUE)
})
fig("07_cv_RMSE",{
 matplot(cvmet$origine,cvmet[,c("RMSE_SARIMA","RMSE_stagionale","RMSE_deriva")],type="b",lty=1:3,pch=c(19,17,15),col=C[c("blu","viola","verde")],xlab="Origine interna (mese)",ylab="RMSE (ppm)",ylim=c(0,3))
 leg(x="top",legend=c("SARIMA","Stagionale","Deriva"),col=C[c("blu","viola","verde")],lty=1:3,pch=c(19,17,15),horiz=TRUE,cex=.75)
})
fig("08_residui_SARIMA",{
 plot(co2$data[14:168],res,type="l",col=C["blu"],xlab="Anno del train",ylab="Residuo (ppm)");abline(h=0,lty=2,col=C["grigio"])
})
fig("09_ACF_residui",{
 acf(res,lag.max=36,main="",xlab="Ritardo (mesi)",ylab="ACF",col=C["blu"],ci.col=C["rame"],lwd=1.7)
})
fig("10_QQ_residui",{
 qqnorm(res,main="",pch=19,cex=.75,col=C["blu"],xlab="Quantili normali teorici",ylab="Residui (ppm)");qqline(res,col=C["rame"],lwd=1.7)
})
fig("11_errore_standard_previsione",{
 plot(fc$h,fc$se,type="l",lwd=2,col=C["blu"],xlab="Orizzonte (mesi)",ylab="Errore standard (ppm)");grid_y()
})
fig("12_copertura_blocchi",{
 bx<-barplot(blocchi$copertura,names.arg=blocchi$blocco,col=C["blu"],border=NA,ylim=c(0,1.12),ylab="Quota dentro l'intervallo",xlab="Orizzonte (mesi)")
 abline(h=.95,lty=2,col=C["rame"]);text(bx,blocchi$copertura+.05,paste0(blocchi$coperti,"/12"),cex=.8)
})
fig("13_ampiezza_intervalli",{
 plot(fc$h,fc$superiore-fc$inferiore,type="l",lwd=2,col=C["viola"],xlab="Orizzonte (mesi)",ylab="Ampiezza 95% (ppm)");grid_y()
})
fig("14_AR1_traiettorie",{
 par(mfrow=c(1,4),cex=1,mar=c(3,2.9,2,.6),mgp=c(1.6,.5,0))
 for(j in 1:4){plot(1:160,arsim[1:160,j],type="l",col=C[c("blu","verde","rame","viola")][j],main=paste("phi =",c(.2,.65,.95,-.6)[j]),xlab="Passo",ylab="X",cex.main=.9,xaxt="n");axis(1,at=c(0,80,160));abline(h=0,col=C["grigio"],lty=3)}
},w=12,hh=3.6,ps=18)
fig("15_AR1_ACF_teorica",{
 matplot(kat,acf_theory[,-1],type="l",lty=1:4,lwd=1.7,col=C[c("blu","verde","rame","viola")],xlab="Ritardo k",ylab="ACF teorica",ylim=c(-1.1,1.1))
 abline(h=0,col=C["grigio"],lty=3)
 leg(x="bottomright",legend=c("phi=0.20","phi=0.65","phi=0.95","phi=-0.60"),col=C[c("blu","verde","rame","viola")],lty=1:4,ncol=2)
})
fig("16_AR1_previsione",{
 plot(c(0,arfc$h),c(2,arfc$media),type="n",xlab="Passi dall'origine",ylab="X",ylim=range(arfc$inferiore,arfc$superiore));grid_y()
 polygon(c(arfc$h,rev(arfc$h)),c(arfc$inferiore,rev(arfc$superiore)),col=adjustcolor(C["blu"],.2),border=NA)
 lines(c(0,arfc$h),c(2,arfc$media),col=C["blu"],lwd=2);points(0,2,pch=19);abline(h=0,lty=3)
 leg(legend=c("Media condizionale","Intervallo 95%, parametri noti"),col=c(C["blu"],adjustcolor(C["blu"],.4)),lty=1,cex=.75)
})
fig("17_AR1_varianza",{
 plot(arfc$h,arfc$varianza,type="l",lwd=2,col=C["blu"],xlab="Orizzonte h",ylab="Varianza",ylim=c(0,1.9))
 abline(h=1/(1-.65^2),lty=2,col=C["rame"]);leg(x="bottomright",legend=c("Errore a h passi","Varianza stazionaria"),col=C[c("blu","rame")],lty=1:2)
})
fig("18_MA1_ACF",{
 z<-ARMAacf(ma=.6,lag.max=12);plot(0:12,z,type="h",lwd=3,col=C["viola"],xlab="Ritardo k",ylab="ACF teorica MA(1)",ylim=c(-.1,1.05));points(0:12,z,pch=19,col=C["viola"],cex=.55);abline(h=0,lty=3)
})
fig("19_risposta_impulso",{
 matplot(imp$lag,imp[,-1],type="b",lty=1:3,pch=c(19,17,15),col=C[c("blu","viola","rame")],xlab="Passi dopo lo shock",ylab="Risposta allo shock")
 leg(x="topright",legend=c("AR(1): phi=.65","MA(1): theta=.60","ARMA(1,1): .65, .40"),col=C[c("blu","viola","rame")],lty=1:3,pch=c(19,17,15),cex=.75)
})
fig("20_ARMA_ACF_PACF",{
 par(mfrow=c(1,2),mar=c(3.5,3.5,1.5,.6),mgp=c(2,.5,0))
 acf(armax,lag.max=20,main="",col=C["blu"],ci.col=C["rame"],xlab="Ritardo",lwd=1.5);mtext("ACF campionaria",side=3,line=.3,cex=.9)
 pacf(armax,lag.max=20,main="",col=C["viola"],ci.col=C["rame"],xlab="Ritardo",ylab="PACF",lwd=1.5);mtext("PACF campionaria",side=3,line=.3,cex=.9)
},w=7.5,hh=3.4,ps=19)
fig("21_differenze_CO2",{
 par(mfrow=c(1,3),cex=1,mar=c(3.3,3,2,.6),mgp=c(1.9,.6,0))
 for(j in 1:3){x<-list(diff(train),diff(train,lag=12),diff(diff(train,lag=12)))[[j]];plot(x,col=C[c("blu","viola","rame")][j],main=c("Ordinaria","Stagionale (12 mesi)","Ordinaria + stagionale")[j],ylab="ppm",xlab="Anno",cex.main=.85);abline(h=0,lty=3)}
},w=11,hh=3.5,ps=17)
fig("22_AIC_train",{
 delta<-aic$AIC-min(aic$AIC);bx<-barplot(delta,names.arg=c("011 x 011","110 x 011","111 x 011"),col=C[c("blu","viola","rame")],border=NA,ylab="Delta AIC nel train",xlab="Ordini non stagionali x stagionali",ylim=c(0,max(delta)*1.3+.1),cex.names=.85)
 text(bx,delta+.15,format(round(aic$AIC,2),nsmall=2),cex=.7)
})
fig("23_AR1_copertura_MC",{
 plot(mc$h,mc$copertura95,type="b",pch=19,cex=.6,col=C["blu"],ylim=c(.92,.98),xlab="Orizzonte h",ylab="Copertura empirica")
 abline(h=.95,lty=2,col=C["rame"]);abline(h=.95+c(-1,1)*1.96*sqrt(.95*.05/2000),lty=3,col=C["grigio"])
})
fig("24_AR1_varianza_MC",{
 plot(mc$h,mc$varianza_teorica,type="l",col=C["rame"],lwd=2,xlab="Orizzonte h",ylab="Varianza",ylim=range(mc$varianza_MC,mc$varianza_teorica));points(mc$h,mc$varianza_MC,pch=19,cex=.5,col=C["blu"])
 leg(x="bottomright",legend=c("Teoria","Monte Carlo"),col=C[c("rame","blu")],lty=c(1,NA),pch=c(NA,19))
})
fig("25_random_walk_varianza",{
 k<-1:36;plot(k,k,type="l",col=C["rame"],lwd=2,xlab="Orizzonte h",ylab="Varianza (sigma2=1)");lines(k,(1-.65^(2*k))/(1-.65^2),col=C["blu"],lwd=2)
 leg(legend=c("Random walk","AR(1), phi=.65"),col=C[c("rame","blu")])
})
fig("26_fossili_train_test",{
 plot(tr$diametro_tot_um,tr$diametro_int_um,pch=19,cex=.55,col=adjustcolor(C["blu"],.6),xlab="Totale (micrometri)",ylab="Interno (micrometri)",xlim=range(f$diametro_tot_um),ylim=range(f$diametro_int_um))
 points(te$diametro_tot_um,te$diametro_int_um,pch=17,cex=.75,col=C["rame"]);abline(mod,col=C["ink"],lwd=1.7)
 leg(legend=c("Train, n=128","Test, n=32","Retta dal solo train"),col=C[c("blu","rame","ink")],pch=c(19,17,NA),lty=c(NA,NA,1),cex=.75)
})
fig("27_fossili_osservato_previsto",{
 rr<-range(pf,te$diametro_int_um);plot(pf,te$diametro_int_um,pch=19,cex=.75,col=C["blu"],xlab="Previsto (micrometri)",ylab="Osservato (micrometri)",xlim=rr,ylim=rr,asp=1);abline(0,1,lty=2,col=C["rame"])
},w=4,hh=3.6,ps=18)
fig("28_fossili_residui",{
 plot(fitted(mod),residuals(mod),pch=19,cex=.55,col=C["blu"],xlab="Valore stimato nel train",ylab="Residuo (micrometri)");abline(h=0,lty=2,col=C["rame"])
})
fig("29_fossili_RMSE",{
 bx<-barplot(fmet$RMSE,names.arg=c("Media train","Regressione"),col=C[c("rame","blu")],border=NA,ylab="RMSE test (micrometri)",ylim=c(0,max(fmet$RMSE)*1.2))
 text(bx,fmet$RMSE+.04,format(round(fmet$RMSE,3),nsmall=3),cex=.8)
})
fig("30_VAR_serie",{
 matplot(processi$passo[1:260],as.matrix(processi[1:260,c("x_VAR","y_VAR")]),type="l",col=C[c("blu","rame")],lty=1:2,xlab="Passo simulato",ylab="Valore",lwd=1)
 abline(v=250.5,lty=3);leg(legend=c("X","Y"),col=C[c("blu","rame")],lty=1:2)
})
fig("31_VAR_autovalori",{
 t<-seq(0,2*pi,length.out=361);plot(cos(t),sin(t),type="l",asp=1,xlim=c(-1.2,1.2),ylim=c(-1.2,1.2),xlab="Parte reale",ylab="Parte immaginaria",col=C["grigio"])
 abline(h=0,v=0,col=adjustcolor(C["grigio"],.25));points(Re(vf$autovalori),Im(vf$autovalori),pch=19,cex=1.2,col=C["blu"])
},w=3.5,hh=3.5,ps=18)
fig("32_VAR_previsioni",{
 par(mfrow=c(1,2),cex=1,mar=c(3.3,3,1.5,.6),mgp=c(1.9,.6,0))
 for(j in 1:2){rr<-range(vo[,j],vp[,j],vb[,j]);rr[2]<-rr[2]+diff(rr)*.25;matplot(1:10,cbind(vo[,j],vp[,j],vb[,j]),type="b",lty=c(1,2,3),pch=c(19,1,NA),col=C[c("ink","blu","rame")],xlab="Passi dall'origine 250",ylab=c("X","Y")[j],ylim=rr,cex=.75);if(j==1)leg(legend=c("Osservato","VAR","Ultimo"),col=C[c("ink","blu","rame")],lty=1:3,cex=.75,horiz=TRUE)}
},w=11,hh=3.5,ps=17)
fig("33_VAR_ACF_residui",{
 par(mfrow=c(1,2),mar=c(3.5,3.5,1.5,.6),mgp=c(2,.5,0))
 acf(residuals(vf$x),lag.max=20,main="",col=C["blu"],ci.col=C["rame"],xlab="Ritardo");mtext("Equazione X",side=3,line=.3,cex=.9)
 acf(residuals(vf$y),lag.max=20,main="",col=C["viola"],ci.col=C["rame"],xlab="Ritardo");mtext("Equazione Y",side=3,line=.3,cex=.9)
},w=7.5,hh=3.4,ps=19)
fig("34_VAR_RMSE",{
 bx<-barplot(rbind(vmet$RMSE_VAR,vmet$RMSE_ultimo),beside=TRUE,names.arg=c("X","Y"),col=C[c("blu","rame")],border=NA,ylab="RMSE sui 10 passi",ylim=c(0,max(vmet[-1])*1.2))
 leg(legend=c("VAR(1)","Ultimo valore"),col=C[c("blu","rame")],lty=1,lwd=6)
})
fig("35_rolling_orizzonte",{
 matplot(cvh$h,cvh[,c("RMSE_SARIMA","RMSE_stagionale")],type="b",pch=c(19,17),lty=1:2,col=C[c("blu","viola")],xlab="Orizzonte h (mesi)",ylab="RMSE (ppm)")
 leg(x="right",legend=c("SARIMA","Stagionale"),col=C[c("blu","viola")],lty=1:2,pch=c(19,17))
})
fig("36_rolling_errori",{
 m<-matrix(cvdense$osservato-cvdense$SARIMA,nrow=12)
 lim<-max(abs(m));pal<-hcl.colors(33,"Blue-Red 3");br<-seq(-lim,lim,length.out=34)
 layout(matrix(1:2,nrow=1),widths=c(5,1.6));par(mar=c(4.1,4.4,1.25,.3))
 image(120:156,1:12,t(m),col=pal,breaks=br,xlab="Origine interna (mese)",ylab="Orizzonte h",useRaster=FALSE)
 par(mar=c(4.1,.5,1.25,3.8));key<-seq(-lim,lim,length.out=33)
 image(c(0,1),key,matrix(rep(key,each=2),nrow=2),col=pal,breaks=br,
  axes=FALSE,xlab="",ylab="",ylim=c(-lim,lim),useRaster=FALSE)
 axis(4,las=1,at=pretty(c(-lim,lim)),cex.axis=.75)
 mtext("Errore (ppm)",side=4,line=2.2,cex=.7,las=3)
},w=6.2,hh=3.3)
# Pannelli separati per la proiezione a circa9.85x5.25cm.
# Le figure14/21/32 complete restano disponibili per una vista comparata.
dir.create("Risultati/Figure/Dettagli",recursive=TRUE,showWarnings=FALSE)
for(j in 1:4) fig(paste0("Dettagli/14",letters[j],"_AR1_phi",j),{
 plot(1:160,arsim[1:160,j],type="l",col=C[c("blu","verde","rame","viola")][j],
  xlab="Passo simulato",ylab="X",lwd=1.4)
 abline(h=0,col=C["grigio"],lty=3)
 mtext(paste("AR(1), phi =",c(.2,.65,.95,-.6)[j]),side=3,line=.2,cex=.8)
})
for(j in 1:3) fig(paste0("Dettagli/21",letters[j],"_differenza_CO2"),{
 x<-list(diff(train),diff(train,lag=12),diff(diff(train,lag=12)))[[j]]
 plot(x,col=C[c("blu","viola","rame")][j],ylab="ppm",xlab="Anno",lwd=1.4)
 abline(h=0,lty=3)
})
for(j in 1:2) fig(paste0("Dettagli/32",letters[j],"_VAR_previsione"),{
 rr<-range(vo[,j],vp[,j],vb[,j]);rr[2]<-rr[2]+diff(rr)*.25
 matplot(1:10,cbind(vo[,j],vp[,j],vb[,j]),type="b",lty=1:3,pch=c(19,1,NA),
  col=C[c("ink","blu","rame")],xlab="Passi dall'origine 250",ylab=c("X","Y")[j],ylim=rr,cex=.8)
 leg(legend=c("Osservato","VAR","Ultimo"),col=C[c("ink","blu","rame")],lty=1:3,cex=.75,horiz=TRUE)
})
write.csv(data.frame(file=files_fig,tipo="PDF vettoriale da R",origine="R/rigenera_calcoli.R + R/genera_figure.R"),"Calcoli/INDICE_FIGURE.csv",row.names=FALSE)
