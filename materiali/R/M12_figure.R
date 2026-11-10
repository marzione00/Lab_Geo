source('R/stile.R')
salva_originale<-salva
salva<-function(mod,id,p,w=5.2,h=3.8){
 mappa<-id%in%c('F01','F02','F03','F04','F06','F07','F08')
 if(mappa)p<-p+guides(fill=guide_colourbar(barwidth=grid::unit(2.7,'in'),barheight=grid::unit(.13,'in')))
 salva_originale(mod,id,p,w,if(mappa)4.2 else h)
}
d<-leggi('raster_v3.csv');d<-d[order(d$riga,d$colonna),];Z<-matrix(d$quota_m,24,byrow=TRUE)
base_map<-function(x=d)ggplot(x,aes(x_m,y_m))+coord_equal()+scale_x_continuous(breaks=c(0,300,600,900))+scale_y_continuous(breaks=c(0,300,600))+labs(x='x (m)',y='y (m)')
cs<-function(nam='Quota (m)',lim=NULL)scale_fill_gradientn(colours=c('#E1E9B2','#3C9F86','#254D67'),name=nam,limits=lim,breaks=if(nam=='Quota (m)')c(900,1000,1100)else waiver())
salva('M12','F01',base_map()+geom_raster(aes(fill=quota_m))+cs())
mask<-d;mask$quota_m[mask$riga%in%4:7 & mask$colonna%in%9:14]<-NA
salva('M12','F02',base_map(mask)+geom_raster(aes(fill=quota_m))+scale_fill_gradientn(colours=c('#E1E9B2','#3C9F86','#254D67'),name='Quota (m)',na.value='#D5B4C8',breaks=c(900,1000,1100),limits=range(d$quota_m)))
d$blocco<-paste(d$riga%/%2,d$colonna%/%2,sep='_');ag<-aggregate(cbind(x_m,y_m,quota_m)~blocco,d,mean)
salva('M12','F03',base_map(ag)+geom_tile(aes(fill=quota_m),width=60,height=60)+cs(lim=range(d$quota_m)))
gx<-(Z[2:23,3:30]-Z[2:23,1:28])/60;gy<-(Z[3:24,2:29]-Z[1:22,2:29])/60
s<-atan(sqrt(gx^2+gy^2));asp<-(atan2(-gx,-gy)%%(2*pi))
inn<-expand.grid(x_m=(1:28)*30,y_m=(1:22)*30);inn$slope<-as.vector(t(s))*180/pi;inn$aspect<-as.vector(t(asp))*180/pi
salva('M12','F04',base_map(inn)+geom_raster(aes(fill=slope))+cs('Pendenza (°)'))
q<-data.frame(gradi=seq(0,70,length.out=200));q$percento<-100*tan(q$gradi*pi/180)
salva('M12','F05',ggplot(q,aes(gradi,percento))+geom_line(colour=geo[1],linewidth=.8)+geom_point(data=data.frame(gradi=45,percento=100),size=3,colour=geo[2])+geom_hline(yintercept=100,linetype=2,colour=geo[6])+scale_x_continuous(breaks=c(0,30,45,60))+labs(x='Angolo (°)',y='Pendenza (%)'))
hill<-function(az)pmax(cos(pi/4)*cos(s)+sin(pi/4)*sin(s)*cos(az*pi/180-asp),0)
inn$luce315<-as.vector(t(hill(315)));inn$luce135<-as.vector(t(hill(135)))
for(k in c(315,135)){
 inn$luce<-inn[[paste0('luce',k)]]
 salva('M12',if(k==315)'F06' else 'F07',base_map(inn)+geom_raster(aes(fill=luce))+scale_fill_gradient(low='#15283E',high='#F8F6F1',limits=c(0,1),breaks=c(0,.5,1),labels=fmt,name=paste('Luce: azimut',k,'°')))
}
R<-.2+.05*cos(d$y_m/150);N<-.4+.1*sin(d$x_m/180);d$indice<-(N-R)/(N+R)
salva('M12','F08',base_map()+geom_raster(aes(fill=indice))+scale_fill_gradient2(low=geo[2],mid=paper,high=geo[1],midpoint=0,limits=c(-1,1),breaks=c(-1,0,1),name='Indice normalizzato'))
cl<-data.frame(x=c(0,30,60,90),classe=c(1,1,2,2));v<-seq(0,90,1);cc<-rbind(data.frame(x=v,classe=approx(cl$x,cl$classe,xout=v)$y,metodo='Lineare'),data.frame(x=v,classe=sapply(v,function(q)cl$classe[which.min(abs(cl$x-q))]),metodo='Vicino'))
salva('M12','F09',ggplot(cc,aes(x,classe,colour=metodo))+geom_line(linewidth=.8)+geom_point(data=cl,aes(x,classe),inherit.aes=FALSE,colour=ink,size=3)+scale_colour_manual(values=c(geo[2],geo[1]))+scale_y_continuous(breaks=c(1,1.5,2),labels=fmt)+scale_x_continuous(breaks=c(0,30,60,90))+labs(x='Posizione (m)',y='Codice nominale'))
zone<-aggregate(quota_m~unita,d,mean);zone$n<-as.integer(table(d$unita)[zone$unita]);zone$area_ha<-zone$n*.09
salva('M12','F10',ggplot(d,aes(unita,quota_m,fill=unita))+geom_boxplot(width=.55,outlier.size=.6)+scale_fill_manual(values=geo[1:2],guide='none')+labs(x='Zona sintetica',y='Quota (m)'))
bid<-paste(d$riga%/%6,d$colonna%/%10,sep='_');bv<-tapply(d$quota_m,bid,mean);set.seed(20261109);boots<-replicate(1999,mean(sample(bv,replace=TRUE)))
salva('M12','F11',ggplot(data.frame(media=boots),aes(media))+geom_histogram(bins=22,fill=geo[1],colour=paper)+geom_vline(xintercept=mean(Z),colour=geo[2],linewidth=.8)+labs(x='Media ricampionata (m)',y='Ripetizioni'))
# Verifiche numeriche e confronto con la georeferenziazione fittizia.
rr<-terra::rast('dati/raster_v3.tif');M<-as.matrix(rr,wide=TRUE)
plane<-outer((0:23)*30,(0:29)*30,function(y,x)900+.12*x+.08*y)
px<-(plane[2:23,3:30]-plane[2:23,1:28])/60;py<-(plane[3:24,2:29]-plane[1:22,2:29])/60
verifica('Griglia completa senza celle duplicate',nrow(d)==720&&!anyDuplicated(paste(d$riga,d$colonna))&&all(diff(sort(unique(d$x_m)))==30)&&all(diff(sort(unique(d$y_m)))==30))
verifica('GeoTIFF: dimensioni e risoluzione',nrow(rr)==24&&ncol(rr)==30&&all(terra::res(rr)==30))
verifica('GeoTIFF: orientamento opposto alla matrice locale',max(abs(M-Z[24:1,]))<.001)
verifica('Superficie complessiva',abs(sum(zone$area_ha)-64.8)<1e-10)
verifica('Maschera: 24 celle esplicite',sum(is.na(mask$quota_m))==24)
verifica('Aggregazione: media conservata',abs(mean(ag$quota_m)-mean(Z))<1e-10&&max(ag$quota_m)<=max(Z))
verifica('Derivate del piano noto',max(abs(px-.12))<1e-12&&max(abs(py-.08))<1e-12)
verifica('Pendenza: 45 gradi corrispondono al 100 per cento',abs(100*tan(pi/4)-100)<1e-10)
verifica('Differenze centrate: 616 celle interne',nrow(inn)==616&&all(is.finite(inn$slope)))
verifica('Ombreggiatura fisicamente limitata',all(inn$luce315>=0&inn$luce315<=1)&&all(inn$luce135>=0&inn$luce135<=1))
# pmax conserva gli attributi del primo argomento: la matrice precede lo zero.
# Verifica indipendente: prodotto scalare normale-luce per ogni coordinata esportata.
idx<-cbind(inn$y_m/30,inn$x_m/30);gx_cella<-gx[idx];gy_cella<-gy[idx]
for(az in c(315,135)){
 luce<-c(sin(az*pi/180)*cos(pi/4),cos(az*pi/180)*cos(pi/4),sin(pi/4))
 attesa<-pmax(0,(-gx_cella*luce[1]-gy_cella*luce[2]+luce[3])/sqrt(1+gx_cella^2+gy_cella^2))
 verifica(paste('Ombreggiatura: geometria e ordine delle celle',az),
          identical(dim(hill(az)),dim(gx)) && max(abs(inn[[paste0('luce',az)]]-attesa))<1e-12)
}
verifica('Indice: denominatore positivo e intervallo',all(N+R>0)&&all(abs(d$indice)<=1))
verifica('Blocchi completi equiponderati',length(bv)==12&&abs(mean(bv)-mean(Z))<1e-10)
terra::readStart(rr);win<-terra::readValues(rr,row=5,nrows=6,col=10,ncols=8,mat=FALSE);terra::readStop(rr)
verifica('Lettura a finestre coerente',max(abs(win-as.vector(t(M[5:10,10:17]))))<1e-10)
out<-'risultati/M12';dir.create(out,recursive=TRUE,showWarnings=FALSE)
write.csv(inn,file.path(out,'derivate_interne.csv'),row.names=FALSE)
write.csv(zone,file.path(out,'statistiche_zonali.csv'),row.names=FALSE)
write.csv(data.frame(media=boots),file.path(out,'bootstrap_blocchi.csv'),row.names=FALSE)
jsonlite::write_json(list(media=mean(Z),massimo=max(Z),media_aggregata=mean(ag$quota_m),massimo_aggregato=max(ag$quota_m),copertura=mean(!is.na(mask$quota_m)),media_disponibili=mean(mask$quota_m,na.rm=TRUE),media_zero=sum(mask$quota_m,na.rm=TRUE)/720,pendenza_piano_gradi=atan(sqrt(.12^2+.08^2))*180/pi,bootstrap_quantili=unname(quantile(boots,c(.025,.975))),estensione_tiff=as.vector(terra::ext(rr))),file.path(out,'valori.json'),auto_unbox=TRUE,pretty=TRUE,digits=12)
