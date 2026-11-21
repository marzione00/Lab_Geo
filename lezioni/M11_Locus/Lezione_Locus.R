# M11 Locus — avvio della sessione didattica.
source("R/stato_lezione.R",encoding="UTF-8")
cat("M11 Locus: 64 siti sintetici, coordinate locali in metri senza EPSG.\n")
print(c(I_A=I_A,I_W=I_W,legami=sum(A)/2))
print(metriche(test$concentrazione,pred_idw))
print(sf::sf_extSoftVersion())
# Rigenerazione completa:
# source("R/rigenera_calcoli.R",encoding="UTF-8")
