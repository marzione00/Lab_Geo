# M11 Locus — calcoli realmente eseguiti e figure riproducibili.
source("R/stato_lezione.R",encoding="UTF-8")
for(p in c("Calcoli","Risultati/Figure","Verifiche"))dir.create(p,recursive=TRUE,showWarnings=FALSE)
salva<-function(x,nome)write.csv(x,file.path("Calcoli",paste0(nome,".csv")),row.names=FALSE,na="")
# Coordinate: piano locale e geografia sintetica rimangono due rappresentazioni distinte.
utm_xy<-sf::st_coordinates(utm);back_xy<-sf::st_coordinates(ritorno)
roundtrip_max<-max(abs(back_xy-as.matrix(d[c("lon","lat")])))
geo0<-sf::st_as_sf(d,coords=c("lon","lat"),crs=NA,remove=FALSE)
geo_assigned<-sf::st_set_crs(geo0,"OGC:CRS84")
D_sfera<-outer(1:n,1:n,Vectorize(function(i,j)haversine(d$lon[i],d$lat[i],d$lon[j],d$lat[j])))
D_utm<-as.matrix(dist(utm_xy))
salva(data.frame(id=d$id,xy,lon=d$lon,lat=d$lat,UTM_E=utm_xy[,1],UTM_N=utm_xy[,2],
 locale_da_S01=D[1,],sfera_da_S01=D_sfera[1,],UTM_da_S01=D_utm[1,],
 errore_ritorno=apply(abs(back_xy-as.matrix(d[c("lon","lat")])),1,max)),"coordinate_verificate")
salva(data.frame(locale=D[upper.tri(D)],sfera=D_sfera[upper.tri(D)],UTM=D_utm[upper.tri(D)]),"distanze_confronto")
sf::st_write(geo,"Risultati/campioni_RFC7946.geojson",driver="GeoJSON",delete_dsn=TRUE,quiet=TRUE,
 layer_options=c("RFC7946=YES","COORDINATE_PRECISION=10"))
geo_riletto<-sf::st_read("Risultati/campioni_RFC7946.geojson",quiet=TRUE)
gidx<-match(d$id,geo_riletto$id)
geojson_error<-max(abs(sf::st_coordinates(sf::st_transform(geo_riletto,"OGC:CRS84"))[gidx,]-as.matrix(d[c("lon","lat")])))
salva(data.frame(fonte=c("x_m/y_m","lon/lat","trasformazione"),CRS=c("Locale ignoto; nessun EPSG","OGC:CRS84","EPSG:32632"),unita=c("m","gradi","m")),"CRS_metadati")
# Partizioni, aggregazioni e supporto; nessuna inferenza areale dai soli punti.
aggregato<-function(gruppo){a<-aggregate(z,list(gruppo=gruppo),mean);names(a)[2]<-"media";a$n<-as.integer(table(gruppo)[a$gruppo]);a}
regioni<-ifelse(d$x_m<1000,"Ovest","Est");agg_oe<-aggregato(regioni)
blocchi<-paste(ifelse(d$x_m<1000,"Ovest","Est"),ifelse(d$y_m<1000,"Sud","Nord"),sep="_")
agg_blocchi<-aggregato(blocchi)
partizioni<-list(Est_Ovest_1000=regioni,Nord_Sud_1000=ifelse(d$y_m<1000,"Sud","Nord"),
 Est_Ovest_750=ifelse(d$x_m<750,"Ovest","Est"),Diagonale=ifelse(d$x_m+d$y_m<1750,"Basso","Alto"))
agg_alt<-do.call(rbind,lapply(names(partizioni),function(nm)data.frame(partizione=nm,aggregato(partizioni[[nm]]))))
salva(agg_oe,"medie_Ovest_Est");salva(agg_blocchi,"medie_blocchi");salva(agg_alt,"aggregazioni_alternative")
member<-cbind(A=d$x_m<=1250,B=d$x_m>=750)
join_table<-do.call(rbind,lapply(1:n,function(i)data.frame(id=d$id[i],regione=colnames(member)[member[i,]],z=z[i])))
salva(join_table,"join_appartenenze");salva(data.frame(id=d$id,A=member[,1],B=member[,2],n_appartenenze=rowSums(member)),"appartenenze_siti")
confini<-data.frame(regola=c("<1000 / >=1000","<=1000 / >=1000","<1000 / >1000"),
 appartenenze=c(sum(d$x_m<1000)+sum(d$x_m>=1000),sum(d$x_m<=1000)+sum(d$x_m>=1000),sum(d$x_m<1000)+sum(d$x_m>1000)),
 duplicati=c(0,sum(d$x_m==1000),0),esclusi=c(0,0,sum(d$x_m==1000)))
