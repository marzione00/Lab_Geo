source('R/stile.R');d<-leggi('ml_v3.csv');out<-'risultati/P11';dir.create(out,recursive=TRUE,showWarnings=FALSE)
vars<-c('SiO2','CaO','MgO','FeO','densita');classes<-sort(unique(d$litologia));tr<-d$split=='train';te<-!tr
verifica('separazione per stazioni',nrow(d)==180&&sum(tr)==150&&sum(te)==30&&length(unique(d$stazione))==18&&length(intersect(d$stazione[tr],d$stazione[te]))==0)
verifica('caratteristiche numeriche finite',all(vapply(d[vars],is.numeric,TRUE))&&all(is.finite(as.matrix(d[vars])))&&!anyDuplicated(d$id))
mu<-colMeans(d[tr,vars]);ss<-vapply(d[tr,vars],sd,0.0);Z<-scale(as.matrix(d[vars]),center=mu,scale=ss)
C<-t(vapply(classes,function(k)colMeans(Z[tr&d$litologia==k,,drop=FALSE]),numeric(length(vars))));rownames(C)<-classes
D2<-sapply(classes,function(k)rowSums(sweep(Z[te,,drop=FALSE],2,C[k,],'-')^2));pr<-classes[max.col(-D2,ties.method='first')];actual<-d$litologia[te]
base<-classes[which.max(table(factor(d$litologia[tr],levels=classes)))];acc<-mean(pr==actual);acc0<-mean(actual==base);conf<-table(osservata=factor(actual,levels=classes),prevista=factor(pr,levels=classes))
verifica('centratura e scala solo train',max(abs(colMeans(Z[tr,])))<1e-12&&max(abs(apply(Z[tr,],2,sd)-1))<1e-12)
verifica('regola di riferimento determinata dal train',base=='Arenaria'&&abs(acc0-1/3)<1e-12)
verifica('classificazione e conteggi',sum(conf)==30&&acc==1&&all(diag(conf)==10))
count<-as.data.frame(table(classe=factor(d$litologia,levels=classes),insieme=factor(ifelse(tr,'Train','Test'),levels=c('Train','Test'))));names(count)[3]<-'n'
salva('P11','F01',ggplot(count,aes(classe,n,fill=insieme))+geom_col(position=position_dodge(width=.75),width=.65)+scale_fill_manual(values=geo[1:2])+scale_y_continuous(breaks=c(0,25,50))+scale_x_discrete(labels=c('Are.','Bas.','Cal.'))+labs(x='Litologia sintetica',y='Campioni'))
proj<-data.frame(Z[,c('SiO2','CaO')],classe=d$litologia,insieme=ifelse(tr,'Train','Test'));cent<-data.frame(C[,c('SiO2','CaO')],classe=classes)
salva('P11','F02',ggplot(proj,aes(SiO2,CaO,colour=classe))+geom_point(data=proj[tr,],alpha=.45,size=1.5)+geom_point(data=proj[te,],shape=17,size=2.6)+geom_point(data=cent,shape=4,stroke=1.3,size=4)+scale_colour_manual(values=geo[1:3])+guides(colour=guide_legend(nrow=2))+labs(x='SiO₂ standardizzata',y='CaO standardizzata'))
long<-data.frame(classe=rep(classes,each=length(vars)),variabile=rep(vars,length(classes)),valore=as.vector(t(C)));long$variabile<-factor(long$variabile,levels=vars)
salva('P11','F03',ggplot(long,aes(variabile,classe,fill=valore))+geom_tile(colour=paper,linewidth=.6)+scale_fill_gradient2(low=geo[2],mid=paper,high=geo[1],midpoint=0,breaks=c(-1,0,1))+scale_x_discrete(labels=c('Si','Ca','Mg','Fe','ρ'))+labs(x='Caratteristica',y='Centroide'))
cf<-as.data.frame(conf);names(cf)[3]<-'n'
salva('P11','F04',ggplot(cf,aes(prevista,osservata,fill=n))+geom_tile(colour=paper,linewidth=1)+geom_text(aes(label=n),size=7,colour=ink)+scale_fill_gradient(low=paper,high='#9ED1C7',guide='none')+coord_equal()+scale_x_discrete(labels=c('Are.','Bas.','Cal.'))+labs(x='Classe prevista',y='Classe osservata'))
metrics<-data.frame(metodo=c('Riferimento','Centroide'),accuracy=c(acc0,acc))
salva('P11','F05',ggplot(metrics,aes(metodo,accuracy,fill=metodo))+geom_col(width=.6)+scale_fill_manual(values=c(Centroide=geo[1],Riferimento=geo[2]),guide='none')+scale_y_continuous(breaks=c(0,.5,1),labels=fmt,limits=c(0,1.08))+labs(x='Procedura prefissata',y='Accuratezza sul test'))
sortd<-t(apply(D2,1,sort));margin<-sortd[,2]-sortd[,1];marg<-data.frame(id=d$id[te],classe=actual,margine=margin)
salva('P11','F06',ggplot(marg,aes(classe,margine))+geom_boxplot(fill=geo[1],alpha=.55,width=.5,outlier.shape=NA)+geom_point(position=position_jitter(width=.08,height=0,seed=17),colour=geo[2],size=2)+scale_x_discrete(labels=c('Are.','Bas.','Cal.'))+labs(x='Classe osservata',y='Margine quadratico'))
verifica('margini e denominatore',all(margin>0)&&length(margin)==30)
model<-list(variabili=vars,centro=mu,scala=ss,centroidi=C,classi=classes,pareggio='prima classe in ordine alfabetico',versione='P11_R5')
saveRDS(model,file.path(out,'centroidi_modello.rds'));back<-readRDS(file.path(out,'centroidi_modello.rds'));verifica('rilettura del modello',identical(back,model))
write.csv(data.frame(id=d$id[te],stazione=d$stazione[te],osservata=actual,prevista=pr,margine=margin),file.path(out,'previsioni.csv'),row.names=FALSE);write.csv(data.frame(variabile=vars,media_train=mu,sd_train=ss),file.path(out,'standardizzazione.csv'),row.names=FALSE);write.csv(C,file.path(out,'centroidi.csv'));write.csv(cf,file.path(out,'confusione.csv'),row.names=FALSE)
card<-list(id='P11_R5',bersaglio='litologia sintetica',variabili=vars,unita=c('SiO2, CaO, MgO, FeO: percentuali in massa didattiche','densita: g/cm3'),origine='ml_v3.csv sintetico del corso',train=list(campioni=150,stazioni=15),test=list(campioni=30,stazioni=3),regola='centroide euclideo nello spazio standardizzato sul train',accuratezza=acc,riferimento=acc0,limiti=c('campione test gia utilizzato nel percorso didattico','stesso generatore sintetico','nessuna validazione su rocce reali','classi assenti non riconosciute','margini non calibrati come probabilita'))
jsonlite::write_json(card,file.path(out,'scheda_modello.json'),auto_unbox=TRUE,pretty=TRUE,digits=12);jsonlite::write_json(list(accuracy=acc,baseline=acc0,classe_baseline=base,confusione=cf,margine_range=range(margin),train_stazioni=sort(unique(d$stazione[tr])),test_stazioni=sort(unique(d$stazione[te]))),file.path(out,'valori.json'),auto_unbox=TRUE,pretty=TRUE,digits=12)
