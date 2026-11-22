# ANNULA M07 - Esercitazioni svolte in R
# Aprire il progetto del modulo o il progetto generale dei notebook.
# Ogni sezione corrisponde al notebook indicato.


# M07_N01 - Risposta, predittore e geometria del fossile
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M07_Annula"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M07_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M07_Annula o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M07_N01")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(7001)


# Lettura e controllo delle misure
# Ogni riga identifica un fossile simulato.
f <- carica_dati("fossili_simulati.csv")
f$morfotipo <- factor(f$morfotipo, levels=c("Rounded", "Spiky"))
x <- f$diametro_tot_um
y <- f$diametro_int_um
stopifnot(nrow(f)==160L, !anyDuplicated(f$id),
          all(is.finite(x)), all(is.finite(y)))
head(f[, c("id", "morfotipo", "diametro_tot_um", "diametro_int_um")])
summary(f[, c("diametro_tot_um", "diametro_int_um")])


# Una nuvola con un vincolo geometrico
# Colori distinti per mantenere visibile l'informazione di gruppo.
colore <- c("#087C74", "#C57E42")[f$morfotipo]
plot(x, y, pch=19, col=adjustcolor(colore,.7),
     xlab="Diametro totale (micrometri)", ylab="Diametro interno (micrometri)")
abline(0,1,lty=2,col="grey45")
legend("topleft",levels(f$morfotipo),pch=19,col=c("#087C74","#C57E42"),bty="n")
scarto_geometrico <- x-y-2*f$spessore_um
c(massimo_scarto=max(abs(scarto_geometrico)), punti_sopra=sum(y>x))


# La domanda condizionata
# Una finestra scelta per illustrare la lettura condizionata.
vicini <- abs(x-6)<=.25
c(n=sum(vicini), diametro_medio=mean(y[vicini]),
  sd_diametro=sd(y[vicini]))
f[vicini, c("id","diametro_tot_um","diametro_int_um","spessore_um")]


# Variante svolta
centri <- c(6,7)
do.call(rbind,lapply(centri,function(a) {
 v <- abs(x-a)<=.25
 data.frame(centro=a,n=sum(v),media=mean(y[v]),sd=sd(y[v]))
}))


# M07_N02 - Pearson, Spearman e forma della relazione
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M07_Annula"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M07_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M07_Annula o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M07_N02")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(7002)


# I due coefficienti sui fossili
# Ogni riga identifica un fossile simulato.
f <- carica_dati("fossili_simulati.csv")
f$morfotipo <- factor(f$morfotipo, levels=c("Rounded", "Spiky"))
x <- f$diametro_tot_um
y <- f$diametro_int_um
stopifnot(nrow(f)==160L, !anyDuplicated(f$id),
          all(is.finite(x)), all(is.finite(y)))
data.frame(metodo=c("Pearson","Spearman"),
 coefficiente=c(cor(x,y),cor(x,y,method="spearman")))
plot(x,y,pch=19,col=adjustcolor("#087C74",.6),
 xlab="Diametro totale (micrometri)",ylab="Diametro interno (micrometri)")


# Unità di misura e simmetria
# Da micrometri a nanometri: moltiplicazione per 1000.
c(r_um=cor(x,y),r_nm=cor(1000*x,y),r_invertito=cor(y,x))
c(pendenza_um=unname(coef(lm(y~x))[2]),
  pendenza_nm=unname(coef(lm(y~I(1000*x)))[2]))


# Una curva può avere correlazione nulla
u <- seq(-2,2,length.out=101)
v <- u^2
c(Pearson=cor(u,v),Spearman=cor(u,v,method="spearman"))
plot(u,v,type="l",lwd=2,col="#5146A5",xlab="X simulato",ylab="Y = X^2")


# Variante svolta
ramo <- u>=0
c(Pearson=cor(u[ramo],v[ramo]),
  Spearman=cor(u[ramo],v[ramo],method="spearman"))


# M07_N03 - La retta dei minimi quadrati a mano
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M07_Annula"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M07_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M07_Annula o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M07_N03")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(7003)


# Il criterio da minimizzare
# Ogni riga identifica un fossile simulato.
f <- carica_dati("fossili_simulati.csv")
f$morfotipo <- factor(f$morfotipo, levels=c("Rounded", "Spiky"))
x <- f$diametro_tot_um
y <- f$diametro_int_um
stopifnot(nrow(f)==160L, !anyDuplicated(f$id),
          all(is.finite(x)), all(is.finite(y)))
# Prima retta proposta: intercetta zero e pendenza uno.
SSE_proposta <- sum((y-x)^2)
c(SSE_proposta=SSE_proposta)


# Coefficienti dalle somme centrate
Sxx <- sum((x-mean(x))^2)
Sxy <- sum((x-mean(x))*(y-mean(y)))
stopifnot(Sxx>0)
b1 <- Sxy/Sxx
b0 <- mean(y)-b1*mean(x)
y_hat <- b0+b1*x
e <- y-y_hat
c(intercetta=b0,pendenza=b1,SSE=sum(e^2))


# Le proprietà della soluzione
c(somma_residui=sum(e),somma_x_residui=sum(x*e),
  scarto_al_baricentro=(b0+b1*mean(x))-mean(y))
plot(x,y,pch=19,col="grey65",xlab="Diametro totale (micrometri)",
 ylab="Diametro interno (micrometri)")
abline(b0,b1,col="#087C74",lwd=2)
points(mean(x),mean(y),pch=23,bg="#C57E42",cex=1.5)


# Variante svolta
b1_alt <- b1+.10
b0_alt <- mean(y)-b1_alt*mean(x)
c(SSE_ottima=sum(e^2),SSE_alternativa=sum((y-b0_alt-b1_alt*x)^2))


# M07_N04 - Stima con lm e interpretazione dei coefficienti
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M07_Annula"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M07_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M07_Annula o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M07_N04")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(7004)


