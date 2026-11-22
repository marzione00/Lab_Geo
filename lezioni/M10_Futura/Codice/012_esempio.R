p_media <- rep(mean(train), 36)
head(p_media)
stopifnot(length(unique(p_media))==1)
