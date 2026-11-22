# Figure meteorologiche della revisione completa.
# Dati archiviati: Meteostat e fornitori, Roma/Ciampino, 16239, 2019--2024.
# Scaricamento del 18 novembre 2026; nessun accesso alla rete in questo script.
# Il dataset comprende osservazioni e stime di modello; leggere la provenienza.
# Figure in PDF vettoriale: testo 12 pt su larghezze 4/4.6 in per leggibilita' in slide.

# Nel progetto distribuito aggiorna Risorse/Figure; se Risorse non esiste,
# usa Figure come cartella autonoma di lavoro.
dir_fig <- if (dir.exists("Risorse")) file.path("Risorse","Figure") else "Figure"
dir.create(dir_fig, showWarnings=FALSE, recursive=TRUE)
met <- read.csv("Dati/meteostat_ciampino_2019_2024.csv")
met$data <- as.Date(met$data)
met <- met[order(met$data), ]
met$anno <- as.integer(format(met$data,"%Y"))
met$mese <- as.integer(format(met$data,"%m"))
stopifnot(nrow(met)==2192L, all(diff(met$data)==1), !anyNA(met$tmax))
d <- subset(met,anno==2024)
mesi <- c("Gen","Feb","Mar","Apr","Mag","Giu","Lug","Ago","Set","Ott","Nov","Dic")
ink <- "#253344"; muted <- "#657180"; teal <- "#1D7890"
purple <- "#7363AA"; ochre <- "#C57E42"; paper <- "#F8F6F1"

inizia <- function(nome,larghezza=4.6,altezza=2.1,
                    margini=c(3.1,3.5,.35,.45)) {
  pdf(file.path(dir_fig,paste0(nome,".pdf")),width=larghezza,height=altezza,
      pointsize=12,family="Helvetica",useDingbats=FALSE)
  par(mar=margini,mgp=c(1.85,.55,0),tcl=-.2,las=1,bty="l",
      col=ink,col.axis=ink,col.lab=ink,cex=1)
}
asse_anni <- function() {
  axis.Date(1,at=as.Date(paste0(2019:2024,"-01-01")),format="%Y")
}
asse_2024 <- function() {
  axis.Date(1,at=as.Date(c("2024-01-01","2024-04-01","2024-07-01","2024-10-01")),
            labels=c("Gen","Apr","Lug","Ott"))
}
chiudi <- function() invisible(dev.off())

# 56. Pioggia giornaliera per mese: mediana nel box, media come rombo.
# boxplot usa le cerniere di Tukey; i quartili interpolati di ggplot2 possono differire.
inizia("plot_median_media",margini=c(3.0,3.5,.35,.4))
boxplot(pioggia ~ factor(mese,levels=1:12),data=d,names=mesi,
        col="#D4E7E6",border=teal,pch=16,cex=.55,
        xlab="Mese (2024)",ylab="Pioggia [mm]",cex.axis=.9,xaxt="n",
        ylim=c(0,max(d$pioggia,na.rm=TRUE)*1.12))
axis(1,at=1:12,labels=mesi,cex.axis=.83,gap.axis=0)
m_mese <- tapply(d$pioggia,d$mese,mean,na.rm=TRUE)
points(1:12,m_mese,pch=18,col=ochre,cex=1.05)
legend("topright",legend="Media mensile",pch=18,col=ochre,bty="n",cex=.9)
chiudi()

# 62. Regressione di Tmax su Tmin, tutti i366 giorni con coppia completa.
# Banda95% per la risposta media del modello, non intervallo di previsione.
ok <- complete.cases(d[c("tmin","tmax")]); reg <- d[ok, ]
fit <- lm(tmax ~ tmin,data=reg)
xg <- seq(min(reg$tmin),max(reg$tmin),length.out=200)
ci <- predict(fit,newdata=data.frame(tmin=xg),interval="confidence",level=.95)
inizia("regressione_tmax_tmin_2024")
plot(reg$tmin,reg$tmax,type="n",xlab="Tmin [°C]",ylab="Tmax [°C]")
polygon(c(xg,rev(xg)),c(ci[,"lwr"],rev(ci[,"upr"])),col="#D4E7E6",border=NA)
points(reg$tmin,reg$tmax,pch=16,cex=.38,col=adjustcolor(teal,alpha.f=.45))
lines(xg,ci[,"fit"],col=teal,lwd=1.6)
legend("topleft",legend=c("n = 366",expression(R^2==0.851)),bty="n",cex=.9)
chiudi()