# La formula e l’oggetto modello
# Ogni riga identifica un fossile simulato.
f <- carica_dati("fossili_simulati.csv")
f$morfotipo <- factor(f$morfotipo, levels=c("Rounded", "Spiky"))
x <- f$diametro_tot_um
y <- f$diametro_int_um
stopifnot(nrow(f)==160L, !anyDuplicated(f$id),
          all(is.finite(x)), all(is.finite(y)))
# La formula mette la risposta a sinistra della tilde.
modello <- lm(diametro_int_um ~ diametro_tot_um, data=f)
e <- residuals(modello)
coef(modello)
head(data.frame(osservato=y,stimato=fitted(modello),residuo=e))


# Incertezza dei coefficienti
# Intervalli al 95% per i coefficienti.
confint(modello,level=.95)
coef(summary(modello))
summary(modello)$sigma


# Un confronto con il calcolo manuale
b1 <- cov(x,y)/var(x)
b0 <- mean(y)-b1*mean(x)
confronto <- cbind(manuale=c(b0,b1),R=unname(coef(modello)))
rownames(confronto) <- c("intercetta","pendenza")
confronto
stopifnot(max(abs(confronto[,1]-confronto[,2]))<1e-10)


# Variante svolta
f$x_centrato <- f$diametro_tot_um-7
m_centrato <- lm(diametro_int_um~x_centrato,data=f)
coef(m_centrato)
predict(modello,newdata=data.frame(diametro_tot_um=7))


# M07_N05 - R², dispersione residua e RMSE
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M07_Annula"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M07_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M07_Annula o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M07_N05")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(7005)


# Una quota della variabilità osservata
# Ogni riga identifica un fossile simulato.
f <- carica_dati("fossili_simulati.csv")
f$morfotipo <- factor(f$morfotipo, levels=c("Rounded", "Spiky"))
x <- f$diametro_tot_um
y <- f$diametro_int_um
stopifnot(nrow(f)==160L, !anyDuplicated(f$id),
          all(is.finite(x)), all(is.finite(y)))
# La formula mette la risposta a sinistra della tilde.
modello <- lm(diametro_int_um ~ diametro_tot_um, data=f)
e <- residuals(modello)
SSE <- sum(e^2)
SST <- sum((y-mean(y))^2)
R2 <- 1-SSE/SST
c(SSE=SSE,SST=SST,R2=R2,R2_da_R=summary(modello)$r.squared)


# La scala dell’errore
n <- nrow(f)
p <- length(coef(modello))
data.frame(n=n,p=p,SD_residua=sqrt(SSE/(n-p)),
           RMSE_campione=sqrt(SSE/n),MAE_campione=mean(abs(e)))
stopifnot(abs(sqrt(SSE/(n-p))-summary(modello)$sigma)<1e-12)


# Il cambio di unità
m_nm <- lm(I(1000*diametro_int_um)~diametro_tot_um,data=f)
data.frame(unita=c("micrometri","nanometri"),
 R2=c(summary(modello)$r.squared,summary(m_nm)$r.squared),
 SD_residua=c(summary(modello)$sigma,summary(m_nm)$sigma))


# Variante svolta
c(R2=summary(modello)$r.squared,r_quadrato=cor(x,y)^2)
stopifnot(abs(summary(modello)$r.squared-cor(x,y)^2)<1e-12)


# M07_N06 - Intervallo per la media e per un individuo
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M07_Annula"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M07_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M07_Annula o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M07_N06")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(7006)


# Due oggetti della previsione
# Ogni riga identifica un fossile simulato.
f <- carica_dati("fossili_simulati.csv")
f$morfotipo <- factor(f$morfotipo, levels=c("Rounded", "Spiky"))
x <- f$diametro_tot_um
y <- f$diametro_int_um
stopifnot(nrow(f)==160L, !anyDuplicated(f$id),
          all(is.finite(x)), all(is.finite(y)))
# La formula mette la risposta a sinistra della tilde.
modello <- lm(diametro_int_um ~ diametro_tot_um, data=f)
e <- residuals(modello)
x0 <- data.frame(diametro_tot_um=7)
IC <- predict(modello,x0,interval="confidence",level=.95)
IP <- predict(modello,x0,interval="prediction",level=.95)
rbind(media=IC,nuovo_individuo=IP)


# La formula spiega la differenza
h0 <- 1/length(x)+(7-mean(x))^2/sum((x-mean(x))^2)
s <- summary(modello)$sigma
tcrit <- qt(.975,df=df.residual(modello))
centro <- as.numeric(predict(modello,x0))
rbind(media=centro+c(-1,1)*tcrit*s*sqrt(h0),
      individuo=centro+c(-1,1)*tcrit*s*sqrt(1+h0))
c(SE_media=s*sqrt(h0),SE_individuo=s*sqrt(1+h0))


# Bande nel dominio osservato
g <- data.frame(diametro_tot_um=seq(min(x),max(x),length.out=100))
ic <- predict(modello,g,interval="confidence")
ip <- predict(modello,g,interval="prediction")
plot(x,y,pch=19,col="grey70",xlab="Diametro totale (micrometri)",
 ylab="Diametro interno (micrometri)")
matlines(g$diametro_tot_um,ip[,2:3],col="#C57E42",lty=3,lwd=1.5)
matlines(g$diametro_tot_um,ic[,2:3],col="#087C74",lty=2,lwd=1.5)
lines(g$diametro_tot_um,ic[,1],col="#087C74",lwd=2)
legend("topleft",c("Media al 95%","Individuo al 95%"),
 col=c("#087C74","#C57E42"),lty=c(2,3),bty="n")


# Variante svolta
nuovo <- data.frame(diametro_tot_um=11)
predict(modello,nuovo,interval="prediction")
nuovo$diametro_tot_um>=min(x) & nuovo$diametro_tot_um<=max(x)


# M07_N07 - Residui contro valori stimati
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M07_Annula"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M07_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M07_Annula o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M07_N07")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(7007)


