# Tessera M12 — calcoli effettivi in R/terra; nessun risultato numerico precostituito.
source("R/stato_lezione.R",encoding="UTF-8")
for(p in c("Calcoli","Risultati/Figure","Verifiche"))dir.create(p,recursive=TRUE,showWarnings=FALSE)
salva<-function(x,nome)write.csv(x,file.path("Calcoli",paste0(nome,".csv")),row.names=FALSE,na="")
tests<-data.frame(controllo=character(),ok=logical(),dettaglio=character())
verifica<-function(nome,ok,dettaglio="") {tests[nrow(tests)+1,]<<-list(nome,isTRUE(ok),dettaglio);if(!isTRUE(ok))stop(paste("VERIFICA FALLITA",nome));invisible(ok)}
# 1. Dati, orientamento e trasformazione affine: origine dei centri esplicita.
raw_error<-max(abs(M-Z[24:1,]))
xy_tiff<-terra::xyFromCell(r,1:720);dN<-d[order(-d$riga,d$colonna),]
xy_att<-cbind(dN$x_m+500015,dN$y_m+4999295)
salva(data.frame(cella=1:720,riga_tiff=rep(1:24,each=30),colonna_tiff=rep(1:30,24),
 E=xy_tiff[,1],N=xy_tiff[,2],x_locale=dN$x_m,y_locale=dN$y_m,quota_tiff=row_values(M),quota_csv=dN$quota_m),"corrispondenza_celle")
salva(data.frame(angolo=c("SO","SE","NO","NE"),x_m=c(0,870,0,870),y_m=c(0,0,690,690),
 quota=c(Z[1,1],Z[1,30],Z[24,1],Z[24,30])),"angoli")
salva(data.frame(parametro=c("righe","colonne","celle","dx_m","dy_m","xmin_E","xmax_E","ymin_N","ymax_N","offset_centro_E","offset_centro_N","area_ha","NoData"),
 valore=c(24,30,720,30,30,as.vector(terra::ext(r)),500015,4999295,64.8,-9999)),"geometria")
salva(data.frame(voce=c("CSV prima riga","TIFF prima riga","CRS assegnato","georeferenziazione"),
 descrizione=c("Sud; y locale=0","Nord; N=4999985","EPSG:32632","Traslazione fittizia: E=x+500015, N=y+4999295")),"convenzioni")
# 2. Maschera artificiale, finestra e superficie realmente inclusa.
crop_sel<-d$x_m>=300&d$x_m<=600&d$y_m>=180&d$y_m<=510
Z_zero<-Z_mask;Z_zero[is.na(Z_zero)]<-0
coverage<-data.frame(dominio=c("Completo","Disponibili","Zero al posto di NA","Finestra centrale"),
 n=c(720,696,720,sum(crop_sel)),area_ha=c(64.8,696*.09,64.8,sum(crop_sel)*.09),
 media=c(mean(Z),mean(Z_mask,na.rm=TRUE),mean(Z_zero),mean(d$quota_m[crop_sel])))
salva(coverage,"domini_maschera_ritaglio")
salva(matrice_df(Z_mask,x,y,"quota_m"),"quote_maschera")
salva(zone,"statistiche_zonali")
obs<-d;obs$disponibile<-!row_values(mask)
zone_mask<-do.call(rbind,lapply(sort(unique(d$unita)),function(a){ss<-obs$unita==a;vv<-ss&obs$disponibile
 data.frame(unita=a,n_totale=sum(ss),n_disponibili=sum(vv),area_totale_ha=sum(ss)*.09,area_disponibile_ha=sum(vv)*.09,
 copertura=sum(vv)/sum(ss),media_disponibili=mean(obs$quota_m[vv]))}))
salva(zone_mask,"zone_maschera")
# 3. Aggregazione 2x2: pari area; gli estremi e la variabilità possono cambiare.
ag2<-matrice_df(A2,x2,y2,"quota_m");salva(ag2,"aggregato_2x2")
agg_summary<-data.frame(passo_m=c(30,60),righe=c(24,12),colonne=c(30,15),n=c(720,180),
 area_ha=c(64.8,64.8),media=c(mean(Z),mean(A2)),minimo=c(min(Z),min(A2)),massimo=c(max(Z),max(A2)),sd=c(sd(c(Z)),sd(c(A2))))
