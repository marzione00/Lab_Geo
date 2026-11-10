# Le grandezze rappresentate sono prodotte da calcoli.R.
col_geo <- c('#087C74','#5146A5','#A05B10','#9B4564')
paper <- '#F8F6F1'; ink <- '#253344'
fmt <- function(v) format(v,trim=TRUE,scientific=FALSE,decimal.mark=',')
tema <- theme_minimal(base_size=18,base_family='Nimbus Sans')+
 theme(plot.background=element_rect(fill=paper,colour=NA),
 panel.background=element_rect(fill=paper,colour=NA),
 panel.grid.minor=element_blank(),panel.grid.major=element_line(colour='#D6DAD9',linewidth=.25),
 axis.text=element_text(size=22,colour=ink),axis.title=element_text(size=19,colour=ink),
 legend.position='top',legend.text=element_text(size=17),legend.title=element_blank(),
 strip.text=element_text(size=18,face='bold',colour=ink),
 plot.margin=margin(9,13,7,8))
theme_set(tema)
registro <- list()
salva <- function(id,p,descrizione,w=5.2,h=3.8){
 ggsave(paste0('figure/M05/',id,'.pdf'),p,width=w,height=h,device=cairo_pdf,bg=paper)
 ggsave(paste0('figure/M05/',id,'.png'),p,width=w,height=h,dpi=180,bg=paper)
 registro[[id]] <<- list(id=id,sorgente='R/M05/figure.R',descrizione=descrizione,width_in=w,height_in=h)
}
# @@ grafico_stazioni
p <- ggplot(d,aes(stazione,densita,colour=affioramento))+
 geom_point(size=3,position=position_jitter(width=.12,height=0,seed=1))+
 geom_point(data=st,shape=18,size=5)+scale_colour_manual(values=col_geo)+
 scale_y_continuous(labels=fmt,breaks=c(2.5,2.6,2.7))+labs(x='Stazione',y='Densità (g/cm³)')
salva('F01',p,'Provini e medie di stazione')
# @@ fine
p<-ggplot(data.frame(stima=c(V$media_st,V$media_pesata),scenario=c('Uguali','A1 × 4')),aes(scenario,stima))+
 geom_point(size=5,colour=col_geo[1])+scale_y_continuous(labels=fmt,breaks=c(2.60,2.62,2.64))+labs(x='Pesi dei provini',y='Densità media (g/cm³)')
salva('F02',p,'Effetto della ponderazione')
p<-ggplot(bias_scenari,aes(stima,colour=base))+geom_density(linewidth=.9)+facet_wrap(~n,nrow=1)+
 geom_vline(xintercept=0,linetype=2)+scale_colour_manual(values=col_geo,labels=c('Completo','Accessibile'))+
 scale_x_continuous(breaks=c(0,1),labels=fmt)+labs(x='Stima della media',y='Densità')+theme(legend.position='bottom',legend.text=element_text(size=17))
salva('F03',p,'Selezione distorta e aumento della numerosità',w=5.2,h=4)
p<-ggplot(data.frame(t=seq(0,5,length.out=300)),aes(t,dexp(t)))+geom_line(linewidth=1,colour=col_geo[1])+
 scale_x_continuous(breaks=c(0,2,4))+labs(x='Valore individuale',y='Densità')
salva('F04',p,'Distribuzione esponenziale di origine')
campionarie$n <- factor(campionarie$n,levels=c('n = 5','n = 40'))
p<-ggplot(campionarie,aes(media,fill=n))+geom_histogram(binwidth=.07,boundary=0,colour=paper)+
 facet_wrap(~n,ncol=1)+scale_fill_manual(values=col_geo)+geom_vline(xintercept=1,linetype=2)+
 scale_x_continuous(breaks=c(0,1,2),labels=fmt)+labs(x='Media campionaria',y='Repliche')+theme(legend.position='none')
salva('F05',p,'Distribuzioni di 6000 medie per numerosità',h=4.4)
p<-ggplot(lln,aes(n,media,colour=percorso))+geom_line(linewidth=.7)+geom_hline(yintercept=1,linetype=2)+
 scale_colour_manual(values=col_geo)+scale_x_continuous(breaks=c(0,750,1500))+
 scale_y_continuous(breaks=c(.5,1,1.5),labels=fmt)+coord_cartesian(ylim=c(.4,1.6))+
 labs(x='Osservazioni cumulative',y='Media cumulativa')+theme(legend.position='none')
salva('F06',p,'Quattro traiettorie della media; asse y limitato a 0,4–1,6')
standardizzate$n <- factor(standardizzate$n,levels=c('n = 5','n = 40'))
p<-ggplot(standardizzate,aes(z,fill=n))+geom_histogram(aes(y=after_stat(density)),binwidth=.35,colour=paper)+
 stat_function(fun=dnorm,colour=ink,linewidth=.8)+facet_wrap(~n,ncol=1)+scale_fill_manual(values=col_geo)+
 scale_y_continuous(breaks=c(0,.2,.4),labels=fmt)+scale_x_continuous(breaks=c(-2,0,2,4))+labs(x='Media standardizzata',y='Densità')+theme(legend.position='none')
