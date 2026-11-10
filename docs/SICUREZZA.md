# Modello di minaccia e misure di protezione

Revisione del 10 novembre 2026 · GeoStat Lab 3.1.2

## Architettura e beni da proteggere

GeoStat Lab distribuisce file statici e svolge i calcoli sul dispositivo dello studente. Non sono presenti API applicative, database, autenticazione degli studenti o caricamenti verso un server. I beni da proteggere sono l’integrità dei programmi e dei materiali scientifici, il contesto di navigazione, gli appunti locali, la disponibilità dell’interfaccia e le autorizzazioni del repository che pubblica il sito.

I contenuti del corso e le dipendenze vendorizzate appartengono alla base di fiducia: una persona che possa modificarli e pubblicarli può modificare il comportamento del sito. Configurazioni importate, parametri nei collegamenti e risultati del codice R personalizzato sono invece ingressi da controllare. Il codice personalizzato rimane un programma scelto esplicitamente dall’utente; l’applicazione non offre un servizio di isolamento di codice ostile.

## Minacce, controlli e prove

| Minaccia | Controllo | Prova o limite |
|---|---|---|
| DOM XSS attraverso appunti o metadati R | Escaping del testo, contratto dei risultati, CSP senza script/eventi inline | Test degli ingressi e dell’importazione nel DOM; CSP verificata nel browser |
| JSON con chiavi pericolose o struttura eccessiva | Rifiuto di `__proto__`, `prototype`, `constructor`; profondità massima e schema | Test con chiavi annidate, valori inattesi e strutture oltre limite |
| Iniezione nel codice dei parametri R | Nomi ammessi e valori numerici/stringa vincolati al catalogo | Test con espressioni R nei parametri, coercizioni e campi sconosciuti |
| Esecuzione involontaria di codice importato | Stato di approvazione separato; auto-ricalcolo disattivato; comando esplicito dall’editor | Il test DOM verifica che importazione e pulsante ordinario non eseguano il programma |
| SVG attivi o con risorse esterne | Parsing XML, elementi grafici ammessi, rifiuto di eventi, script, foreignObject, DTD, entity e URL esterni | Otto payload ostili respinti; 150 figure R esistenti accettate |
| Formula injection nei CSV | Parsing CSV con virgolette/newline; apostrofo davanti ai valori testuali interpretabili come formula | Test con formule, tabulazioni, separatori, newline e numeri negativi |
| Calcoli interminabili o coda di richieste | Termine di 60 secondi, interruzione manuale, eliminazione dei lavori obsoleti | Il limite riduce il rischio; non impone una quota rigida alla memoria del browser |
| Path traversal o esposizione di file locali | Radice `dist`, percorsi decodificati verificati, realpath, blocco symlink esterni e file nascosti | Richieste dirette con traversal codificato, NUL, backslash e link simbolico |
| DNS rebinding sul server di sviluppo | Bind loopback, lista Host locale, rifiuto delle richieste Fetch Metadata cross-site | Prove HTTP con Host estraneo e `Sec-Fetch-Site: cross-site` |
| Modifica di dipendenze distribuite | Inventario SHA-256 e confronto con manifesti upstream disponibili | 249 file; una variazione interrompe la verifica |
| Compromissione della catena CI | Azioni dirette fissate a commit, lockfile npm, hash Python, permessi separati, niente credenziali nel checkout | Controlli strutturali locali; esecuzione remota e impostazioni GitHub da verificare sul repository finale |
| Clickjacking | X-Frame-Options e frame-ancestors su host con header configurabili | Il meta HTML non può imporre frame-ancestors; limite esplicito su GitHub Pages |
| Connessioni indesiderate | `connect-src 'self'` nel documento e nei worker su host configurabili | I worker caricati da URL non ereditano la CSP del documento; su Pages puro serve un proxy per applicare l’header del worker |
| DDoS, compromissione del browser o dell’account GitHub | Hosting con protezioni di rete, aggiornamenti, MFA, branch rules | Richiedono configurazione e gestione esterne al codice del sito |
| SQL injection, CSRF su sessioni applicative, upload server-side | Nessun database, sessione applicativa o endpoint di modifica | Non applicabili all’architettura attuale; da rivalutare se vengono introdotti backend o account |

## Limiti applicativi

| Risorsa | Limite |
|---|---:|
| File JSON importato | 2.000.000 byte prima della lettura |
| Collegamento con parametri | 16.000 caratteri |
| Profondità JSON | 12 livelli |
| Programma R personalizzato | 100.000 caratteri |
| Appunti | 20.000 caratteri |
| Avvio del motore R | 180 secondi |
| Singolo calcolo R | 60 secondi |
| Risultato JSON | 16.000.000 caratteri |
| Tabella completa | 100.000 righe, 80 colonne |
| Anteprima tabellare | 80 righe |
| Riepilogo | 80 righe |
| Figure per risultato | 6 |
| Singola figura SVG | 5.000.000 caratteri |

I controlli della struttura sono applicati prima del rendering. I limiti sull’output non impediscono al programma di allocare memoria durante il calcolo: un’allocazione eccessiva può ancora portare alla chiusura del worker o della scheda. Un watchdog non è una protezione DDoS del provider. Per analisi più grandi è disponibile lo script R autonomo.