salva(confini,"confini_semiaperti")
center<-c(750,750);r0<-sqrt(rowSums(sweep(xy,2,center,"-")^2));rr<-c(300,600,900)
buffers<-data.frame(raggio_m=rr,n=vapply(rr,function(r)sum(r0<=r),0),media=vapply(rr,function(r)mean(z[r0<=r]),0))
salva(buffers,"buffer_raggi")
# Vicinati e distinzione fra A binaria e W normalizzata per riga.
edges<-which(upper.tri(A)&A==1,arr.ind=TRUE)
salva(data.frame(da=d$id[edges[,1]],a=d$id[edges[,2]],distanza=D[edges]),"archi_vicinato")
salva(data.frame(id=d$id,A),"matrice_A");salva(data.frame(id=d$id,W),"matrice_W")
salva(data.frame(id=d$id,n_vicini=nv,peso_singolo=1/nv,lag_valore=as.vector(W%*%z),v=v,lag_W=lag_W),"vicinati_e_lag")
cutoffs<-c(249,250,260,354,500,750)
sens<-do.call(rbind,lapply(cutoffs,function(r){aa<-1*(D>0&D<=r);nn<-rowSums(aa);ww<-normalizza_righe(aa,"zero");
 data.frame(raggio=r,archi=sum(aa)/2,isolati=sum(nn==0),grado_min=min(nn),grado_max=max(nn),
 I_A=if(sum(aa)>0)moran_I(z,aa)else NA_real_,I_W=if(sum(ww)>0)moran_I(z,ww)else NA_real_)}))
salva(sens,"sensibilita_vicinato")
scatter_fit<-lm(lag_W~v)
quadrante<-ifelse(v>=0&lag_W>=0,"HH",ifelse(v<0&lag_W<0,"LL",ifelse(v>=0,"HL","LH")))
salva(data.frame(id=d$id,v=v,lag_W=lag_W,quadrante=quadrante,contributo_W=v*lag_W/(sum(v^2)/n)),"Moran_scatter")
salva(data.frame(pesi=c("A binaria","W per riga"),S0=c(sum(A),sum(W)),I=c(I_A,I_W)),"Moran_indici")
# B100 riproduce M11_N14: blocchi consecutivi di64 uniformi del CSV, ordinati.
u<-casuali$u;B100<-100L
null100<-sapply(1:B100,function(b)moran_centrato(v[order(u[((b-1)*64+1):(b*64)])],A))
set.seed(20261109);B999<-999L;null999<-replicate(B999,moran_centrato(sample(v),A))
p100<-(1+sum(null100>=I_A))/(B100+1);p999<-(1+sum(null999>=I_A))/(B999+1)
salva(data.frame(b=1:B100,I_A=null100),"permutazioni_100_originali")
salva(data.frame(b=1:B999,I_A=null999),"permutazioni_999")
salva(data.frame(B=c(B100,B999),I_osservato=I_A,superamenti=c(sum(null100>=I_A),sum(null999>=I_A)),
 p_plus1=c(p100,p999),media_null=c(mean(null100),mean(null999)),atteso=-1/(n-1)),"permutazioni_riepilogo")
# Trend e residui: soltanto descrizione, senza un falso test esatto dei residui permutati.
salva(data.frame(id=d$id,x_m=d$x_m,y_m=d$y_m,osservato=z,trend=fitted(trend),residuo=residui),"trend_residui")
salva(data.frame(termine=names(coef(trend)),stima=coef(trend)),"trend_coefficienti")
I_res_A<-moran_I(residui,A);I_res_W<-moran_I(residui,W)
salva(data.frame(serie=c("Grezza","Residui del trend"),I_A=c(I_A,I_res_A),I_W=c(I_W,I_res_W),interpretazione="descrittiva; nessun test esatto sui residui"),"Moran_trend_residui")
# Coppie non indipendenti: i<j, senza diagonale e senza duplicare orientamento.
salva(coppie,"coppie_semivarianza");salva(vg,"semivariogramma")
cp_res<-coppie_spaziali(xy,residui);vg_res<-variogramma_bin(cp_res);salva(vg_res,"semivariogramma_residui")
direzionali<-do.call(rbind,lapply(c("Grezza","Residui"),function(tipo){cp<-if(tipo=="Grezza")coppie else cp_res;
 do.call(rbind,lapply(c("Est_Ovest","Nord_Sud"),function(dir){ss<-if(dir=="Est_Ovest")cp$angolo<=22.5 else cp$angolo>=67.5;
 data.frame(serie=tipo,direzione=dir,variogramma_bin(cp[ss,]))}))}))