# Ricostruire gli scarti
# Ogni riga identifica un fossile simulato.
f <- carica_dati("fossili_simulati.csv")
f$morfotipo <- factor(f$morfotipo, levels=c("Rounded", "Spiky"))
x <- f$diametro_tot_um
y <- f$diametro_int_um
stopifnot(nrow(f)==160L, !anyDuplicated(f$id),
          all(is.finite(x)), all(is.finite(y)))
# La formula mette la risposta a sinistra della tilde.
modello <- lm(diametro_int_um ~ diametro_tot_um, data=f)
e <- residuals(modello)
head(data.frame(id=f$id,osservato=y,stimato=fitted(modello),residuo=e))
stopifnot(max(abs(e-(y-fitted(modello))))<1e-12)


# Andamento e dispersione
plot(fitted(modello),e,pch=19,col=adjustcolor("#087C74",.65),
 xlab="Diametro interno stimato (micrometri)",ylab="Residuo (micrometri)")
abline(h=0,lty=2,col="grey45")
lines(lowess(fitted(modello),e),col="#C57E42",lwd=2)
cor(fitted(modello),e)


# Un esempio con curvatura nota
set.seed(707)
u <- seq(-2,2,length.out=80)
v <- 1+.6*u+.8*u^2+rnorm(80,sd=.25)
fit_curva <- lm(v~u)
plot(fitted(fit_curva),resid(fit_curva),pch=19,col="#5146A5",
 xlab="Valore stimato dalla retta",ylab="Residuo")
abline(h=0,lty=2)
lines(lowess(fitted(fit_curva),resid(fit_curva)),col="#C57E42",lwd=2)


# Variante svolta
fit2 <- lm(v~u+I(u^2))
c(RMSE_retta=sqrt(mean(resid(fit_curva)^2)),
  RMSE_quadratico=sqrt(mean(resid(fit2)^2)))
plot(fitted(fit2),resid(fit2),pch=19,col="#087C74",
 xlab="Valore stimato dal modello quadratico",ylab="Residuo")
abline(h=0,lty=2)


# M07_N08 - Distribuzione dei residui e differenze fra gruppi
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M07_Annula"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M07_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M07_Annula o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M07_N08")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(7008)


# Quantili dei residui
# Ogni riga identifica un fossile simulato.
f <- carica_dati("fossili_simulati.csv")
f$morfotipo <- factor(f$morfotipo, levels=c("Rounded", "Spiky"))
x <- f$diametro_tot_um
y <- f$diametro_int_um
stopifnot(nrow(f)==160L, !anyDuplicated(f$id),
          all(is.finite(x)), all(is.finite(y)))
# La formula mette la risposta a sinistra della tilde.
modello <- lm(diametro_int_um ~ diametro_tot_um, data=f)
e <- residuals(modello)
qqnorm(rstandard(modello),pch=19,col="#087C74",main="QQ plot dei residui standardizzati",
 xlab="Quantili gaussiani",ylab="Residui standardizzati")
qqline(rstandard(modello),col="#C57E42",lwd=2)


# Residui distinti per morfotipo
aggregate(e,list(morfotipo=f$morfotipo),mean)
boxplot(e~f$morfotipo,col=c("#B9DDD7","#E5C7A8"),
 xlab="Morfotipo",ylab="Residuo della retta comune (micrometri)")
abline(h=0,lty=2)


# Un indicatore aggiunto alla retta
m_gruppo <- lm(diametro_int_um~diametro_tot_um+morfotipo,data=f)
coef(m_gruppo)
c(SD_comune=summary(modello)$sigma,SD_con_gruppo=summary(m_gruppo)$sigma)
aggregate(resid(m_gruppo),list(morfotipo=f$morfotipo),mean)


# Variante svolta
m_interazione <- lm(diametro_int_um~diametro_tot_um*morfotipo,data=f)
b <- coef(m_interazione)
c(pendenza_Rounded=b[2],pendenza_Spiky=b[2]+b[4],
  differenza_a_7=b[3]+7*b[4])


# M07_N09 - Leva e influenza di un’osservazione
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M07_Annula"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M07_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M07_Annula o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M07_N09")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(7009)


# Tre quantità per ogni individuo
# Ogni riga identifica un fossile simulato.
f <- carica_dati("fossili_simulati.csv")
f$morfotipo <- factor(f$morfotipo, levels=c("Rounded", "Spiky"))
x <- f$diametro_tot_um
y <- f$diametro_int_um
stopifnot(nrow(f)==160L, !anyDuplicated(f$id),
          all(is.finite(x)), all(is.finite(y)))
# La formula mette la risposta a sinistra della tilde.
modello <- lm(diametro_int_um ~ diametro_tot_um, data=f)
e <- residuals(modello)
diag <- data.frame(id=f$id,x=x,residuo=e,
 leva=hatvalues(modello),Cook=cooks.distance(modello))
diag[order(diag$Cook,decreasing=TRUE)[1:6],]
c(somma_leve=sum(diag$leva),numero_coefficienti=length(coef(modello)))


# Il grafico con dimensione proporzionale a Cook
rs <- rstandard(modello)
plot(diag$leva,rs,pch=21,bg="#B9DDD7",col="#087C74",
 cex=.8+3*sqrt(diag$Cook/max(diag$Cook)),
 xlab="Leva",ylab="Residuo standardizzato")
abline(h=0,lty=2)
j <- which.max(diag$Cook)
text(diag$leva[j],rs[j],labels=f$id[j],pos=2,cex=.8)


# Analisi di sensibilità documentata
senza <- lm(diametro_int_um~diametro_tot_um,data=f[-j,])
rbind(tutti=coef(modello),senza_caso=coef(senza))
data.frame(id_escluso=f$id[j],Cook=diag$Cook[j],
 variazione_pendenza=coef(senza)[2]-coef(modello)[2])


