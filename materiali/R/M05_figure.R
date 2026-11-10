# Calcoli, figure e verifiche del modulo nel medesimo ambiente locale.
local({
 vecchie_opzioni <- options()
 on.exit(options(vecchie_opzioni))
 source('R/M05/calcoli.R',local=TRUE)
 source('R/M05/figure.R',local=TRUE)
 source('R/M05/verifica.R',local=TRUE)
 source('R/M05/verifica_diagrammi.R',local=TRUE)
 writeLines(capture.output(sessionInfo()),'verifiche/M05/sessionInfo_R.txt')
})
