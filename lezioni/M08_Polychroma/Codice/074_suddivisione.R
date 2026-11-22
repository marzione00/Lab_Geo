# Una suddivisione di un gruppo.
g74a <- rep(1, nrow(u59))
g74b <- rep(1:2, each=3)
w74 <- function(lab) {
 cent <- rowsum(u59,lab) /
   as.vector(table(lab))
 sum((u59-cent[lab,,drop=FALSE])^2)
}
c(un_gruppo=w74(g74a),
  due_gruppi=w74(g74b))