## CSP, integrità e worker

`config/security.json` contiene la CSP del documento. Non ammette JavaScript inline, gestori di eventi inline o `unsafe-eval`; consente la compilazione WebAssembly. Gli stili inline sono mantenuti per compatibilità con MathJax e con proprietà grafiche calcolate. Script e stili caricati dall’HTML sono accompagnati da SRI SHA-384; gli script dei moduli e MathJax caricati dinamicamente ricevono le impronte dal manifesto generato durante la build.

Le quattro pagine HTML accessorie ricevono anch’esse una CSP nella copia web. Il filtro del registro delle slide, che usa uno script inline nei materiali originali, è autorizzato con l’hash SHA-256 del solo script incluso; i sorgenti R6 rimangono invariati.

Gli hash rendono rilevabile una modifica della risorsa rispetto al documento o al manifesto atteso. Non proteggono quando un attaccante può modificare e pubblicare contemporaneamente documento, manifesto e risorsa; per questo contano anche revisione del codice e protezione dell’account.

webR 0.6.0 usa funzioni Emscripten che richiedono valutazione dinamica di JavaScript nel worker. La politica HTTP dedicata permette tale operazione soltanto nella directory del runtime e limita le connessioni all’origine. La pagina mantiene la propria politica restrittiva. Le distribuzioni upstream di webR non sono modificate.

La build produce un file `_headers` per hosting compatibili. GitHub Pages non lo interpreta; la CSP del documento rimane attiva tramite meta, ma i controlli che esistono soltanto come header non sono automaticamente presenti. Usare un hosting con header configurabili e un’origine dedicata se occorre imporre anche il confine di rete del worker. Il codice R approvato non deve essere considerato non fidato, indipendentemente dall’hosting.

## Dipendenze e vulnerabilità note

`npm audit` controlla i 39 pacchetti npm di sviluppo presenti nel lockfile. L’audit della consegna non ha segnalato vulnerabilità note; il risultato è datato e non garantisce che rimanga valido. Gli script npm di installazione sono disabilitati con `--ignore-scripts`.

L’inventario `security/vendor-integrity.json` comprende 249 file. Ulteriori controlli confrontano webR con il manifesto di provenienza e i 23 pacchetti R con le impronte degli archivi. Si tratta di controlli d’integrità, non di una scansione esaustiva delle vulnerabilità dei binari WASM o di R. Anche una distribuzione autentica può contenere un difetto.

MathJax 3.2.2 è conservato per compatibilità con le formule esistenti; la configurazione limita le estensioni TeX a quelle necessarie, escludendo caricamento dinamico ed estensioni HTML. Le formule del corso sono contenuti revisionati, non input degli studenti. Le segnalazioni che riguardano MathJax incorporato in altre applicazioni, per esempio ambienti desktop con accesso a Node, non vanno trasferite automaticamente al modello del browser; l’upstream deve comunque essere monitorato e gli aggiornamenti sottoposti al collaudo di tutte le formule.

Playwright 1.65.0 e greenlet 3.5.6 sono fissati con gli hash dei wheel ufficiali PyPI. Le versioni dei browser di collaudo non determinano la versione del browser utilizzata dagli studenti, che deve essere aggiornata dal proprietario del dispositivo. Dependabot propone aggiornamenti delle dipendenze npm, Python e delle azioni dirette; le dipendenze transitive interne alle azioni e i componenti R richiedono anche la revisione degli avvisi upstream.

## Dati e riservatezza

Appunti e progresso sono conservati nel localStorage della stessa origine e possono essere letti dalle altre applicazioni che vi appartengono. L’interfaccia non invia questi dati a un backend. Un’esportazione JSON può contenere appunti, codice e risultati: rileggerla prima di condividerla. I collegamenti condivisi contengono i parametri del programma standard, non gli appunti né il codice personalizzato.

Tutti i file inseriti nei percorsi distribuiti dalla build sono destinati alla consultazione pubblica. `.gitignore` limita errori comuni ma non sostituisce una revisione dei file. La scansione di segreti inclusa riconosce alcuni formati frequenti; non può riconoscere ogni credenziale, parola d’accesso o dato personale.

## Fonti tecniche

Consultate il 10 novembre 2026:

- [OWASP — Content Security Policy Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html).
- [MDN — Content-Security-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy), comprese le politiche dei worker e i limiti del meta.
- [OWASP — CSV Injection](https://owasp.org/www-community/attacks/CSV_Injection).
- [GitHub — Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use).
- [GitHub — Securing a Pages site with HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https).
- [Cloudflare Pages — Headers](https://developers.cloudflare.com/pages/configuration/headers/).
- [webR — R API e interazione JavaScript](https://docs.r-wasm.org/webr/latest/api/r.html).
- [MathJax — TeX input options](https://docs.mathjax.org/en/v3.2/options/input/tex.html).

Le misure sono ispirate alle indicazioni pertinenti a questa architettura; non costituiscono una certificazione né un penetration test indipendente.
