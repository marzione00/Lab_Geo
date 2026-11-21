# Formula esplicita e denominatore
bayes17 <- function(prior, pa, pb) {
  pA <- pa*prior + pb*(1-prior)
  if (pA == 0) return(NA_real_)
  pa*prior/pA
}
bayes17(.4, .8, .2)
bayes17(.4, 0, 0)  # condizione nulla
