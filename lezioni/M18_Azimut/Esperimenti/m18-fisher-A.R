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
p <- list(N = 8, k = 30, seed = 17)
set.seed(p$seed)
vett <- function(az, inc) cbind(cos(inc * pi/180) * cos(az * pi/180), cos(inc * pi/180) * sin(az * pi/180), 
    sin(inc * pi/180))

m0 <- vett(0, 60)[1, ]

e1 <- c(0, 0, 1) - m0[3] * m0

e1 <- e1/sqrt(sum(e1^2))

e2 <- c(m0[2] * e1[3] - m0[3] * e1[2], m0[3] * e1[1] - m0[1] * e1[3], m0[1] * e1[2] - m0[2] * e1[1])

ct <- 1 + log(1 - runif(p$N) * (1 - exp(-2 * p$k)))/p$k

ph <- runif(p$N, 0, 2 * pi)

X <- outer(ct, m0) + outer(sqrt(1 - ct^2) * cos(ph), e1) + outer(sqrt(1 - ct^2) * sin(ph), e2)

s <- colSums(X)

R <- sqrt(sum(s^2))

N <- p$N

k <- (N - 1)/(N - R)

a95 <- acos(1 - (N - R)/R * (20^(1/(N - 1)) - 1))

m <- s/R

b1 <- c(0, 0, 1) - m[3] * m

b1 <- b1/sqrt(sum(b1^2))

b2 <- c(m[2] * b1[3] - m[3] * b1[2], m[3] * b1[1] - m[1] * b1[3], m[1] * b1[2] - m[2] * b1[1])

tt <- seq(0, 2 * pi, length.out = 120)

cono <- outer(rep(cos(a95), 120), m) + sin(a95) * (outer(cos(tt), b1) + outer(sin(tt), b2))

proietta <- function(V) {
    V <- V * sign(V[, 3])
    r <- sqrt(2) * sin((pi/2 - asin(pmin(1, V[, 3])))/2)
    data.frame(x = r * sin(atan2(V[, 2], V[, 1])), y = r * cos(atan2(V[, 2], V[, 1])))
}

data <- proietta(X)

plots <- list(ggplot(data, aes(x, y)) + geom_path(data = data.frame(x = sin(seq(0, 2 * pi, length.out = 200)), 
    y = cos(seq(0, 2 * pi, length.out = 200))), colour = "#273E4A") + geom_point(colour = col_geo[1], 
    size = 2.4) + geom_path(data = proietta(cono), colour = col_geo[2], linewidth = 1) + geom_point(data = proietta(rbind(m0)), 
    colour = col_geo[3], shape = 8, size = 4, stroke = 1.2) + annotate("text", x = 0, y = 1.08, label = "N") + 
    coord_equal() + labs(title = "Direzioni simulate e cono alfa95", subtitle = "Emisfero inferiore; asterisco: direzione vera", 
    x = NULL, y = NULL) + theme(axis.text = element_blank(), panel.grid.major = element_blank()))

metrics <- metric(`alfa95 (gradi)` = f(a95 * 180/pi), `Approssimazione 140/radice(kN) (gradi)` = f(140/sqrt(k * 
    N)), `k stimato` = f(k), `Distanza dalla direzione vera (gradi)` = f(acos(min(1, sum(m * m0))) * 
    180/pi))
print(metrics,row.names=FALSE)
ggplot2::ggsave('m18-fisher-A.svg',plots[[1]],device=svglite::svglite,width=7.7,height=5.0,bg='#F8F6F1')
