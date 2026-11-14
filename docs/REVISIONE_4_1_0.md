# Revisione della versione 4.1.0

Revisione del 14 novembre 2026. Ambito: impianto grafico, impaginazione, briefing iniziale e audio di bordo, a partire dalla versione 4.0.0. I materiali didattici R6, i dati, le slide, i 139 programmi R e il motore di calcolo non sono stati modificati. L’ispirazione è l’interfaccia di una nave stellare con mappa galattica; il sito non riprende loghi, nomi, caratteri tipografici, suoni o melodie di opere esistenti. Non c’è alcuna voce narrante.

## Misure prima e dopo

| Misura | 4.0.0 | 4.1.0 |
|---|---|---|
| Altezza dell’intestazione, telefono 390 px e desktop 1440 px | 190 px; 151 px | 102 px; 105 px |
| Posizione della mappa galattica nella home, desktop e telefono | sotto la prima schermata (912 px; 1390 px) | nella prima schermata (307 px; 404 px) |
| Dimensioni di carattere nei fogli di stile | 31 valori in pixel | 7 gradini in rem |
| Caratteri visibili sotto 12 px nella home | 28%, fino a 7 px | nessuno |
| Colori del testo delle famiglie azzurra e oro | 199 valori distinti | 8 toni |
| Caratteri per riga dei paragrafi lunghi, desktop | fino a 145 | da 58 a 75 |
| Lunghezza del catalogo degli esperimenti, telefono e desktop | 34.646 px; 12.587 px | 2.728 px; 1.919 px |
| Lighthouse mobile, home: prestazioni, LCP, TBT | 61; 4,1 s; 1.460 ms | 61–63; 4,1–4,2 s; 1.110–1.280 ms |
| Lighthouse mobile, modulo M05: prestazioni, LCP, TBT | 63–67; 4,4–4,5 s; 730–940 ms | 63–67; 4,6 s; 670–890 ms |
| Task lunghi in 10 s a regime: home, sistema, modulo | non misurato con la mappa visibile; 0; 0 | 0; 0; da 0 a 117 ms in due esecuzioni |
| Spostamento del layout al primo caricamento, valore massimo | 0,002 | 0,019 |
| Parte comune della pagina, compressa | 193.580 B | 198.382 B |
| axe-core 4.14 sulle 254 rotte a 390 e 1440 px | 0 violazioni | 0 violazioni, anche con il briefing aperto |

La parte comune cresce di 4,8 KB compressi: circa 2,3 KB vengono da tipografia, colori e impaginazione, circa 1,9 KB dal caricamento di briefing e audio. I tre file caricati su richiesta pesano 3,9 KB (`briefing.js`), 1,4 KB (`briefing.css`) e 3,1 KB (`audio.js`) compressi. Il primo avvio di R scarica ancora 46 file per 48,3 MiB.

## Interventi

**Fondamenta grafiche.** Le 31 dimensioni in pixel diventano una scala di sette gradini in rem (`--fs-1` … `--fs-7`, minimo 12 px), che rispetta la dimensione del carattere scelta nel browser; i due glifi decorativi delle classi stellari mantengono la loro misura, espressa in rem. Le 212 dichiarazioni di colore del testo con 199 valori azzurri e oro confluiscono in otto toni; i ruoli `--action`, `--info` e `--alert` e le superfici `--bg`, `--surface`, `--surface-raised` sono variabili nominate. `tests/contrast.test.mjs` verifica il contrasto di ogni tono su ogni superficie (WCAG AA, 4,5:1) e l’assenza di dimensioni in pixel. Il pannello `.hud-panel`, con angoli a staffa condivisi, è usato dalla mappa, dal pannello del sistema selezionato, dal briefing e dai suggerimenti. Una regola unica azzera le animazioni con movimento ridotto.

**Impaginazione.** L’intestazione su telefono ha due righe: marchio e pulsanti, poi una navigazione che scorre lateralmente con un bordo sfumato; il pulsante del movimento mostra soltanto l’icona e conserva il testo come nome accessibile. Sui telefoni la riga di attribuzione è nascosta, perché il piè di pagina riporta già autore e sito principale. Nella home la mappa occupa la prima schermata e il testo introduttivo passa nel «Dossier della spedizione» sotto la mappa; su schermi stretti una barra fissa in basso tiene a portata il sistema selezionato. I pulsanti della mappa vengono collocati prima del primo disegno, così la mappa nella prima schermata non sposta il layout. Il catalogo degli esperimenti è raggruppato per modulo in sezioni richiudibili, con una barra degli strumenti che resta visibile sui desktop e una vista a elenco. Il testo corrente è limitato a 60ch; gli elenchi di codice sono esclusi.