salva('F07',p,'Limite centrale: confronto con la normale standard',h=4.4)
a<-expand.grid(m=1:16,eta=c(0,.3,.6));a$deff<-1+(a$m-1)*a$eta
p<-ggplot(a,aes(m,deff,colour=factor(eta)))+geom_line(linewidth=1)+scale_colour_manual(values=col_geo,labels=c('ICC 0','ICC 0,3','ICC 0,6'))+
 scale_x_continuous(breaks=c(1,8,16))+labs(x='Provini per stazione',y='Effetto del disegno')
salva('F08',p,'Inflazione della varianza nel modello equicorrelato')
a<-data.frame(n=5:200,se=1/sqrt(5:200))
p<-ggplot(a,aes(n,se))+geom_line(colour=col_geo[1],linewidth=1)+scale_x_continuous(breaks=c(25,100,200))+
 scale_y_continuous(labels=fmt,breaks=c(.1,.2,.4))+labs(x='Unità indipendenti',y='SE con σ = 1')
salva('F09',p,'Legge della radice quadrata')
a<-data.frame(tipo=factor(c('± SD','± SE','IC 95%'),levels=c('± SD','± SE','IC 95%')),centro=xb,ampiezza=c(s,se,critico*se))
p<-ggplot(a,aes(tipo,centro,ymin=centro-ampiezza,ymax=centro+ampiezza,colour=tipo))+
 geom_pointrange(linewidth=.8,size=.8)+scale_colour_manual(values=col_geo)+scale_y_continuous(labels=fmt)+
 labs(x=NULL,y='Diametro (µm)')+theme(legend.position='none')
salva('F10',p,'SD, SE e intervallo: stesso centro, significati diversi')
a<-data.frame(t=seq(-4,4,length.out=400));a$d<-dt(a$t,19)
p<-ggplot(a,aes(t,d))+geom_area(data=subset(a,abs(t)<=qt(.975,19)),fill=col_geo[1],alpha=.3)+
 geom_line(linewidth=.9,colour=col_geo[1])+geom_vline(xintercept=c(-1,1)*qt(.975,19),linetype=2)+
 scale_x_continuous(breaks=c(-2,0,2))+labs(x='Perno t, 19 gradi di libertà',y='Densità')
salva('F11',p,'Area centrale 0,95 della distribuzione t')
p<-ggplot(copertura[1:60,],aes(replica,media,ymin=basso,ymax=alto,colour=copre))+
 geom_linerange(linewidth=.6)+geom_point(size=1)+geom_hline(yintercept=5,linetype=2)+
 scale_colour_manual(values=c('FALSE'=col_geo[3],'TRUE'=col_geo[1]),labels=c('Esclude μ','Include μ'))+
 scale_x_continuous(breaks=c(1,30,60))+labs(x='Campione simulato',y='Media e IC 95%')
salva('F12',p,'Primi 60 dei 2000 intervalli normali simulati')
a<-data.frame(tipo=c('Media','Nuovo individuo'),basso=c(ic_t[1],ip_t[1]),alto=c(ic_t[2],ip_t[2]),centro=xb)
p<-ggplot(a,aes(tipo,centro,ymin=basso,ymax=alto,colour=tipo))+geom_pointrange(linewidth=.8)+
 scale_colour_manual(values=col_geo)+scale_y_continuous(labels=fmt)+labs(x=NULL,y='Diametro (µm)')+theme(legend.position='none')
salva('F13',p,'Intervallo di confidenza e intervallo predittivo sotto normalità')
a<-data.frame(E=seq(.1,.5,length.out=100));a$n<-ceiling((qnorm(.975)*.8/a$E)^2)
p<-ggplot(a,aes(E,n))+geom_line(colour=col_geo[1],linewidth=1)+scale_x_continuous(breaks=c(.1,.3,.5),labels=fmt)+
 labs(x='Semiampiezza desiderata (µm)',y='Numerosità orientativa')
salva('F14',p,'Pianificazione con sigma pilota 0,8 µm')
a<-data.frame(id=seq_len(n),molteplicita=frequenze)
p<-ggplot(a,aes(id,molteplicita))+geom_col(fill=col_geo[1],width=.8)+scale_x_continuous(breaks=c(1,40,80))+
 scale_y_continuous(breaks=0:max(frequenze))+labs(x='Indice nel campione',y='Estrazioni nella replica')