# 69. Istogrammi sul medesimo insieme di361 giorni con pioggia disponibile.
p <- d$pioggia[!is.na(d$pioggia)]
inizia("hist_pioggia_2024",larghezza=4.0,margini=c(3.1,3.5,.4,.45))
hist(p,breaks=seq(0,max(p),length.out=41),freq=TRUE,col="#BFDDE1",border=teal,
     main="",xlab="Pioggia [mm/giorno]",ylab="Giorni")
legend("topright",legend=paste("n =",length(p)),bty="n",cex=.9)
chiudi()
lp <- log1p(p/1) # Riferimento p0 = 1 mm.
inizia("hist_pioggia_log1p_2024",larghezza=4.0,margini=c(3.1,3.5,.4,.45))
hist(lp,breaks=seq(0,max(lp),length.out=41),freq=TRUE,col="#C9DED6",border="#087C74",
     main="",xlab=expression(log(1+p/p[0])),ylab="Giorni")
legend("topright",legend=c(paste("n =",length(p)),"p0 = 1 mm"),bty="n",cex=.9)
chiudi()

# 70. Tmax e z-score: tutti i 366 valori termici, indipendentemente dalla pioggia.
mu2024 <- mean(d$tmax); s2024 <- sd(d$tmax)
inizia("tmax_raw_2024",larghezza=4.0,margini=c(2.6,3.5,.4,.45))
plot(d$data,d$tmax,type="l",col=teal,lwd=.9,xaxt="n",xlab="",ylab="Tmax [°C]")
abline(h=mu2024,col=muted,lty=2)
asse_2024(); chiudi()
inizia("zscore_tmax_2024",larghezza=4.0,margini=c(2.6,3.5,.4,.45))
plot(d$data,(d$tmax-mu2024)/s2024,type="l",col=purple,lwd=.9,xaxt="n",xlab="",ylab="z-score")
abline(h=0,col=muted,lty=2)
asse_2024(); chiudi()

# 73. Boxplot dei giorni disponibili, aggregati per mese sul 2019--2024.
# Il 2019 non contribuisce alla pioggia; gli altri anni hanno coperture diverse.
inizia("seasonality_prcp_box",margini=c(3.0,3.5,.35,.4))
boxplot(pioggia ~ factor(mese,levels=1:12),data=met,names=mesi,
        col="#D4E7E6",border=teal,pch=16,cex=.5,cex.axis=.9,
        xlab="Mese",ylab="Pioggia [mm]",xaxt="n",ylim=c(0,max(met$pioggia,na.rm=TRUE)*1.05))
axis(1,at=1:12,labels=mesi,cex.axis=.83,gap.axis=0)
chiudi()

# 74. Somme disponibili e copertura: nessuna pioggia disponibile nel 2019.
anni <- 2019:2024
giorni_attesi <- sapply(anni,function(y) as.integer(as.Date(paste0(y+1,"-01-01"))-as.Date(paste0(y,"-01-01"))))
validi <- as.integer(tapply(!is.na(met$pioggia),met$anno,sum))
somma <- as.numeric(tapply(met$pioggia,met$anno,function(x) if(all(is.na(x))) NA_real_ else sum(x,na.rm=TRUE)))
copertura <- data.frame(anno=anni,giorni_validi=validi,giorni_attesi=giorni_attesi,somma_mm=somma)
write.csv(copertura,"Dati/meteostat_copertura_pioggia.csv",row.names=FALSE,na="NA")
completo <- validi==giorni_attesi
inizia("annual_prcp_totals",margini=c(3.4,3.6,.4,.4))
xx <- barplot(ifelse(is.na(somma),0,somma),
              names.arg=rep("",length(anni)),axisnames=FALSE,
              col=ifelse(completo,"#087C74","#DFC2A5"),border=ifelse(completo,"#087C74",ochre),
              ylab="Somma [mm]",ylim=c(0,850),cex.names=.9)