**Briefing.** Alla prima visita della home si apre un dialogo nativo con cinque schede: destinazione, navigazione, laboratori, taccuino e indice testuale. Ogni scheda incornicia l’elemento reale corrispondente e si sposta dalla parte opposta; la scheda sulla navigazione evidenzia Aster, primo sistema del percorso. Esc, «Salta» e le frecce funzionano da tastiera, e alla chiusura il focus torna al contenuto. I testi stanno in `content/briefing.json`, con i numeri calcolati dai dati. Chi arriva da un link diretto entra subito nella pagina; il pulsante «Rivedi il briefing» nel piè di pagina lo riapre. Alla prima visita di un sistema, di un modulo e di un laboratorio compare una riga di suggerimento sotto l’elemento a cui si riferisce, senza spostare il layout.

**Audio.** I suoni sono sintetizzati con la Web Audio API, senza file audio: la CSP mantiene `media-src 'none'`. L’audio è spento per impostazione predefinita; si accende dalla prima scheda del briefing o dal pulsante nell’intestazione, e solo allora viene caricato `audio.js`. Il contesto audio nasce dentro il clic, a 24 kHz. Il tappeto sonoro è in re minore, con coppie di oscillatori a dente di sega leggermente stonate, un filtro che si apre e si chiude in decine di secondi e accordi di 26 secondi in dissolvenza. Ci sono suoni brevi per passaggio, selezione, apertura ed errore, e suoni per viaggio, arrivo, avvio di R e calcolo concluso. La scelta resta memorizzata; se era «acceso», l’audio riparte alla prima interazione con la pagina. Si sospende quando la scheda del browser è nascosta. Il cursore del volume compare sugli schermi larghi.

## Scelte motivate

- **Oro anche come colore di categoria.** Il piano prevedeva l’oro soltanto per ciò che si clicca. La legenda della mappa usa però l’oro per le esplorazioni e l’azzurro per il corso, e l’indagine guidata è tutta in oro. Ricolorare quei testi avrebbe tolto informazione, quindi l’oro marca azioni, stati selezionati e categoria; i ruoli sono scritti nei commenti dei token.
- **Pannello del sistema accanto alla mappa sul desktop.** Sovrapposto a destra avrebbe coperto i sistemi elencati su quel lato.
- **Barra fissa sul telefono al posto di un pannello che sale dal basso.** Un pannello sopra la mappa ne avrebbe nascosto metà; la barra occupa 52 px e porta al viaggio.
- **Il briefing evidenzia Aster senza far partire il viaggio.** Il viaggio della camera porta dentro il sistema e cambierebbe pagina mentre il briefing è aperto.
- **Barra degli strumenti del catalogo non fissa sui telefoni.** Con tre righe avrebbe occupato un terzo dello schermo.
- **Galassia disegnata su richiesta con il renderer CPU.** Con la mappa nella prima schermata, la rotazione continua del renderer software occupava il thread principale per tutti i 10 secondi misurati. Ora disegna solo su selezione, trascinamento e viaggio, con il campo stellare memorizzato in un livello e una densità di un pixel per pixel CSS. Con WebGL hardware la rotazione continua resta invariata.

## Verifiche

- `npm test`: 70 test Node, tra cui contrasto dei token, contenuti del briefing e catena audio su un contesto simulato, poi lint con la soglia di complessità abbassata da 14 a 13 funzioni, controllo dell’ordine dei moduli, build, distribuzione, HTTP, sicurezza e coerenza.
- `npm run test:dom`: 28 moduli e 1190 espressioni matematiche.
- Suite Chromium, 19 gruppi superati:
  - il nuovo gruppo controlla briefing alla prima visita, chiusura con Esc e ritorno del focus, axe-core con il briefing aperto a 390 e 1440 px, link diretto senza briefing, suggerimento nel laboratorio;
  - audio assente prima del consenso e avviato dopo, scelta ricordata in attesa di un gesto, interruttore;
  - task lunghi con l’audio acceso: 0 ms nella home, da 0 a 207 ms nel modulo in due esecuzioni;
  - il controllo dei task lunghi a regime ora include la home.
- Controllo del pacchetto con gli strumenti della revisione:
  - axe-core sulle 254 rotte a 390 e 1440 px;
  - scorrimento laterale nei 28 moduli a nove larghezze;
  - Lighthouse mobile ripetuto due volte;
  - peso della parte comune e download del primo avvio di R.