salva(direzionali,"variogrammi_direzionali")
hh<-seq(0,2500,by=10);nugget<-.2;psill<-4;rpratico<-1200
models<-data.frame(h=hh,Esponenziale=ifelse(hh==0,0,nugget+psill*(1-exp(-3*hh/rpratico))),
 Gaussiano=ifelse(hh==0,0,nugget+psill*(1-exp(-3*(hh/rpratico)^2))),
 Sferico=ifelse(hh==0,0,nugget+psill*ifelse(hh<rpratico,1.5*hh/rpratico-.5*(hh/rpratico)^3,1)))
salva(models,"modelli_variogramma_teorici")
salva(data.frame(modello=c("Esponenziale","Gaussiano","Sferico"),nugget=.2,sill_parziale=4,
 parametro_scala=c(400,1200/sqrt(3),1200),nota=c("C(h)=4 exp(-h/a),h>0","C(h)=4 exp(-(h/a)^2),h>0","Portata esatta r=1200; altre curve portata pratica circa1200")),"parametri_variogrammi_teorici")
# Copertura e medie: target dichiarato, nessun errore standard iid automatico.
road<-d$y_m<=250
copertura<-data.frame(campione=c("Reticolo completo","Strada"),n=c(n,sum(road)),media=c(mean(z),mean(z[road])))
salva(copertura,"copertura_strada")
cov_y<-data.frame(y=sort(unique(d$y_m)),n_totale=8,n_strada=vapply(sort(unique(d$y_m)),function(y)sum(road&d$y_m==y),0))
salva(cov_y,"copertura_per_fila")
unequal<-aggregato(ifelse(d$x_m<750,"Ovest","Est"));unequal$peso_siti<-unequal$n/n;unequal$peso_blocchi<-.5
salva(unequal,"pesi_blocchi_squilibrati")
salva(data.frame(stimando=c("Media dei64siti","Media blocchi uguale peso","Media blocchi pesata per n"),
 media=c(mean(z),mean(unequal$media),weighted.mean(unequal$media,unequal$n))),"confronto_medie_pesate")
# IDW, punto didattico, superficie e trasferimento geografico.
target<-c(900,900);dist_target<-sqrt(rowSums(sweep(xy,2,target,"-")^2))
powers<-1:3;weights<-sapply(powers,function(p)idw_weights(xy,target,p))
salva(data.frame(id=d$id,distanza=dist_target,p1=weights[,1],p2=weights[,2],p3=weights[,3]),"IDW_pesi")
idw_powers<-data.frame(p=powers,previsione=as.numeric(t(weights)%*%z),n_eff_pesi=1/colSums(weights^2))
salva(idw_powers,"IDW_potenze")
grid<-expand.grid(x_m=seq(0,1750,length.out=45),y_m=seq(0,1750,length.out=45))
grid$previsto<-idw_pred(xy,z,as.matrix(grid),p=2);salva(grid,"IDW_superficie")
pred_mean<-rep(mean(train$concentrazione),nrow(test));pred_nn<-nn_pred(xy[train_idx,],z[train_idx],xy[test_idx,])
metrics<-data.frame(modello=c("Media_train","Nearest_neighbour","IDW_p2"),
 rbind(metriche(test$concentrazione,pred_mean),metriche(test$concentrazione,pred_nn),metriche(test$concentrazione,pred_idw)))
err<-test$concentrazione-pred_idw;dmin<-apply(dist_cross(xy[train_idx,],xy[test_idx,]),1,min)
predictions<-data.frame(id=test$id,x_m=test$x_m,y_m=test$y_m,osservato=test$concentrazione,
 IDW_p2=pred_idw,Media_train=pred_mean,Nearest_neighbour=pred_nn,errore_IDW=err,distanza_train=dmin)
