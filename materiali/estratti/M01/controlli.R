densita <- function(massa,volume) {
 stopifnot(length(massa)==length(volume))
 stopifnot(all(is.finite(massa)),
           all(is.finite(volume)))
 stopifnot(all(massa>0), all(volume>0))
 massa / volume
}
stopifnot(densita(107.2,40)==2.68)
