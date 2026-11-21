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

# Conserva l'oggetto test e tutti gli avvisi: i limiti tabulati non sono errori.
cattura_test <- function(expr) {
  avvisi <- character()
  risultato <- withCallingHandlers(expr, warning=function(w) {
    avvisi <<- c(avvisi, conditionMessage(w))
    invokeRestart("muffleWarning")
  })
  list(test=risultato, avvisi=avvisi)
}

# Tabella compatta: p_stampato e' il valore restituito dalla funzione.
# Il segno mantiene la distinzione fra p approssimato e limite tabulato.
riga_test <- function(nome, test, esito) {
  a <- paste(esito$avvisi,collapse=" | ")
  relazione <- if (grepl("smaller than",a,fixed=TRUE)) "<" else
    if (grepl("greater than",a,fixed=TRUE)) ">" else "circa"
  t <- esito$test
  data.frame(serie=nome,test=test,statistica=unname(t$statistic),
    p_stampato=t$p.value,relazione_p=relazione,
    parametro=if(length(t$parameter)) unname(t$parameter) else NA_real_,
    avvisi=a,stringsAsFactors=FALSE)
}

# Tutti i test ricevono una serie finita. L'ADF di tseries include costante
# e trend lineare; k=4 aggiunge quattro differenze ritardate.
tabella_test <- function(nome, x, k=4L) {
  stopifnot(requireNamespace("tseries",quietly=TRUE),all(is.finite(x)))
  do.call(rbind,list(
    riga_test(nome,"ADF: costante+trend",cattura_test(tseries::adf.test(x,k=k))),
    riga_test(nome,"KPSS: Level",cattura_test(tseries::kpss.test(x,null="Level"))),
    riga_test(nome,"KPSS: Trend",cattura_test(tseries::kpss.test(x,null="Trend")))
  ))
}

# AR(1) in equilibrio con varianza unitaria, innovazioni indipendenti normali.
# La prima osservazione viene estratta dalla distribuzione stazionaria.
simula_ar1 <- function(n,phi=.7) {
  stopifnot(n>=2L,abs(phi)<1)
  x <- numeric(n);x[1] <- rnorm(1)
  for(i in 2:n) x[i] <- phi*x[i-1]+sqrt(1-phi^2)*rnorm(1)
  x
}
