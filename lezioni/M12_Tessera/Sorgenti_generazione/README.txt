GENERAZIONE DELLE SLIDE M12 — TESSERA

assembla.py produce il TeX, i frammenti R e gli indici da parte01.py–parte05.py.
componenti.py definisce layout, diagrammi TikZ, tabelle e richiami.
contenuti.py riunisce le parti e imposta le pagine panoramiche.
preambolo.tex conserva lo stile della collana (20 × 12,5 cm).

Il generatore non esegue né sostituisce i calcoli scientifici. Le 42 figure PDF
sono prodotte da R/genera_figure.R, richiamato da R/rigenera_calcoli.R.
I riferimenti numerici e le didascalie vanno aggiornati insieme ai risultati
quando si modifica il caso guida o una convenzione.

La cartella Codice contiene 39 esempi visibili nelle slide. Il file
Codice/esegui_frammenti.R li esegue nella stessa sessione, dopo la preparazione.
Le pagine panoramiche non nascondono codice escluso dalla rappresentazione.

Il preambolo registra le dimensioni effettive di titoli, richiami e colonne
come FULLBOX nel log. I controlli editoriali combinano queste misure con
l’ispezione visiva delle 110 pagine e la verifica di link, glifi e figure.
