h_dx <- hist(x_h, breaks = b_h,
             right = TRUE,
             plot = FALSE)
h_sx <- hist(x_h, breaks = b_h,
             right = FALSE,
             plot = FALSE)
rbind(destra = h_dx$counts,
      sinistra = h_sx$counts)
