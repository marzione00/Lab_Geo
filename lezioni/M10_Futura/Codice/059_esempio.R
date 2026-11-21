res <- as.numeric(residuals(fit))
res <- res[14:length(res)]
stopifnot(length(res)==155,
          all(is.finite(res)))
