v79 <- split(provini$densita,
              provini$stazione)
# Sei indici illustrativi
j79 <- c(2, 2, 6, 4, 1, 3)
mean(unlist(v79[j79]))
mean(sapply(v79[j79], mean))
# Identici: 4 provini per stazione
