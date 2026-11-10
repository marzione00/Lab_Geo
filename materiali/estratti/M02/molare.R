frazione_Mg <- function(MgO,FeO) {
 stopifnot(length(MgO)==length(FeO))
 stopifnot(all(is.finite(MgO)),all(is.finite(FeO)))
 stopifnot(all(MgO>=0),all(FeO>=0))
 a <- MgO/40.304; b <- FeO/71.844
 stopifnot(all(a+b>0))
 a/(a+b)
}
stopifnot(frazione_Mg(40.304,71.844)==0.5)
