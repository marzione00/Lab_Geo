# GeoStat Lab · La memoria del ghiaccio
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
  # Mese confrontato fra anni
  month = "9",
  # Anno iniziale (termine fisso: 2024)
  start_year = 1979,
  # Seme riproducibile: Riservato a eventuali estensioni campionarie; il calcolo corrente è deterministico.
  seed = 2026
)
# Rende ripetibile la sequenza pseudocasuale.
set.seed(p$seed)

# Legge la copia locale documentata, senza interrogare servizi esterni.
observations <- read.csv("data.csv", stringsAsFactors=FALSE, check.names=FALSE)

# Confronta lo stesso mese tra anni: marzo e settembre non vengono mescolati.
data <- observations[observations$month == as.integer(p$month) &
  observations$year >= p$start_year & is.finite(observations$extent_million_km2), ]
data <- data[order(data$year), ]
stopifnot(nrow(data) >= 20)

# La pendenza beta esprime milioni di km2 per anno; moltiplicarla per 10 dà il tasso decennale.
fit <- lm(extent_million_km2 ~ year, data = data)
data$fitted_million_km2 <- as.numeric(predict(fit))
data$residual_million_km2 <- resid(fit)
beta <- unname(coef(fit)['year'])

# Il riferimento 1981-2010 usa sempre il medesimo mese, anche quando cambia l'inizio del periodo.
reference <- observations[observations$month == as.integer(p$month) &
  observations$year >= 1981 & observations$year <= 2010, ]
baseline <- mean(reference$extent_million_km2, na.rm = TRUE)
percent_decade <- 100 * 10 * beta / baseline

# La correlazione al ritardo 1 segnala dipendenza residua; non costituisce una prova di indipendenza.
lag1 <- as.numeric(acf(data$residual_million_km2, lag.max = 1, plot = FALSE)$acf[2])
metrics <- metric('Anni osservati' = nrow(data),
  'Pendenza [milioni km2 / decennio]' = f(10 * beta),
  'Pendenza [% del riferimento / decennio]' = f(percent_decade),
  'Riferimento 1981-2010 [milioni km2]' = f(baseline),
  'Correlazione residua al ritardo 1' = f(lag1))
month_name <- if (p$month == '3') 'Marzo' else 'Settembre'

# Mostra osservazioni e retta stimata, limitando la rappresentazione all'intervallo studiato.
g1 <- ggplot(data, aes(year, extent_million_km2)) +
  geom_line(colour = '#A0ADB7', linewidth = 0.55) +
  geom_point(colour = '#168B9C', size = 2.6) +
  geom_line(aes(y = fitted_million_km2), colour = '#BC5B35', linewidth = 1.15) +
  labs(title = paste('Estensione artica ·', month_name),
    subtitle = 'NSIDC Sea Ice Index v4 · osservazioni e tendenza lineare',
    x = 'Anno', y = 'Estensione [milioni di km2]')

# I residui conservano l'ordine temporale, così eventuali sequenze rimangono visibili.
g2 <- ggplot(data, aes(year, residual_million_km2)) +
  geom_hline(yintercept = 0, colour = '#64748B', linetype = 2) +
  geom_line(colour = '#7054A4', linewidth = 0.75) +
  geom_point(colour = '#7054A4', size = 2.3) +
  labs(title = 'Scarti dalla tendenza lineare',
    subtitle = 'Diagnostica descrittiva: verificare struttura temporale e sensibilità al periodo',
    x = 'Anno', y = 'Residuo [milioni di km2]')
plots <- list(g1, g2)


print(metrics, row.names=FALSE)
for (i in seq_along(plots)) {
  print(plots[[i]])
  ggsave(paste0("figura_",i,".pdf"),plots[[i]],width=9,height=5.5)
}
write.csv(data,"risultati.csv",row.names=FALSE)
