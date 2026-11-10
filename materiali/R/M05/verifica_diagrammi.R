# Controlli degli esempi numerici e degli indici usati nei diagrammi TikZ.
# Eseguire dalla radice del progetto; non richiede pacchetti esterni.
esiti_tikz <- data.frame(controllo=character(),esito=logical())
check_tikz <- function(nome,ok) {
  esiti_tikz[nrow(esiti_tikz)+1,] <<- list(nome,isTRUE(ok))
  if(!isTRUE(ok)) stop(nome)
}
eq <- function(a,b) isTRUE(all.equal(as.numeric(a),as.numeric(b),tolerance=1e-12))
check_tikz('D02: sei stazioni con quattro provini',6*4==24)
check_tikz('D03: media dei provini 2.72',eq(weighted.mean(c(2.4,2.8),c(2,8)),2.72))
check_tikz('D03: media delle stazioni 2.60',eq(mean(c(2.4,2.8)),2.6))
campioni <- combn(5,2)
check_tikz('D04: dieci campioni e probabilita di inclusione 2/5',ncol(campioni)==10&&all(tabulate(campioni,nbins=5)/10==.4))
check_tikz('D06: aree proporzionali a varianza, bias quadrato e MSE',eq(c(2^2,1.5^2,2.5^2)/2.5^2,c(.64,.36,1)))
eta <- .6; Sigma6 <- kronecker(diag(2),(1-eta)*diag(3)+eta*matrix(1,3,3))
check_tikz('D08: matrice a due blocchi e varianza della media',eq(sum(Sigma6)/36,(1+2*eta)/6))
check_tikz('D11: quadruplicare n dimezza SE',eq((1/sqrt(16))/(1/sqrt(4)),.5))
griglia <- expand.grid(media=seq(-2,2,.2),mu=seq(-2,2,.3),se=c(.3,.8,1.4))
q <- qt(.975,19); T <- with(griglia,(media-mu)/se)
evento1 <- abs(T)<=q
evento2 <- with(griglia,media-q*se<=mu & mu<=media+q*se)
check_tikz('D12: equivalenza dei due eventi su una griglia',identical(evento1,evento2))
x <- c(4,5,7,8); J <- c(3,3,1,4); N <- tabulate(J,nbins=4)
check_tikz('D14: molteplicità 1 0 2 1',identical(N,c(1L,0L,2L,1L)))
check_tikz('D15: replica 7 7 4 8, media 6.5',identical(x[J],c(7,7,4,8))&&eq(mean(x[J]),6.5))
check_tikz('D14-D15: due rappresentazioni della stessa media',eq(sum(N*x)/length(x),mean(x[J])))
a <- c(7.2,6.8,6.1); b <- c(6.3,5.8,5.5); jj <- c(2,2,1)
check_tikz('D19: coppie ricampionate e differenze ricampionate',eq(mean(a[jj]-b[jj]),mean((a-b)[jj])))
z <- matrix(seq_len(12),nrow=3,byrow=TRUE); jg <- c(2,2,1)
check_tikz('D20: gruppi bilanciati e medie locali',eq(mean(z[jg,]),mean(rowMeans(z)[jg])))
starts <- c(4,1,4); l <- 3; n <- 8
ix <- unlist(lapply(starts,function(a)a:(a+l-1)))[seq_len(n)]
check_tikz('D22: concatenazione e troncamento dei blocchi',eq(ix,c(4,5,6,1,2,3,4,5))&&all(starts<=n-l+1))
dir.create('verifiche/M05',showWarnings=FALSE)
write.csv(esiti_tikz,'verifiche/M05/test_diagrammi_R.csv',row.names=FALSE)
cat(nrow(esiti_tikz),'controlli dei diagrammi superati\n')
