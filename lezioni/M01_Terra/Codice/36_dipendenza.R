# Serie didattica a intervalli uguali
x <- c(1, 2, 3, 4, 4, 3,
       2, 1, 1, 2, 3, 4)
# Correlazione per ritardi crescenti
acf(x, lag.max = 5,
    main = "Serie didattica")
