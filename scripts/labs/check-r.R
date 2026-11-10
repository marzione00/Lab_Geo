args<-commandArgs(TRUE);root<-normalizePath(args[1]);setwd(root);suppressPackageStartupMessages(library(jsonlite));source('R/lab-common.R')
acts<-fromJSON(args[2],simplifyVector=FALSE);results<-list();dir.create('qa',showWarnings=FALSE);dir.create('assets/experiments',showWarnings=FALSE)
for(a in acts){
 p0<-setNames(lapply(a$controls,function(c)c$value),sapply(a$controls,function(c)c$key));cases<-list(default=p0)
 if(length(args)>2&&args[3]=='edges')for(c in a$controls){if(c$key=='seed')next;vals<-if(c$type=='number')list(c$min,c$max)else lapply(c$options,function(x)x$value);for(j in seq_along(vals)){v<-p0;v[[c$key]]<-vals[[j]];cases[[paste(c$key,j,sep='_')]]<-v}}
 for(nm in names(cases)){
  e<-new.env(parent=globalenv());e$p<-cases[[nm]];set.seed(e$p$seed)
  ans<-tryCatch({eval(parse(text=a$code),e);stopifnot(is.data.frame(e$data),is.data.frame(e$metrics),length(e$plots)>0,all(vapply(e$plots,inherits,logical(1),'ggplot')));for(pl in e$plots)invisible(ggplot_build(pl));'ok'},error=function(err)conditionMessage(err))
  results[[length(results)+1]]<-list(activity=a$id,scenario=nm,result=ans)
  if(ans!='ok')cat('FAIL',a$id,nm,ans,'\n')
  if(nm=='default'&&ans=='ok'){
   meta<-list(metrics=e$metrics,data=head(e$data,80),rows=nrow(e$data),R=R.version.string,ggplot2=as.character(packageVersion('ggplot2')))
   write_json(meta,paste0('assets/experiments/',a$id,'.json'),auto_unbox=TRUE,pretty=FALSE,na='null',digits=10)
   for(j in seq_along(e$plots))ggsave(paste0('assets/experiments/',a$id,'-',j,'.svg'),e$plots[[j]],width=9,height=5.5,device=grDevices::svg,bg='#F5F6F3')
  }
 }
 cat(a$id,length(cases),'scenari\n')
}
write_json(results,'qa/experiments-r.json',auto_unbox=TRUE,pretty=TRUE);bad<-sum(vapply(results,function(x)x$result!='ok',logical(1)));cat('CHECKS',length(results),'FAILURES',bad,'\n');if(bad>0)quit(status=1)