salva('F15',p,'Molteplicità di selezione nella singola replica bootstrap')
histboot<-function(v,label,lims=FALSE,assi=waiver()){
 p<-ggplot(data.frame(stima=v),aes(stima))+geom_histogram(bins=32,fill=col_geo[2],colour=paper)+
 scale_x_continuous(labels=fmt,n.breaks=3,breaks=assi)+labs(x=label,y='Repliche')
 if(lims)p<-p+geom_vline(xintercept=q95(v),linetype=2,linewidth=.8)
 p
}
salva('F16',histboot(b_R,'Media Rounded (µm)',assi=c(5.8,6.1,6.4)), 'Bootstrap della media Rounded')
salva('F17',histboot(b_R,'Media Rounded (µm)',TRUE,assi=c(5.8,6.1,6.4)),'Limiti percentili 2,5% e 97,5%')
salva('F18',histboot(b_mediana,'Mediana Rounded (µm)',TRUE),'Bootstrap della mediana Rounded')
p<-ggplot(data.frame(nS=b_pool['quota',]),aes(nS))+geom_histogram(binwidth=2,boundary=0,fill=col_geo[2],colour=paper)+
 geom_vline(xintercept=80,linetype=2)+labs(x='Spiky estratti su 160',y='Repliche')
salva('F19',p,'Quote casuali nel ricampionamento pooled')
a<-data.frame(stima=c(b_pool['media',],b_strat),schema=rep(c('Pooled','Stratificato'),each=B))
p<-ggplot(a,aes(stima,colour=schema))+geom_density(linewidth=1)+scale_colour_manual(values=col_geo)+
 scale_x_continuous(labels=fmt,n.breaks=3)+labs(x='Media della miscela (µm)',y='Densità')
salva('F20',p,'Pooled e stratificato: distribuzioni condizionali')
salva('F21',histboot(b_delta,'Spiky − Rounded (µm)',TRUE),'Contrasto orientato fra morfotipi')
a<-data.frame(stima=c(b_righe,b_stazioni),schema=rep(c('Provini','Stazioni'),each=B))
p<-ggplot(a,aes(stima,colour=schema))+geom_density(linewidth=1)+scale_colour_manual(values=col_geo)+
 scale_x_continuous(labels=fmt,breaks=c(2.55,2.60,2.65))+labs(x='Densità media (g/cm³)',y='Densità di probabilità')
salva('F22',p,'Ricampionamento dei provini e delle medie di stazione')
salva('F23',histboot(b_AB,'Affioramento A − B (g/cm³)',TRUE),'Contrasto stratificato: tre stazioni per affioramento')
p<-ggplot(mc,aes(factor(B),se))+geom_point(position=position_jitter(width=.13,height=0,seed=1),colour=col_geo[1],size=2.3)+
 geom_hline(yintercept=V$boot_R_se_esatto,linetype=2)+scale_y_continuous(labels=fmt,n.breaks=3)+
 labs(x='Repliche per esecuzione',y='SE bootstrap (µm)')
salva('F24',p,'Dodici esecuzioni indipendenti per ciascun B')
a<-data.frame(metodo=factor(c('Righe','Blocchi 8','Modello AR'),levels=c('Righe','Blocchi 8','Modello AR')),se=c(V$ar_se_iid,V$ar_se_blocchi,V$ar_se_teorico))
p<-ggplot(a,aes(metodo,se))+geom_col(fill=col_geo[1],width=.6)+scale_y_continuous(labels=fmt,n.breaks=3)+
 scale_x_discrete(labels=c('Blocchi 8'='Blocchi\n(8)','Modello AR'='Modello\nAR','Righe'='Righe'))+labs(x=NULL,y='Errore standard')
salva('F25',p,'Serie AR(1): bootstrap IID, blocchi e SE teorico')
a<-data.frame(metodo=c('t','Percentile'),centro=xb,basso=c(ic_t[1],V$boot_R_lo),alto=c(ic_t[2],V$boot_R_hi))
p<-ggplot(a,aes(metodo,centro,ymin=basso,ymax=alto))+geom_pointrange(colour=col_geo[1],linewidth=.8)+
 scale_y_continuous(labels=fmt,n.breaks=3)+labs(x='Metodo per Rounded',y='Media e IC (µm)')
salva('F26',p,'Confronto t e percentile sullo stesso estimando')
a<-data.frame(p=seq(0,1,length.out=200));a$se<-sqrt(a$p*(1-a$p)/40)
p<-ggplot(a,aes(p,se))+geom_line(colour=col_geo[1],linewidth=1)+scale_x_continuous(breaks=c(0,.5,1),labels=fmt)+
 scale_y_continuous(labels=fmt,n.breaks=3)+labs(x='Proporzione p',y='SE con n = 40')
salva('F27',p,'Errore standard teorico della proporzione')
a<-data.frame(n=5:200);a$Varianza<-1/a$n;a$MSE<-1+1/a$n
long<-data.frame(n=rep(a$n,2),valore=c(a$Varianza,a$MSE),quantita=rep(c('Varianza','MSE, bias = 1'),each=nrow(a)))
p<-ggplot(long,aes(n,valore,colour=quantita))+geom_line(linewidth=1)+scale_colour_manual(values=col_geo)+
 scale_x_continuous(breaks=c(5,100,200))+scale_y_continuous(labels=fmt,breaks=c(0,.5,1))+
 labs(x='Numerosità',y='Errore quadratico')
salva('F28',p,'Decomposizione MSE = varianza + bias al quadrato')
write_json(registro,'figure/M05/REGISTRO.json',pretty=TRUE,auto_unbox=TRUE)
