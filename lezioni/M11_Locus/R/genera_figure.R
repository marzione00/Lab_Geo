# Figure vettoriali M11, da oggetti effettivamente calcolati in rigenera_calcoli.R.
# Palette del corso; supporto e scale sono espliciti e comuni nei confronti.
C<-c(blu="#1D7890",rame="#C57E42",viola="#7363AA",verde="#087C74",grigio="#657180",ink="#253344",paper="#F8F6F1")
files_fig<-character();figure_desc<-character();figure_wide<-logical()
pal_z<-colorRampPalette(c("#E9D9C1","#C99A61","#6CA4AA","#185A70"))(80)
pal_div<-colorRampPalette(c(C["blu"],C["paper"],C["rame"]))(81)
zlim<-range(z)
fig<-function(nome,expr,w=5.8,hh=3.1,ps=16,descrizione=""){
 file<-file.path("Risultati/Figure",paste0(nome,".pdf"));files_fig<<-c(files_fig,file)
 figure_desc<<-c(figure_desc,descrizione);figure_wide<<-c(figure_wide,w>7)
 pdf(file,width=w,height=hh,pointsize=ps,family="Helvetica",bg=C["paper"],useDingbats=FALSE)
 par(mar=c(3.6,4.1,.9,.7),mgp=c(2.35,.65,0),tcl=-.25,col=C["ink"],col.axis=C["grigio"],col.lab=C["ink"],fg=C["ink"],las=1,bty="l",cex.axis=.86,cex.lab=.92)
 eval.parent(substitute(expr));invisible(dev.off())
}
leg<-function(x="topleft",legend,col,lty=1,pch=NULL,cex=.79,y.intersp=1.15,...){
 lty[is.na(lty)]<-0
 legend(x,legend=legend,col=col,lty=lty,pch=pch,bty="n",cex=cex,inset=.01,y.intersp=y.intersp,...)
}
grid_y<-function()abline(h=axTicks(2),col=adjustcolor(C["grigio"],.17),lwd=.65)
cols<-function(val,lim=zlim,pal=pal_z){i<-pmin(length(pal),pmax(1,1+floor((length(pal)-1)*(val-lim[1])/diff(lim))));pal[i]}
map_blank<-function(main="",xlab="x (m)",ylab="y (m)"){
 plot(xy,type="n",asp=1,xlim=c(-90,1840),ylim=c(-90,1840),axes=FALSE,xlab=xlab,ylab=ylab,xaxs="i",yaxs="i",main=main,cex.main=.92)
 axis(1,at=c(0,750,1500));axis(2,at=c(0,750,1500));box(col=adjustcolor(C["grigio"],.3))
}
map_points<-function(val=z,lim=zlim,pal=pal_z,main="",cex=1.2){map_blank(main);points(xy,pch=21,bg=cols(val,lim,pal),col=C["paper"],lwd=.5,cex=cex)}
color_key<-function(lim=zlim,pal=pal_z,label="Conc. (u.a.)"){
 par(mar=c(3.2,.1,.8,.3));plot(c(0,1),c(0,1),type="n",axes=FALSE,xlab="",ylab="",xaxs="i",yaxs="i")
 yy<-seq(.05,.86,length.out=length(pal)+1);rect(.06,head(yy,-1),.27,tail(yy,-1),col=pal,border=NA)
 vv<-pretty(lim,n=4);vv<-vv[vv>=lim[1]&vv<=lim[2]];yp<-.05+.81*(vv-lim[1])/diff(lim)
 text(.34,yp,format(vv,trim=TRUE),adj=0,cex=.8);text(.06,.98,label,adj=c(0,1),cex=.77)
}
map_single<-function(val=z,lim=zlim,pal=pal_z,label="Conc. (u.a.)",extra=NULL){
 layout(matrix(1:2,1),widths=c(4.4,1.4));par(mar=c(3.2,3.15,.7,.1),mgp=c(2,.55,0));map_points(val,lim,pal)
 if(!is.null(extra))extra();color_key(lim,pal,label)
}
map_pair<-function(a,b,titles,lim=zlim,pal=pal_z,label="u.a."){
 layout(matrix(1:3,1),widths=c(2.5,2.5,.8));par(cex=1)
 for(i in 1:2){par(mar=c(3.2,3.2,1.6,.15),mgp=c(1.8,.5,0));map_points(list(a,b)[[i]],lim,pal,titles[i])};color_key(lim,pal,label)
}
fig("01_mappa_punti",{map_single()},descrizione="64 misure puntuali sul piano locale, scala comune di concentrazione")
perm_display<-order(u[1:64]);z_perm<-z[perm_display]
fig("02_marginale_permutata",{map_pair(z,z_perm,c("Originale","Permutata"))},w=5.8,hh=3.1,ps=16,descrizione="Stessa distribuzione marginale e scala; diversa disposizione nello spazio")
block_mean<-ave(z,blocchi,FUN=mean)
fig("03_supporto_blocchi",{map_pair(z,block_mean,c("Misure puntuali","Media dei punti per blocco"))},w=10.2,hh=3.35,ps=17,descrizione="Aggregazione descrittiva dei punti; non osservazione di medie areali")
fig("04_coordinate_invertite",{
 par(mfrow=c(1,2),cex=1,mar=c(3.7,3.8,1.6,.45),mgp=c(2.1,.55,0))
 for(j in 1:2){xx<-if(j==1)d$lon else d$lat;yy<-if(j==1)d$lat else d$lon
 plot(xx,yy,xlim=range(xx)+diff(range(xx))*c(-.05,.18),pch=21,bg=C[if(j==1)"blu" else "rame"],col=C["paper"],cex=.85,xlab="x (gradi)",ylab="y (gradi)",main=c("x=lon, y=lat","x=lat, y=lon")[j],cex.main=.96,axes=FALSE)
 ax<-if(j==1)c(9,9.02)else c(45,45.015);ay<-if(j==1)c(45,45.015)else c(9,9.02)
 axis(1,at=ax,labels=format(ax,nsmall=if(j==1)2 else 3));axis(2,at=ay,labels=format(ay,nsmall=if(j==1)3 else 2));box(col=adjustcolor(C["grigio"],.3))}
},w=5.8,hh=3.1,ps=14,descrizione="Scambio di assi:entrambe le coppie restano numericamente plausibili ma designano luoghi diversi")
fig("05_distanze_piano",{
 par(mar=c(3.2,3.2,.6,.5),mgp=c(2,.6,0));map_blank();points(xy,pch=19,col=adjustcolor(C["grigio"],.25),cex=.7)
 ids<-c(2,10,64);co<-C[c("blu","rame","viola")]
 for(j in 1:3){segments(0,0,xy[ids[j],1],xy[ids[j],2],col=co[j],lwd=2);points(xy[ids[j],1],xy[ids[j],2],pch=19,col=co[j],cex=1.2)}
 points(0,0,pch=21,bg=C["ink"],col=C["paper"],cex=1.3)
 leg("topleft",legend=sprintf("S01-S%02d: %.1f m",ids,D[1,ids]),col=co,lwd=2,cex=.76)
},descrizione="Distanze euclidee fra siti, con metri espliciti")
fig("06_distanze_geografiche",{
 ij<-upper.tri(D);xx<-D[ij];plot(xx,D_sfera[ij]-xx,pch=19,cex=.45,col=adjustcolor(C["blu"],.45),xlab="Distanza locale (m)",ylab="Differenza (m)",ylim=c(-4,5));grid_y()
 points(xx,D_utm[ij]-xx,pch=1,cex=.5,col=adjustcolor(C["rame"],.6));abline(h=0,lty=3,col=C["grigio"])
 leg("topleft",legend=c("Sfera (R = 6371 km) - locale","UTM 32N - locale"),col=C[c("blu","rame")],lty=NA,pch=c(19,1),cex=.76)
},descrizione="Coordinate geografiche sintetiche: confronto delle 2016 distanze con il piano locale")
fig("07_proiezione_UTM",{
 layout(matrix(1:2,1),widths=c(4.4,1.4));par(mar=c(3.45,3.8,.65,.1),mgp=c(2.3,.55,0))
 plot(utm_xy[,1]-500000,utm_xy[,2]-4982950,pch=21,bg=cols(z),col=C["paper"],cex=1.2,asp=1,xlab="E - 500000 (m)",ylab="N - 4982950 m",axes=FALSE)
 axis(1,at=c(0,750,1500));axis(2,at=c(0,750,1500));box(col=adjustcolor(C["grigio"],.3));color_key()
},descrizione="Trasformazione sf reale in EPSG32632; traslazioni grafiche degli assi dichiarate")
fig("08_confini_aggregazioni",{
 layout(matrix(1:2,1),widths=c(4,1.8));par(mar=c(3.2,3.2,.6,.1),mgp=c(2,.6,0));map_blank();abline(v=1000,lty=2,col=C["ink"])
 points(xy,pch=21,bg=ifelse(regioni=="Ovest",C["blu"],C["rame"]),col=C["paper"],cex=1.2)
 par(mar=c(2,.1,.6,.2));plot.new();leg("center",legend=sprintf("%s\nn = %d\nmedia %.2f",agg_oe$gruppo,agg_oe$n,agg_oe$media),col=ifelse(agg_oe$gruppo=="Ovest",C["blu"],C["rame"]),pch=19,lty=NA,cex=.79,y.intersp=1.5)
},descrizione="Partizione semichiusa x<1000 / x>=1000;32punti per gruppo")
fig("09_aggregazioni_alternative",{
 pp<-c("Est_Ovest_1000","Nord_Sud_1000","Est_Ovest_750","Diagonale");labs<-c("E/O: x=1000","N/S: y=1000","E/O: x=750","Diagonale")
 plot(c(1,4),range(agg_alt$media)+c(-.6,.6),type="n",xlab="Partizione dichiarata",ylab="Media dei punti (u.a.)",xaxt="n");grid_y();axis(1,at=1:4,labels=labs,cex.axis=.69)
 for(j in 1:4){a<-agg_alt[agg_alt$partizione==pp[j],];segments(j,min(a$media),j,max(a$media),col=C["grigio"],lwd=2);points(rep(j,2)+c(-.04,.04),a$media,pch=21,bg=C[c("blu","rame")],col=C["paper"],cex=1.2)}
 abline(h=mean(z),lty=2,col=C["viola"])
},descrizione="Le medie cambiano quando cambiano i gruppi; linea comune media dei64siti")
fig("10_confini_semiaperti",{
 vals<-t(as.matrix(confini[,c("appartenenze","duplicati","esclusi")]));bx<-barplot(vals,beside=TRUE,col=C[c("blu","rame","viola")],border=NA,ylim=c(0,100),names.arg=c("< / >=","<= / >=","< / >"),xlab="Regola al confine x = 1000 m",ylab="Conteggio",cex.names=.85)
 text(bx,vals+2,vals,cex=.72);abline(h=64,lty=3,col=C["grigio"]);leg("topright",legend=c("Appartenenze","Duplicati","Esclusi"),col=C[c("blu","rame","viola")],lwd=6,cex=.69,ncol=3)
},descrizione="Controllo del confine: la partizione semichiusa assegna ciascun sito una volta")
fig("11_join_sovrapposto",{
 layout(matrix(1:2,1),widths=c(4.15,1.65));par(mar=c(3.2,3.2,.6,.1),mgp=c(2,.6,0));map_blank();rect(750,-90,1250,1840,col=adjustcolor(C["viola"],.12),border=NA)
 points(xy,pch=21,bg=ifelse(rowSums(member)==2,C["viola"],ifelse(member[,1],C["blu"],C["rame"])),col=C["paper"],cex=1.2)
 abline(v=c(750,1250),lty=2,col=C["viola"])
 par(mar=c(2,.1,.6,.2));plot.new();leg("center",legend=c("Solo A\n24 siti","A e B\n24 siti","Solo B\n16 siti"),col=C[c("blu","viola","rame")],pch=19,lty=NA,cex=.79,y.intersp=1.7)
},descrizione="Join uno-a-molti:A x<=1250,B x>=750;88appartenenze,24duplicati")
fig("12_buffer_raggi",{
 layout(matrix(1:2,1),widths=c(4.15,1.65));par(mar=c(3.2,3.2,.6,.1),mgp=c(2,.6,0));map_blank();points(xy,pch=19,col=adjustcolor(C["grigio"],.55),cex=.8)
 co<-C[c("blu","rame","viola")];for(j in 3:1)symbols(750,750,circles=rr[j],inches=FALSE,add=TRUE,fg=co[j],lwd=1.8)
 points(750,750,pch=3,lwd=2,cex=1.2);par(mar=c(2,.1,.6,.2));plot.new();leg("center",legend=sprintf("r = %d m\nn = %d",buffers$raggio_m,buffers$n),col=co,lwd=2,cex=.78,y.intersp=1.7)
},descrizione="Buffer euclidei centrati in750,750;conteggi reali e troncamento al bordo")
fig("13_vicini_soglia",{
 par(mar=c(3.2,3.2,.6,.5),mgp=c(2,.6,0));map_blank()
 segments(xy[edges[,1],1],xy[edges[,1],2],xy[edges[,2],1],xy[edges[,2],2],col=adjustcolor(C["blu"],.45),lwd=1.2)
 points(xy,pch=21,bg=C["blu"],col=C["paper"],cex=1.0)
},descrizione="112archi non orientati con soglia260m; diagonale esclusa")
fig("14_gradi_vicinato",{
 vals<-as.integer(table(nv));bx<-barplot(vals,names.arg=names(table(nv)),col=C[c("rame","viola","blu")],border=NA,ylim=c(0,44),xlab="Numero di vicini",ylab="Numero di siti");text(bx,vals+2,vals,cex=.9)
 leg("topleft",legend=c("2: angoli","3: bordo","4: interno"),col=C[c("rame","viola","blu")],lwd=6,cex=.76)
},descrizione="Distribuzione dei gradi:4angoli,24bordi,36interni")
fig("15_matrici_A_W",{
 par(mfrow=c(1,2),cex=1,mar=c(3.5,3.2,1.6,.5),mgp=c(2.1,.55,0))
 for(j in 1:2){mm<-if(j==1)A else W;image(1:64,1:64,t(mm[64:1,]),col=c(C["paper"],colorRampPalette(c("#B7D5DD",C["blu"]))(40)),zlim=c(0,if(j==1)1 else .5),useRaster=FALSE,axes=FALSE,xlab="Indice j",ylab="Indice i",main=c("A binaria","W per riga")[j],cex.main=.9)
 axis(1,at=c(1,32,64));axis(2,at=c(1,33,64),labels=c(64,32,1));box(col=adjustcolor(C["grigio"],.3))}
},w=5.8,hh=3.1,ps=14,descrizione="Struttura delle due matrici;scale diverse,stesso ordinamento dei64siti")
fig("16_lag_spaziale",{map_pair(z,as.vector(W%*%z),c("Valore z","Media vicini Wz"))},w=5.8,hh=3.1,ps=16,descrizione="Lag dei valori con pesi W per riga;scala di concentrazione comune")
fig("17_effetti_bordo",{
 layout(matrix(1:2,1),widths=c(4.4,1.4));par(mar=c(3.2,3.15,.7,.1),mgp=c(2,.55,0));map_blank()
 cc<-C[c("rame","viola","blu")][match(nv,c(2,3,4))];points(xy,pch=21,bg=cc,col=C["paper"],cex=1.2)
 par(mar=c(2,.1,.6,.2));plot.new();legend("center",legend=c("2 vicini\nw = 1/2","3 vicini\nw = 1/3","4 vicini\nw = 1/4"),pch=19,col=C[c("rame","viola","blu")],bty="n",cex=.82,y.intersp=1.8)
},descrizione="Un vicino ha peso diverso al bordo e all'interno dopo normalizzazione per riga")
fig("18_Moran_confronto",{
 vals<-c(I_A,I_W);bx<-barplot(vals,names.arg=c("A binaria","W per riga"),col=C[c("blu","rame")],border=NA,ylim=c(-.23,.98),ylab="Indice di Moran I",cex.names=.85);abline(h=-1/63,lty=2,col=C["viola"])
 text(bx,vals+.055,sprintf("%.4f",vals),cex=.92);text(mean(bx),-.15,"E[I] = -1/63 sotto permutazione",cex=.75,col=C["grigio"])
},descrizione="I_A e I_W non coincidono;aspettativa nulla condizionata ai valori")
fig("19_Moran_scatter",{
 plot(v,lag_W,pch=21,bg=C["blu"],col=C["paper"],cex=1.0,xlab="Valore centrato v (u.a.)",ylab="Lag Wv (u.a.)");abline(h=0,v=0,lty=3,col=C["grigio"]);abline(scatter_fit,col=C["rame"],lwd=2)
 leg("topleft",legend=sprintf("Pendenza = I_W = %.4f",I_W),col=C["rame"],lwd=2,cex=.78)
},descrizione="Regressione con intercetta:pendenza I_W;intercetta effettiva0.011109")
fig("20_quadranti",{
 co<-setNames(C[c("rame","blu","viola","verde")],c("HH","LL","HL","LH"));layout(matrix(1:2,1),widths=c(4.4,1.4))
 par(mar=c(3.2,3.15,.7,.1),mgp=c(2,.55,0));map_blank();points(xy,pch=21,bg=co[quadrante],col=C["paper"],cex=1.2)
 par(mar=c(2,.1,.6,.2));plot.new();leg("center",legend=paste0(names(co),": ",as.integer(table(factor(quadrante,levels=names(co))))),col=co,pch=19,lty=NA,cex=.85)
},descrizione="Quadranti descrittivi dei segni di v e Wv;non significativita locale")
fig("21_permutazioni100_999",{
 par(mfrow=c(1,2),cex=1,mar=c(3.7,3.4,1.6,.5),mgp=c(2.1,.55,0));bb<-seq(-.4,.85,length.out=26)
 for(j in 1:2){vv<-list(null100,null999)[[j]];hist(vv,breaks=bb,freq=FALSE,col=adjustcolor(C["blu"],.75),border=C["paper"],xlab="I_A permutato",ylab="Densita",main=c("B = 100","B = 999")[j],cex.main=.96,xlim=c(-.4,.85),ylim=c(0,7.4),axes=FALSE);axis(1,at=c(-.3,0,.3,.6));axis(2,at=c(0,3,6));box(bty="l");abline(v=I_A,col=C["rame"],lwd=2);abline(v=-1/63,lty=2,col=C["viola"]);text(.34,6.9,c("p = 1/101","p = 1/1000")[j],cex=.87,col=C["rame"])}
},w=5.8,hh=3.1,ps=14,descrizione="Test upper-tail suA;formula plus1 e0superamenti in entrambi i casi")
fig("22_trend_residui",{
 layout(matrix(1:4,1),widths=c(3.7,3.7,3.7,1.4));par(cex=1);limr<-c(-1,1)*max(abs(residui))
 for(j in 1:3){par(mar=c(3.2,3.1,1.7,.15),mgp=c(2,.55,0));map_points(list(z,as.numeric(fitted(trend)),residui)[[j]],if(j==3)limr else zlim,if(j==3)pal_div else pal_z,c("Osservato","Trend lineare x + y","Residuo")[j])};color_key(limr,pal_div,"Residuo (u.a.)")
},w=12.5,hh=3.45,ps=17,descrizione="Trend e residui descrittivi;primi due pannelli scala osservazioni,ultimo scala simmetrica")
fig("23_coppie_semivarianza",{
 plot(coppie$h,coppie$gamma,pch=19,cex=.45,col=adjustcolor(C["blu"],.23),xlab="Distanza h (m)",ylab=expression((z[i]-z[j])^2/2),ylim=c(0,max(coppie$gamma)*1.03));grid_y()
},descrizione="Nuvola di2016coppie i<j condivise fra siti e non indipendenti")
fig("24_semivariogramma",{
 plot(vg$h,vg$gamma,type="b",pch=19,col=C["blu"],lwd=2,xlab="Distanza media nel bin (m)",ylab="Semivarianza (u.a.^2)",ylim=c(0,max(vg$gamma)*1.13));grid_y()
 lines(vg_res$h,vg_res$gamma,type="b",pch=17,col=C["rame"],lwd=1.8)
 leg("topleft",legend=c("Valori grezzi","Residui del trend"),col=C[c("blu","rame")],pch=c(19,17),cex=.78)
},descrizione="Quattro bin fissi;confronto descrittivo prima e dopo trend")
fig("25_numerosita_coppie",{
 bx<-barplot(vg$n,names.arg=c("0-300","300-600","600-1000","1000-2500"),col=C["blu"],border=NA,ylim=c(0,1250),xlab="Bin di distanza h (m)",ylab="Numero di coppie",cex.names=.77);text(bx,vg$n+65,vg$n,cex=.86)
},descrizione="Conteggi112,362,476,1066;totale2016 senza equivalenza a campioni indipendenti")
fig("26_direzionali",{
 par(mfrow=c(1,2),cex=1,mar=c(3.8,4.2,1.7,1),mgp=c(2.2,.6,0));ymax<-max(direzionali$gamma,na.rm=TRUE)
 for(j in 1:2){dd<-direzionali[direzionali$serie==c("Grezza","Residui")[j],];plot(c(0,1600),c(0,ymax*1.05),type="n",xlab="Distanza (m)",ylab="Semivarianza (u.a.^2)",main=c("Valori grezzi","Residui del trend")[j],cex.main=.9)
 for(k in 1:2){qq<-dd[dd$direzione==c("Est_Ovest","Nord_Sud")[k],];lines(qq$h,qq$gamma,type="b",pch=c(19,17)[k],lty=k,lwd=1.7,col=C[c("blu","rame")][k])};if(j==1)leg("topleft",legend=c("Est-Ovest","Nord-Sud"),col=C[c("blu","rame")],pch=c(19,17),lty=1:2,cex=.78)}
},w=10.2,hh=3.35,ps=17,descrizione="Settori entro22.5gradi dagli assi;confronto a scala comune prima e dopo trend")
fig("27_modelli_variogramma",{
 matplot(models$h[-1],models[-1,-1],type="l",xlim=c(0,2500),lty=1:3,lwd=2,col=C[c("blu","rame","viola")],xlab="Distanza h (m)",ylab="Semivarianza teorica",ylim=c(0,5.3));abline(h=c(.2,4.2),lty=3,col=C["grigio"]);points(0,0,pch=19,col=C["ink"],cex=.65);points(0,.2,pch=1,col=C["ink"],cex=.65)
 leg("topleft",legend=c("Esponenziale","Gaussiano","Sferico"),col=C[c("blu","rame","viola")],lty=1:3,lwd=2,cex=.76,ncol=2)
},descrizione="Curve didattiche non stimate:nugget0.2,sill parziale4,portata pratica circa1200m")
fig("28_strada_campione",{
 layout(matrix(1:2,1),widths=c(4.15,1.65));par(mar=c(3.2,3.2,.6,.1),mgp=c(2,.6,0));map_blank();rect(-90,-90,1840,250,col=adjustcolor(C["rame"],.12),border=NA);abline(h=250,lty=2,col=C["rame"])
 points(xy,pch=21,bg=ifelse(road,C["rame"],C["paper"]),col=ifelse(road,C["paper"],adjustcolor(C["grigio"],.6)),cex=1.15)
 par(mar=c(2,.1,.6,.2));plot.new();leg("center",legend=c("Strada\n16 siti\ny <= 250","Restanti\n48 siti"),col=C[c("rame","grigio")],pch=c(19,1),lty=NA,cex=.78,y.intersp=1.5)
},descrizione="Selezione lungo strada:solo le due file meridionali")
fig("29_copertura",{
 vals<-rbind(cov_y$n_strada,cov_y$n_totale-cov_y$n_strada);barplot(vals,names.arg=cov_y$y,col=c(C["rame"],"#D8DBDA"),border=C["paper"],ylim=c(0,10.5),xlab="Coordinata y della fila (m)",ylab="Siti della fila",cex.names=.7)
 leg("top",legend=c("Campionati lungo strada","Non campionati"),col=c(C["rame"],"#D8DBDA"),lwd=6,cex=.75,horiz=TRUE)
},descrizione="Copertura del reticolo di riferimento per ciascuna delle8file")
fig("30_medie_blocchi",{
 bx<-barplot(agg_blocchi$media,names.arg=gsub("_","\n",agg_blocchi$gruppo),col=C[c("rame","blu","viola","verde")],border=NA,ylim=c(0,max(agg_blocchi$media)*1.2),ylab="Media dei punti (u.a.)",cex.names=.76)
 abline(h=mean(z),lty=2,col=C["ink"]);text(bx,agg_blocchi$media+.8,sprintf("%.2f",agg_blocchi$media),cex=.8)
},descrizione="Quattro blocchi con16siti ciascuno;linea media dei64siti")
fig("31_pesi_squilibrati",{
 esempio_n<-c(2,8);esempio_media<-c(10,20)
 vals<-rbind(esempio_n/sum(esempio_n),c(.5,.5));bx<-barplot(vals,beside=TRUE,names.arg=c("Blocco A\nn=2, media=10","Blocco B\nn=8, media=20"),col=C[c("blu","rame")],border=NA,ylim=c(0,1.15),ylab="Peso del gruppo",cex.names=.72)
 text(bx,vals+.04,sprintf("%.1f",vals),cex=.8);leg("topleft",legend=c("Siti: media 18","Blocchi: media 15"),col=C[c("blu","rame")],lwd=6,cex=.76)
 write.csv(data.frame(blocco=c("A","B"),n=esempio_n,media=esempio_media,peso_siti=esempio_n/sum(esempio_n),peso_blocchi=.5),"Calcoli/esempio_pesi_2_8.csv",row.names=FALSE)
},descrizione="Esempio costruito n2/8,medie10/20:media per sito18 e media per blocco15")
fig("32_idw_pesi",{
 oo<-order(dist_target);matplot(dist_target[oo],weights[oo,],type="b",pch=c(19,17,15),cex=.55,lty=1:3,lwd=1.3,col=C[c("blu","rame","viola")],xlab="Distanza dal punto (900,900) m",ylab="Peso IDW normalizzato",ylim=c(0,max(weights)*1.15));grid_y()
 leg("topright",legend=paste0("p = ",1:3),col=C[c("blu","rame","viola")],lty=1:3,pch=c(19,17,15),cex=.78)
},descrizione="Effetto di p sui pesi normalizzati per i64siti in un punto fissato")
fig("33_idw_potenze",{
 plot(idw_powers$p,idw_powers$previsione,type="b",xlim=c(.75,3.25),pch=19,col=C["blu"],lwd=2,xaxt="n",xlab="Potenza p",ylab="Previsione IDW (u.a.)",ylim=range(idw_powers$previsione)+c(-.2,.3));axis(1,at=1:3);grid_y();text(1:3,idw_powers$previsione+.12,sprintf("%.3f",idw_powers$previsione),cex=.85)
},descrizione="Previsione al medesimo punto900,900;non confronto di accuratezza")
fig("34_idw_superficie",{
 layout(matrix(1:2,1),widths=c(4.4,1.4));par(mar=c(3.2,3.15,.7,.1),mgp=c(2,.55,0));map_blank()
 image(sort(unique(grid$x_m)),sort(unique(grid$y_m)),matrix(grid$previsto,45,45),col=pal_z,zlim=zlim,add=TRUE,useRaster=FALSE)
 points(xy,pch=21,bg=NA,col=adjustcolor(C["paper"],.9),cex=.57,lwd=.8);color_key()
},descrizione="Superficie IDW p2 ricostruita da64punti;griglia45x45 e scala delle misure")
fig("35_split_spaziale",{
 layout(matrix(1:2,1),widths=c(4.15,1.65));par(mar=c(3.2,3.2,.6,.1),mgp=c(2,.6,0));map_blank();rect(0,0,1000,1750,col=adjustcolor(C["blu"],.1),border=C["blu"],lty=3);abline(v=1250,lty=2,col=C["rame"])
 points(xy,pch=ifelse(train_idx,21,24),bg=ifelse(train_idx,C["blu"],C["rame"]),col=C["paper"],cex=1.15)
 par(mar=c(2,.1,.6,.2));plot.new();leg("center",legend=c("Train: 40\nx < 1250","Test: 24\nx >= 1250"),col=C[c("blu","rame")],pch=c(19,17),lty=NA,cex=.78,y.intersp=1.8)
},descrizione="Test a est,esterno all'inviluppo convesso del train;trasferimento geografico")
fig("36_previsioni_confronto",{
 vals<-rbind(metrics$MAE,metrics$RMSE);bx<-barplot(vals,beside=TRUE,names.arg=c("Media train","Vicino","IDW p=2"),col=C[c("blu","rame")],border=NA,ylim=c(0,max(vals)*1.32),ylab="Errore sul test (u.a.)",cex.names=.79)
 text(bx,vals+.18,sprintf("%.2f",vals),cex=.69);leg("topright",legend=c("MAE","RMSE"),col=C[c("blu","rame")],lwd=6,horiz=TRUE,cex=.77)
},descrizione="Confronto delle tre regole sullo stesso test24siti;nessun vantaggio imposto aIDW")
fig("37_errori_spaziali",{
 lim<-c(-1,1)*max(abs(err));layout(matrix(1:2,1),widths=c(4.4,1.4));par(mar=c(3.2,3.15,.7,.1),mgp=c(2,.55,0));map_blank()
 points(xy[train_idx,],pch=1,col=adjustcolor(C["grigio"],.35),cex=.85);points(xy[test_idx,],pch=21,bg=cols(err,lim,pal_div),col=C["paper"],cex=1.3);color_key(lim,pal_div,"Obs - pred")
},descrizione="Errori IDW sul test con scala simmetrica;positivi indicano sottoprevisione")
fig("38_tuning_blocchi",{
 plot(inner_metrics$p,inner_metrics$RMSE,type="b",xlim=c(.75,3.25),pch=19,col=C["blu"],lwd=2,xaxt="n",xlab="Potenza p (solo train)",ylab="RMSE interno (u.a.)",ylim=range(inner_metrics$RMSE)+c(-.15,.3));axis(1,at=1:3);grid_y()
 text(inner_metrics$p,inner_metrics$RMSE+.13,sprintf("%.3f",inner_metrics$RMSE),cex=.82)
 mtext("Frontiere: 500, 750, 1000 m; 24 previsioni per p",side=3,line=-.4,cex=.65,col=C["grigio"])
},descrizione="Tre frontiere all'interno dei40train;valida una colonna esterna8punti perfrontiera")
fig("39_kriging_pesi",{
 vals<-ok$fit$weights;bx<-barplot(vals,names.arg=c("A: x=0","B: x=500","C: x=1000"),col=ifelse(vals>=0,C["blu"],C["rame"]),border=NA,ylim=c(-.28,.88),ylab="Peso di kriging ordinario",cex.names=.77)
 abline(h=0,col=C["ink"]);text(bx,vals+ifelse(vals>=0,.06,-.055),sprintf("%.4f",vals),cex=.85)
},descrizione="Tre siti e covarianza gaussiana nota;target250m,peso del sitoC negativo")
fig("40_kriging_varianza",{
 plot(ok_curve$x,ok_curve$varianza,type="l",col=C["blu"],lwd=2,xlab="Posizione di previsione x (m)",ylab="Varianza condizionale",ylim=c(0,max(ok_curve$varianza)*1.12));grid_y()
 points(ok$xy[,1],rep(0,3),pch=19,col=C["ink"],cex=.9);abline(v=250,lty=3,col=C["rame"]);points(250,ok$fit$variance,pch=21,bg=C["rame"],col=C["paper"],cex=1.1)
 leg("top",legend=c("Covarianza nota, nessun nugget","Siti osservati","Target x=250"),col=C[c("blu","ink","rame")],lty=c(1,NA,NA),pch=c(NA,19,19),cex=.71,ncol=1)
},descrizione="Varianza calcolata dal sistema;zero ai siti,nessuna incertezza di stima dei parametri")
manifest<-data.frame(file=basename(files_fig),pannello_largo=figure_wide,descrizione=figure_desc)
write.csv(manifest,"Calcoli/indice_figure.csv",row.names=FALSE)
stopifnot(length(files_fig)==40,all(file.exists(files_fig)))
cat("Figure vettoriali generate:",length(files_fig),"\n")
