# Laboratorio applicativo — Differenze a mano
# Laboratorio R autonomo; eseguire dalla radice del progetto.

# Questo blocco prepara soltanto percorsi, funzioni di servizio e riproducibilità.
# Non scarica dati, non installa pacchetti, non elimina oggetti e non modifica i CSV.
trova_radice <- function() {
  p <- normalizePath(getwd(), winslash = "/", mustWork = TRUE)
  repeat {
    if (file.exists(file.path(p, "Notebook_R_Geologia.Rproj"))) return(p)
    genitore <- dirname(p)
    if (identical(p, genitore)) stop("Aprire Notebook_R_Geologia.Rproj e riprovare.")
    p <- genitore
  }
}
root <- trova_radice()
source(file.path(root, "R", "funzioni_comuni.R"), local = TRUE)
ctx <- inizia_notebook("M06_N20")
set.seed(1012)
options(width = 100, digits = 5)
if (requireNamespace("knitr", quietly = TRUE)) {
  knitr::opts_chunk$set(echo = TRUE, error = FALSE, warning = TRUE, message = TRUE,
                       fig.width = 8, fig.height = 5, dpi = 120, fig.align = "center")
}


# Preparazione: La coppia è parte del dato
a <- leggi_dati("misure_appaiate_simulate.csv")
richiedi_colonne(a,c("id","prima","dopo"))
stopifnot(nrow(a)==24L,anyDuplicated(a$id)==0L)
stopifnot(all(complete.cases(a[c("prima","dopo")])) )
a$differenza <- a$dopo-a$prima
head(a)
c(media_prima=mean(a$prima),media_dopo=mean(a$dopo),
  media_differenze=mean(a$differenza))


# Preparazione: Mostrare le coppie con segmenti
stile_grafico()
matplot(c(1,2),t(as.matrix(a[c("prima","dopo")])),type="b",
        pch=19,lty=1,col=adjustcolor(palette_geo[1],alpha.f=.55),xaxt="n",
        xlab="Condizione",ylab="Misura (unità convenzionali)",
        main="Stessi 24 ID prima e dopo")
axis(1,at=1:2,labels=c("Prima","Dopo"))
sum(a$differenza>0)
sum(a$differenza<0)


# Preparazione: Il test appaiato è un test sulle differenze
ta <- t.test(a$dopo,a$prima,paired=TRUE)
td <- t.test(a$differenza,mu=0)
stopifnot(abs(ta$p.value-td$p.value)<1e-12)
ris_appaiato <- data.frame(effetto=mean(a$differenza),
                           basso95=ta$conf.int[1],alto95=ta$conf.int[2],
                           p_value=ta$p.value)
ris_appaiato
stile_grafico()
qqnorm(a$differenza,main="Q-Q delle differenze appaiate")
qqline(a$differenza,col=palette_geo[2],lwd=2)


# Preparazione: Ignorare le coppie cambia l’incertezza
ti <- t.test(a$dopo,a$prima,paired=FALSE)
confronto_disegno <- data.frame(
  metodo=c("Appaiato: coerente con il file","Indipendenti: confronto improprio qui"),
  p=c(ta$p.value,ti$p.value),
  ampiezza_IC=c(diff(ta$conf.int),diff(ti$conf.int)))
confronto_disegno
cor(a$prima,a$dopo)


# Preparazione: Ranghi indipendenti: quale ipotesi?
f <- leggi_dati("fossili_simulati.csv")
x <- f$diametro_tot_um[f$morfotipo=="Spiky"]
y <- f$diametro_tot_um[f$morfotipo=="Rounded"]
wr <- wilcox.test(x,y,paired=FALSE,exact=FALSE)
wr
# Stima descrittiva della probabilità di superiorità, includendo metà dei pareggi.
confronti <- outer(x,y,"-")
prob_superiorita <- mean(confronti>0)+.5*mean(confronti==0)
prob_superiorita


# Preparazione: Ranghi appaiati: non basta cambiare un argomento
ws <- wilcox.test(a$dopo,a$prima,paired=TRUE,exact=FALSE)
non_zero <- a$differenza[a$differenza!=0]
test_segni <- binom.test(sum(non_zero>0),length(non_zero),p=.5)
data.frame(test=c("Signed-rank appaiato","Segni: positivi tra non nulli"),
           p=c(ws$p.value,test_segni$p.value))
c(coppie=nrow(a),pareggi=sum(a$differenza==0),non_nulle=length(non_zero))


# Preparazione: Categorie: osservato e atteso in una tabella
tab <- matrix(c(18,12,9,21),nrow=2,byrow=TRUE,
              dimnames=list(gruppo=c("A","B"),presenza=c("Si","No")))
chi <- chisq.test(tab,correct=FALSE)
fisher <- fisher.test(tab)
tab
chi$expected
data.frame(test=c("Chi-quadrato senza correzione","Fisher"),
           p=c(chi$p.value,fisher$p.value))
# Associazione descrittiva: differenza delle proporzioni.
prop_A <- tab["A","Si"]/sum(tab["A",])
prop_B <- tab["B","Si"]/sum(tab["B",])
prop_A-prop_B


# Preparazione: Più gruppi: ANOVA come confronto globale
r <- leggi_dati("rocce_simulate.csv")
r$litologia_generatrice <- factor(r$litologia_generatrice)
modello <- aov(densita ~ litologia_generatrice,data=r)
summary(modello)
aggregate(densita ~ litologia_generatrice,r,mean)
# Confronto globale di Welch: non impone varianze uguali.
oneway.test(densita ~ litologia_generatrice,data=r,var.equal=FALSE)


# Preparazione: Confronti multipli: la famiglia di domande
p_grezzi <- c(.01,.03,.04,.20)
molteplicita <- data.frame(confronto=1:4,p_grezzo=p_grezzi,
                           p_Holm=p.adjust(p_grezzi,method="holm"))
molteplicita
# Esempio di tre confronti pianificati tra litologie; varianze non pooled.
pairwise.t.test(r$densita,r$litologia_generatrice,
                p.adjust.method="holm",pool.sd=FALSE)
# Probabilità teorica di almeno un falso positivo in 20 test indipendenti.
1-(1-.05)^20


# Preparazione: Una tabella di decisione ragionata
salva_tabella(ris_appaiato,"test_appaiato.csv",ctx$out)
salva_tabella(confronto_disegno,"effetto_del_disegno.csv",ctx$out)
salva_tabella(molteplicita,"correzione_Holm.csv",ctx$out)
salva_tabella(as.data.frame(as.table(tab)),"conteggi_2x2.csv",ctx$out)
salva_testo(c("Le misure prima/dopo sono appaiate per ID.",
              "Il rank-sum non è genericamente un test delle mediane.",
              "Il signed-rank richiede attenzione alla simmetria delle differenze.",
              "ANOVA e confronti multipli sono approfondimenti guidati."),
            "note_metodologiche.txt",ctx$out)


# Analisi principale: Laboratorio applicativo — Differenze a mano
a <- leggi_dati("misure_appaiate_simulate.csv")
c(differenze=mean(a$dopo-a$prima),differenza_medie=mean(a$dopo)-mean(a$prima))
