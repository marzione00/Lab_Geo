frazione_mg <- function(mgo,feo) {
  stopifnot(length(mgo)==length(feo),
    all(is.finite(mgo)), all(mgo>=0),
    all(is.finite(feo)), all(feo>=0))
  a <- mgo/40.304; b <- feo/71.844
  stopifnot(all(a+b>0))
  a/(a+b)
}
stopifnot(
  frazione_mg(40.304,71.844)==0.5)
