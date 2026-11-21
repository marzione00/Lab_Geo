
# Silhouette di ogni osservazione: a = distanza media entro gruppo;
# b = minima distanza media verso un altro gruppo. I singleton valgono 0.
silhouette_base <- function(lab, D) {
  lab <- as.integer(factor(lab))
  DD <- as.matrix(D)
  stopifnot(nrow(DD)==length(lab), ncol(DD)==length(lab),
            all(is.finite(DD)), length(unique(lab))>=2L)
  vapply(seq_along(lab), function(i) {
    stessi <- which(lab==lab[i] & seq_along(lab)!=i)
    if (!length(stessi)) return(0)
    a <- mean(DD[i, stessi])
    altri <- setdiff(unique(lab), lab[i])
    b <- min(vapply(altri, function(g) mean(DD[i, lab==g]), numeric(1)))
    if (max(a,b)==0) 0 else (b-a)/max(a,b)
  }, numeric(1))
}

# Accordo delle coappartenenze: include sia le coppie unite in entrambe
# le partizioni sia quelle separate in entrambe. Non corregge per il caso.
accordo_coppie <- function(a,b) {
  stopifnot(length(a)==length(b),length(a)>=2L,!anyNA(a),!anyNA(b))
  A <- outer(a,a,"==")
  B <- outer(b,b,"==")
  sopra <- upper.tri(A)
  mean(A[sopra]==B[sopra])
}

# Indice di Rand corretto: sottrae l'accordo atteso date le dimensioni
# dei gruppi. Puo assumere valori negativi; 1 identifica la stessa partizione.
indice_rand_corretto <- function(a,b) {
  stopifnot(length(a)==length(b),length(a)>=2L,!anyNA(a),!anyNA(b))
  tab <- table(a,b)
  scegli2 <- function(x) x*(x-1)/2
  osservato <- sum(scegli2(tab))
  riga <- sum(scegli2(rowSums(tab)))
  colonna <- sum(scegli2(colSums(tab)))
  atteso <- riga*colonna/scegli2(sum(tab))
  massimo <- (riga+colonna)/2
  if (abs(massimo-atteso)<1e-15) {
    return(as.numeric(accordo_coppie(a,b)==1))
  }
  (osservato-atteso)/(massimo-atteso)
}
