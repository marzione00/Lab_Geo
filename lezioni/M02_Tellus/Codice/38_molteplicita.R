# Una seconda riga per il sito A
siti2 <- rbind(siti, siti[1, ])
siti2$quota[3] <- 12
j2 <- merge(provini, siti2,
            by = "sito")
nrow(j2)       # 5 righe
table(j2$sito) # A: 4; B: 1
