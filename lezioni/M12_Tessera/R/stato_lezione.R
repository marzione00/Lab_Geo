# Stato leggero per frammenti e lezione: nessuna figura o esportazione.
source("setup.R",encoding="UTF-8")
d<-read.csv("Dati/raster_v3.csv");d<-d[order(d$riga,d$colonna),]
casuali<-read.csv("Dati/casuali_comuni_v3.csv");u<-casuali$u
x<-sort(unique(d$x_m));y<-sort(unique(d$y_m));dx<-30;dy<-30
Z<-matrix(d$quota_m,nrow=24,byrow=TRUE)
r<-terra::rast("Dati/raster_v3.tif");M<-as.matrix(r,wide=TRUE)
mask<-matrix(FALSE,24,30);mask[5:8,10:15]<-TRUE;Z_mask<-Z;Z_mask[mask]<-NA_real_
A2<-aggrega2(Z);x2<-(0:14)*60+15;y2<-(0:11)*60+15
morph<-morfometria(Z);gx<-morph$gx;gy<-morph$gy;g<-morph$g
slope_deg<-morph$slope_deg;slope_pct<-morph$slope_pct;aspect_deg<-morph$aspect_deg
inn<-expand.grid(x_m=x[2:29],y_m=y[2:23]);inn$gx<-row_values(gx);inn$gy<-row_values(gy)
inn$pendenza_gradi<-row_values(slope_deg);inn$pendenza_percento<-row_values(slope_pct);inn$aspect_gradi<-row_values(aspect_deg)
hill315<-hillshade_normale(gx,gy,315);hill135<-hillshade_normale(gx,gy,135)
inn$luce315<-row_values(hill315);inn$luce135<-row_values(hill135)
R_band<-.2+.05*cos(d$y_m/150);NIR<-.4+.1*sin(d$x_m/180)
nd<-indice_normalizzato(NIR,R_band);indice<-nd$indice
zone<-aggregate(quota_m~unita,d,mean);names(zone)[2]<-"media"
zone$n<-as.numeric(table(d$unita)[zone$unita]);zone$area_ha<-zone$n*dx*dy/10000
zone$sd<-as.numeric(tapply(d$quota_m,d$unita,sd)[zone$unita])
block_means<-numeric(12);block_id<-matrix(NA_integer_,24,30);k<-1L
for(i in 1:4)for(j in 1:3){rr<-((i-1)*6+1):(i*6);cc<-((j-1)*10+1):(j*10)
 block_means[k]<-mean(Z[rr,cc]);block_id[rr,cc]<-k;k<-k+1L}
ix300<-matrix(floor(u[1:3600]*12)+1,300,byrow=TRUE)
boot300<-apply(ix300,1,function(i)mean(block_means[i]))
set.seed(20261109);boot1999<-replicate(1999,mean(sample(block_means,replace=TRUE)))
