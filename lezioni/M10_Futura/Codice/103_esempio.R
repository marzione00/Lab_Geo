fossilifit <- lm(
  diametro_int_um~diametro_tot_um,
  data=fossilitrain)
p_fos <- predict(fossilifit,
                 newdata=fossilitest)