# Variante svolta
u <- seq(0,5,length.out=24)
set.seed(709)
v <- 1+1.2*u+rnorm(24,sd=.5)
con_punto <- function(y_nuovo) {
 m <- lm(c(v,y_nuovo)~c(u,8))
 c(leva=tail(hatvalues(m),1),Cook=tail(cooks.distance(m),1))
}
rbind(vicino_alla_retta=con_punto(1+1.2*8),lontano=con_punto(3))


# M07_N10 - Un protocollo per separare training e test
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M07_Annula"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M07_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M07_Annula o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M07_N10")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(7010)


# Una regola riproducibile
# Ogni riga identifica un fossile simulato.
f <- carica_dati("fossili_simulati.csv")
f$morfotipo <- factor(f$morfotipo, levels=c("Rounded", "Spiky"))
x <- f$diametro_tot_um
y <- f$diametro_int_um
stopifnot(nrow(f)==160L, !anyDuplicated(f$id),
          all(is.finite(x)), all(is.finite(y)))
# Partizione fissata prima del confronto dei modelli.
# Nel CSV didattico ogni quinto individuo forma il test.
is_test <- seq_len(nrow(f)) %% 5L == 0L
train <- f[!is_test, ]
test <- f[is_test, ]
stopifnot(nrow(train)==128L, nrow(test)==32L,
          length(intersect(train$id, test$id))==0L)
table(insieme=ifelse(is_test,"test","train"),morfotipo=f$morfotipo)
head(train$id)
head(test$id)


# Controlli sulla separazione
c(n_training=nrow(train),n_test=nrow(test),
  id_condivisi=length(intersect(train$id,test$id)))
stopifnot(setequal(c(train$id,test$id),f$id))
data.frame(insieme=c("train","test"),
 minimo_x=c(min(train$diametro_tot_um),min(test$diametro_tot_um)),
 massimo_x=c(max(train$diametro_tot_um),max(test$diametro_tot_um)))


# I candidati e la metrica
formule <- list(
 lineare=diametro_int_um~diametro_tot_um,
 con_morfotipo=diametro_int_um~diametro_tot_um+morfotipo,
 polinomio3=diametro_int_um~poly(diametro_tot_um,3))
formule
# Salviamo soltanto gli ID e la decisione di partizione.
write.csv(data.frame(id=f$id,insieme=ifelse(is_test,"test","train")),
 percorso_risultati("partizione.csv"),row.names=FALSE)


# Variante svolta
stazione <- rep(c("A","B"),each=10)
test_riga <- seq_along(stazione)%%5==0
intersect(unique(stazione[test_riga]),unique(stazione[!test_riga]))
# Una separazione per stazione conserva le repliche insieme.
test_stazione <- stazione=="B"
intersect(unique(stazione[test_stazione]),unique(stazione[!test_stazione]))


# M07_N11 - Una previsione di riferimento
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M07_Annula"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M07_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M07_Annula o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M07_N11")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(7011)


# Il riferimento usa soltanto il training
# Ogni riga identifica un fossile simulato.
f <- carica_dati("fossili_simulati.csv")
f$morfotipo <- factor(f$morfotipo, levels=c("Rounded", "Spiky"))
x <- f$diametro_tot_um
y <- f$diametro_int_um
stopifnot(nrow(f)==160L, !anyDuplicated(f$id),
          all(is.finite(x)), all(is.finite(y)))
# Partizione fissata prima del confronto dei modelli.
# Nel CSV didattico ogni quinto individuo forma il test.
is_test <- seq_len(nrow(f)) %% 5L == 0L
train <- f[!is_test, ]
test <- f[is_test, ]
stopifnot(nrow(train)==128L, nrow(test)==32L,
          length(intersect(train$id, test$id))==0L)
media_training <- mean(train$diametro_int_um)
mediana_training <- median(train$diametro_int_um)
c(media=media_training,mediana=mediana_training)


# Due funzioni di perdita
metriche <- function(osservato,previsto) {
 stopifnot(length(osservato)==length(previsto),
           all(is.finite(osservato)),all(is.finite(previsto)))
 c(MAE=mean(abs(osservato-previsto)),
   RMSE=sqrt(mean((osservato-previsto)^2)))
}
rbind(media=metriche(train$diametro_int_um,
                    rep(media_training,nrow(train))),
      mediana=metriche(train$diametro_int_um,
                      rep(mediana_training,nrow(train))))


# Il riferimento nelle partizioni interne
set.seed(714)
fold <- sample(rep(1:5,length.out=nrow(train)))
base_cv <- do.call(rbind,lapply(1:5,function(k) {
 stima <- train[fold!=k,]
 verifica <- train[fold==k,]
 p <- rep(mean(stima$diametro_int_um),nrow(verifica))
 data.frame(fold=k,t(metriche(verifica$diametro_int_um,p)))
}))
base_cv
colMeans(base_cv[,c("MAE","RMSE")])


# Variante svolta
osservato <- c(5,5,5,5)
buono <- c(5.1,4.9,5.1,4.9)
con_errore <- buono
con_errore[4] <- osservato[4]+3
rbind(piccoli_errori=metriche(osservato,buono),
      un_errore_grande=metriche(osservato,con_errore))


# M07_N12 - Validazione interna sul solo training
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M07_Annula"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M07_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M07_Annula o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M07_N12")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(7012)


# Le cinque partizioni
# Ogni riga identifica un fossile simulato.
f <- carica_dati("fossili_simulati.csv")
f$morfotipo <- factor(f$morfotipo, levels=c("Rounded", "Spiky"))
x <- f$diametro_tot_um
y <- f$diametro_int_um
stopifnot(nrow(f)==160L, !anyDuplicated(f$id),
          all(is.finite(x)), all(is.finite(y)))
