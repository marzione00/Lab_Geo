source('R/stile.R')
d<-leggi('ml_v3.csv');out<-'risultati/M16';dir.create(out,recursive=TRUE,showWarnings=FALSE)
f<-c('SiO2','CaO','MgO','FeO','densita');tr<-d$split=='train';te<-!tr;lev<-sort(unique(d$litologia));X<-as.matrix(d[f]);y<-factor(d$litologia,levels=lev)
mu<-colMeans(X[tr,]);s<-apply(X[tr,],2,sd);Ztr<-scale(X[tr,],mu,s);Zte<-scale(X[te,],mu,s)
cpred<-function(A,y,B){C<-t(sapply(lev,function(k)colMeans(A[y==k,,drop=FALSE])));D<-sapply(1:3,function(j)rowSums(sweep(B,2,C[j,],'-')^2));lev[max.col(-D,ties.method='first')]}
pred<-factor(cpred(Ztr,y[tr],Zte),levels=lev);C<-table(osservata=y[te],prevista=pred);acc<-mean(pred==y[te])
verifica('split geografico disgiunto',length(intersect(d$stazione[tr],d$stazione[te]))==0&&sum(tr)==150&&sum(te)==30)
verifica('scaling sul training',max(abs(colMeans(Ztr)))<1e-12&&max(abs(apply(Ztr,2,sd)-1))<1e-12)
verifica('classi effettive',identical(lev,c('Arenaria','Basalto','Calcare')))
verifica('conteggi matrice di confusione',sum(C)==30&&all(rowSums(C)==10))
cols<-setNames(geo[1:3],lev)
salva('M16','F01',ggplot(d,aes(SiO2,densita,colour=litologia,shape=split))+geom_point(size=2,alpha=.8)+scale_colour_manual(values=cols)+scale_shape_manual(values=c(train=16,test=1),labels=c(train='Training',test='Test'))+theme(legend.box='vertical',legend.box.just='left')+guides(colour=guide_legend(order=1,nrow=1),shape=guide_legend(order=2,nrow=1))+scale_y_continuous(labels=fmt)+labs(x='SiO₂ (% in massa)',y='Densità (g/cm³)'))
ms<-data.frame(variabile=rep(f,2),media=c(colMeans(Ztr),colMeans(Zte)),insieme=rep(c('Training','Test'),each=5));ms$variabile[ms$variabile=='densita']<-'Densità'
salva('M16','F02',ggplot(ms,aes(media,variabile,colour=insieme))+geom_vline(xintercept=0,colour=geo[6],linetype=2)+geom_point(size=2.6)+scale_colour_manual(values=geo[1:2])+scale_x_continuous(labels=fmt)+labs(x='Media standardizzata',y=NULL))
# Cinque partizioni per gruppi, identiche per tutti i valori di k.
fold<-as.integer(sub('.*S','',d$stazione[tr]));ks<-c(1,3,7,15);cv<-matrix(NA_real_,5,4);cv_cent<-numeric(5)
for(j in 1:5){a<-fold!=j;b<-!a;xx<-X[tr,];yy<-y[tr];mu0<-colMeans(xx[a,]);s0<-apply(xx[a,],2,sd);A<-scale(xx[a,],mu0,s0);B<-scale(xx[b,],mu0,s0)
 verifica(paste('separazione stazioni fold',j),length(intersect(d$stazione[tr][a],d$stazione[tr][b]))==0)
 cv_cent[j]<-mean(cpred(A,yy[a],B)==yy[b]);for(k in seq_along(ks)){set.seed(1700+100*j+k);cv[j,k]<-mean(class::knn(A,B,yy[a],k=ks[k])==yy[b])}}
