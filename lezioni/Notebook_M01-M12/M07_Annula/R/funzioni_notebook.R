# Funzioni minime per i notebook GeoStat Lab.
# Il chiamante ha gia individuato la radice del progetto e l'ID.
.gs_prepara_notebook <- function(radice, id) {
  .gs_dati <- file.path(radice,"Dati")
  .gs_uscita <- file.path(radice,"Risultati",id)
  dir.create(.gs_uscita,recursive=TRUE,showWarnings=FALSE)
  list(
    carica_dati=function(nome,...) {
      argomenti <- modifyList(list(file=file.path(.gs_dati,nome),
                          stringsAsFactors=FALSE,check.names=FALSE),list(...))
      do.call(read.csv,argomenti)
    },
    percorso_dati=function(nome) {
      normalizePath(file.path(.gs_dati,nome),winslash="/",mustWork=TRUE)
    },
    percorso_risultati=function(nome) {
      if (length(nome)!=1L || grepl("(^/|[.][.])",nome)) {
        stop("Usare un nome relativo nella cartella dei risultati.")
      }
      destinazione <- file.path(.gs_uscita,nome)
      dir.create(dirname(destinazione),recursive=TRUE,showWarnings=FALSE)
      destinazione
    }
  )
}


# Metriche della risposta continua: entrambe hanno l'unita' di y.
metriche <- function(osservato,previsto) {
  stopifnot(length(osservato)==length(previsto),length(osservato)>0,
            all(is.finite(osservato)),all(is.finite(previsto)))
  c(MAE=mean(abs(osservato-previsto)),
    RMSE=sqrt(mean((osservato-previsto)^2)))
}

# Procedura fissata nel notebook M07_N12.
# Questa funzione riceve soltanto il training: non accede al test.
seleziona_modello <- function(train,seme=714) {
  formule <- list(lineare=diametro_int_um~diametro_tot_um,
    con_morfotipo=diametro_int_um~diametro_tot_um+morfotipo,
    polinomio3=diametro_int_um~poly(diametro_tot_um,3))
  set.seed(seme)
  fold <- sample(rep(1:5,length.out=nrow(train)))
  cv <- do.call(rbind,lapply(names(formule),function(nome) {
    do.call(rbind,lapply(1:5,function(k) {
      tr <- train[fold!=k,]
      va <- train[fold==k,]
      m <- lm(formule[[nome]],data=tr)
      met <- metriche(va$diametro_int_um,predict(m,newdata=va))
      data.frame(modello=nome,fold=k,MAE=unname(met["MAE"]),
                 RMSE=unname(met["RMSE"]))
    }))
  }))
  media_cv <- aggregate(cbind(MAE,RMSE)~modello,cv,mean)
  list(nome=media_cv$modello[which.min(media_cv$RMSE)],
       formule=formule,riepilogo=media_cv,dettaglio=cv,fold=fold)
}