salva(metrics,"metriche_test");salva(predictions,"previsioni_test")
salva(data.frame(id=d$id,train=train_idx,test=test_idx),"split_geografico")
salva(do.call(rbind,lapply(split(predictions,predictions$x_m),function(q)data.frame(x_m=q$x_m[1],n=nrow(q),distanza=min(q$distanza_train),t(metriche(q$osservato,q$IDW_p2))))),"errori_per_colonna")
# Approfondimento: tre frontiere di validazione all'interno dei40 siti train.
cuts<-c(500,750,1000)
inner<-do.call(rbind,lapply(cuts,function(cut){it<-train$x_m<cut;iv<-train$x_m==cut;
 do.call(rbind,lapply(1:3,function(p){pr<-idw_pred(as.matrix(train[it,c("x_m","y_m")]),train$concentrazione[it],as.matrix(train[iv,c("x_m","y_m")]),p);
 data.frame(frontiera=cut,p=p,id=train$id[iv],osservato=train$concentrazione[iv],previsto=pr,n_train=sum(it))}))}))
inner_metrics<-do.call(rbind,lapply(split(inner,inner$p),function(a)data.frame(p=a$p[1],n=nrow(a),t(metriche(a$osservato,a$previsto)))))
p_inner<-inner_metrics$p[which.min(inner_metrics$RMSE)]
salva(inner,"validazione_interna_IDW");salva(inner_metrics,"tuning_blocchi")
# Kriging: esempio separato con covarianza gaussiana dichiarata, non stimata dal reticolo.
ok_weights<-data.frame(sito=c("A","B","C"),x=ok$xy[,1],y=ok$xy[,2],z=ok$z,lambda=ok$fit$weights)
salva(ok_weights,"kriging_pesi");salva(data.frame(ok$C),"kriging_C")
salva(data.frame(c0=ok$c0),"kriging_c0")
ok_x<-seq(-250,1250,by=10)
ok_curve<-do.call(rbind,lapply(ok_x,function(x){c0<-4*exp(-rowSums(sweep(ok$xy,2,c(x,0),"-")^2)/800^2);
 oo<-ok_solve(ok$C,c0,4,ok$z);data.frame(x=x,previsto=oo$prediction,varianza=oo$variance,
 lambda1=oo$weights[1],lambda2=oo$weights[2],lambda3=oo$weights[3])}))
salva(ok_curve,"kriging_varianza")
salva(data.frame(somma_pesi=sum(ok$fit$weights),previsione=ok$fit$prediction,varianza_diretta=ok$fit$variance_direct,
 varianza_sistema=ok$fit$variance_system,moltiplicatore=ok$fit$mu,pesi_negativi=sum(ok$fit$weights<0)),"kriging_riepilogo")
# Casi noti e rischi reali di implementazione.
changed<-d;changed$concentrazione[test_idx]<-changed$concentrazione[test_idx]+1000*seq_len(sum(test_idx))
tr_changed<-changed[changed$x_m<1250,];p_changed<-idw_pred(as.matrix(tr_changed[c("x_m","y_m")]),tr_changed$concentrazione,xy[test_idx,])
ok_ind<-ok_solve(diag(3),rep(0,3),1,c(2,5,8))
checks<-data.frame(controllo=c("reticolo64_metri","112archi224S0","W_righe_uno","Moran_matrice","pendenza_IW",
 "permutazione_conserva_valori","2016coppie","variogramma_conteggi","confini_partizione","join88_24duplicati",
 "IDW_somma_uno","IDW_esatto_siti","IDW_limiti","IDW_coincidenti_media","split40_24","test_perturbato_invariato",
 "CRS_assegnazione_invariante","CRS_ritorno","GeoJSON_64_id_valori","OK_somma_uno","OK_varianze_coerenti",
 "OK_peso_negativo","OK_indipendente_caso_noto","OK_esatto_siti","haversine_1grado_equatore"),
 esito=c(n==64&&all(range(xy)==c(0,1750)),sum(A)==224&&nrow(edges)==112,
 max(abs(rowSums(W)-1))<1e-12,abs(I_A-n/sum(A)*as.numeric(t(v)%*%A%*%v)/sum(v^2))<1e-12,
 abs(unname(coef(scatter_fit)[2])-I_W)<1e-12,identical(sort(v),sort(v[order(u[1:64])])),
 nrow(coppie)==2016,sum(vg$n)==2016,identical(sort(as.integer(table(regioni))),c(32L,32L)),
 sum(member)==88&&sum(rowSums(member)==2)==24,max(abs(colSums(weights)-1))<1e-12,
 max(abs(idw_pred(xy,z,xy)-z))<1e-12,all(grid$previsto>=min(z)&grid$previsto<=max(z)),
 abs(idw_pred(rbind(c(0,0),c(0,0),c(1,0)),c(2,4,100),matrix(c(0,0),nrow=1))-3)<1e-12,
 sum(train_idx)==40&&sum(test_idx)==24,max(abs(p_changed-pred_idw))<1e-12,
 identical(sf::st_coordinates(geo0),sf::st_coordinates(geo_assigned)),roundtrip_max<1e-7,
 nrow(geo_riletto)==64&&setequal(geo_riletto$id,d$id)&&max(abs(geo_riletto$concentrazione[gidx]-z))<1e-10&&geojson_error<1e-7,
 abs(sum(ok$fit$weights)-1)<1e-12,abs(ok$fit$variance_direct-ok$fit$variance_system)<1e-12,
 any(ok$fit$weights<0),max(abs(ok_ind$weights-1/3))<1e-12&&abs(ok_ind$variance-4/3)<1e-12,
 max(abs(ok_curve$varianza[ok_curve$x%in%ok$xy[,1]]))<1e-10,
 abs(haversine(0,0,1,0)-6371000*pi/180)<1e-8))
