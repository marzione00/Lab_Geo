# Pubblicazione e gestione operativa

## GitHub Pages

La directory estratta deve diventare la radice del repository. Lo ZIP include sorgenti, dipendenze web distribuite localmente e materiali del corso; non contiene `.git`, `node_modules`, `dist` o identificativi della pubblicazione privata. Il README riporta i comandi per il primo push.

Selezionare **Settings → Pages → Source → GitHub Actions**. Il workflow `pages.yml` verifica il progetto, costruisce `dist/`, esegue Chromium e pubblica esclusivamente dal branch predefinito. Le pull request sono collaudate con permessi di lettura e non pubblicano. I branch ammessi dai trigger sono `main` e `master`: se il branch predefinito ha un nome diverso occorre aggiornare i trigger in entrambi i workflow.

L’ambiente è fissato a **Ubuntu 24.04, Node 22 e Python 3.12**. Playwright e le sue dipendenze sono fissati, con hash dei wheel, in `security/requirements.txt` (Playwright 1.65.0 in questa consegna). Un controllo preliminare respinge una piattaforma diversa prima di installare Chromium. Non sostituire automaticamente `ubuntu-24.04` con `ubuntu-latest`.

La build riceve `SITE_URL` dal passaggio `configure-pages` e ricava `repositoryUrl` da `GITHUB_REPOSITORY`. Non occorrono token personali, chiavi API o segreti applicativi. Le credenziali temporanee di pubblicazione sono gestite da GitHub Actions.

## Impostazioni del repository

Queste impostazioni appartengono a GitHub e non possono essere attivate copiando i file dello ZIP:

| Impostazione | Configurazione da verificare |
|---|---|
| Account dei manutentori | Autenticazione a più fattori; rimozione degli accessi inutilizzati |
| Branch predefinito | Pull request, revisione e controlli obbligatori prima del merge |
| Protezione della cronologia | Vietare force-push e cancellazione del branch di pubblicazione |
| Workflow | Permessi predefiniti di lettura; azioni ammesse limitate alle necessarie |
| Environment `github-pages` | Pubblicazione consentita dal branch predefinito; revisori, se appropriati |
| Segnalazioni private | Abilitare Private vulnerability reporting |
| Dipendenze | Abilitare Dependabot alerts e security updates, se disponibili |
| Segreti | Abilitare secret scanning e push protection, dove previsti dal piano |
| CodeQL | Usare il workflow incluso; evitare una configurazione automatica duplicata |
| Trasporto | Enforce HTTPS; DNS e certificati verificati per un dominio personalizzato |

Il controllo CodeQL viene eseguito automaticamente nei repository pubblici. Per un repository privato occorrono i diritti del servizio GitHub Code Security e la variabile `ENABLE_PRIVATE_CODEQL=true`. La consegna predispone il controllo; non afferma che il servizio sia stato eseguito sul repository dell’utente.

## Header HTTP e isolamento dell’origine

L’HTML principale contiene una CSP funzionante anche su GitHub Pages. Essa limita script, connessioni e risorse all’origine del sito, impedisce JavaScript inline, eventi HTML inline, oggetti incorporati, form e modifica della base degli URL. `wasm-unsafe-eval` consente WebAssembly; gli stili inline rimangono necessari a MathJax e all’interfaccia.

`frame-ancestors`, X-Frame-Options, HSTS e Permissions-Policy richiedono header HTTP reali. GitHub Pages non offre un file di configurazione equivalente a `_headers`: copiarlo nel repository non attiva questi header. Per controllarli usare un hosting statico che supporti gli header o un reverse proxy/CDN davanti a un dominio dedicato. Il codice genera `dist/_headers` nel formato Cloudflare Pages; l’effettiva applicazione va controllata sulla risposta HTTP dopo la pubblicazione.

La politica del worker R è separata: Emscripten richiede `unsafe-eval` per il collegamento dinamico delle librerie, mentre il documento principale continua a vietarlo. Su host compatibili il worker può collegarsi soltanto all’origine del sito. Su GitHub Pages puro questa restrizione HTTP del worker **non è garantita**. Non usare tale distribuzione come servizio di esecuzione di codice non fidato.

I progetti pubblicati sotto lo stesso dominio `OWNER.github.io` condividono l’origine, anche se hanno sottocartelle diverse. Per una separazione più forte pubblicare GeoStat Lab su un proprio sottodominio. Non ospitare sulla stessa origine applicazioni riservate o servizi che dipendono da cookie privilegiati.

Un’infrastruttura pubblica deve inoltre gestire protezione DDoS, limiti di traffico, logging, disponibilità e aggiornamenti del provider. Il server Node incluso è un server di sviluppo locale, non un reverse proxy o un WAF.

## Controllo dopo la pubblicazione

- Aprire la home, un laboratorio e una slide con formule anche da mobile.
- Verificare un risultato ricalcolato in R, non soltanto la figura iniziale.
- Provare esportazione/importazione JSON e un calcolo con parametri diversi.
- Controllare i tipi MIME di `.mjs` e `.wasm`, l’assenza di errori CSP inattesi e gli header realmente restituiti.
- Verificare l’esito dei workflow e conservare gli artefatti diagnostici dei fallimenti.

## Ripristino

Per annullare una modifica applicativa, creare un commit di revert e lasciare che la pipeline ricostruisca il sito. Se una dipendenza o il repository risultano compromessi, scegliere un commit verificato e rivalutare anche credenziali e autorizzazioni: il semplice ripristino della pagina non revoca un segreto sottratto.

## Risoluzione dei problemi

| Sintomo | Verifica |
|---|---|
| Playwright segnala un sistema non supportato | Confermare Ubuntu 24.04, Python 3.12 e installazione da `security/requirements.txt` |
| `npm ci` fallisce con `E404` su `css-color-3.2.1.tgz` | Sostituire `package.json` e `package-lock.json` con quelli della consegna 3.2.4, poi creare un nuovo commit. Il lockfile corretto usa `@asamuzakjp/css-color@3.2.0` e il vincolo ufficiale di `cssstyle`. Non modificare a mano versioni, URL o impronte nel lockfile. |
| Altri errori di `npm ci` | Usare Node 22 o successivo; mantenere allineati `package.json` e `package-lock.json`. Per il collaudo della consegna usare una cache npm vuota e verificare anche `npm ls --all`. |
| Controllo SHA-256 fallito | Accertare provenienza e integrità del file; non aggiornare il manifesto senza revisione |
| Pagina vuota in locale | Usare `npm start`, non `file://`; controllare che la build sia completa |
| R non si avvia | Verificare MIME, worker, CSP, connessione e memoria del dispositivo |
| R si arresta al limite di tempo | Ridurre i parametri o eseguire lo script scaricato in R nativo |
| CodeQL ignorato nel repository privato | Verificare servizio GitHub e variabile di abilitazione |
| `Get Pages site failed` / `Not Found` | Selezionare Settings → Pages → Source → GitHub Actions, poi rilanciare il workflow esistente |
| `Horizontal overflow` nel test Chromium | Consultare `layout.json`, screenshot e trace nell’artefatto `browser-diagnostics`; mantenere il controllo e correggere l’elemento fuori misura |
| Pubblicazione rifiutata | Verificare Pages, branch predefinito, environment e permessi, senza ampliare quelli dei test |
