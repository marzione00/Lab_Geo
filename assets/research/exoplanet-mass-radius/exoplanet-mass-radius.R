# GeoStat Lab · Massa e raggio: un modello da mettere alla prova
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
  # Errore relativo massimo ammesso
  max_relative_error = 0.5,
  # Raggio massimo [R⊕]
  max_radius = 4,
  # Quota dei sistemi per la stima
  train_fraction = 0.7,
  # Seme riproducibile: Determina quali sistemi stellari entrano nell’insieme di stima; cambia il seme per valutare la sensibilità alla partizione.
  seed = 2026
)
# Rende ripetibile la sequenza pseudocasuale.
set.seed(p$seed)

# Legge la copia locale documentata, senza interrogare servizi esterni.
observations <- read.csv("data.csv", stringsAsFactors=FALSE, check.names=FALSE)

# Richiede entrambi gli errori asimmetrici: i mancanti non vengono sostituiti con zero.
mass_err <- pmax(abs(observations$pl_bmasseerr1), abs(observations$pl_bmasseerr2)) / observations$pl_bmasse
radius_err <- pmax(abs(observations$pl_radeerr1), abs(observations$pl_radeerr2)) / observations$pl_rade
keep <- is.finite(mass_err) & is.finite(radius_err) &
  mass_err > 0 & radius_err > 0 &
  mass_err <= p$max_relative_error & radius_err <= p$max_relative_error &
  observations$pl_rade >= 0.5 & observations$pl_rade <= p$max_radius
keep[is.na(keep)] <- FALSE
data <- observations[keep, , drop = FALSE]
stopifnot(nrow(data) >= 20)

# Divide per stella: tutti i pianeti dello stesso sistema rimangono nello stesso insieme.
# L’ordine dei nomi è fissato byte per byte, indipendentemente dalla lingua del sistema.
hosts <- sort(unique(data$hostname), method="radix")
stopifnot(length(hosts) >= 10)
train_hosts <- sample(hosts, size = floor(length(hosts) * p$train_fraction))
data$insieme <- ifelse(data$hostname %in% train_hosts, "Stima", "Verifica")
data$log_radius <- log10(data$pl_rade)
data$log_mass <- log10(data$pl_bmasse)
train <- data[data$insieme == "Stima", , drop = FALSE]
test <- data[data$insieme == "Verifica", , drop = FALSE]

# Stima il modello soltanto sui sistemi assegnati all’insieme di addestramento.
fit <- lm(log_mass ~ log_radius, data = train)
data$predicted_log_mass <- as.numeric(predict(fit, newdata = data))
data$residuo_log <- data$log_mass - data$predicted_log_mass
test_prediction <- as.numeric(predict(fit, newdata = test))
rmse <- sqrt(mean((test$log_mass - test_prediction)^2))
baseline_rmse <- sqrt(mean((test$log_mass - mean(train$log_mass))^2))
metrics <- metric(
  "Pianeti dopo i filtri" = nrow(data),
  "Sistemi di stima" = length(train_hosts),
  "Sistemi di verifica" = length(hosts) - length(train_hosts),
  "Pendenza beta" = f(unname(coef(fit)[2])),
  "RMSE verifica [dex]" = f(rmse),
  "RMSE previsione costante [dex]" = f(baseline_rmse)
)

# Disegna il modello di stima sull’intervallo osservato; i punti di verifica restano distinguibili.
grid <- data.frame(log_radius = seq(min(data$log_radius), max(data$log_radius), length.out = 100))
grid$log_mass <- as.numeric(predict(fit, newdata = grid))
g1 <- ggplot(data, aes(x = log_radius, y = log_mass, colour = insieme)) +
  geom_point(size = 2.3, alpha = 0.65) +
  geom_line(data = grid, aes(x = log_radius, y = log_mass), inherit.aes = FALSE,
            colour = "#172F42", linewidth = 1) +
  scale_colour_manual(values = c("Stima" = col_geo[1], "Verifica" = col_geo[2])) +
  labs(title = "Relazione massa–raggio: modello di riferimento",
       subtitle = "NASA Exoplanet Archive · partizione per sistema stellare",
       x = "log10 del raggio [R/R⊕]", y = "log10 della massa [M/M⊕]")

# La struttura dei residui suggerisce quali aspetti il modello lineare non descrive.
g2 <- ggplot(data, aes(x = predicted_log_mass, y = residuo_log, colour = insieme)) +
  geom_hline(yintercept = 0, colour = "#64748B", linetype = 2) +
  geom_point(size = 2.3, alpha = 0.65) +
  scale_colour_manual(values = c("Stima" = col_geo[1], "Verifica" = col_geo[2])) +
  labs(title = "Residui e valori previsti", subtitle = "Un residuo è osservato meno previsto, in scala logaritmica",
       x = "log10 della massa prevista [M/M⊕]", y = "Residuo [dex]")
plots <- list(g1, g2)

print(metrics, row.names=FALSE)
for (i in seq_along(plots)) {
  print(plots[[i]])
  ggsave(paste0("figura_",i,".pdf"),plots[[i]],width=9,height=5.5)
}
write.csv(data,"risultati.csv",row.names=FALSE)
