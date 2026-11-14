# GeoStat Lab · Quando il sensore raggiunge il limite
# Dati osservati: consultare provenance.json.
# Estrarre il pacchetto; impostare questa cartella come directory di lavoro.
# install.packages("ggplot2")

# GeoStat Lab — funzioni comuni. R >= 4.3; ggplot2 >= 3.4; jsonlite.
suppressPackageStartupMessages(library(ggplot2))
col_geo <- c('#168B9C','#BC5B35','#7054A4','#A17B19','#227864','#64748B')
theme_set(theme_minimal(base_size=17, base_family='sans') + theme(
  plot.background=element_rect(fill='#F5F6F3',colour=NA),
  panel.background=element_rect(fill='#F5F6F3',colour=NA),
  panel.grid.minor=element_blank(),panel.grid.major=element_line(colour='#DCE3E2'),
  plot.title=element_text(size=19,face='bold',colour='#122D3B'),
  plot.subtitle=element_text(size=13,colour='#405560',margin=margin(b=12)),
  axis.text=element_text(size=15,colour='#273E4A'),axis.title=element_text(size=16),
  legend.position='bottom',legend.title=element_blank(),legend.text=element_text(size=14),
  strip.text=element_text(size=15,face='bold'),plot.margin=margin(18,24,18,18)))
metric <- function(...) data.frame(grandezza=names(c(...)),valore=as.character(c(...)),check.names=FALSE)
f <- function(x,d=3) {out<-formatC(x,digits=d,format='fg');out[!is.finite(x)]<-'Non definito';out}
line_plot <- function(d,x='x',y='y',title='',xl=x,yl=y,group=NULL) {
 p<-ggplot(d,aes(x=.data[[x]],y=.data[[y]]))
 if(is.null(group)) p<-p+geom_line(colour=col_geo[1],linewidth=1.05) else p<-p+aes(colour=.data[[group]],group=.data[[group]])+geom_line(linewidth=1)+scale_colour_manual(values=col_geo)
 p+labs(title=title,x=xl,y=yl)
}
point_plot <- function(d,x='x',y='y',title='',xl=x,yl=y,group=NULL) {
 p<-ggplot(d,aes(x=.data[[x]],y=.data[[y]]))
 if(is.null(group))p<-p+geom_point(colour=col_geo[1],size=2.5,alpha=.8) else p<-p+aes(colour=.data[[group]])+geom_point(size=2.7,alpha=.85)+scale_colour_manual(values=col_geo)
 p+labs(title=title,x=xl,y=yl)
}
hist_plot<-function(x,title='',xl='Valore',bins=20)ggplot(data.frame(x=x),aes(x))+geom_histogram(bins=bins,fill=col_geo[1],colour='#F5F6F3')+labs(title=title,x=xl,y='Frequenza')
bar_plot<-function(d,x='gruppo',y='valore',title='',yl='Valore')ggplot(d,aes(x=.data[[x]],y=.data[[y]],fill=.data[[x]]))+geom_col(width=.65)+scale_fill_manual(values=rep(col_geo,length.out=length(unique(d[[x]])) ))+guides(fill='none')+labs(title=title,x=NULL,y=yl)
map_plot<-function(d,z='z',title='',xl='Est [km]',yl='Nord [km]')ggplot(d,aes(x,y,fill=.data[[z]]))+geom_raster()+coord_equal()+scale_fill_gradientn(colours=c('#153F56','#298C9C','#B8CDB2','#F1D889','#AD542F'))+labs(title=title,x=xl,y=yl)
acf_data<-function(x,lag=20){a<-acf(x,lag.max=min(lag,length(x)-1),plot=FALSE);data.frame(x=as.vector(a$lag)[-1],y=as.vector(a$acf)[-1])}
# AR(1), distribuzione marginale stazionaria N(0, 1).
ar_series<-function(n,rho){x<-numeric(n);x[1]<-rnorm(1);for(i in 2:n)x[i]<-rho*x[i-1]+sqrt(1-rho^2)*rnorm(1);x}
# Distanze euclidee in unità metriche già dichiarate; nessuna conversione implicita di CRS.
dist_cross<-function(a,b)sqrt(outer(a[,1],b[,1],'-')^2+outer(a[,2],b[,2],'-')^2)
# Predittore IDW: i punti coincidenti ricevono esattamente il valore osservato.
idw<-function(xy,z,new,power=2){dd<-dist_cross(new,xy);apply(dd,1,function(d)if(any(d<1e-10))mean(z[d<1e-10])else weighted.mean(z,d^(-power)))}
# CART didattico binario: divisioni assiali che minimizzano l'impurità di Gini.
cart_fit<-function(x,y,depth=2,minleaf=4){
 node<-list(p=mean(y),n=length(y));if(depth<1||length(unique(y))<2||length(y)<2*minleaf)return(node)
 best<-Inf
 for(j in seq_len(ncol(x))){v<-sort(unique(x[,j])); if(length(v)<2)next
  for(cut in (head(v,-1)+tail(v,-1))/2){left<-x[,j]<=cut;nl<-sum(left);nr<-sum(!left);if(min(nl,nr)<minleaf)next
   score<-nl*mean(y[left])*(1-mean(y[left]))+nr*mean(y[!left])*(1-mean(y[!left]))
   if(score<best){best<-score;node$j<-j;node$cut<-cut;split<-left}
  }
 }
 if(is.finite(best)){node$left<-cart_fit(x[split,,drop=FALSE],y[split],depth-1,minleaf);node$right<-cart_fit(x[!split,,drop=FALSE],y[!split],depth-1,minleaf)};node
}
cart_predict<-function(tree,x)apply(x,1,function(row){t<-tree;while(!is.null(t$j))t<-if(row[t$j]<=t$cut)t$left else t$right;t$p})

