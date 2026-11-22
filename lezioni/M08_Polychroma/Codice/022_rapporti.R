# Il totale si semplifica nel rapporto.
lr_prima <- log(assolute[, 1] /
                assolute[, 2])
lr_dopo <- log(frazioni[, 1] /
               frazioni[, 2])
max(abs(lr_prima - lr_dopo))
