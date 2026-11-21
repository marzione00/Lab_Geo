# Verifica dei notebook M11

## Esecuzione e coerenza

I 20 notebook sono stati eseguiti nel runtime R 4.6.0 / WebR 0.6.1 dopo gli ultimi ritocchi editoriali e grafici. Il registro conserva 100 blocchi, zero errori non gestiti e zero avvisi. Le 20 figure derivano da dispositivi PDF aperti durante queste esecuzioni. Gli HTML sono generati dai medesimi blocchi, output e sorgenti Rmd; i relativi SHA-256 sono in `VERIFICA_NOTEBOOK.csv`.

N05, N06 e N20 utilizzano sf reale. N06 contiene un errore intenzionale e catturato: trasformare un oggetto senza CRS. N20 scrive e rilegge GeoJSON RFC7946 con dieci cifre decimali delle coordinate; controlla 64 geometrie POINT, ID, coordinate e attributi, allineandosi per ID. La precisione di serializzazione non è accuratezza di rilievo.

## Figure e impaginazione

Sono stati ispezionati tutti i 20 grafici nel montaggio `grafici_montaggio.jpg`. Tre difetti sono stati corretti nel codice R e verificati di nuovo a grandezza piena: etichette dei siti superiori in N01, margine sinistro e asse UTM in N05, etichetta della classe più distante in N15. Le immagini finali mantengono titoli, unità, assi e annotazioni visibili.

Le anteprime `index_layout.png`, `M11_N05_layout.png`, `M11_N13_layout.png` e `M11_N20_layout.png` mostrano il primo foglio di un rendering temporaneo con WeasyPrint 70, media screen e pagina 1400 × 1000 px. Sono stati controllati intestazioni, navigazione, stato di esecuzione e indice: non sono emersi ritagli o sovrapposizioni. Queste anteprime non equivalgono a un collaudo nel browser. WeasyPrint non convalida il rendering MathML; i PDF temporanei non sono distribuiti come notebook. Le formule sono incorporate come MathML negli HTML e non richiedono un servizio remoto.

## Collegamenti e provenienza

`Sorgenti_generazione/verifica_html.py` verifica le 22 pagine HTML, i riferimenti interni, l’assenza di risorse runtime esterne e le impronte dei sorgenti e degli HTML. Il raccordo alle slide usa il PDF del pacchetto completo, nel percorso `../../02_PDF/M11_Locus/Locus_M11_statistica_spaziale.pdf`. Se il PDF non è ancora presente, l’audit lo segnala senza sostituirlo con un file provvisorio. Dopo l’inclusione del PDF, rieseguire la verifica e `Sorgenti_generazione/riepilogo_qa.py`.

I 20 originali R e i 2 CSV coincidono byte per byte con i blob Git del commit dichiarato; sono verificati sia SHA-256 sia SHA-1 del blob Git. Il dettaglio finale è in `Verifiche/audit_provenienza_finale.json`.
