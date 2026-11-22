# 42 figure vettoriali Tessera: dati e oggetti reali di rigenera_calcoli.R.
C<-c(blu="#1D7890",rame="#C57E42",viola="#7363AA",verde="#087C74",grigio="#657180",ink="#253344",paper="#F8F6F1",na="#D5B4C8")
pal_z<-colorRampPalette(c("#E1E9B2","#71AD94","#358F8B","#254D67"))(90)
pal_div<-colorRampPalette(c(C["blu"],C["paper"],C["rame"]))(91)
pal_asp<-colorRampPalette(c(C["blu"],C["viola"],C["rame"],"#8EA975",C["blu"]))(91)
pal_hill<-colorRampPalette(c("#15283E",C["paper"]))(80)
zlim<-range(Z);files_fig<-character();figure_desc<-character();figure_wide<-logical()
fig<-function(nome,expr,w=5.8,hh=3.1,ps=16,descrizione="") {
 file<-file.path("Risultati/Figure",paste0(nome,".pdf"));files_fig<<-c(files_fig,file);figure_desc<<-c(figure_desc,descrizione);figure_wide<<-c(figure_wide,w>7)
 pdf(file,width=w,height=hh,pointsize=ps,family = "Helvetica",bg=C["paper"],useDingbats=FALSE)
 par(mar=c(3.5,4,.8,.6),mgp=c(2.25,.6,0),tcl=-.25,col=C["ink"],col.axis=C["grigio"],col.lab=C["ink"],fg=C["ink"],las=1,bty = "l",cex.axis=.86,cex.lab=.92)
 eval.parent(substitute(expr));invisible(dev.off())
}
leg<-function(x="topleft",legend,col,lty = 1,pch=NULL,cex=.79,...)legend(x,legend=legend,col=col,lty = lty,pch=pch,bty = "n",cex=cex,inset=.01,...)
grid_y<-function()abline(h=axTicks(2),col=adjustcolor(C["grigio"],.18),lwd=.6)
map_plot<-function(mm=Z,xx=x,yy = y,lim=zlim,pal=pal_z,main="",xlab="x (m)",ylab="y (m)",border=FALSE) {
 hx<-if(length(xx)>1)diff(xx)[1]/2 else 15;hy<-if(length(yy)>1)diff(yy)[1]/2 else 15
 image(xx,yy,t(mm),zlim=lim,col=pal,asp=1,useRaster=FALSE,xlim=range(xx)+c(-hx,hx),ylim=range(yy)+c(-hy,hy),
  xlab=xlab,ylab=ylab,axes=FALSE,xaxs="i",yaxs="i",main=main,cex.main=.94)
 axis(1,at=if(max(xx)>500)c(0,300,600,900) else pretty(range(xx),3));axis(2,at=if(max(yy)>500)c(0,300,600) else pretty(range(yy),3));box(col=adjustcolor(C["grigio"],.45))
 if(anyNA(mm)){ids<-which(is.na(mm),arr.ind=TRUE);rect(xx[ids[,2]]-hx,yy[ids[,1]]-hy,xx[ids[,2]]+hx,yy[ids[,1]]+hy,col=C["na"],border=NA)}
 if(border){abline(v=seq(min(xx)-hx,max(xx)+hx,2*hx),h=seq(min(yy)-hy,max(yy)+hy,2*hy),col=adjustcolor(C["paper"],.3),lwd=.3)}
}
color_key<-function(lim=zlim,pal=pal_z,label="Quota (m)",ticks=NULL) {
 par(mar=c(3.1,.1,.8,.3));plot(c(0,1),c(0,1),type="n",axes=FALSE,xlab="",ylab="",xaxs="i",yaxs="i")
 ys<-seq(.05,.83,length.out=length(pal)+1);rect(.05,head(ys,-1),.25,tail(ys,-1),col=pal,border=NA)
 vv<-if(is.null(ticks))pretty(lim,n=4)else ticks;vv<-vv[vv>=lim[1]&vv<=lim[2]]
 text(.32,.05+.78*(vv-lim[1])/diff(lim),format(vv,trim=TRUE,digits=4),adj=0,cex=.77);text(.05,.98,label,adj=c(0,1),cex=.76)
}
map_single<-function(mm=Z,xx=x,yy = y,lim=zlim,pal=pal_z,label="Quota (m)",extra=NULL,ticks=NULL) {
 layout(matrix(1:2,1),widths=c(4.5,1.3));par(mar=c(3.2,3.15,.5,.05),mgp=c(2,.55,0));map_plot(mm,xx,yy,lim,pal)
 if(!is.null(extra))extra();color_key(lim,pal,label,ticks)
}
map_multi<-function(mats,xs,ys,titles,lim=zlim,pal=pal_z,label="Quota (m)",extra=NULL) {
 k<-length(mats);layout(matrix(seq_len(k+1),1),widths=c(rep(3,k),1.1));par(cex=1)
 for(i in seq_len(k)){par(mar=c(3.2,3.1,1.55,.1),mgp=c(2,.5,0));map_plot(mats[[i]],xs[[i]],ys[[i]],lim,pal,titles[i]);if(!is.null(extra))extra(i)}
 color_key(lim,pal,label)
}
fig("01_dem",{map_single()},descrizione="DEM sintetico originale720 celle; centri0..870 e0..690m, valori in metri")
fig("02_orientamento",{
 map_multi(list(Z,Z[24:1,]),list(x,x),list(y,y),c("Locale: prima riga a Sud","Inversione letta come locale"),extra=function(i){points(c(0,870),c(0,690),pch=c(21,24),cex=1.5,bg=C["paper"],col=C["ink"])} )
},w=10.2,hh=3.35,ps=17,descrizione="Stessi numeri e distribuzione; solo la prima carta rispetta l'orientamento locale. La seconda illustra l'errore")
fig("03_celle_centri",{
 par(mar=c(3.2,3.3,.8,.8),mgp=c(2,.5,0));xx<-x[1:5];yy<-y[1:4]
 map_plot(Z[1:4,1:5],xx,yy,zlim,pal_z,border=TRUE)
 abline(v=seq(-15,135,30),h=seq(-15,105,30),col=C["paper"],lwd=1.2);points(expand.grid(xx,yy),pch=3,cex=.7,col=C["ink"])
 points(0,0,pch=21,bg=C["paper"],cex=1.7);text(10,8,"(0,0)",adj=0,cex=.82)
},descrizione="Centri e bordi: la prima cella locale si estende da-15 a15metri")
fig("04_maschera_nodata",{map_single(Z_mask,extra=function(){rect(255,105,435,225,border=C["viola"],lwd=1.5)})},descrizione="24celle NA artificiali; nessuna sostituzione con zero; scala del DEM originale")
fig("05_effetto_zero",{
 vv<-coverage$media[1:3];plot(1:3,vv,pch=21,bg=C[c("blu","viola","rame")],col=C["paper"],cex=1.8,xlim=c(.5,3.5),ylim=range(vv)+c(-7,12),xaxt="n",xlab="Trattamento del dato",ylab="Quota media (m)");grid_y();axis(1,at=1:3,labels=c("Completo","Disponibili","NA = 0"),cex.axis=.8)
 text(1:3,vv+6,sprintf("%.2f",vv),cex=.82);abline(h=mean(Z),col=C["blu"],lty = 3)
},descrizione="Medie effettive dei tre trattamenti: lo zero altera il dominio e il valore")
fig("06_ritaglio",{map_single(extra=function(){rect(285,165,615,525,border=C["rame"],lwd=2);text(450,345,paste0(sum(crop_sel)," celle"),col=C["paper"],font=2,cex=.95)})},descrizione="Finestra selezionata per i centri x300..600,y180..510;132celle e11.88ha")
fig("07_superficie_zone",{
 a<-c(64.8,696*.09,24*.09,sum(crop_sel)*.09);bp<-barplot(a,names.arg=c("Totale","Disponibili","Escluse","Finestra"),col=C[c("blu","verde","viola","rame")],border=NA,ylim=c(0,76),ylab="Superficie (ha)",cex.names=.76)
 text(bp,a+3,sprintf("%.2f",a),cex=.84)
},descrizione="Area planimetrica900m2per cella; finestre e maschera dichiarate")
fig("08_aggregazione",{map_multi(list(Z,A2),list(x,x2),list(y,y2),c("30 m: 720 celle","60 m: 180 medie"))},w=10.2,hh=3.35,ps=17,descrizione="Aggregazione2x2 sullo stesso dominio; scala cromatica comune")
fig("09_perdita_estremi",{
 vals<-t(as.matrix(agg_summary[,c("minimo","media","massimo")]));plot(c(1,3),range(vals)+c(-10,10),type="n",xlim=c(.55,3.45),xaxt="n",xlab="Sintesi",ylab="Quota (m)");grid_y();axis(1,at=1:3,labels=c("Minimo","Media","Massimo"))
 lines(1:3,vals[,1],type="b",pch=19,col=C["blu"],lwd=1.8);lines(1:3,vals[,2],type="b",pch=17,col=C["rame"],lwd=1.8)
 leg("topleft",c("Celle 30 m","Medie 60 m"),C[c("blu","rame")],pch=c(19,17),cex=.76)
},descrizione="La media si conserva per blocchi completi equiponderati; gli estremi si attenuano")
fig("10_risoluzioni_analitiche",{
 aa<-analytic;cmin<-min(vapply(aa,function(a)min(a$Z),0));cmax<-max(vapply(aa,function(a)max(a$Z),0))
 map_multi(lapply(aa,`[[`,"Z"),lapply(aa,`[[`,"x"),lapply(aa,`[[`,"y"),paste(c(10,30,100),"m"),lim=c(cmin,cmax),extra=function(i){rect(100,100,800,500,border=C["rame"],lwd=1.6,lty = 2)})
},w=11.5,hh=3.35,ps=17,descrizione="Superficie analitica separata, dominio900x600m; finestra comune28ha tratteggiata")
fig("11_sensibilita_pendenza",{
 a<-analytic_summary;plot(a$passo_m,a$RMSE_pendenza_gradi,type="b",pch=21,bg=C["blu"],col=C["blu"],lwd=2,xaxt="n",xlim=c(0,112),xlab="Passo della griglia analitica (m)",ylab="RMSE pendenza (gradi)",ylim=c(0,max(a$RMSE_pendenza_gradi)*1.2));grid_y();axis(1,at=a$passo_m)
 text(a$passo_m,a$RMSE_pendenza_gradi+.08*max(a$RMSE_pendenza_gradi),sprintf("%.3f",a$RMSE_pendenza_gradi),cex=.8)
},descrizione="Errore rispetto alla derivata esatta; pesi delle intersezioni sul medesimo dominio28ha")
fig("12_ricampionamento_continuo",{
 map_multi(list(Z,res15_nn,res15_bi),list(x,x15,x15),list(y,y15,y15),c("Originale 30 m","Vicino 15 m","Bilineare 15 m"))
},w=11.5,hh=3.35,ps=17,descrizione="Ricampionamenti realmente eseguiti da terra;15m è la griglia di uscita, non nuova risoluzione osservata")
fig("13_ricampionamento_classi",{
 qq<-seq(0,90,1);li<-approx(xc,cl,xout=qq)$y;nn<-sapply(qq,function(q)cl[which.min(abs(xc-q))])
 plot(qq,li,type="l",col=C["rame"],lwd=2,xlab="Posizione (m)",ylab="Codice nominale",ylim=c(.85,2.25),yaxt="n");axis(2,at=c(1,1.5,2));lines(qq,nn,col=C["blu"],lwd=2,type="s");points(xc,cl,pch=21,bg=C["ink"],col=C["paper"],cex=1.15)
 leg("topleft",c("Lineare: inadatto","Vicino"),C[c("rame","blu")],cex=.77)
},descrizione="Esempio originaleN08: il codice1.5 non è una classe; parità del vicino risolta con il primo indice")
fig("14_origini_15m",{
 par(mar=c(3.3,3.3,.7,.8),mgp=c(2.1,.5,0));plot(c(-15,135),c(-15,105),type="n",asp=1,xlab="x locale (m)",ylab="y locale (m)",xaxs="i",yaxs="i")
 for(xv in seq(-15,105,30))segments(xv,-15,xv,105,col=C["blu"],lwd=1.3)
 for(yv in seq(-15,105,30))segments(-15,yv,105,yv,col=C["blu"],lwd=1.3)
 for(xv in seq(0,120,30))segments(xv,-15,xv,105,col=C["rame"],lty = 2,lwd=1.3)
 points(expand.grid(seq(0,90,30),seq(0,90,30)),pch=19,col=C["blu"],cex=.55)
 points(expand.grid(seq(15,105,30),seq(0,90,30)),pch=3,col=C["rame"],cex=.8)
 rect(-8,75,28,92,col=adjustcolor(C["paper"],.9),border=NA);arrows(0,72,15,72,length=.07,col=C["ink"],code=3);text(7.5,84,"15 m",cex=.8)
},descrizione="Geometrie traslate di mezza cella; stessa forma della matrice non equivale a stessi luoghi")
fig("15_allineamento_errori",{
 lim<-max(abs(shifts[["15"]]$errori),na.rm=TRUE)
 map_single(shifts[["15"]]$errori,lim=c(-lim,lim),pal=pal_div,label="Scarto (m)")
},descrizione="Stessi valori attribuiti a una geometria+15mE, poi riallineati con terra bilinear; scarto dalla quota originale")
fig("16_piano_noto",{map_single(plane,lim=range(plane),extra=function(){contour(x,y,t(plane),add=TRUE,drawlabels=TRUE,col=adjustcolor(C["ink"],.4),labcex=.85)})},descrizione="Piano900+0.12x+0.08y; caso analitico esatto per i segni e le unità del gradiente")
fig("17_gradienti_xy",{
 ll<-max(abs(c(gx,gy)));map_multi(list(gx,gy),list(x[2:29],x[2:29]),list(y[2:23],y[2:23]),c("g_x: verso Est","g_y: verso Nord"),lim=c(-ll,ll),pal=pal_div,label="m/m")
},w=10.2,hh=3.35,ps=17,descrizione="Componenti centrate sui616centri interni, scala divergente comune")
fig("18_gradiente_pendenza",{
 plot(row_values(g),row_values(slope_deg),pch=19,col=adjustcolor(C["blu"],.4),cex=.55,xlab="Modulo del gradiente (m/m)",ylab="Pendenza (gradi)");grid_y()
 gg<-seq(0,max(g),length.out=200);lines(gg,atan(gg)*180/pi,col=C["rame"],lwd=1.5)
},descrizione="Conversione non lineare atan del modulo; punti616celle e curva analitica")
fig("19_pendenza_mappa",{map_single(slope_deg,x[2:29],y[2:23],lim=c(0,max(slope_deg)),label="Gradi")},descrizione="616pendenze interne del DEM, differenze centrate4vicini; bordo escluso")
fig("20_gradi_percentuale",{
 aa<-seq(0,70,length.out=300);plot(aa,100*tan(aa*pi/180),type="l",lwd=2,col=C["blu"],xlab="Pendenza (gradi)",ylab="Pendenza (%)",xaxt="n");grid_y();axis(1,at=c(0,30,45,60));abline(h=100,v=45,lty = 3,col=C["grigio"]);points(45,100,pch=21,bg=C["rame"],col=C["paper"],cex=1.5);text(43,125,"45 gradi = 100%",adj=1,cex=.83)
},descrizione="Relazione100tan(theta); gradi e percento non sono intercambiabili")
fig("21_bordo_maschera",{
 map_multi(list(slope_full,masked_full),list(x,x),list(y,y),c("Solo bordo: 104 NA",paste0("Bordo e buco: ",sum(is.na(masked_full))," NA")),lim=c(0,max(slope_deg)),label="Gradi")
},w=10.2,hh=3.35,ps=17,descrizione="Rosa=NA: centro e4vicini devono essere validi; i24buchi propagano la maschera alle derivate")
fig("22_aspect",{map_single(aspect_deg,x[2:29],y[2:23],lim=c(0,360),pal=pal_asp,label="Azimut",ticks=c(0,90,180,270,360))},descrizione="Azimut di massima discesa:0Nord,90Est; piano con gradiente nullo escluso")
fig("23_media_circolare",{
 par(mar=c(.3,.3,.4,.3));plot(c(-1.5,1.5),c(-1.4,1.4),type="n",asp=1,axes=FALSE,xlab="",ylab="")
 tt<-seq(0,2*pi,len=300);lines(sin(tt),cos(tt),col=adjustcolor(C["grigio"],.5));segments(-1.1,0,1.1,0,col=adjustcolor(C["grigio"],.25));segments(0,-1.1,0,1.1,col=adjustcolor(C["grigio"],.25))
 points(sin(c(359,1)*pi/180),cos(c(359,1)*pi/180),pch=c(19,1),col=C["blu"],cex=1.6)
 arrows(0,0,0,.88,length=.1,col=C["blu"],lwd=2);arrows(0,0,0,-.88,length=.1,col=C["rame"],lwd=2)
 text(.1,.55,"Circolare: 0",adj=0,col=C["blu"],cex=.84);text(.1,-.55,"Aritmetica: 180",adj=0,col=C["rame"],cex=.84)
 text(0,1.2,"359 e 1 gradi",cex=.86);text(0,-1.2,sprintf("Risultante R = %.5f",media_circolare(c(359,1))[2]),cex=.83)
},descrizione="Due direzioni adiacenti al Nord: media circolare0 e risultante0.99985; media aritmetica180 fuorviante")
fig("24_confronto_terra",{
 plot(row_values(slope_deg),row_values(t8s-slope_deg),pch=19,cex=.55,col=adjustcolor(C["rame"],.6),xlab="Pendenza centrata, 4 vicini (gradi)",ylab="Scarto terra (gradi)",ylim=range(c(t8s-slope_deg,-.005,.005))+c(0,.08));grid_y();abline(h=0,lty = 3,col=C["grigio"])
 points(row_values(slope_deg),row_values(t4s-slope_deg),pch=19,cex=.4,col=C["blu"])
 leg("topright",c("neighbors=8","neighbors=4"),C[c("rame","blu")],lty = 0,pch=19,cex=.76)
},descrizione="4vicini coincide con il calcolo esplicito;8vicini è un algoritmo diverso, non un errore di arrotondamento")
fig("25_hillshade_confronto",{
 map_multi(list(hill315,hill135),list(x[2:29],x[2:29]),list(y[2:23],y[2:23]),c("Azimut 315: Nord-Ovest","Azimut 135: Sud-Est"),lim=c(0,1),pal=pal_hill,label="Luce")
},w=10.2,hh=3.35,ps=17,descrizione="Stesso terreno e altezza45gradi; illuminazione da normale prodotto luce, troncata a zero")
fig("26_illuminazione_profilo",{
 a<-light_profile;plot(a$x_m,a$luce315,type="l",lwd=2,col=C["blu"],ylim=c(0,1),xlab=paste0("x (m), profilo y = ",unique(a$y_m),"m"),ylab="Intensità di luce");grid_y();lines(a$x_m,a$luce135,col=C["rame"],lwd=2)
 leg("bottomleft",c("Azimut 315","Azimut 135"),C[c("blu","rame")],cex=.8)
},descrizione="Due illuminazioni sulle medesime28celle del profilo y330m; quote invariate")
fig("27_bande_R_NIR",{
 rb<-matrix(R_band,24,byrow=TRUE);nb<-matrix(NIR,24,byrow=TRUE)
 map_multi(list(rb,nb),list(x,x),list(y,y),c("Rosso sintetico","NIR sintetico"),lim=c(0,.5),label="Riflettanza")
},w=10.2,hh=3.35,ps=17,descrizione="Bande interamente sintetiche e comparabili, medesima scala0..0.5; nessun sensore osservato")
fig("28_indice_normalizzato",{map_single(matrix(indice,24,byrow=TRUE),lim=c(-1,1),pal=rev(pal_div),label="Indice",ticks=c(-1,0,1))},descrizione="(NIR-R)/(NIR+R) sulle720 celle sintetiche; denominatore sempre positivo")
fig("29_spettro_indice",{
 plot(R_band,NIR,pch=19,cex=.55,col=adjustcolor(C["blu"],.45),xlab="Banda rossa sintetica",ylab="Banda NIR sintetica",xlim=c(.1,.3),ylim=c(.25,.62));grid_y()
 for(q in c(.2,.4,.6))abline(a=0,b=(1+q)/(1-q),col=adjustcolor(C["rame"],.55),lty = 2)
 leg("topleft",c("720 celle","Isolinee indice 0.2/0.4/0.6"),C[c("blu","rame")],lty = c(0,2),pch=c(19,NA),cex=.72)
},descrizione="Relazione tra bande e isolinee dell'indice; il contrasto dipende dalla coppia di valori")
fig("30_denominatore",{
 den<-10^seq(-10,-1,len=300);delta<-1e-6;idx<-(den/3+delta)/(den+delta)
 plot(den,idx,type="l",log="x",col=C["rame"],lwd=2,ylim=c(.25,1.04),xlab="Somma delle bande",ylab="Indice calcolato");abline(h=1/3,lty = 2,col=C["blu"]);abline(v=1e-6,lty = 3,col=C["viola"])
 leg("topright",c("NIR perturbata di 1e-6","Indice originale 1/3","Soglia 1e-6"),C[c("rame","blu","viola")],lty = c(1,2,3),cex=.72)
},descrizione="Esperimento analitico: perturbazione assoluta fissa produce forte sensibilità relativa vicino a zero")
fig("31_scaling_offset",{
 plot(indice,idx_DN,pch=19,cex=.5,col=adjustcolor(C["rame"],.5),xlim=range(indice),ylim=range(c(idx_DN,indice)),xlab="Indice dopo scala e offset",ylab="Indice dai DN: errato");grid_y();abline(0,1,lty = 2,col=C["blu"])
},descrizione="Bande sintetiche codificate con scala2.75e-5 e offset-0.2; la sola scala comune si cancella, l'offset no")
fig("32_zone",{
 map_single(class_mat,lim=c(.5,2.5),pal=C[c("blu","rame")],label="Zona",ticks=c(1,2),extra=function(){text(c(210,660),rep(345,2),c("A","B"),col=C["paper"],font=2,cex=1.5)})
},descrizione="Zone sintetiche A/B originali,360celle ciascuna; codici nominali")
fig("33_sintesi_zonali",{
 boxplot(d$quota_m~d$unita,col=C[c("blu","rame")],border=C["ink"],outline=FALSE,ylab="Quota (m)",xlab="Zona sintetica",boxwex=.5)
 points(1:2,zone$media,pch=23,bg=C["paper"],col=C["ink"],cex=1.2)
},descrizione="Distribuzioni originali per zona; rombi=medie, box=quartili, nessun intervallo inferenziale")
fig("34_pesi_aree",{
 par(mar=c(3.5,5.2,1,.7))
 vals<-c(weighted.mean(zone_mask$media_disponibili,zone_mask$n_disponibili),mean(zone_mask$media_disponibili));plot(1:2,vals,pch=21,bg=C[c("blu","rame")],col=C["paper"],cex=1.7,xaxt="n",xlim=c(.5,2.5),ylim=range(vals)+c(-.5,1),ylab="",xlab="Sintesi delle due zone");grid_y();axis(1,at=1:2,labels=c("Pesi area osservata","Pesi uguali"),cex.axis=.77)
 mtext("Media disponibile (m)",side=2,line=3.4,las=0,cex=.92);text(1:2,vals+.35,sprintf("%.3f",vals),cex=.82);mtext("A: 336 celle; B: 360 celle; passo 30 m",side=3,line=-.1,cex=.75)
},descrizione="Dopo la maschera le zone hanno aree osservate diverse; il peso corretto ricostruisce la media delle696celle")
fig("35_differenze30_300",{
 vals<-diff_summary$media_abs;bp<-barplot(vals,names.arg=c("30 m","300 m"),col=C[c("blu","rame")],border=NA,ylim=c(0,max(vals)*1.3),ylab="Media assoluta (m)",xlab="Separazione orizzontale")
 text(bp,vals+max(vals)*.05,sprintf("%.2f\nn = %d",vals,diff_summary$n_coppie),adj=c(.5,0),cex=.82)
},descrizione="Differenze E-O originali:696coppie30m e480coppie300m; non prove indipendenti")
fig("36_blocchi12",{
 map_single(block_id,lim=c(.5,12.5),pal=rep(C[c("blu","rame","viola","verde")],3),label="Blocco",ticks=c(1,4,8,12),extra=function(){
 abline(v=c(285,585),h=c(165,345,525),col=C["paper"],lwd=2)
 for(i in 1:4)for(j in 1:3)text((j-1)*300+135,(i-1)*180+75,(i-1)*3+j,col=C["paper"],font=2,cex=1.0)
 })
},descrizione="12blocchi non sovrapposti6x10celle,60valori e5.4ha ciascuno; ordine Sud-Nord, Ovest-Est")
fig("37_bootstrap300_1999",{
 par(mfrow=c(1,2),cex=1,mar=c(3.4,3.4,1.65,.4),mgp=c(2.05,.55,0));lim<-range(c(boot300,boot1999));br<-seq(floor(lim[1]/5)*5,ceiling(lim[2]/5)*5,by = 5)
 for(i in 1:2){bb<-list(boot300,boot1999)[[i]];hist(bb,breaks=br,col=C["blu"],border=C["paper"],xlim=range(br),xlab="Media ricampionata (m)",ylab="Ripetizioni",main=c("300: uniformi originali","1999: seed 20261109")[i],cex.main=.94);abline(v=mean(Z),col=C["rame"],lwd=1.8);abline(v=quantile(bb,c(.025,.975)),col=C["viola"],lty = 2)}
},w=10.2,hh=3.35,ps=17,descrizione="Due protocolli distinti: centro=media originale, tratteggi=quantili2.5/97.5%; nessuna garanzia di copertura")
fig("38_bootstrap_confronto",{
 boxplot(list("Celle singole"=boot_cells,"Blocchi da 60 celle"=boot1999),col=C[c("rame","blu")],border=C["ink"],outline=FALSE,boxwex=.55,ylab="Media ricampionata (m)",xlab="1999 repliche per metodo",cex.axis=.8)
 abline(h=mean(Z),col=C["viola"],lty = 2)
},descrizione="Il ricampionamento di celle ignora dipendenza; blocchi cambiano distribuzione, non garantiscono inferenza valida")
fig("39_memoria",{
 par(mar=c(3.5,5.2,.8,.7))
 nn<-10^seq(3,8,length.out=200);plot(nn,nn*8/1e6,type="l",log="xy",lwd=2,col=C["blu"],xlab="Numero di celle",ylab="",ylim=c(.005,4000));lines(nn,nn*4*8/1e6,lwd=2,col=C["rame"])
 mtext("Memoria valori (MB)",side=2,line=3.4,las=0,cex=.92);leg("topleft",c("1 banda double","4 bande double"),C[c("blu","rame")],cex=.79)
},descrizione="Memoria teorica8byte/valore; overhead degli oggetti, copie e compressione del file esclusi")
fig("40_finestra_halo",{
 map_single(extra=function(){
 # Indici TIFF row5..10,col10..17: conversione in bordi locali.
 rect(225,375,525,615,border=C["viola"],lwd=2,lty = 2)
 rect(255,405,495,585,border=C["rame"],lwd=2)
 text(375,495,"48",col=C["paper"],font=2,cex=1.1)
 })
},descrizione="Finestra6x8 da leggere e halo8x10per produrre tutte le48derivate, senza perdere i bordi della finestra")
fig("41_export_pendenze",{map_single(slope_full,lim=c(0,max(slope_deg)),label="Gradi",extra=function(){rect(15,15,855,675,border=C["ink"],lwd=1.2)})},descrizione="GeoTIFF completo:616valori più104NoData; rettangolo=estensione del secondo export interno22x28")
fig("42_controllo_roundtrip",{
 rb<-matrice_locale(reread$pendenze_interne);xx<-row_values(slope_deg);yy<-row_values(rb)
 plot(xx,yy,pch=19,cex=.55,col=adjustcolor(C["blu"],.5),xlab="Pendenza calcolata (gradi)",ylab="Pendenza riletta (gradi)");abline(0,1,lty = 2,col=C["rame"])
 leg("topleft",sprintf("616 celle; errore max=%.1e",max(abs(xx-yy))),C["blu"],lty = 0,pch=19,cex=.8)
},descrizione="Valori realmente riletti dal GeoTIFF FLT8S; confronto numerico con il calcolo R")
write.csv(data.frame(file=basename(files_fig),panorama=figure_wide,descrizione=figure_desc),"Calcoli/figure_manifest.csv",row.names=FALSE)
cat("FIGURE",length(files_fig),"PDF vettoriali\n")