# Partizione fissata prima del confronto dei modelli.
# Nel CSV didattico ogni quinto individuo forma il test.
is_test <- seq_len(nrow(f)) %% 5L == 0L
train <- f[!is_test, ]
test <- f[is_test, ]
stopifnot(nrow(train)==128L, nrow(test)==32L,
          length(intersect(train$id, test$id))==0L)
set.seed(714)
fold <- sample(rep(1:5,length.out=nrow(train)))
table(fold)
formule <- list(lineare=diametro_int_um~diametro_tot_um,
 con_morfotipo=diametro_int_um~diametro_tot_um+morfotipo,
 polinomio3=diametro_int_um~poly(diametro_tot_um,3))


# Ristimare il modello a ogni giro
cv <- do.call(rbind,lapply(names(formule),function(nome) {
 do.call(rbind,lapply(1:5,function(k) {
  tr <- train[fold!=k,]
  va <- train[fold==k,]
  m <- lm(formule[[nome]],data=tr)
  pr <- predict(m,newdata=va)
  met <- metriche(va$diametro_int_um,pr)
  data.frame(modello=nome,fold=k,
             MAE=unname(met["MAE"]),RMSE=unname(met["RMSE"]))
 }))
}))
cv


# Scelta dichiarata dal criterio
media_cv <- aggregate(cbind(MAE,RMSE)~modello,cv,mean)
media_cv
scelto <- media_cv$modello[which.min(media_cv$RMSE)]
scelto
barplot(media_cv$RMSE,names.arg=media_cv$modello,
 col=c("#087C74","#C57E42","#7363AA"),
 ylab="Media dei RMSE interni (micrometri)",cex.names=.85)


# Variante svolta
automatica <- seleziona_modello(train,seme=714)
automatica$riepilogo
stopifnot(identical(automatica$nome,scelto),
 max(abs(automatica$riepilogo$RMSE-media_cv$RMSE))<1e-12)


# M07_N13 - Ristima e valutazione sul test
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M07_Annula"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M07_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M07_Annula o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M07_N13")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(7013)


# Ristima sulla totalità del training
# Ogni riga identifica un fossile simulato.
f <- carica_dati("fossili_simulati.csv")
f$morfotipo <- factor(f$morfotipo, levels=c("Rounded", "Spiky"))
x <- f$diametro_tot_um
y <- f$diametro_int_um
stopifnot(nrow(f)==160L, !anyDuplicated(f$id),
          all(is.finite(x)), all(is.finite(y)))
# Partizione fissata prima del confronto dei modelli.
# Nel CSV didattico ogni quinto individuo forma il test.
is_test <- seq_len(nrow(f)) %% 5L == 0L
train <- f[!is_test, ]
test <- f[is_test, ]
stopifnot(nrow(train)==128L, nrow(test)==32L,
          length(intersect(train$id, test$id))==0L)
# La funzione ripete la stima su cinque partizioni del solo training.
# Il suo codice completo e' spiegato nel notebook N12.
scelta <- seleziona_modello(train, seme=714)
finale <- lm(scelta$formule[[scelta$nome]], data=train)
scelta$nome
coef(finale)
nobs(finale)


# Lo stesso test per modello e riferimento
p_modello <- as.numeric(predict(finale,newdata=test))
p_base <- rep(mean(train$diametro_int_um),nrow(test))
errori <- rbind(media_training=metriche(test$diametro_int_um,p_base),
               modello=metriche(test$diametro_int_um,p_modello))
errori
stopifnot(length(p_modello)==32L)


# Previsioni per individuo
previsioni <- data.frame(id=test$id,osservato=test$diametro_int_um,
 previsto=p_modello,residuo=test$diametro_int_um-p_modello)
previsioni[order(abs(previsioni$residuo),decreasing=TRUE)[1:6],]
plot(previsioni$osservato,previsioni$previsto,pch=19,col="#087C74",
 xlab="Osservato nel test (micrometri)",ylab="Previsto (micrometri)")
abline(0,1,lty=2)
write.csv(previsioni,percorso_risultati("previsioni_test.csv"),row.names=FALSE)


# Variante svolta
riduzione <- 1-errori["modello","RMSE"]/errori["media_training","RMSE"]
c(riduzione_RMSE_percento=100*riduzione)


# M07_N14 - Errore di training e generalizzazione
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M07_Annula"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M07_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M07_Annula o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M07_N14")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(7014)


# Training e test del modello selezionato
# Ogni riga identifica un fossile simulato.
f <- carica_dati("fossili_simulati.csv")
f$morfotipo <- factor(f$morfotipo, levels=c("Rounded", "Spiky"))
x <- f$diametro_tot_um
y <- f$diametro_int_um
stopifnot(nrow(f)==160L, !anyDuplicated(f$id),
          all(is.finite(x)), all(is.finite(y)))
# Partizione fissata prima del confronto dei modelli.
# Nel CSV didattico ogni quinto individuo forma il test.
is_test <- seq_len(nrow(f)) %% 5L == 0L
train <- f[!is_test, ]
test <- f[is_test, ]
stopifnot(nrow(train)==128L, nrow(test)==32L,
          length(intersect(train$id, test$id))==0L)
# La funzione ripete la stima su cinque partizioni del solo training.
# Il suo codice completo e' spiegato nel notebook N12.
scelta <- seleziona_modello(train, seme=714)
finale <- lm(scelta$formule[[scelta$nome]], data=train)
rbind(training=metriche(train$diametro_int_um,predict(finale,train)),
      test=metriche(test$diametro_int_um,predict(finale,test)))


# Una simulazione con complessità crescente
set.seed(714)
tr <- data.frame(x=seq(-1,1,length.out=24))
tr$y <- sin(3*tr$x)+rnorm(nrow(tr),sd=.4)
nuovi <- data.frame(x=seq(-1,1,length.out=150))
nuovi$y <- sin(3*nuovi$x)+rnorm(nrow(nuovi),sd=.4)
ris <- do.call(rbind,lapply(1:9,function(g) {
 m <- lm(y~poly(x,g),data=tr)
 data.frame(grado=g,training=metriche(tr$y,predict(m,tr))["RMSE"],
  nuovi=metriche(nuovi$y,predict(m,nuovi))["RMSE"])
}))
ris


