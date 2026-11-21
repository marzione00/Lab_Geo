xy_tr <- d[tr,c("x_m","y_m")];xy_te <- d[te,c("x_m","y_m")]
pred_idw <- idw_pred(xy_tr,d$concentrazione[tr],xy_te,p=2)
pred_media <- rep(mean(d$concentrazione[tr]),sum(te))
dist_te <- distanze_incrociate(xy_te,xy_tr)
vicino <- apply(dist_te,1,which.min)
pred_vicino <- d$concentrazione[tr][vicino]
previsioni <- data.frame(id=d$id[te],x_m=d$x_m[te],y_m=d$y_m[te],
  IDW_p2=pred_idw,Media_train=pred_media,Vicino=pred_vicino)
head(previsioni,6)
stopifnot(all(is.finite(as.matrix(previsioni[,4:6]))))
