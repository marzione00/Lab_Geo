pop <- c(2,4,6,8,10); nc <- 2L
combinazioni <- combn(pop,nc)
medie_srs <- colMeans(combinazioni)
var_design <- mean((medie_srs-mean(pop))^2)
var_fpc <- (1-nc/length(pop))*var(pop)/nc