# Il grafico degli errori
matplot(ris$grado,ris[,c("training","nuovi")],type="b",pch=c(16,17),
 col=c("#087C74","#C57E42"),lty=1,xlab="Grado del polinomio",ylab="RMSE")
legend("topright",c("Training","Nuovi dati"),col=c("#087C74","#C57E42"),
 pch=c(16,17),lty=1,bty="n")


# Variante svolta
g_scelto <- ris$grado[which.min(ris$nuovi)]
mod_scelto <- lm(y~poly(x,g_scelto),data=tr)
set.seed(7141)
ultimo <- data.frame(x=seq(-1,1,length.out=150))
ultimo$y <- sin(3*ultimo$x)+rnorm(nrow(ultimo),sd=.4)
c(grado_scelto=g_scelto,RMSE_finale=metriche(ultimo$y,predict(mod_scelto,ultimo))["RMSE"])


# M07_N15 - Trasformazioni apprese nel training
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M07_Annula"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M07_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M07_Annula o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M07_N15")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(7015)


# Media e scala sono parametri stimati
# Ogni riga identifica un fossile simulato.
f <- carica_dati("fossili_simulati.csv")
f$morfotipo <- factor(f$morfotipo, levels=c("Rounded", "Spiky"))
x <- f$diametro_tot_um
y <- f$diametro_int_um
stopifnot(nrow(f)==160L, !anyDuplicated(f$id),
          all(is.finite(x)), all(is.finite(y)))
# Partizione fissata prima del confronto dei modelli.
# Nel CSV didattico ogni quinto individuo forma il test.
is_test <- seq_len(nrow(f)) %% 5L == 0L
train <- f[!is_test, ]
test <- f[is_test, ]
stopifnot(nrow(train)==128L, nrow(test)==32L,
          length(intersect(train$id, test$id))==0L)
mu <- mean(train$diametro_tot_um)
sx <- sd(train$diametro_tot_um)
stopifnot(sx>0)
train$z <- (train$diametro_tot_um-mu)/sx
test$z <- (test$diametro_tot_um-mu)/sx
c(media_training=mean(train$z),sd_training=sd(train$z),
  media_test=mean(test$z),sd_test=sd(test$z))


# Le previsioni sulla stessa scala
m_x <- lm(diametro_int_um~diametro_tot_um,data=train)
m_z <- lm(diametro_int_um~z,data=train)
p_x <- predict(m_x,test)
p_z <- predict(m_z,test)
c(massima_differenza=max(abs(p_x-p_z)))
coef(m_z)
stopifnot(max(abs(p_x-p_z))<1e-10)


# La trasformazione all’interno di ogni fold
set.seed(714)
fold <- sample(rep(1:5,length.out=nrow(train)))
scale_cv <- do.call(rbind,lapply(1:5,function(k) {
 a <- train[fold!=k,];b <- train[fold==k,]
 media_k <- mean(a$diametro_tot_um)
 sd_k <- sd(a$diametro_tot_um)
 a$z <- (a$diametro_tot_um-media_k)/sd_k
 b$z <- (b$diametro_tot_um-media_k)/sd_k
 m <- lm(diametro_int_um~z,data=a)
 data.frame(fold=k,media=media_k,sd=sd_k,
  RMSE=metriche(b$diametro_int_um,predict(m,b))["RMSE"])
}))
scale_cv


# Variante svolta
test_errato <- test
test_errato$z <- as.numeric(scale(test$diametro_tot_um))
p_errate <- predict(m_z,test_errato)
head(data.frame(previsione_coerente=p_z,previsione_scala_errata=p_errate))


# M07_N16 - Risposta binaria e regressione logistica
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M07_Annula"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M07_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M07_Annula o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M07_N16")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(7016)


# La codifica dell’evento
# Ogni riga identifica un fossile simulato.
f <- carica_dati("fossili_simulati.csv")
f$morfotipo <- factor(f$morfotipo, levels=c("Rounded", "Spiky"))
x <- f$diametro_tot_um
y <- f$diametro_int_um
stopifnot(nrow(f)==160L, !anyDuplicated(f$id),
          all(is.finite(x)), all(is.finite(y)))
# Partizione fissata prima del confronto dei modelli.
# Nel CSV didattico ogni quinto individuo forma il test.
is_test <- seq_len(nrow(f)) %% 5L == 0L
train <- f[!is_test, ]
test <- f[is_test, ]
stopifnot(nrow(train)==128L, nrow(test)==32L,
          length(intersect(train$id, test$id))==0L)
train$spiky <- as.integer(train$morfotipo=="Spiky")
test$spiky <- as.integer(test$morfotipo=="Spiky")
table(train$morfotipo,train$spiky)
head(train[,c("morfotipo","spiky","diametro_tot_um","rapporto_int_tot")])


# Il modello del logit
# Spiky=1 e Rounded=0: la probabilita' riguarda Spiky.
train$spiky <- as.integer(train$morfotipo=="Spiky")
test$spiky <- as.integer(test$morfotipo=="Spiky")
logit <- glm(spiky ~ diametro_tot_um + rapporto_int_tot,
             data=train, family=binomial())
stopifnot(logit$converged)
prob <- as.numeric(predict(logit, newdata=test, type="response"))
stopifnot(all(is.finite(prob)), all(prob>=0 & prob<=1))
coef(logit)
head(data.frame(id=test$id,osservato=test$spiky,probabilita=prob))


# Odds e incrementi interpretabili
b <- coef(logit)
c(OR_per_1_micrometro=exp(b["diametro_tot_um"]),
  OR_per_001_rapporto=exp(.01*b["rapporto_int_tot"]))
eta <- predict(logit,test,type="link")
stopifnot(max(abs(plogis(eta)-prob))<1e-12)


