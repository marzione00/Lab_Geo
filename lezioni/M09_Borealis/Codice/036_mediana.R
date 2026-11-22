v_es <- c(0, .2, -.1, .1, 6, -.1, .2, 0, .1)
med_es <- runmed(v_es, k = 3, endrule = "keep")
avg_es <- stats::filter(v_es, rep(1/3, 3))
cbind(v_es, med_es, avg_es)
# Una finestra di tre valori.
