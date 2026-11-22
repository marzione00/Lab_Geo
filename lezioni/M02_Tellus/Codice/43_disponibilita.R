due <- c("diametro_tot_um",
         "diametro_int_um")
tre <- c(due, "diaframma_um")
c(due_misure = sum(complete.cases(
    fossili[due])),
  tre_misure = sum(complete.cases(
    fossili[tre])))
