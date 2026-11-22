# Chiave della tabella dei siti
chiave <- siti$sito
stopifnot(!anyNA(chiave))
stopifnot(all(nzchar(trimws(chiave))))
stopifnot(!anyDuplicated(chiave))
# La ripetizione e' attesa nei provini
table(provini$sito)
