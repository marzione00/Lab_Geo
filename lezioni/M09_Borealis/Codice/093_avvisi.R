w93 <- character()
a93 <- withCallingHandlers(
  tseries::adf.test(as.numeric(y), k = 4),
  warning = function(w) {
    w93 <<- c(w93, conditionMessage(w))
  })
# Gli avvisi sono registrati e restano visibili.
list(test = a93, avvisi = w93)
