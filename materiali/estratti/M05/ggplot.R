p <- ggplot(d,aes(stazione,densita,colour=affioramento))+
 geom_point(size=3,position=position_jitter(width=.12,height=0,seed=1))+
 geom_point(data=st,shape=18,size=5)+scale_colour_manual(values=col_geo)+
 scale_y_continuous(labels=fmt,breaks=c(2.5,2.6,2.7))+labs(x='Stazione',y='Densità (g/cm³)')
