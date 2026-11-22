# Figure delle applicazioni: eseguire dalla cartella root_proof.
options(warn=2)
source("R/laboratori_gemina.R", encoding="UTF-8")
source("R/scenari_gemina.R", encoding="UTF-8")
dir.create("coordinate",showWarnings=FALSE)
for (s in scenari_gemina) {
  z <- do.call(get(paste0("lab_",s$id)),s$p)
  write.csv(z$data,
    paste0("coordinate/lab_",s$id,"_",s$scenario,".csv"),
    row.names=FALSE)
  if (s$id == "welch") {
    write.csv(data.frame(stima=z$metrics[1],
      lo=z$test$conf.int[1],hi=z$test$conf.int[2]),
      paste0("coordinate/lab_welch_ci_",s$scenario,".csv"),
      row.names=FALSE)
  }
  if (s$id == "anova") {
    a <- split(z$data$valore,z$data$gruppo)
    tab <- data.frame(gruppo=names(a),
      media=vapply(a,mean,numeric(1)),
      sd=vapply(a,sd,numeric(1)))
    write.csv(tab,
      paste0("coordinate/lab_anova_medie_",s$scenario,".csv"),
      row.names=FALSE)
  }
}
cat("Coordinate degli undici laboratori esportate.\n")
