# POLYCHROMA M08 - Rigenerazione dei risultati delle lezioni.
# Eseguire con source("R/rigenera_calcoli.R") dal progetto del modulo,
# oppure con Rscript indicando il percorso completo di questo file.
# Usa solo R base: non installa pacchetti e non scarica dati.
.trova_modulo <- function() {
  sorgenti <- unlist(lapply(sys.frames(),function(e) {
    x <- e$ofile; if(is.null(x)) character() else as.character(x)
  }),use.names=FALSE)
  arg <- grep("^--file=",commandArgs(FALSE),value=TRUE)
  if(length(arg)) sorgenti <- c(sorgenti,sub("^--file=","",arg))
  basi <- c(getwd(),dirname(normalizePath(sorgenti,mustWork=FALSE)))
  candidati <- character()
  for(b in basi) for(j in 0:5) {
    candidati <- c(candidati,b,file.path(b,"Polychroma_M08"),file.path(b,"M08_Polychroma"))
    b <- dirname(b)
  }
  for(p in unique(candidati)) if(file.exists(file.path(p,"Dati","rocce_simulate.csv")) &&
      file.exists(file.path(p,"R","funzioni_analisi.R"))) return(normalizePath(p))
  stop("Cartella del modulo non trovata: conservare insieme R, Dati e Calcoli.")
}
modulo <- .trova_modulo()
source(file.path(modulo,"R","funzioni_analisi.R"),local=TRUE)
ari <- indice_rand_corretto
out <- file.path(modulo,"Calcoli")
dir.create(out,recursive=TRUE,showWarnings=FALSE)
r <- read.csv(file.path(modulo,"Dati","rocce_simulate.csv"))
f <- read.csv(file.path(modulo,"Dati","fossili_simulati.csv"))
v <- c("SiO2","CaO","MgO","FeO","densita","grana_mm","colore","fossili")
X <- as.matrix(r[v]); Z <- scale(X)
stopifnot(nrow(X)==90,ncol(X)==8,all(is.finite(X)),!anyDuplicated(r$id))
pc <- prcomp(X,center=TRUE,scale.=TRUE)
equiv <- prcomp(Z,center=FALSE,scale.=FALSE)
lambda <- pc$sdev^2; quota <- lambda/sum(lambda)
salva <- function(x,nome) write.csv(x,file.path(out,paste0(nome,".csv")),row.names=FALSE)
salva(data.frame(id=r$id,pc$x),"pca_scores")
salva(data.frame(variabile=v,pc$rotation),"pca_rotation")
salva(data.frame(variabile=v,cor(Z,pc$x)),"pca_correlations")
salva(data.frame(PC=1:8,lambda=lambda,quota=quota,cumulata=cumsum(quota)),"variance")
salva(data.frame(variabile=v,media=colMeans(X),sd=apply(X,2,sd)),"scaling")
salva(data.frame(id=r$id,Z),"standardized")
salva(data.frame(variabile=v,cor(Z),check.names=FALSE),"correlations")
D <- dist(Z)
set.seed(816);km <- kmeans(Z,3,nstart=50,iter.max=100)
h <- hclust(D,method="ward.D2");ward <- cutree(h,3)
sil <- silhouette_base(km$cluster,D)
d2 <- rowSums((Z-km$centers[km$cluster,,drop=FALSE])^2)
salva(data.frame(id=r$id,kmeans=km$cluster,ward=ward,silhouette=sil,distanza2=d2),"assignments")
salva(aggregate(r[v],list(cluster=km$cluster),mean),"profiles_original")
salva(aggregate(as.data.frame(Z),list(cluster=km$cluster),mean),"profiles_z")
salva(as.data.frame(table(cluster=km$cluster,generatore=r$litologia_generatrice)),"cluster_generator_table")
salva(as.data.frame(table(kmeans=km$cluster,ward=ward)),"kmeans_ward_table")
set.seed(817); ks <- 2:7
fits <- lapply(ks,function(k)kmeans(Z,k,nstart=50,iter.max=100))
indici <- data.frame(k=ks,WSS=vapply(fits,function(m)m$tot.withinss,numeric(1)),
 silhouette=vapply(fits,function(m)mean(silhouette_base(m$cluster,D)),numeric(1)))