salva(agg_summary,"aggregazione_riepilogo")
# 4. Ricampionamenti terra reali, geometria e origine +/-15 m.
r_csv<-raster_locale(Z,x,y)
r15<-terra::rast(nrows=48,ncols=60,ext=terra::ext(r),crs=terra::crs(r))
r15_bi<-terra::resample(r_csv,r15,method="bilinear",threads=FALSE)
r15_nn<-terra::resample(r_csv,r15,method="near",threads=FALSE)
res15_bi<-matrice_locale(r15_bi);res15_nn<-matrice_locale(r15_nn)
x15<-seq(-7.5,877.5,15);y15<-seq(-7.5,697.5,15)
resample_df<-matrice_df(res15_bi,x15,y15,"bilineare");resample_df$vicino<-row_values(res15_nn)
salva(resample_df,"ricampionamento_15m")
class_mat<-matrix(as.integer(factor(d$unita)),24,byrow=TRUE)
rclass<-raster_locale(class_mat,x,y)
class_near<-matrice_locale(terra::resample(rclass,r15,method="near",threads=FALSE))
class_bilinear<-matrice_locale(terra::resample(rclass,r15,method="bilinear",threads=FALSE))
class_df<-matrice_df(class_near,x15,y15,"vicino");class_df$bilineare_inadatto<-row_values(class_bilinear)
salva(class_df,"classi_terra")
xc<-c(0,30,60,90);cl<-c(1,1,2,2);xq<-seq(0,90,15)
class_1d<-data.frame(x_m=xq,lineare_ERRATO=approx(xc,cl,xout=xq)$y,vicino=sapply(xq,function(q)cl[which.min(abs(xc-q))]))
salva(class_1d,"classi_originale_N08")
shifts<-list();shift_summary<-data.frame()
for(ss in c(-15,15)) {
 rs<-terra::shift(r_csv,dx=ss,dy=0);ra<-terra::resample(rs,r_csv,method="bilinear",threads=FALSE)
 va<-matrice_locale(ra);er<-va-Z;ok<-is.finite(er);shifts[[as.character(ss)]]<-list(valori=va,errori=er)
 shift_summary<-rbind(shift_summary,data.frame(shift_m=ss,shift_pixel=ss/30,n_comparabili=sum(ok),
  differenza_matrice_ingenua=0,MAE_dopo_allineamento=mean(abs(er[ok])),RMSE_dopo_allineamento=sqrt(mean(er[ok]^2)),bias_dopo_allineamento=mean(er[ok])))
 sf<-matrice_df(er,x,y,"errore_m");sf$shift_m<-ss;salva(sf,paste0("allineamento_",if(ss<0)"meno15" else "piu15"))
}
salva(shift_summary,"allineamento_riepilogo")
# 5. Gradiente centrato, piano esatto, pendenza/aspect e confronto algoritmico.
plane<-outer(y,x,function(yy,xx)900+.12*xx+.08*yy);pm<-morfometria(plane)
slope_plane<-atan(sqrt(.12^2+.08^2))*180/pi
salva(data.frame(gx=.12,gy=.08,modulo=sqrt(.12^2+.08^2),pendenza_gradi=slope_plane,
 pendenza_percento=100*sqrt(.12^2+.08^2),aspect_gradi=(atan2(-.12,-.08)*180/pi)%%360,
 errore_gx=max(abs(pm$gx-.12)),errore_gy=max(abs(pm$gy-.08))),"piano_noto")
salva(inn,"derivate_interne")
slope_full<-matrix(NA_real_,24,30);slope_full[2:23,2:29]<-slope_deg
masked_morph<-morfometria(Z_mask);masked_full<-matrix(NA_real_,24,30);masked_full[2:23,2:29]<-masked_morph$slope_deg
salva(matrice_df(masked_full,x,y,"pendenza_gradi"),"pendenze_maschera")
slope_summary<-data.frame(n=length(slope_deg),minimo=min(slope_deg),media=mean(slope_deg),mediana=median(slope_deg),massimo=max(slope_deg),
 n_validi_con_maschera=sum(is.finite(masked_morph$slope_deg)),celle_bordo=104)
