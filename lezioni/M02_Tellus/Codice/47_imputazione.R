x_imp <- x_na # 4, NA, 6
x_imp[is.na(x_imp)] <- media_oss
c(media = mean(x_imp),
  var_disponibili = var(x_na,
                        na.rm = TRUE),
  var_imputati = var(x_imp))
