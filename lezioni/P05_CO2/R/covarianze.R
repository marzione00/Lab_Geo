# Covarianze robuste: nessun prewhitening; convenzioni esplicitate nelle slide.
hac_cov <- function(X,resid,lag) {
 X<-as.matrix(X);n<-nrow(X);k<-ncol(X)
 stopifnot(length(resid)==n,lag>=0,lag<n,lag==as.integer(lag),qr(X)$rank==k)
 score<-X*as.numeric(resid);meat<-crossprod(score)
 if(lag>0) for(j in seq_len(lag)) {
  G<-crossprod(score[(j+1):n,,drop=FALSE],score[1:(n-j),,drop=FALSE])
  meat<-meat+(1-j/(lag+1))*(G+t(G))
 }
 bread<-solve(crossprod(X));(n/(n-k))*bread%*%meat%*%bread
}
hc3_cov <- function(X,resid) {
 X<-as.matrix(X);bread<-solve(crossprod(X));h<-rowSums((X%*%bread)*X)
 stopifnot(length(resid)==nrow(X),all(h<1))
 Z<-X*(as.numeric(resid)/(1-h));bread%*%crossprod(Z)%*%bread
}
intervallo <- function(beta,se,df=NULL) {
 q<-if(is.null(df)) qnorm(.975) else qt(.975,df)
 c(beta-q*se,beta+q*se)
}