salva(slope_summary,"pendenza_riepilogo")
terra4<-terra::terrain(r_csv,v=c("slope","aspect"),neighbors=4,unit="degrees")
terra8<-terra::terrain(r_csv,v=c("slope","aspect"),neighbors=8,unit="degrees")
t4s<-matrice_locale(terra4[[1]])[2:23,2:29];t4a<-matrice_locale(terra4[[2]])[2:23,2:29]
t8s<-matrice_locale(terra8[[1]])[2:23,2:29]
terra_compare<-inn[c("x_m","y_m","pendenza_gradi")];terra_compare$terra4_gradi<-row_values(t4s);terra_compare$terra8_gradi<-row_values(t8s)
terra_compare$differenza4<-terra_compare$terra4_gradi-terra_compare$pendenza_gradi
terra_compare$differenza8<-terra_compare$terra8_gradi-terra_compare$pendenza_gradi
salva(terra_compare,"confronto_terra_4_8")
flat<-matrix(900,24,30);flat_morph<-morfometria(flat)
terra_flat<-terra::terrain(raster_locale(flat,x,y),v="aspect",neighbors=4,unit="degrees")
flat_vals<-as.vector(terra::values(terra_flat));flat_vals<-flat_vals[is.finite(flat_vals)]
circ_examples<-rbind(data.frame(caso="359 e 1",aritmetica=180,t(media_circolare(c(359,1)))),
 data.frame(caso="0 e 180",aritmetica=90,t(media_circolare(c(0,180)))),
 data.frame(caso="Esposizioni DEM",aritmetica=mean(aspect_deg,na.rm=TRUE),t(media_circolare(aspect_deg))))
salva(circ_examples,"media_circolare")
salva(data.frame(convenzione=c("Tessera: piatto","terra neighbors4: piatto"),aspect_gradi=c(NA_real_,unique(flat_vals)[1])),"aspect_piano")
# Medesimo supporto60m interno, due ordini operativi diversi.
coarse_morph<-morfometria(A2,60);fine_mean_slope<-aggrega2(slope_full)[2:11,2:14]
op_df<-matrice_df(coarse_morph$slope_deg,x2[2:14],y2[2:11],"media_quota_poi_pendenza")
op_df$pendenza_poi_media<-row_values(fine_mean_slope);op_df$differenza<-op_df$media_quota_poi_pendenza-op_df$pendenza_poi_media
salva(op_df,"confronto_operazioni")
salva(data.frame(n=nrow(op_df),media_quota_poi_pendenza=mean(op_df$media_quota_poi_pendenza),
 pendenza_poi_media=mean(op_df$pendenza_poi_media),MAE=mean(abs(op_df$differenza)),max_abs=max(abs(op_df$differenza))),"confronto_operazioni_riepilogo")
