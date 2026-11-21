ii <- c(1,30,361,720)
data.frame(riga=d$riga[ii],colonna=d$colonna[ii],differenza=nir[ii]-rosso[ii],
  somma=nir[ii]+rosso[ii],indice=indice[ii])
stopifnot(max(abs(indice*(nir+rosso)-(nir-rosso)))<1e-12)
