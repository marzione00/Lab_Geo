# Convenzioni grafiche condivise, coerenti con il template delle slide.
suppressPackageStartupMessages(library(ggplot2))
geo <- c('#087C74','#5146A5','#A05B10','#9B4564','#326A9A','#657180')
paper <- '#F8F6F1'; ink <- '#253344'
fmt <- function(x) format(x,trim=TRUE,scientific=FALSE,decimal.mark=',')
tema <- theme_minimal(base_size=18,base_family='Nimbus Sans')+
 theme(plot.background=element_rect(fill=paper,colour=NA),
 panel.background=element_rect(fill=paper,colour=NA),
 panel.grid.minor=element_blank(),panel.grid.major=element_line(colour='#D6DAD9',linewidth=.25),
 axis.text=element_text(size=22,colour=ink),axis.title=element_text(size=19,colour=ink),
 legend.position='top',legend.text=element_text(size=17),legend.title=element_blank(),
 strip.text=element_text(size=18,face='bold'),plot.margin=margin(9,13,7,8))
theme_set(tema)
salva <- function(mod,id,p,w=5.2,h=3.8) {
 dest<-file.path('figure',mod);dir.create(dest,recursive=TRUE,showWarnings=FALSE)
 ggsave(file.path(dest,paste0(id,'.pdf')),p,width=w,height=h,device=cairo_pdf,bg=paper)
 ggsave(file.path(dest,paste0(id,'.png')),p,width=w,height=h,dpi=150,bg=paper)
}
leggi <- function(nome) read.csv(file.path('dati',nome),stringsAsFactors=FALSE)
verifica <- function(nome,condizione) {
 if(!isTRUE(condizione)) stop(nome)
 cat('OK:',nome,'\n')
}
