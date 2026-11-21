tab_lab <- data.frame(id = 1:8,
  lunghezza = c(1.1,1.3,1.2,1.5,
                1.4,1.1,1.6,1.2))
# Due modifiche come nel laboratorio
tab_lab$id[8] <- 7
tab_lab$lunghezza[8] <- 1200
c(righe = nrow(tab_lab),
  chiavi = length(unique(tab_lab$id)),
  duplicati =
    sum(duplicated(tab_lab$id)),
  fuori = sum(tab_lab$lunghezza > 10))
