# Tabelle numeriche per la preparazione delle figure Iride.
source("setup.R", encoding = "UTF-8")
dir.create("Calcoli", showWarnings = FALSE)
salva_calcolo <- function(x, file) {
  write.csv(x, file.path("Calcoli", file), row.names = FALSE)
}
g <- split(fossili$diametro_tot_um, fossili$morfotipo)
g$Totale <- fossili$diametro_tot_um
sintesi <- do.call(rbind, lapply(names(g), function(nome) {
  x <- g[[nome]]
  data.frame(gruppo = nome, n = length(x), media = mean(x), mediana = median(x),
             varianza = var(x), sd = sd(x), IQR = IQR(x), minimo = min(x), massimo = max(x))
}))
salva_calcolo(sintesi, "fossili_sintesi.csv")
quantili <- do.call(rbind, lapply(names(g), function(nome) {
  p <- c(0,.25,.5,.75,1)
  data.frame(gruppo = nome, p = p,
             quantile7 = unname(quantile(g[[nome]],p,type=7)))
}))
salva_calcolo(quantili, "fossili_quantili.csv")
box <- do.call(rbind, lapply(names(g), function(nome) {
  b <- boxplot.stats(g[[nome]], coef=1.5)
  data.frame(gruppo=nome, statistica=c("baffo_inf","hinge_inf","mediana","hinge_sup","baffo_sup"),
             valore=b$stats, n=b$n)
}))
salva_calcolo(box, "fossili_boxplot.csv")
out <- do.call(rbind,lapply(names(g),function(nome) {
  b <- boxplot.stats(g[[nome]],coef=1.5)$out
  if(length(b)) data.frame(gruppo=nome,valore=b) else NULL
}))
if(is.null(out)) out <- data.frame(gruppo=character(),valore=numeric())
salva_calcolo(out, "fossili_boxplot_fuori_baffi.csv")
ec <- do.call(rbind,lapply(names(g),function(nome) {
  x <- sort(unique(g[[nome]]))
  data.frame(gruppo=nome,x=x,F=ecdf(g[[nome]])(x))
}))
salva_calcolo(ec, "fossili_ecdf.csv")
for (passo in c(.5,1)) {
  lim <- range(fossili$diametro_tot_um)
  estremi <- seq(floor(lim[1]),ceiling(lim[2])+passo,by=passo)
  ht <- do.call(rbind,lapply(names(g),function(nome) {
    h <- hist(g[[nome]],breaks=estremi,plot=FALSE,right=TRUE,include.lowest=TRUE)
    data.frame(gruppo=nome,limite_inf=head(h$breaks,-1),limite_sup=tail(h$breaks,-1),
               centro=h$mids,n=h$counts,densita=h$density)
  }))
  salva_calcolo(ht,paste0("fossili_hist_",if(passo==.5)"0_5" else "1",".csv"))
}
print(sintesi)
print(quantili)
print(box)
