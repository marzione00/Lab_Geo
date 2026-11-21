nord_sud <- terra::as.matrix(r,wide=TRUE)
data.frame(scarto_errato_m=max(abs(nord_sud-Z)),
  scarto_corretto_m=max(abs(nord_sud[24:1,]-Z)),
  media_invariata=abs(mean(nord_sud)-mean(Z))<1e-10)
stopifnot(max(abs(nord_sud-Z))>0)