# 6. Sensibilità analitica separata: dominio900x600; confronto comune28ha.
analytic<-list();analytic_summary<-data.frame()
for(h in c(10,30,100)) {
 xx<-seq(h/2,900-h/2,h);yy<-seq(h/2,600-h/2,h)
 ZZ<-outer(yy,xx,function(y,x)superficie_analitica(x,y));mm<-morfometria(ZZ,h)
 xi<-xx[-c(1,length(xx))];yi<-yy[-c(1,length(yy))];ggrid<-expand.grid(x_m=xi,y_m=yi)
 exact<-gradiente_analitico(ggrid$x_m,ggrid$y_m);exact_slope<-atan(sqrt(exact$gx^2+exact$gy^2))*180/pi
 ww<-row_values(pesi_finestra(xi,yi,h));err<-row_values(mm$slope_deg)-exact_slope
 ad<-data.frame(passo_m=h,ggrid,gx=row_values(mm$gx),gy=row_values(mm$gy),gx_esatto=exact$gx,gy_esatto=exact$gy,
  pendenza_gradi=row_values(mm$slope_deg),pendenza_esatta=exact_slope,errore_gradi=err,peso_area_m2=ww)
 salva(ad,paste0("analitico_",h,"m"));salva(matrice_df(ZZ,xx,yy,"quota_m"),paste0("analitico_quote_",h,"m"))
 analytic[[as.character(h)]]<-list(x=xx,y=yy,Z=ZZ,morph=mm,dati=ad)
 analytic_summary<-rbind(analytic_summary,data.frame(passo_m=h,n_raster=length(ZZ),area_totale_ha=54,
  n_derivate=nrow(ad),celle_intersezione=sum(ww>0),area_confronto_ha=sum(ww)/10000,
  RMSE_pendenza_gradi=sqrt(weighted.mean(err^2,ww)),MAE_pendenza_gradi=weighted.mean(abs(err),ww),
  pendenza_media=weighted.mean(ad$pendenza_gradi,ww),pendenza_esatta_media=weighted.mean(exact_slope,ww)))
}
salva(analytic_summary,"sensibilita_analitica")
# 7. Illuminazione: normale-luce, azimut e limiti fisici.
light_summary<-data.frame(azimut=c(315,135),altezza=45,minimo=c(min(hill315),min(hill135)),
 media=c(mean(hill315),mean(hill135)),massimo=c(max(hill315),max(hill135)))
salva(light_summary,"hillshade_riepilogo")
profile_row<-12L;light_profile<-data.frame(x_m=inn$x_m[inn$y_m==y[profile_row]],y_m=y[profile_row],
 quota_m=Z[profile_row,2:29],luce315=hill315[profile_row-1,],luce135=hill135[profile_row-1,])
salva(light_profile,"hillshade_profilo")
# 8. Bande sintetiche, denominatore e scala/offset (esempio analitico).
sp<-d[c("x_m","y_m")];sp$rosso<-R_band;sp$NIR<-NIR;sp$denominatore<-NIR+R_band;sp$indice<-indice
salva(sp,"bande_indice")
demo_R<-c(.2,0,1e-10,.3);demo_N<-c(.4,0,2e-10,.2);den_demo<-indice_normalizzato(demo_N,demo_R)
salva(data.frame(R=demo_R,N=demo_N,den=den_demo$denominatore,usato=den_demo$valido,indice=den_demo$indice),"denominatore_originale_N14")
# Riflessioni simulate codificate con parametri dichiarati; nessun dato Landsat osservato.
scale_factor<-0.0000275;scale_offset<--.2
DN_R<-(R_band-scale_offset)/scale_factor;DN_N<-(NIR-scale_offset)/scale_factor
idx_DN<-(DN_N-DN_R)/(DN_N+DN_R)
scale_demo<-data.frame(x_m=d$x_m,y_m=d$y_m,R=R_band,NIR=NIR,DN_R=DN_R,DN_N=DN_N,
 indice_corretto=indice,indice_su_DN_ERRATO=idx_DN,indice_solo_scala=indice_normalizzato(NIR*2,R_band*2)$indice)
salva(scale_demo,"scala_offset_analitico")
# 9. Dipendenza e bootstrap di12blocchi: protocolli distinti.
diff30<-row_values(Z[,2:30]-Z[,1:29]);diff300<-row_values(Z[,11:30]-Z[,1:20])
diff_summary<-data.frame(distanza_m=c(30,300),n_coppie=c(length(diff30),length(diff300)),
 media_abs=c(mean(abs(diff30)),mean(abs(diff300))),semivarianza=c(mean(diff30^2)/2,mean(diff300^2)/2))
