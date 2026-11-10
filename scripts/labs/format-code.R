suppressPackageStartupMessages(library(jsonlite))
x<-fromJSON('content/experiments.json',simplifyVector=FALSE);common<-paste(readLines('R/lab-common.R',warn=FALSE),collapse='\n')
for(i in seq_along(x$activities)){
 a<-x$activities[[i]];expr<-parse(text=a$code);code<-paste(vapply(expr,function(e)paste(deparse(e,width.cutoff=88L),collapse='\n'),character(1)),collapse='\n\n');a$code<-code;x$activities[[i]]<-a
 p<-setNames(lapply(a$controls,function(c)c$value),sapply(a$controls,function(c)c$key));param<-paste(deparse(p,width.cutoff=85L),collapse='\n');script<-paste0('# GeoStat Lab · ',a$title,'\n# ',a$goal,'\n# Dati sintetici; parametri e ambiente dichiarati.\n# Dipendenze: install.packages(c("ggplot2", "jsonlite", "svglite"))\n\n',common,'\n\np <- ',param,'\nset.seed(p$seed)\n\n',code,'\n\nprint(metrics, row.names = FALSE)\nif (!interactive()) grDevices::cairo_pdf("figure_esperimento.pdf", width=9, height=5.5)\nfor (g in plots) print(g)\nif (!interactive()) grDevices::dev.off()\n# write.csv(data, "dati_esperimento.csv", row.names = FALSE)\n# ggsave("figura.svg", plots[[1]], width = 9, height = 5.5)\n');writeLines(script,a$source,useBytes=TRUE)
}
write_json(x,'content/experiments.json',auto_unbox=TRUE,pretty=TRUE,na='null',digits=12);write_json(x$activities,'content/experiments-draft.json',auto_unbox=TRUE,pretty=TRUE,na='null',digits=12)
cat(length(x$activities),'programmi R formattati\n')
