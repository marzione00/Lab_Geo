col_finali <- c("id", "morfotipo",
  "diametro_tot_um",
  "diametro_int_um",
  "spessore_um", "rapporto_int_tot")
analitica <- geometria[col_finali]
rownames(analitica) <- NULL
stopifnot(nrow(analitica) == 21,
          !anyNA(analitica))
head(analitica)
