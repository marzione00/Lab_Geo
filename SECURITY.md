# Politica di sicurezza

## Ambito e versioni

La versione applicativa mantenuta è **3.5.0**. La revisione di sicurezza documentata riguarda **GeoStat Lab 3.2.1**, applicazione statica con R eseguito nel browser. La manutenzione va applicata alla versione corrente; non è previsto il mantenimento parallelo delle versioni precedenti. Le condizioni dei materiali didattici R6 restano quelle indicate in LICENSE.md.

Sono compresi nell’ambito gli ingressi dell’interfaccia, i file di configurazione importati, il rendering dei risultati, gli script di build, il server locale e i workflow GitHub. La sicurezza degli account GitHub, dei browser, del sistema operativo e del provider di hosting richiede interventi e aggiornamenti separati.

## Segnalare una vulnerabilità

Nel repository GitHub usare **Security → Advisories → Report a vulnerability**, dopo che il proprietario ha abilitato le segnalazioni private. Il pacchetto non può attivare tale impostazione e non presume che il canale sia già disponibile. Se il pulsante manca, aprire soltanto una richiesta generica di contatto privato al manutentore, senza pubblicare dettagli sfruttabili, dati personali, credenziali o prove contenenti informazioni riservate.

La segnalazione dovrebbe comprendere:

- versione o commit interessato e URL di distribuzione, se pertinente;
- descrizione della vulnerabilità e del suo impatto;
- passi minimi di riproduzione su una copia locale;
- browser, sistema operativo e configurazione dell’hosting;
- eventuale correzione proposta, con una prova di regressione.

Non eseguire attacchi volumetrici, tentativi di accesso ad account altrui o prove su dati reali degli studenti. Un test locale con dati sintetici è sufficiente a descrivere il problema. Non viene dichiarato un programma di ricompense né un tempo di risposta garantito.

## Gestione di un incidente

1. Individuare versione, file e distribuzioni interessate, preservando la prova tecnica senza esporre dati riservati.
2. Se il contenuto distribuito è compromesso, sospendere la pubblicazione o ripristinare un commit conosciuto e verificato. Un sospetto segreto va revocato prima di rimuoverne le copie.
3. Correggere la causa, introdurre un test che riproduca il difetto e rieseguire i controlli appropriati.
4. Pubblicare la correzione attraverso la pipeline; documentare impatto, versioni e misure necessarie per gli utenti.
5. Riesaminare le credenziali, le autorizzazioni GitHub e le dipendenze eventualmente coinvolte. Non risolvere un errore eliminando i test o allargando indiscriminatamente la CSP.

## Confine del codice R

L’editor permette l’esecuzione intenzionale di programmi R. I file importati sono trattati come dati fino all’approvazione esplicita nell’interfaccia; ciò non rende innocuo il codice approvato. webR dispone di funzioni di interazione con JavaScript e il browser. Il worker non va considerato un ambiente isolato per l’analisi di software ostile. Usare programmi verificati e dati non sensibili, preferibilmente su un’origine dedicata.

Il modello di minaccia completo è in [docs/SICUREZZA.md](docs/SICUREZZA.md); il rapporto delle prove è in [docs/COLLAUDO_SICUREZZA.md](docs/COLLAUDO_SICUREZZA.md).
