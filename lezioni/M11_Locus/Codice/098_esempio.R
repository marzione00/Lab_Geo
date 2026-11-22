pred <- idw_pred(xy[train_idx,],
 z[train_idx],xy[test_idx,],p=2)
e <- z[test_idx]-pred
c(MAE=mean(abs(e)),
 RMSE=sqrt(mean(e^2)),bias=mean(e))
