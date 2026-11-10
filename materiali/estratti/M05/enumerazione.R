piccolo <- c(4,5,7,8)
# Tutte le 4^4 = 256 sequenze ordinate, equiprobabili con reinserimento.
indici_esatti <- as.matrix(expand.grid(rep(list(seq_len(4)),4)))
medie_esatte <- apply(indici_esatti,1,function(ii)mean(piccolo[ii]))