salva(indici,"cluster_choices")
gruppi <- vector("list",nrow(h$merge));delta <- numeric(length(gruppi))
for(i in seq_along(gruppi)) {
 ab <- lapply(h$merge[i,],function(j)if(j<0)-j else gruppi[[j]])
 A <- ab[[1]];B <- ab[[2]]
 delta[i] <- length(A)*length(B)/(length(A)+length(B))*sum((colMeans(Z[A,,drop=FALSE])-colMeans(Z[B,,drop=FALSE]))^2)
 gruppi[[i]] <- c(A,B)
}
salva(data.frame(step=seq_along(delta),left=h$merge[,1],right=h$merge[,2],height=h$height,deltaW=delta),"ward_merges")
salva(data.frame(position=1:90,row=h$order,id=r$id[h$order]),"ward_order")
rec <- pc$x[,1:2,drop=FALSE]%*%t(pc$rotation[,1:2,drop=FALSE])
Xrec <- sweep(sweep(rec,2,pc$scale,"*"),2,pc$center,"+")
salva(data.frame(id=r$id,rec),"reconstruction_Z2")
salva(data.frame(id=r$id,Xrec),"reconstruction_X2")
set.seed(818)
st <- t(replicate(30,{
 m <- kmeans(Z,3,nstart=1,iter.max=100)
 c(WSS=m$tot.withinss,accordo=accordo_coppie(km$cluster,m$cluster),ARI=ari(km$cluster,m$cluster))
}))
salva(data.frame(ripetizione=1:30,st),"stability")
set.seed(819);ampiezze <- c(0,.05,.1,.2,.4,.8)
pert <- do.call(rbind,lapply(ampiezze,function(sd)do.call(rbind,lapply(1:20,function(b) {
 ZZ <- Z+matrix(rnorm(length(Z),sd=sd),nrow(Z))
 m <- kmeans(ZZ,3,nstart=50,iter.max=100)
 data.frame(sd=sd,ripetizione=b,accordo=accordo_coppie(km$cluster,m$cluster),ARI=ari(km$cluster,m$cluster))
}))))
salva(pert,"perturbations")
salva(aggregate(cbind(accordo,ARI)~sd,pert,mean),"perturbations_mean")
set.seed(820);sottocampioni <- replicate(40,{
 idx <- sort(sample(1:90,72,replace=FALSE))
 m <- kmeans(Z[idx,,drop=FALSE],3,nstart=30,iter.max=100)
 out <- rep(NA_integer_,90);out[idx] <- m$cluster;out
})
co <- matrix(NA_real_,90,90);presenze <- matrix(0L,90,90)
for(i in 1:90)for(j in 1:90){ok <- !is.na(sottocampioni[i,])&!is.na(sottocampioni[j,]);presenze[i,j]<-sum(ok);if(any(ok))co[i,j]<-mean(sottocampioni[i,ok]==sottocampioni[j,ok])}
salva(data.frame(id=r$id,co),"co_membership")
salva(data.frame(id=r$id,presenze),"co_presence")
parti <- c("SiO2","CaO","MgO","FeO","resto_wt")
comp <- as.matrix(r[parti]);stopifnot(all(comp>0))
clr <- log(comp)-rowMeans(log(comp));pc_clr <- prcomp(clr,scale.=FALSE)
salva(data.frame(variabile=parti,pc_clr$rotation),"clr_rotation")
salva(data.frame(id=r$id,clr),"clr_data")
salva(data.frame(PC=1:5,lambda=pc_clr$sdev^2,quota=pc_clr$sdev^2/sum(pc_clr$sdev^2)),"clr_variance")
M <- as.matrix(f[c("diametro_tot_um","diametro_int_um","spessore_um")]);pc_f <- prcomp(M,scale.=TRUE)
set.seed(819);chimica <- kmeans(scale(r[c("SiO2","CaO","MgO","FeO")]),3,nstart=50)
set.seed(1601);km4 <- kmeans(Z,4,nstart=50)
salva(aggregate(r[v],list(cluster=km4$cluster),mean),"profiles_k4")
salva(data.frame(id=r$id,cluster=km4$cluster),"assignments_k4")
val <- c(n=nrow(X),p=ncol(X),variancefirst2=sum(quota[1:2]),
 reconstructionq2fraction=sum((Z-rec)^2)/sum(Z^2),reconstructionq2SSE=sum((Z-rec)^2),
 reconstructionq2RMSE=sqrt(mean((Z-rec)^2)),
 Wardidentitymaxerr=max(abs(h$height^2/2-delta)),
 eigenvalues_svd_maxerr=max(abs(lambda-svd(Z)$d^2/89)),
 orthogonality_maxerr=max(abs(crossprod(pc$rotation)-diag(8))),
 scores_identity_maxerr=max(abs(pc$x-Z%*%pc$rotation)),
 covariance_identity_maxerr=max(abs(cov(pc$x)-diag(lambda))),
 equivalent_sd_maxerr=max(abs(pc$sdev-equiv$sdev)),
 equivalent_scores_maxerr=max(abs(pc$x-equiv$x)),
 WSS_k3=km$tot.withinss,TSS=km$totss,silhouette_k3=mean(sil),
 silhouette_min=min(sil),silhouette_max=max(sil),
 WSS_manual_maxerr=abs(sum(d2)-km$tot.withinss),
 n_cluster1=sum(km$cluster==1),n_cluster2=sum(km$cluster==2),n_cluster3=sum(km$cluster==3),
 k_best_silhouette=indici$k[which.max(indici$silhouette)],
 kmeans_ward_agreement=accordo_coppie(km$cluster,ward),
 kmeans_ward_ARI=ari(km$cluster,ward),
 kmeans_generator_ARI=ari(km$cluster,r$litologia_generatrice),
 chemistry_agreement=accordo_coppie(km$cluster,chimica$cluster),
 chemistry_ARI=ari(km$cluster,chimica$cluster),
 closure_maxerr=max(abs(rowSums(comp)-100)),clr_rowsum_maxerr=max(abs(rowSums(clr))),
 clr_last_sd=tail(pc_clr$sdev,1),
 fossil_relation_maxerr=max(abs(M[,1]-M[,2]-2*M[,3])),fossil_third_sd=pc_f$sdev[3],
 stability_min=min(st[,"accordo"]),stability_mean=mean(st[,"accordo"]))
salva(data.frame(nome=names(val),valore=unname(val)),"valori")
writeLines(R.version.string,file.path(out,"ambiente.txt"))
stopifnot(max(abs(pc$x-Z%*%pc$rotation))<1e-10,max(abs(h$height^2/2-delta))<1e-9,
 abs(sum((Z-rec)^2)-(89*sum(lambda[-(1:2)])))<1e-9,
 max(abs(cor(Z,pc$x)-sweep(pc$rotation,2,pc$sdev,"*")))<1e-10)
print(val);print(indici)

# JSON scritto con R base: nomi e valori numerici verificabili anche fuori da R.
json <- c("{",paste0('  "',names(val),'": ',sprintf("%.17g",unname(val)),
                  c(rep(",",length(val)-1),"")),"}")
writeLines(json,file.path(out,"metrics.json"))
