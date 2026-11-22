stl_T <- stl(z, s.window = "periodic",
             robust = TRUE)
componenti_T <- stl_T$time.series
err_stl <- max(abs(rowSums(componenti_T) -
                   as.numeric(z)))
stopifnot(err_stl < 1e-10)
plot(stl_T)