salva(diff_summary,"dipendenza_30_300");salva(data.frame(distanza_m=30,differenza_m=diff30),"differenze_30m");salva(data.frame(distanza_m=300,differenza_m=diff300),"differenze_300m")
salva(data.frame(blocco=1:12,n=60,area_ha=5.4,media=block_means),"blocchi12")
salva(matrice_df(block_id,x,y,"blocco"),"appartenenze_blocchi")
salva(data.frame(replica=1:300,media=boot300),"bootstrap300_originale")
salva(data.frame(replica=1:1999,media=boot1999),"bootstrap1999_estensione")
set.seed(20261110);boot_cells<-replicate(1999,mean(sample(as.vector(Z),replace=TRUE)))
salva(data.frame(replica=1:1999,media=boot_cells),"bootstrap_celle1999_esempio")
boot_summary<-do.call(rbind,lapply(list(list("Blocchi originale",boot300,"u[1:3600]"),
 list("Blocchi estensione",boot1999,"seed20261109"),list("Celle singole esempio",boot_cells,"seed20261110")),function(a){
 q<-quantile(a[[2]],c(.025,.975),type=7);data.frame(protocollo=a[[1]],B=length(a[[2]]),generatore=a[[3]],
 media_boot=mean(a[[2]]),sd_boot=sd(a[[2]]),q025=q[1],q975=q[2],ampiezza=diff(q))}))
salva(boot_summary,"bootstrap_riepilogo")
# 10. Finestra terra reale e halo per le derivate (indici TIFF a partire da1).
terra::readStart(r);win<-terra::readValues(r,row=5,nrows=6,col=10,ncols=8,mat=FALSE)
halo<-terra::readValues(r,row=4,nrows=8,col=9,ncols=10,mat=FALSE);terra::readStop(r)
win_error<-max(abs(win-row_values(M[5:10,10:17])))
H<-matrix(halo,8,byrow=TRUE);hcalc<-morfometria(H[8:1,])$slope_deg
expected_window<-slope_full[24:1,][5:10,10:17]
halo_error<-max(abs(hcalc[6:1,]-expected_window))
salva(data.frame(riga_tiff=rep(5:10,each=8),colonna_tiff=rep(10:17,6),quota_m=win),"finestra48")
salva(data.frame(celle_uscita=48,celle_lettura_con_halo=80,errore_lettura=win_error,errore_derivate_halo=halo_error),"finestra_verifica")
mem<-expand.grid(n_celle=c(720,1e6,1e8),bande=c(1,4));mem$bytes_double<-mem$n_celle*mem$bande*8
mem$MB_decimali<-mem$bytes_double/1e6;mem$MiB<-mem$bytes_double/2^20
salva(mem,"memoria_teorica")
salva(data.frame(oggetto=c("Matrice24x30","Finestra6x8","Finestra con halo8x10"),celle=c(720,48,80),
 bytes_valori=c(720,48,80)*8,bytes_oggetto_R=c(as.numeric(object.size(Z)),as.numeric(object.size(matrix(win,6,byrow=TRUE))),as.numeric(object.size(H)))),"memoria_oggetti")
# 11. GeoTIFF effettivi: valori materializzati e compressione NONE dichiarata.
export_specs<-list(pendenze_interne=raster_locale(slope_deg,x[2:29],y[2:23]),
 pendenze_con_bordo_NA=raster_locale(slope_full,x,y),quote_maschera=raster_locale(Z_mask,x,y))
