valida_campioni <- function(x) {
 stopifnot(is.data.frame(x),nrow(x)>0,
  all(c('id','stazione','massa_g','volume_cm3')%in%names(x)),
  !anyNA(x$id),!anyDuplicated(x$id),all(nzchar(as.character(x$id))),
  !anyNA(x$stazione),all(nzchar(as.character(x$stazione))),
  is.numeric(x$massa_g),is.numeric(x$volume_cm3),
  all(is.finite(x$massa_g)),all(is.finite(x$volume_cm3)),
  all(x$massa_g>0),all(x$volume_cm3>0))
 x
}
trasforma_campioni <- function(x) {
 x<-valida_campioni(x);x$densita<-x$massa_g/x$volume_cm3;x
}
sintesi_campioni <- function(x) {
 x<-trasforma_campioni(x);s<-aggregate(densita~stazione,x,mean)
 s<-s[order(s$stazione),];rownames(s)<-NULL;s
}
