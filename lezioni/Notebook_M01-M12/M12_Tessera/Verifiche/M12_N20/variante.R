sbagliata <- terra::as.matrix(letto,wide=TRUE)
data.frame(scarto_senza_ribaltamento=max(abs(sbagliata-s)),
  media_invariata=abs(mean(sbagliata)-mean(s))<1e-10,
  scarto_corretto=max(abs(sbagliata[nrow(sbagliata):1,]-s)))
stopifnot(max(abs(sbagliata-s))>0)