export_summary<-data.frame();reread<-list()
for(nm in names(export_specs)) {
 rr<-export_specs[[nm]];names(rr)<-if(grepl("pendenze",nm))"pendenza_gradi" else "quota_m"
 fn<-file.path("Risultati",paste0(nm,".tif"));terra::writeRaster(rr,fn,overwrite=TRUE,datatype="FLT8S",NAflag=-9999,gdal="COMPRESS=NONE")
 rb<-terra::rast(fn);a<-as.vector(terra::values(rr));b<-as.vector(terra::values(rb));sameNA<-identical(is.na(a),is.na(b))
 er<-max(abs(a-b),na.rm=TRUE);geom_ok<-terra::compareGeom(rr,rb,stopOnError=FALSE)
 reread[[nm]]<-rb
 export_summary<-rbind(export_summary,data.frame(file=basename(fn),righe=nrow(rb),colonne=ncol(rb),validi=sum(is.finite(b)),NoData=sum(is.na(b)),
  minimo=min(b,na.rm=TRUE),massimo=max(b,na.rm=TRUE),errore_max=er,maschera_identica=sameNA,geometria_identica=geom_ok))
}
salva(export_summary,"export_verifica")
write.csv(inn[c("x_m","y_m","pendenza_gradi")],"Risultati/pendenze.csv",row.names=FALSE)
# 12. Verifiche sostanziali: casi esatti, maschere, supporto e file realmente riletti.
verifica("Griglia completa unica e regolare",nrow(d)==720&&!anyDuplicated(paste(d$riga,d$colonna))&&all(diff(x)==30)&&all(diff(y)==30))
verifica("Geometria GeoTIFF originale",nrow(r)==24&&ncol(r)==30&&all(terra::res(r)==30)&&all(as.vector(terra::ext(r))==c(500000,500900,4999280,5000000)))
verifica("Orientamento CSV-TIFF",raw_error<.001,paste("errore massimo",raw_error))
verifica("Coordinate dei centri e mezza cella",max(abs(xy_tiff-xy_att))<1e-10)
verifica("Maschera24 e copertura696",sum(is.na(Z_mask))==24&&sum(is.finite(Z_mask))==696)
verifica("Area completa64.8ha",abs(sum(zone$area_ha)-64.8)<1e-10)
verifica("Media aggregata conservata",abs(mean(A2)-mean(Z))<1e-10&&max(A2)<=max(Z))
verifica("Near conserva codici nominali",all(class_near%in%c(1,2)))
verifica("Bilineare crea codici intermedi",any(!class_bilinear%in%c(1,2)))
verifica("Derivate piano esatte",max(abs(pm$gx-.12))<1e-12&&max(abs(pm$gy-.08))<1e-12)
verifica("Piano pendenza e aspect",max(abs(pm$slope_deg-slope_plane))<1e-11&&max(abs(pm$aspect_deg-(atan2(-.12,-.08)*180/pi)%%360))<1e-10)
verifica("616 celle interne e104bordo",length(slope_deg)==616&&sum(is.na(slope_full))==104)
verifica("45gradi=100percento",abs(100*tan(pi/4)-100)<1e-10)
verifica("Centro e4vicini richiesti",!any(is.finite(masked_morph$slope_deg)&!masked_morph$valido)&&sum(masked_morph$valido)<616)
verifica("Flat: pendenza0 e aspectNA",all(flat_morph$slope_deg==0)&&all(is.na(flat_morph$aspect_deg)))
verifica("Media circolare359/1",abs(media_circolare(c(359,1))[1])<1e-10&&abs(media_circolare(c(359,1))[2]-cos(pi/180))<1e-12)
verifica("Direzioni opposte senza media definita",is.na(media_circolare(c(0,180))[1]))
verifica("terra4 coincide con differenze centrate",max(abs(t4s-slope_deg))<1e-10)
verifica("Aspect terra4 coincide modulo360",max(abs(((t4a-aspect_deg+180)%%360)-180),na.rm=TRUE)<1e-10)
verifica("terra documenta aspect90 sui piani",all(flat_vals==90))
verifica("Dominio analitico comune28ha",all(abs(analytic_summary$area_confronto_ha-28)<1e-10))
verifica("Hillshade limitata",all(hill315>=0&hill315<=1)&&all(hill135>=0&hill135<=1))
for(az in c(315,135)) {
 aa<-az*pi/180;asp<-aspect_deg*pi/180;sl<-slope_deg*pi/180
 trig<-pmax(cos(pi/4)*cos(sl)+sin(pi/4)*sin(sl)*cos(aa-asp),0)
 hh<-hillshade_normale(gx,gy,az)
 verifica(paste("Hillshade normale-trigonometria",az),identical(dim(hh),c(22L,28L))&&max(abs(hh-trig))<1e-12)
}
verifica("Flat hillshade fisica",all(abs(hillshade_normale(flat_morph$gx,flat_morph$gy)-sin(pi/4))<1e-12))
verifica("Indice sintetico finito e limitato",all(NIR+R_band>0)&&all(abs(indice)<=1))
verifica("Denominatore mascherato",sum(is.na(den_demo$indice))==2)
verifica("Scala comune si cancella, offset no",max(abs(scale_demo$indice_solo_scala-indice))<1e-12&&max(abs(idx_DN-indice))>.01)
verifica("Media zonale pesata ricostruisce totale",abs(weighted.mean(zone$media,zone$n)-mean(Z))<1e-10)
verifica("Zone mascherate pesate ricostruiscono disponibili",abs(weighted.mean(zone_mask$media_disponibili,zone_mask$n_disponibili)-mean(Z_mask,na.rm=TRUE))<1e-10)
verifica("696 e480 coppie a30 e300m",length(diff30)==696&&length(diff300)==480)
verifica("12 blocchi60celle e media conservata",length(block_means)==12&&all(table(block_id)==60)&&abs(mean(block_means)-mean(Z))<1e-10)
verifica("Bootstrap originale300 da3600uniformi",length(boot300)==300&&all(ix300>=1&ix300<=12))
verifica("Finestra terra48 esatta",length(win)==48&&win_error<1e-10)
verifica("Halo riproduce derivate globali",length(halo)==80&&halo_error<1e-7,paste("errore",halo_error))
verifica("Export geometria valori maschera",all(export_summary$geometria_identica)&all(export_summary$maschera_identica)&all(export_summary$errore_max<1e-10))
verifica("Export616validi e104NoData",export_summary$validi[1]==616&&export_summary$NoData[1]==0&&export_summary$validi[2]==616&&export_summary$NoData[2]==104)
write.csv(tests,"Verifiche/test_numerici.csv",row.names=FALSE)
writeLines(capture.output(sessionInfo()),"Verifiche/SESSIONE_R.txt")
writeLines(capture.output(terra::gdal(lib="all")),"Verifiche/VERSIONI_TERRA_GDAL.txt")
summary<-list(modulo="M12 Tessera",n=720,n_righe=24,n_colonne=30,passo_m=30,area_ha=64.8,
 origine_centri_fittizia=c(E=500015,N=4999295),estensione_tiff=as.vector(terra::ext(r)),errore_tiff_csv=raw_error,
 quota=list(min=min(Z),media=mean(Z),max=max(Z),sd=sd(c(Z))),domini=coverage,aggregazione=agg_summary,
 pendenza=slope_summary,piano=list(gx=.12,gy=.08,gradi=slope_plane,percento=100*sqrt(.12^2+.08^2),aspect=(atan2(-.12,-.08)*180/pi)%%360),
 terra=list(versione=as.character(packageVersion("terra")),librerie=terra::gdal(lib="all"),errore4=max(abs(t4s-slope_deg)),
 differenza8=list(MAE=mean(abs(t8s-slope_deg)),max_abs=max(abs(t8s-slope_deg)))),
 confronto_operazioni=list(n=nrow(op_df),MAE=mean(abs(op_df$differenza)),max_abs=max(abs(op_df$differenza))),
 sensibilita_analitica=analytic_summary,media_circolare=circ_examples,hillshade=light_summary,
 indice=list(min=min(indice),media=mean(indice),max=max(indice),den_min=min(NIR+R_band)),zone=zone,zone_maschera=zone_mask,
 dipendenza=diff_summary,bootstrap=boot_summary,allineamento=shift_summary,finestra=list(n=48,halo=80,errore=win_error,errore_halo=halo_error),
 export=export_summary,verifiche=list(superate=sum(tests$ok),totale=nrow(tests)),R=R.version.string,
 limiti=c("Dati integralmente sintetici; georeferenziazione fittizia","Bootstrap descrittivo sotto scambiabilita dei blocchi; nessuna copertura garantita",
 "Sensibilita10/30/100: superficie analitica separata, non ricostruzione osservata","GeoTIFF FLT8S senza compressione; NoData=-9999"))
writeLines(to_json(summary),"Calcoli/summary.json");writeLines(to_json(summary),"Calcoli/riassunto.json")
cat("CALCOLI PASS",nrow(tests),"verifiche\n")
if(file.exists("R/genera_figure.R"))source("R/genera_figure.R",encoding="UTF-8")
cat("TESSERA COMPLETATO\n")