text(xx,ifelse(is.na(somma),NA_real_,somma+35),
     ifelse(is.na(somma),"",format(round(somma,1),nsmall=1)),cex=.9)
text(xx[1],40,"n.d.",cex=.9,col=muted)
mtext(anni,side=1,at=xx,line=.6,cex=.9)
mtext(paste0(validi,"/",giorni_attesi),side=1,at=xx,line=1.7,cex=.83)
legend("topleft",legend=c("Parziale","Completa"),fill=c("#DFC2A5","#087C74"),
       border=NA,bty="n",horiz=TRUE,cex=.9)
chiudi()

# 80. I metodi sono quelli dello script originale, ora su periodo fisso 2019--2024.
# Con 30 pesi e sides=2, la finestra va da t-14 a t+15.
ma30 <- as.numeric(stats::filter(met$tmax,rep(1/30,30),sides=2))
stopifnot(all(which(is.na(ma30)) == c(1:14,(nrow(met)-14):nrow(met))))
tempo <- as.numeric(met$data)
lo <- loess(met$tmax ~ tempo,span=.2,degree=2,family="gaussian")
lhat <- as.numeric(predict(lo))
inizia("trend_smoothing_tmax",margini=c(2.7,3.5,.4,.4))
plot(met$data,met$tmax,type="l",col="#C1C8CC",lwd=.55,xaxt="n",xlab="",ylab="Tmax [°C]",ylim=c(0,47))
lines(met$data,ma30,col=teal,lwd=1)
lines(met$data,lhat,col=purple,lwd=1.5)
asse_anni()
legend("topright",legend=c("Media mobile 30","LOESS 0,2"),col=c(teal,purple),lty=1,lwd=c(1,1.5),bty="n",cex=.9,horiz=TRUE)
chiudi()

# 81. Scarti da medie mensili del campione 2019--2024, non normali30ennali.
ref <- tapply(met$tmax,met$mese,mean)
anom <- met$tmax - ref[as.character(met$mese)]
inizia("anomalies_tmax",margini=c(2.7,3.5,.4,.4))
plot(met$data,anom,type="l",col=ochre,lwd=.65,xaxt="n",xlab="",ylab="Scarto [°C]")
abline(h=0,col=muted,lty=2); asse_anni(); chiudi()

# 82. Salto artificiale dello script originale: +1.5°C dalla riga al 55% del campione.
data_salto <- met$data[round(nrow(met)*.55)]
con_salto <- ifelse(met$data>=data_salto,met$tmax+1.5,met$tmax)
med31 <- runmed(con_salto,k=31,endrule="median")
inizia("discontinuity_demo",margini=c(2.7,3.5,.4,.4))
plot(met$data,con_salto,type="l",col="#C1C8CC",lwd=.55,xaxt="n",xlab="",ylab="Tmax [°C]",ylim=c(0,47))
lines(met$data,med31,col=purple,lwd=1)
abline(v=as.numeric(data_salto),col=ochre,lty=2)
asse_anni()
legend("topleft",legend="Salto simulato: +1,5°C dal 20/04/2022",bty="n",cex=.9)
chiudi()

# Riepilogo numerico verificabile.
cat("Periodo:",format(min(met$data)),"--",format(max(met$data)),"; righe",nrow(met),"\n")
print(copertura,row.names=FALSE)
cat("Regressione 2024: n=",nrow(reg),"; coefficienti:",coef(fit),"; R2=",summary(fit)$r.squared,"\n")
cat("Tmax 2024: n=",nrow(d),"; media=",mu2024,"; sd=",s2024,"\n")
cat("Pioggia 2024: n=",length(p),"; giorni asciutti=",sum(p==0),"\n")
cat("Boxplot mensili 2019--2024, n validi:\n");print(tapply(!is.na(met$pioggia),met$mese,sum))
cat("Salto artificiale:",format(data_salto),"; ampiezza 1.5°C; mediana 31.\n")
cat("Media mobile30: 14 NA iniziali e 15 finali; LOESS span=.2 degree=2.\n")
