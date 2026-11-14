# Native R checks: observed datasets, parameter domains, ggplot builds and previews.
suppressPackageStartupMessages(library(jsonlite))
source('R/lab-common.R')
files <- list.files('content', '^research-.*[.]json$', full.names=TRUE)
stopifnot(length(files)==5)
results <- list(); locale_checks <- list()
for (file in files) {
  a <- fromJSON(file,simplifyVector=FALSE)
  path <- file.path('assets/research',a$id)
  observations <- read.csv(file.path(path,'data.csv'),stringsAsFactors=FALSE,check.names=FALSE)
  stopifnot(nrow(observations)>0,nrow(observations)<10000)
  p0 <- setNames(lapply(a$controls,function(c)c$value),vapply(a$controls,function(c)c$key,''))
  values <- lapply(a$controls,function(c) if(c$key=='seed') c(c$value,1,9999) else if(c$type=='select') vapply(c$options,function(o)o$value,'') else unique(c(c$value,c$min,c$max)))
  names(values) <- names(p0)
  grid <- expand.grid(values,stringsAsFactors=FALSE)
  cases <- c(list(default=p0),lapply(seq_len(nrow(grid)),function(i)as.list(grid[i,])))
  for (j in seq_along(cases)) {
    e <- new.env(parent=globalenv());e$p<-cases[[j]];e$observations<-observations
    set.seed(e$p$seed)
    eval(parse(text=a$code),envir=e)
    stopifnot(is.data.frame(e$data),is.data.frame(e$metrics),nrow(e$data)>0,length(e$plots)>0)
    for (plot in e$plots) invisible(ggplot_build(plot))
    results[[length(results)+1]] <- list(project=a$id,parameters=e$p,rows=nrow(e$data),plots=length(e$plots),status='passed')
    if(j==1){
      for(k in seq_along(e$plots)) ggsave(file.path(path,paste0('figure-',k,'.svg')),e$plots[[k]],width=9,height=5.5,device=grDevices::svg,bg='#F5F6F3')
      write_json(list(parameters=e$p,metrics=e$metrics,rows=nrow(e$data),R=R.version.string,ggplot2=as.character(packageVersion('ggplot2'))),file.path(path,'preview.json'),auto_unbox=TRUE,pretty=TRUE,na='null')
    }
  }
  cat(a$id, length(cases), 'scenarios passed\n')
  if(a$id=='exoplanet-mass-radius') {
    old_locale <- Sys.getlocale('LC_COLLATE'); reference <- NULL
    for(locale in c('C','C.UTF-8')) {
      actual <- Sys.setlocale('LC_COLLATE',locale)
      if(!nzchar(actual)) stop(paste('Locale unavailable for regression:',locale))
      e <- new.env(parent=globalenv());e$p<-p0;e$observations<-observations
      set.seed(p0$seed);eval(parse(text=a$code),envir=e)
      checked <- list(hosts=e$train_hosts,beta=unname(coef(e$fit)[2]),rmse=e$rmse)
      if(!is.null(reference))stopifnot(identical(reference,checked))
      reference <- checked
      locale_checks[[locale]] <- list(beta=checked$beta,rmse=checked$rmse,systems=length(checked$hosts),status='passed')
    }
    Sys.setlocale('LC_COLLATE',old_locale)
  }
}
write_json(list(status='passed',R=R.version.string,ggplot2=as.character(packageVersion('ggplot2')),checks=results,localeChecks=locale_checks),'qa/research-r.json',auto_unbox=TRUE,pretty=TRUE)