p <- list(
  # Soglia minima di irradiamento
  minimum_class = "C",
  # Eventi nelle sequenze
  sequence = "all",
  # Seme riproducibile: Riservato a eventuali estensioni campionarie; il calcolo corrente è deterministico.
  seed = 2026
)
# Rende ripetibile la sequenza pseudocasuale.
set.seed(p$seed)

# Legge la copia locale documentata, senza interrogare servizi esterni.
observations <- read.csv("data.csv", stringsAsFactors=FALSE, check.names=FALSE)

# I tempi sono UTC; la durata termina secondo la definizione operativa dell'archivio GOES.
data <- observations
start <- as.POSIXct(data$start_time, format = '%Y-%m-%d %H:%M:%S', tz = 'UTC')
end <- as.POSIXct(data$end_time, format = '%Y-%m-%d %H:%M:%S', tz = 'UTC')
data$duration_minutes <- as.numeric(difftime(end, start, units = 'mins'))
valid <- is.finite(data$duration_minutes) & data$duration_minutes > 0 &
  is.finite(data$xrsb_irrad) & data$xrsb_irrad > 0
missing_duration <- sum(!valid)

# La soglia di irradiamento seleziona un sottocampione; non corregge la completezza del catalogo.
threshold <- switch(p$minimum_class, B = 1e-7, C = 1e-6, M = 1e-5)
selection <- valid & data$xrsb_irrad >= threshold
if (p$sequence == 'first') selection <- selection & data$sequential_flare_num == 1
selected <- data[selection, ]

# I picchi saturati rimangono visibili nel conteggio ma sono sempre esclusi dalla regressione.
saturated <- selected[selected$peak_saturated == 1, ]
data <- selected[!is.na(selected$peak_saturated) & selected$peak_saturated == 0, ]
stopifnot(nrow(data) >= 10)
data$log_duration <- log10(data$duration_minutes)
data$log_irradiance <- log10(data$xrsb_irrad)

# La retta riassume l'associazione logaritmica; le osservazioni non identificano un rapporto causale.
fit <- lm(log_irradiance ~ log_duration, data = data)
data$fitted_log_irradiance <- as.numeric(predict(fit))
data$residual_log_irradiance <- resid(fit)
rho <- cor(data$duration_minutes, data$xrsb_irrad, method = 'spearman')
metrics <- metric('Eventi nel file originale' = nrow(observations),
  'Durata o intensità non utilizzabile' = missing_duration,
  'Eventi selezionati prima del controllo saturazione' = nrow(selected),
  'Picchi saturati esclusi dal modello' = nrow(saturated),
  'Eventi nel modello' = nrow(data),
  'Pendenza in scala log10' = f(unname(coef(fit)[2])),
  'Correlazione di Spearman' = f(rho))

# Assi logaritmici mantengono visibili eventi che differiscono per diversi ordini di grandezza.
g1 <- ggplot(data, aes(duration_minutes, xrsb_irrad)) +
  geom_point(colour = '#BC5B35', alpha = 0.5, size = 1.9) +
  geom_smooth(method = 'lm', formula = y ~ x, se = FALSE, colour = '#168B9C', linewidth = 1.1) +
  scale_x_log10() + scale_y_log10() +
  labs(title = 'Brillamenti solari · GOES 2003',
    subtitle = 'Soli picchi non saturati · regressione descrittiva in scala logaritmica',
    x = 'Durata [minuti; scala log10]', y = 'Irradiamento di picco [W/m2; scala log10]')

# Il grafico dei residui aiuta a riconoscere dispersione variabile e forme non lineari.
g2 <- ggplot(data, aes(fitted_log_irradiance, residual_log_irradiance)) +
  geom_hline(yintercept = 0, colour = '#64748B', linetype = 2) +
  geom_point(colour = '#7054A4', alpha = 0.5, size = 1.9) +
  labs(title = 'Diagnostica della relazione durata–irradiamento',
    subtitle = 'Confrontare soglie e primi eventi di sequenza prima di interpretare la pendenza',
    x = 'Valore stimato [log10 W/m2]', y = 'Residuo [log10 W/m2]')
plots <- list(g1, g2)


print(metrics, row.names=FALSE)
for (i in seq_along(plots)) {
  print(plots[[i]])
  ggsave(paste0("figura_",i,".pdf"),plots[[i]],width=9,height=5.5)
}
write.csv(data,"risultati.csv",row.names=FALSE)
