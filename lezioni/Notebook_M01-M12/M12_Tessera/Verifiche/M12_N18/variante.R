nord <- leggi_finestra(r,1,12,1,30)
sud <- leggi_finestra(r,13,12,1,30)
media_finestre <- weighted.mean(c(mean(nord),mean(sud)),c(length(nord),length(sud)))
data.frame(n_nord=length(nord),n_sud=length(sud),media_finestre=media_finestre,
  media_intera=mean(M),scarto=abs(media_finestre-mean(M)))
stopifnot(length(nord)+length(sud)==720L,abs(media_finestre-mean(M))<1e-10)