cvt<-data.frame(k=ks,accuracy=colMeans(cv));best<-ks[which.max(cvt$accuracy)];set.seed(17);pk<-class::knn(Ztr,Zte,y[tr],k=best)
salva('M16','F03',ggplot(cvt,aes(k,accuracy))+geom_line(colour=geo[1],linewidth=.7)+geom_point(size=2.5,colour=geo[1])+scale_x_continuous(breaks=ks)+scale_y_continuous(limits=c(0,1),breaks=c(0,.5,1),labels=fmt)+labs(x='Numero di vicini k',y='Accuratezza media CV'))
conf<-as.data.frame(C);short<-c(Arenaria='Are.',Basalto='Bas.',Calcare='Calc.')
salva('M16','F04',ggplot(conf,aes(prevista,osservata,fill=Freq))+geom_tile(colour=paper,linewidth=1)+geom_text(aes(label=Freq),colour=ink,size=7)+scale_fill_gradient(low=paper,high='#8AC6BE')+scale_x_discrete(labels=short)+scale_y_discrete(labels=short)+coord_equal()+guides(fill='none')+labs(x='Classe prevista',y='Classe osservata'))
# Vista bidimensionale: classificatore distinto, usato per mostrare la geometria.
A<-Ztr[,c(1,5)];cc<-t(sapply(lev,function(k)colMeans(A[y[tr]==k,,drop=FALSE])));g<-expand.grid(z1=seq(-2.8,2.8,len=100),z2=seq(-2.8,2.8,len=100));g$classe<-cpred(A,y[tr],as.matrix(g));aa<-data.frame(z1=A[,1],z2=A[,2],classe=y[tr]);cen<-data.frame(z1=cc[,1],z2=cc[,2],classe=lev)
salva('M16','F05',ggplot(g,aes(z1,z2))+geom_raster(aes(fill=classe),alpha=.18)+geom_point(data=aa,aes(colour=classe),size=1.1)+geom_point(data=cen,aes(colour=classe),shape=4,size=5,stroke=1.5)+scale_colour_manual(values=cols)+scale_fill_manual(values=cols)+guides(fill='none',colour=guide_legend(nrow=1))+scale_x_continuous(breaks=c(-2,0,2))+scale_y_continuous(breaks=c(-2,0,2))+coord_equal()+labs(x='SiO₂ standardizzata',y='Densità standardizzata'))
# Logistica binaria sulla sola densità.
fit<-glm(yb~dens,data=data.frame(yb=as.integer(y[tr]=='Basalto'),dens=Ztr[,5]),family=binomial());prob<-as.numeric(predict(fit,data.frame(dens=Zte[,5]),type='response'));yb<-as.integer(y[te]=='Basalto');brier<-mean((prob-yb)^2)
verifica('probabilita finite',all(is.finite(prob))&&all(prob>=0&prob<=1))
gg<-data.frame(dens=seq(min(Ztr[,5]),max(Ztr[,5]),len=150));gg$p<-predict(fit,gg,type='response')
salva('M16','F06',ggplot(gg,aes(dens,p))+geom_line(colour=geo[2],linewidth=.8)+geom_point(data=data.frame(dens=Zte[,5],p=yb),colour=geo[1],shape=1,size=2)+scale_y_continuous(breaks=c(0,.5,1),labels=fmt)+labs(x='Densità standardizzata',y='Probabilità di Basalto'))
th<-data.frame(soglia=c(.2,.5,.8));th$n<-sapply(th$soglia,function(t)sum(prob>=t));verifica('positivi annidati',all(diff(th$n)<=0))
salva('M16','F07',ggplot(th,aes(factor(soglia),n))+geom_col(fill=geo[2],width=.6)+scale_x_discrete(labels=c('0,2','0,5','0,8'))+scale_y_continuous(limits=c(0,30),breaks=c(0,10,20,30))+labs(x='Soglia di decisione',y='Positivi previsti'))
grp<-cut(prob,c(-Inf,1/3,2/3,Inf));cal<-aggregate(cbind(prob,yb)~grp,data.frame(prob,yb,grp),mean);cal$n<-as.integer(table(grp)[as.character(cal$grp)])
salva('M16','F08',ggplot(cal,aes(prob,yb))+geom_abline(slope=1,intercept=0,colour=geo[6],linetype=2)+geom_point(colour=geo[1],size=3)+geom_text(aes(label=paste0('n=',n)),nudge_y=.09,size=5)+scale_x_continuous(limits=c(0,1),breaks=c(0,.5,1),labels=fmt)+scale_y_continuous(limits=c(0,1.14),breaks=c(0,.5,1),labels=fmt)+labs(x='Probabilità media prevista',y='Frequenza osservata'))
# Complessità: confronto sul training e nella CV per gruppi.
dep<-c(1,2,3,6);treeacc<-numeric(4);treecv<-numeric(4);train<-data.frame(y=y[tr],X[tr,])
for(i in seq_along(dep)){control<-rpart::rpart.control(cp=0,minsplit=2,minbucket=1,maxdepth=dep[i],xval=0);tt<-rpart::rpart(y~.,train,method='class',control=control);treeacc[i]<-mean(predict(tt,train,type='class')==y[tr]);treecv[i]<-mean(sapply(1:5,function(j){a<-fold!=j;ff<-rpart::rpart(y~.,train[a,],method='class',control=control);mean(predict(ff,train[!a,],type='class')==train$y[!a])}))}
treeplot<-data.frame(profondita=rep(dep,2),accuracy=c(treeacc,treecv),insieme=rep(c('Training','CV per stazioni'),each=4))
salva('M16','F09',ggplot(treeplot,aes(profondita,accuracy,colour=insieme))+geom_line(linewidth=.8)+geom_point(size=2)+scale_colour_manual(values=geo[1:2])+scale_x_continuous(breaks=dep)+scale_y_continuous(limits=c(0,1),breaks=c(0,.5,1),labels=fmt)+labs(x='Profondità massima',y='Accuratezza'))
# Diagnosi illustrativa della sensibilità: 30 permutazioni per variabile.
set.seed(20261109);perm<-sapply(1:5,function(j)replicate(30,{Q<-Zte;Q[,j]<-sample(Q[,j]);acc-mean(cpred(Ztr,y[tr],Q)==y[te])}));pt<-data.frame(variabile=rep(f,each=30),calo=c(perm));pt$variabile[pt$variabile=='densita']<-'Densità'
salva('M16','F10',ggplot(pt,aes(calo,variabile))+geom_vline(xintercept=0,linetype=2,colour=geo[6])+geom_boxplot(fill='#BCE0DA',colour=geo[1],width=.55,outlier.size=1.8)+scale_x_continuous(breaks=c(0,.1,.2),labels=fmt)+labs(x='Calo di accuratezza',y=NULL))
imb<-data.frame(metrica=factor(c('Accuratezza','Media dei\nrichiami'),levels=c('Accuratezza','Media dei\nrichiami')),valore=c(.9,.5));salva('M16','F11',ggplot(imb,aes(metrica,valore,fill=metrica))+geom_col(width=.55)+scale_fill_manual(values=geo[1:2])+guides(fill='none')+scale_y_continuous(limits=c(0,1),breaks=c(0,.5,1),labels=fmt)+labs(x=NULL,y='Valore della metrica'))
set.seed(17);rf<-randomForest::randomForest(x=X[tr,],y=y[tr],ntree=80,mtry=2);prf<-predict(rf,X[te,]);verifica('classi forest nel dominio',all(prf%in%lev))
TP<-sum(pred=='Basalto'&y[te]=='Basalto');FP<-sum(pred=='Basalto'&y[te]!='Basalto');FN<-sum(pred!='Basalto'&y[te]=='Basalto')
verifica('conteggio positivi',TP+FN==10)
write.csv(data.frame(d[te,c('id','stazione','litologia')],predetta=pred,p_basalto=prob),file.path(out,'predizioni.csv'),row.names=FALSE)
write.csv(cvt,file.path(out,'cv_k.csv'),row.names=FALSE);write.csv(conf,file.path(out,'confusione.csv'),row.names=FALSE);write.csv(cal,file.path(out,'calibrazione.csv'),row.names=FALSE);write.csv(pt,file.path(out,'permutazioni.csv'),row.names=FALSE)
jsonlite::write_json(list(centroide_accuracy=acc,baseline=1/3,confusione=unclass(C),cv_centroidi=cv_cent,k_cv=cvt,k_scelto=best,knn_accuracy=mean(pk==y[te]),forest_accuracy=mean(prf==y[te]),brier=brier,logistica_coef=coef(fit),soglie=th,calibrazione=cal,alberi=treeplot,TP=TP,FP=FP,FN=FN),file.path(out,'valori.json'),pretty=TRUE,auto_unbox=TRUE,digits=12)
