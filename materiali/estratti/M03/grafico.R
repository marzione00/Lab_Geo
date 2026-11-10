source('R/stile.R')
d <- leggi('fossili_simulati.csv')
p <- ggplot(d,aes(diametro_tot_um,
 diaframma_um,colour=morfotipo))+
 geom_point(size=2,alpha=.75)+
 scale_colour_manual(values=geo[1:2])+
 labs(x='Diametro totale (µm)',
      y='Diaframma (µm)')
print(p)