stopifnot(all(checks$esito));write.csv(checks,"Verifiche/test_numerici.csv",row.names=FALSE)
writeLines(capture.output(sessionInfo()),"Verifiche/SESSIONE_R.txt")
writeLines(capture.output(sf::sf_extSoftVersion()),"Verifiche/VERSIONI_SF.txt")
saveRDS(trend,"Risultati/modello_trend.rds");saveRDS(ok,"Risultati/esempio_kriging.rds")
summary<-list(edizione="2026-11-20",R=as.character(getRversion()),sf=as.character(packageVersion("sf")),sf_librerie=as.list(sf::sf_extSoftVersion()),
 dati=list(n=n,passo_m=250,media=mean(z),sd=sd(z),min=min(z),max=max(z),train_n=40,test_n=24),
 CRS=list(epsg_proiettato=32632,roundtrip_max_gradi=roundtrip_max,geojson_max_gradi=geojson_error,
 UTM_E_min=min(utm_xy[,1]),UTM_E_max=max(utm_xy[,1]),UTM_N_min=min(utm_xy[,2]),UTM_N_max=max(utm_xy[,2]),
 max_diff_sfera_locale_m=max(abs(D_sfera-D)),max_diff_UTM_locale_m=max(abs(D_utm-D))),
 Moran=list(I_A=I_A,I_W=I_W,S0_A=sum(A),S0_W=sum(W),archi=nrow(edges),gradi=as.list(table(nv)),
 scatter_slope=unname(coef(scatter_fit)[2]),scatter_intercept=unname(coef(scatter_fit)[1]),atteso_perm=-1/(n-1),p100=p100,p999=p999,
 I_residui_A=I_res_A,I_residui_W=I_res_W),
 aggregazioni=list(n_ovest=sum(regioni=="Ovest"),n_est=sum(regioni=="Est"),appartenenze=sum(member),duplicati=sum(rowSums(member)==2),
 media_unici=mean(z),media_appartenenze=mean(join_table$z),media_blocchi_sbilanciati=mean(unequal$media)),
 copertura=list(n_strada=sum(road),media_strada=mean(z[road]),media_reticolo=mean(z),scarto_strada=mean(z[road])-mean(z)),
 variogramma=list(coppie=nrow(coppie),n_bin=as.list(setNames(vg$n,as.character(vg$classe)))),
 IDW=list(p_principale=2,target=c(900,900),previsioni_p1_p2_p3=idw_powers$previsione,MAE=metrics$MAE[3],RMSE=metrics$RMSE[3],bias=metrics$bias[3],
 RMSE_media=metrics$RMSE[1],RMSE_NN=metrics$RMSE[2],p_tuning_train=p_inner,n_origini_interne=3),
 kriging=list(lambda=ok$fit$weights,moltiplicatore=ok$fit$mu,previsione=ok$fit$prediction,varianza=ok$fit$variance,pesi_negativi=sum(ok$fit$weights<0),scala_m=800,sigma2=4),
 verifiche=list(n=nrow(checks),tutti_superati=all(checks$esito)))
writeLines(to_json(summary),"Calcoli/summary.json");writeLines(to_json(summary),"Calcoli/riassunto.json")
if(file.exists("R/genera_figure.R"))source("R/genera_figure.R",encoding="UTF-8")
cat("M11: calcoli completati.\n");print(metrics);print(vg);print(summary$Moran);print(summary$kriging)
