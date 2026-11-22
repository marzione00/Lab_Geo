opposte <- media_circolare(c(0,180))
opposte
stopifnot(is.na(opposte["media_gradi"]),opposte["risultante"]<1e-8)
