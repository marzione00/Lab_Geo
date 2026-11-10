# Consolidamento della revisione 3.1.1

**GeoStat Lab · 10 novembre 2026**

La revisione risponde al controllo delle stratificazioni effettuato sulla consegna 3.1.0. Riguarda il collaudo delle metriche, la specificità dei limiti didattici, la coerenza della documentazione e la rimozione delle implementazioni superate.

## Interventi

| Riscontro | Correzione |
|---|---|
| Falsi positivi con metriche mancanti, rinominate o non numeriche | Comparatore condiviso fra Node e browser: insieme dei nomi, unicità, tipi, contenuti e tolleranze; ogni differenza fa fallire l’attività |
| Paragrafo generico ripetuto in 121 esperimenti | 121 testi specifici verificati sul codice R; conservati i 18 limiti già specifici, per 139 testi distinti |
| Schede dei moduli incentrate soltanto sulle slide | 28 schede allineate agli esperimenti e alle tre fasi delle spedizioni mediante un generatore riproducibile |
| Istruzioni di pubblicazione sovrapposte | DEPLOYMENT.md come procedura operativa unica; la pagina precedente rimanda alla procedura corrente |
| Due preparatori dei test e anteprima iframe incompatibile | Unico preparatore Node, collaudo aperto direttamente e viewport impostato nel browser |
| Vecchie pagine non richiamate dal routing | Rimosse modulePage, funzioni collegate e ramo irraggiungibile della precedente homepage |
| Possibile disallineamento fra copie e download | Controllo automatico di catalogo, fonti editoriali, schede dei moduli, archivi e collegamenti |

## Conservazione dei contenuti scientifici

La revisione mantiene programmi R, parametri, formule e figure iniziali. I nuovi paragrafi esplicitano il generatore, le assunzioni effettivamente adottate, le semplificazioni e ciò che il risultato non consente di inferire. La formulazione varia con l’attività e conserva la terminologia del procedimento.

I materiali R6 rimangono soggetti al loro manifesto originale. Le schede README e il catalogo degli esperimenti sono prodotti del sito e vengono aggiornati senza modificare i fascicoli o i sorgenti del corso.

## Criterio di confronto

Le metriche sono associate per nome, indipendentemente dall’ordine. Nomi mancanti, aggiunti o duplicati e cambi di tipo sono errori. Le stringhe decimali finite sono confrontate numericamente, ammettendo spazi esterni; per testi, valori logici e nulli è richiesta uguaglianza esatta. Il limite numerico resta `max(10⁻⁵, 0,025 × max(|x|, |y|))` e non viene allargato per nascondere discrepanze.

I rapporti 3.0 e 3.1.0 conservano i risultati osservati all’epoca, con una nota sul limite del comparatore precedente. Le loro prove non sono presentate come nuove esecuzioni del comparatore corretto.

## Verifica della consegna

| Prova eseguita | Esito |
|---|---|
| Regressioni Node, compresi i falsi positivi | 21 gruppi superati; il test dell’harness verifica che le discrepanze incrementino gli errori |
| Catalogo completo in Chromium con comparatore v2 | 139 esperimenti superati, 0 errori, 150 SVG validati, nessuna discrepanza nelle metriche |
| Documentazione e fonti editoriali | 139 limiti distinti, 28 schede allineate, 45 documenti controllati |
| Archivi scaricabili | 1.097 file confrontati byte per byte con i rispettivi sorgenti |
| DOM, formule e ingressi ostili | 1.730 espressioni matematiche; 8 payload SVG respinti e 150 figure iniziali accettate |
| Integrità e protocollo HTTP | Materiali R6, 249 file vendorizzati, CSP/SRI e controlli HTTP superati |
| Conservazione degli algoritmi | Confronto strutturato con la revisione precedente: cambiano soltanto i limiti di 121 attività; codice, controlli e formule invariati |

Il catalogo completo è stato eseguito nella pagina di collaudo mediante il browser disponibile, con lo stesso runtime R e il comparatore utilizzati dal progetto. Il rapporto [qa/consolidation-browser.json](../qa/consolidation-browser.json) registra `comparisonVersion: 2`. Il test completo Playwright del workflow GitHub non viene dichiarato eseguito localmente.

Il rapporto [qa/consistency.json](../qa/consistency.json) conserva l’esito dei controlli sulle fonti. Sono state inoltre osservate nel browser la pagina delle spedizioni, la navigazione al laboratorio M05 e la visualizzazione del paragrafo specifico e del formalismo.

GitHub Actions e CodeQL devono essere eseguiti nel repository GitHub di destinazione. Questa revisione non costituisce una nuova lettura visiva integrale delle 861 slide né un penetration test indipendente.