# Variante svolta
casi <- data.frame(diametro_tot_um=c(6,6),rapporto_int_tot=c(.75,.85))
cbind(casi,probabilita_Spiky=predict(logit,casi,type="response"))


# M07_N17 - Probabilità e classi: due valutazioni
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M07_Annula"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M07_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M07_Annula o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M07_N17")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(7017)


# Previsioni e riferimento probabilistico
# Ogni riga identifica un fossile simulato.
f <- carica_dati("fossili_simulati.csv")
f$morfotipo <- factor(f$morfotipo, levels=c("Rounded", "Spiky"))
x <- f$diametro_tot_um
y <- f$diametro_int_um
stopifnot(nrow(f)==160L, !anyDuplicated(f$id),
          all(is.finite(x)), all(is.finite(y)))
# Partizione fissata prima del confronto dei modelli.
# Nel CSV didattico ogni quinto individuo forma il test.
is_test <- seq_len(nrow(f)) %% 5L == 0L
train <- f[!is_test, ]
test <- f[is_test, ]
stopifnot(nrow(train)==128L, nrow(test)==32L,
          length(intersect(train$id, test$id))==0L)
# Spiky=1 e Rounded=0: la probabilita' riguarda Spiky.
train$spiky <- as.integer(train$morfotipo=="Spiky")
test$spiky <- as.integer(test$morfotipo=="Spiky")
logit <- glm(spiky ~ diametro_tot_um + rapporto_int_tot,
             data=train, family=binomial())
stopifnot(logit$converged)
prob <- as.numeric(predict(logit, newdata=test, type="response"))
stopifnot(all(is.finite(prob)), all(prob>=0 & prob<=1))
p_base <- mean(train$spiky)
c(probabilita_riferimento=p_base,n_test=nrow(test))


# Brier score
Brier <- mean((prob-test$spiky)^2)
Brier_base <- mean((p_base-test$spiky)^2)
c(Brier_modello=Brier,Brier_riferimento=Brier_base)
head(data.frame(osservato=test$spiky,p=prob,perdita=(prob-test$spiky)^2))


# Soglia e matrice di confusione
soglia <- .5
classe <- as.integer(prob>=soglia)
table(osservato=factor(test$spiky,levels=0:1),
      previsto=factor(classe,levels=0:1))
c(accuratezza=mean(classe==test$spiky),soglia=soglia)


# Variante svolta
p <- c(.51,.99)
data.frame(p=p,classe=as.integer(p>=.5),Brier_individuale=(p-1)^2)


# M07_N18 - Calibrazione descrittiva con pochi dati
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M07_Annula"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M07_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M07_Annula o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M07_N18")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(7018)


# Fasce fissate in anticipo
# Ogni riga identifica un fossile simulato.
f <- carica_dati("fossili_simulati.csv")
f$morfotipo <- factor(f$morfotipo, levels=c("Rounded", "Spiky"))
x <- f$diametro_tot_um
y <- f$diametro_int_um
stopifnot(nrow(f)==160L, !anyDuplicated(f$id),
          all(is.finite(x)), all(is.finite(y)))
# Partizione fissata prima del confronto dei modelli.
# Nel CSV didattico ogni quinto individuo forma il test.
is_test <- seq_len(nrow(f)) %% 5L == 0L
train <- f[!is_test, ]
test <- f[is_test, ]
stopifnot(nrow(train)==128L, nrow(test)==32L,
          length(intersect(train$id, test$id))==0L)
# Spiky=1 e Rounded=0: la probabilita' riguarda Spiky.
train$spiky <- as.integer(train$morfotipo=="Spiky")
test$spiky <- as.integer(test$morfotipo=="Spiky")
logit <- glm(spiky ~ diametro_tot_um + rapporto_int_tot,
             data=train, family=binomial())
stopifnot(logit$converged)
prob <- as.numeric(predict(logit, newdata=test, type="response"))
stopifnot(all(is.finite(prob)), all(prob>=0 & prob<=1))
val <- data.frame(prob=prob,osservato=test$spiky,
 fascia=cut(prob,breaks=seq(0,1,.2),include.lowest=TRUE))
table(val$fascia)
head(val)


# Una tabella con le numerosità
cal <- aggregate(cbind(prob,osservato)~fascia,val,mean)
numeri <- aggregate(osservato~fascia,val,length)
names(numeri)[2] <- "n"
cal <- merge(cal,numeri,by="fascia",all.x=TRUE)
cal


# Un grafico leggibile
plot(cal$prob,cal$osservato,xlim=c(0,1),ylim=c(-.04,1.12),pch=19,
 col="#087C74",xlab="Probabilita' media prevista",
 ylab="Frequenza osservata di Spiky")
abline(0,1,lty=2,col="grey50")
text(cal$prob,cal$osservato,labels=paste0("n=",cal$n),pos=3,cex=.8)
write.csv(cal,percorso_risultati("calibrazione_descrittiva.csv"),row.names=FALSE)


# Variante svolta
val$fascia2 <- cut(prob,c(0,.5,1),include.lowest=TRUE)
aggregate(cbind(prob,osservato)~fascia2,val,mean)
table(val$fascia2)


# M07_N19 - MAE e RMSE nelle decisioni di previsione
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M07_Annula"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M07_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M07_Annula o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M07_N19")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(7019)


# Un calcolo controllabile a mano
osservato <- c(1,2,3)
previsto <- c(1,2,6)
e <- osservato-previsto
data.frame(osservato,previsto,errore=e,assoluto=abs(e),quadrato=e^2)
metriche(osservato,previsto)


# Due modelli con errori distribuiti diversamente
vero <- rep(0,10)
regola_A <- rep(.8,10)
regola_B <- c(rep(0,9),3)
rbind(A=metriche(vero,regola_A),B=metriche(vero,regola_B))
barplot(rbind(abs(vero-regola_A),abs(vero-regola_B)),beside=TRUE,
 col=c("#087C74","#C57E42"),xlab="Caso",ylab="Errore assoluto")
