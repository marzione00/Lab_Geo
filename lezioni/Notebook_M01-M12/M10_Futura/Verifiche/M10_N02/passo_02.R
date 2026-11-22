deriva <- (as.numeric(tail(train,1))-as.numeric(head(train,1)))/(length(train)-1)
pred_deriva <- as.numeric(tail(train,1))+seq_len(h)*deriva
data.frame(ppm_per_mese=deriva,ppm_per_anno=12*deriva)
tail(data.frame(h=1:h,previsto=pred_deriva),3)