legend("topleft",c("A","B"),fill=c("#087C74","#C57E42"),bty="n")


# Le metriche sul caso dei fossili
# Ogni riga identifica un fossile simulato.
f <- carica_dati("fossili_simulati.csv")
f$morfotipo <- factor(f$morfotipo, levels=c("Rounded", "Spiky"))
x <- f$diametro_tot_um
y <- f$diametro_int_um
stopifnot(nrow(f)==160L, !anyDuplicated(f$id),
          all(is.finite(x)), all(is.finite(y)))
# Partizione fissata prima del confronto dei modelli.
# Nel CSV didattico ogni quinto individuo forma il test.
is_test <- seq_len(nrow(f)) %% 5L == 0L
train <- f[!is_test, ]
test <- f[is_test, ]
stopifnot(nrow(train)==128L, nrow(test)==32L,
          length(intersect(train$id, test$id))==0L)
# La funzione ripete la stima su cinque partizioni del solo training.
# Il suo codice completo e' spiegato nel notebook N12.
scelta <- seleziona_modello(train, seme=714)
finale <- lm(scelta$formule[[scelta$nome]], data=train)
p <- predict(finale,test)
p0 <- rep(mean(train$diametro_int_um),nrow(test))
rbind(riferimento=metriche(test$diametro_int_um,p0),
 modello=metriche(test$diametro_int_um,p))


# Variante svolta
rbind(unita_iniziale=metriche(osservato,previsto),
       unita_mille_volte_piu_piccola=metriche(1000*osservato,1000*previsto))


# M07_N20 - Probabilità, soglia e costo degli errori
# Trova la cartella del modulo, anche dal progetto generale del corso.
.gs_cerca <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
repeat {
  .gs_candidati <- c(.gs_cerca, file.path(.gs_cerca, "M07_Annula"))
  .gs_ok <- file.exists(file.path(.gs_candidati, "M07_N01.Rmd")) &
    file.exists(file.path(.gs_candidati, "R", "funzioni_notebook.R"))
  if (any(.gs_ok)) {
    .gs_modulo <- .gs_candidati[which(.gs_ok)[1L]]
    break
  }
  .gs_padre <- dirname(.gs_cerca)
  if (.gs_padre == .gs_cerca) {
    stop("Aprire il progetto M07_Annula o quello generale dei notebook.")
  }
  .gs_cerca <- .gs_padre
}
# Usa sempre le funzioni di questo modulo e i suoi dati.
source(file.path(.gs_modulo, "R", "funzioni_notebook.R"), local=TRUE)
.gs_funzioni <- .gs_prepara_notebook(.gs_modulo, "M07_N20")
carica_dati <- .gs_funzioni$carica_dati
percorso_dati <- .gs_funzioni$percorso_dati
percorso_risultati <- .gs_funzioni$percorso_risultati
options(width=88, digits=6)
# Il seme consente di ripetere le estrazioni casuali di questo notebook.
set.seed(7020)


# Stessa classe, probabilità differenti
p <- c(.51,.99)
data.frame(probabilita=p,classe=as.integer(p>=.5),
 perdita_se_evento1=(p-1)^2,perdita_se_evento0=p^2)


# Una soglia definita dai costi
C_FP <- 1
C_FN <- 3
soglia <- C_FP/(C_FP+C_FN)
griglia <- seq(0,1,length.out=101)
plot(griglia,C_FP*(1-griglia),type="l",lwd=2,col="#C57E42",
 ylim=c(0,3),xlab="Probabilita' dell'evento",ylab="Costo atteso")
lines(griglia,C_FN*griglia,col="#087C74",lwd=2)
abline(v=soglia,lty=2)
legend("topleft",c("Decisione 1","Decisione 0"),
 col=c("#C57E42","#087C74"),lwd=2,bty="n")
soglia


# Applicazione con regole già fissate
# Ogni riga identifica un fossile simulato.
f <- carica_dati("fossili_simulati.csv")
f$morfotipo <- factor(f$morfotipo, levels=c("Rounded", "Spiky"))
x <- f$diametro_tot_um
y <- f$diametro_int_um
stopifnot(nrow(f)==160L, !anyDuplicated(f$id),
          all(is.finite(x)), all(is.finite(y)))
# Partizione fissata prima del confronto dei modelli.
# Nel CSV didattico ogni quinto individuo forma il test.
is_test <- seq_len(nrow(f)) %% 5L == 0L
train <- f[!is_test, ]
test <- f[is_test, ]
stopifnot(nrow(train)==128L, nrow(test)==32L,
          length(intersect(train$id, test$id))==0L)
# Spiky=1 e Rounded=0: la probabilita' riguarda Spiky.
train$spiky <- as.integer(train$morfotipo=="Spiky")
test$spiky <- as.integer(test$morfotipo=="Spiky")
logit <- glm(spiky ~ diametro_tot_um + rapporto_int_tot,
             data=train, family=binomial())
stopifnot(logit$converged)
prob <- as.numeric(predict(logit, newdata=test, type="response"))
stopifnot(all(is.finite(prob)), all(prob>=0 & prob<=1))
valuta_soglia <- function(t) {
 cl <- as.integer(prob>=t)
 FP <- sum(cl==1 & test$spiky==0)
 FN <- sum(cl==0 & test$spiky==1)
 data.frame(soglia=t,FP=FP,FN=FN,
 accuratezza=mean(cl==test$spiky),costo_medio=(C_FP*FP+C_FN*FN)/nrow(test))
}
rbind(valuta_soglia(.5),valuta_soglia(soglia))
c(Brier=mean((prob-test$spiky)^2))


# Variante svolta
C_FP_nuovo <- 4
C_FN_nuovo <- 3
C_FP_nuovo/(C_FP_nuovo+C_FN_nuovo)
