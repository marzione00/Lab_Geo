/* Course membership and difficulty are independent; all worlds stay accessible. */
(function (root) {
  'use strict';
  const course = {
    T00: ['Introduttivo', [], 'Operazioni aritmetiche e lettura di semplici espressioni.'],
    M01: ['Introduttivo', [], 'Nessuna conoscenza statistica preliminare.'],
    M02: ['Introduttivo', ['T00'], 'Vettori, istruzioni e calcolo scientifico.'],
    M03: ['Introduttivo', ['M01', 'M02'], 'Variabili, tabelle e operazioni fondamentali in R.'],
    M04: ['Introduttivo', ['M01', 'M02'], 'Variabili e simulazione mediante istruzioni R.'],
    M05: ['Intermedio', ['M03', 'M04'], 'Distribuzioni, probabilità e variabilità dei dati.'],
    M06: ['Intermedio', ['M05'], 'Campionamento, stima e intervalli di confidenza.'],
    M07: ['Intermedio', ['M03', 'M05', 'M06'], 'Covariabilità, stima e confronto fra ipotesi.'],
    M08: ['Avanzato', ['M07'], 'Regressione e nozioni di algebra matriciale.'],
    M09: ['Avanzato', ['M07'], 'Regressione, residui e dipendenza fra osservazioni.'],
    M10: ['Intermedio', ['M07'], 'Regressione e distinzione fra stima e previsione.'],
    M11: ['Avanzato', ['M07'], 'Regressione, distanze e dipendenza fra osservazioni.'],
    M12: ['Avanzato', ['M02', 'M03', 'M11'], 'Gestione dei dati, rappresentazioni grafiche e coordinate spaziali.'],
    M13: ['Avanzato', ['M05', 'M09'], 'Incertezza della misura e dipendenza temporale.'],
    M14: ['Avanzato', ['M04', 'M05'], 'Distribuzioni di probabilità e incertezza della stima.'],
    M15: ['Intermedio', ['M02', 'M05'], 'Script R, gestione dei dati e inferenza statistica.'],
    M16: ['Avanzato', ['M07', 'M08', 'M10'], 'Regressione, analisi multivariata e validazione delle previsioni.'],
  };
  const links = {
    radiation: {
      label: 'NASA Exoplanet Archive · Relazioni fra parametri fisici',
      url: 'https://exoplanetarchive.ipac.caltech.edu/docs/pscp_calc.html',
    },
    orbit: {
      label: 'NASA · Orbite e leggi di Keplero',
      url: 'https://science.nasa.gov/solar-system/orbits-and-keplers-laws/',
    },
    maps: {
      label: 'USGS · Cartografia geologica planetaria',
      url: 'https://www.usgs.gov/special-topics/planetary-geologic-mapping/interactive-planetary-maps',
    },
    stars: { label: 'NASA · Stelle e sistemi planetari', url: 'https://science.nasa.gov/exoplanets/stars/' },
  };
  const explorations = {
    rock: {
      discipline: 'Planetologia',
      symbol: '◇',
      level: 'Introduttivo',
      prerequisites: ['M01', 'M03'],
      preparation: 'Distinguere una misura da una descrizione e leggere una tabella.',
      title: 'Dall’immagine alla misura',
      introduces: 'Osservazioni della superficie, parametri fisici e limiti dell’interpretazione.',
      paragraphs: [
        'L’immagine di un mondo roccioso invita a riconoscere crateri e fratture; perché tali forme possano sostenere un’interpretazione geologica, occorre però conoscere la risoluzione dell’osservazione, l’area esaminata e il procedimento con cui sono state identificate. Una superficie rappresentata nell’atlante offre un contesto visivo, mentre i suoi parametri appartengono al modello dichiarato.',
        'Confronta il raggio, la distanza orbitale e l’energia incidente dei cinque mondi. Queste grandezze descrivono aspetti differenti: il raggio esprime una dimensione, la distanza determina il flusso per una data stella, mentre la storia degli impatti richiederebbe osservazioni ulteriori. La cartografia planetaria reale mostra come le unità geologiche vengano definite attraverso evidenze esplicite.',
      ],
      question:
        'Quale informazione aggiungeresti per confrontare la frequenza dei crateri su due superfici? Indica anche una conclusione che la sola texture non permette di sostenere.',
      sources: ['maps', 'radiation'],
    },
    lava: {
      discipline: 'Astrofisica',
      symbol: '✧',
      level: 'Avanzato',
      prerequisites: ['M04', 'M07'],
      preparation:
        'Bilancio energetico, interpretazione dei modelli e distinzione fra correlazione e spiegazione fisica.',
      title: 'Le sorgenti dell’energia',
      introduces: 'Separazione fra riscaldamento stellare e apporto energetico interno.',
      paragraphs: [
        'La temperatura di equilibrio riportata nella scheda deriva dal bilancio fra radiazione stellare assorbita ed emissione termica, sotto ipotesi precise. Un mondo rappresentato con attività vulcanica richiede una discussione ulteriore: nel modello radiativo dell’atlante mancano sia il calore interno sia una descrizione del trasporto dell’energia fino alla superficie.',
        'Confronta i mondi dello stesso sistema, verificando come distanza e albedo concorrano alla temperatura calcolata. La presenza grafica di lava non fornisce una misura di temperatura e non identifica una sorgente di riscaldamento. Un’interpretazione del vulcanismo richiederebbe un modello geofisico e osservazioni dedicate; il confronto serve a riconoscere dove termina la capacità esplicativa del calcolo disponibile.',
      ],
      question:
        'Quali termini aggiungeresti a un bilancio energetico per discutere una sorgente interna? Spiega perché la temperatura di equilibrio qui calcolata non misura la temperatura della lava.',
      sources: ['radiation', 'maps'],
    },
    terrestrial: {
      discipline: 'Planetologia',
      symbol: '◇',
      level: 'Intermedio',
      prerequisites: ['M03', 'M04'],
      preparation: 'Proporzionalità, potenze e interpretazione di una relazione fra variabili.',
      title: 'L’equilibrio radiativo di un mondo',
      introduces: 'Flusso incidente, albedo di Bond e temperatura di equilibrio.',
      paragraphs: [
        'La quantità di energia che raggiunge un pianeta dipende dalla luminosità della stella e dalla distanza orbitale. Soltanto una parte viene assorbita, poiché l’albedo di Bond descrive la frazione complessivamente riflessa. Per ricavare una temperatura occorre inoltre stabilire come l’energia venga redistribuita ed emessa.',
        'Nel confronto proposto si assumono orbite circolari, emissività unitaria e redistribuzione uniforme del calore. Atmosfera e calore interno rimangono esclusi. Leggi quindi la temperatura come risultato di queste ipotesi: per discutere la temperatura superficiale servirebbero informazioni e processi aggiuntivi, che una texture oceanica non documenta.',
      ],
      question:
        'Come cambierebbe la temperatura di equilibrio aumentando l’albedo a luminosità e distanza costanti? Quale informazione atmosferica manca per discutere la temperatura superficiale?',
      sources: ['radiation', 'stars'],
    },
    gas: {
      discipline: 'Astronomia',
      symbol: '⊙',
      level: 'Intermedio',
      prerequisites: ['M03', 'M07'],
      preparation: 'Rapporti, potenze e lettura di relazioni non lineari.',
      title: 'Dimensione e tempo orbitale',
      introduces: 'Legge di Keplero e distinzione fra dimensione planetaria e periodo.',
      paragraphs: [
        'Il gigante gassoso domina la scena per dimensione apparente, ma il periodo orbitale del modello dipende dal semiasse maggiore e dalla massa stellare. La massa planetaria è trascurata; il raggio del pianeta non compare nella relazione impiegata. Questa separazione consente di distinguere ciò che attira l’attenzione nella rappresentazione da ciò che governa il calcolo.',
        'Confronta il periodo del gigante con quello degli altri mondi e verifica come aumenti al crescere della distanza. Le distanze sullo schermo sono adattate alla leggibilità: per il confronto quantitativo usa i valori in unità astronomiche. Le bande della texture rappresentano un’atmosfera e non costituiscono misure dei suoi moti.',
      ],
      question:
        'Quale rapporto fra periodi prevedi quando il semiasse maggiore raddoppia, mantenendo la stessa stella? Spiega il ruolo della massa planetaria nell’approssimazione usata.',
      sources: ['orbit', 'radiation'],
    },
    desert: {
      discipline: 'Planetologia',
      symbol: '◇',
      level: 'Intermedio',
      prerequisites: ['M03', 'M11'],
      preparation: 'Leggere variabili spaziali e distinguere forme, processi e misure.',
      title: 'Sedimenti e superfici aride',
      introduces: 'Rilievi, trasporto dei sedimenti e limiti dell’interpretazione morfologica.',
      paragraphs: [
        'Dune e depositi possono registrare il trasporto dei sedimenti, mentre la geometria dei rilievi dipende anche dalle proprietà dei materiali e dalla storia geologica. Per ricostruire un processo a partire dalle forme occorrono misure della topografia, della granulometria e delle condizioni ambientali.',
        'La texture desertica dell’atlante offre un’ambientazione immaginaria. I parametri del sistema descrivono il bilancio radiativo assunto e l’orbita; per interpretare una superficie reale servirebbero osservazioni geologiche e atmosferiche, raccolte a risoluzioni note.',
      ],
      question:
        'Quali misure useresti per distinguere un deposito eolico da una superficie erosa? Indica quali osservazioni mancano nella rappresentazione del pianeta.',
      sources: ['maps', 'radiation'],
    },
    ice: {
      discipline: 'Planetologia',
      symbol: '◇',
      level: 'Intermedio',
      prerequisites: ['M03', 'M05'],
      preparation: 'Confronti fra variabili, ipotesi di un modello e incertezza.',
      title: 'Ghiaccio, albedo e interpretazione',
      introduces: 'Ruolo dell’albedo e limiti delle inferenze sulla superficie e sull’interno.',
      paragraphs: [
        'La superficie ghiacciata suggerisce una riflessione intensa della radiazione; nel modello questa proprietà è riassunta da un unico valore di albedo di Bond. Il parametro aggrega interazioni che, in un’osservazione reale, dipenderebbero anche dallo spettro stellare e dalle proprietà della superficie e dell’atmosfera.',
        'Confronta flusso e temperatura dei mondi, tenendo distinta la variazione della distanza da quella dell’albedo. La temperatura di equilibrio descrive un bilancio radiativo semplificato: per indagare l’interno, eventuali strati liquidi o sorgenti di calore occorrerebbero osservazioni e modelli ulteriori. La mappa geologica di un corpo ghiacciato offre un esempio di come organizzare evidenze e interpretazioni.',
      ],
      question:
        'Come separeresti l’effetto della distanza da quello dell’albedo? Indica quali condizioni manterresti fisse e quale grandezza confronteresti.',
      sources: ['radiation', 'maps'],
    },
  };
  function moduleInfo(id) {
    const c = course[id];
    return c ? { level: c[0], prerequisites: c[1], preparation: c[2] } : null;
  }
  function forPlanet(s, p) {
    if (p.isTarget) return { track: 'course', label: 'Modulo ' + s.id + ' · Corso', symbol: '◎', ...moduleInfo(s.id) };
    const e = explorations[p.category],
      f = root.GeoFamilies?.byId[p.familyId],
      project = root.GeoResearch?.forWorld(p.id);
    return {
      track: 'exploration',
      label: project ? 'Mini-progetto · Dati reali' : 'Esplorazione · ' + e.discipline,
      ...e,
      ...(f ? { level: root.GeoFamilies.levels[f.level], family: f } : {}),
      ...(project
        ? {
            project,
            title: project.title,
            introduces: project.question,
            preparation: project.preparation,
            prerequisites: project.prerequisites,
          }
        : {}),
      relation: project
        ? 'La missione impiega i metodi dei moduli indicati nei prerequisiti. Da questo sistema puoi riprendere ' +
          s.id +
          ' · ' +
          s.subject +
          '.'
        : 'Si collega a ' +
          s.id +
          ' · ' +
          s.subject +
          '. Il confronto dei parametri prepara una lettura critica delle misure e delle ipotesi impiegate nel modulo.',
    };
  }
  const esc = root.GeoHTML.escape;
  const icon = (track, symbol) =>
    '<span class="path-symbol path-symbol-' +
    track +
    '" aria-hidden="true">' +
    esc(symbol || (track === 'course' ? '◎' : '◇')) +
    '</span>';
  function badge(meta) {
    return (
      '<span class="path-badge path-' + meta.track + '">' + icon(meta.track, meta.symbol) + esc(meta.label) + '</span>'
    );
  }
  function prerequisites(meta) {
    return (
      '<div class="path-prerequisites"><strong>Preparazione consigliata</strong><p>' +
      esc(meta.preparation) +
      '</p>' +
      (meta.prerequisites.length
        ? '<div>' +
          meta.prerequisites
            .map(
              id =>
                '<a href="#modulo-' +
                id +
                '">' +
                id +
                ' · ' +
                esc(root.GEO_CATALOG.modules.find(m => m.id === id)?.title || id) +
                '</a>',
            )
            .join('') +
          '</div>'
        : '') +
      '</div>'
    );
  }
  function legend() {
    return (
      '<div class="path-legend" aria-label="Legenda dei percorsi"><span>' +
      icon('course') +
      '<strong>Corso</strong> · modulo principale</span><span>' +
      icon('exploration') +
      '<strong>Esplorazioni</strong> · approfondimenti facoltativi</span><small>L1–L5 · dall’ambiente accogliente alla ricerca estrema. L’ospitalità è una metafora didattica. Tutti i mondi sono accessibili.</small></div>'
    );
  }
  function tabs(active) {
    return (
      '<nav class="journal-paths" aria-label="Percorsi del taccuino"><a class="path-course" href="#taccuino"' +
      (active === 'course' ? ' aria-current="page"' : '') +
      '>' +
      icon('course') +
      'Corso</a><a class="path-exploration" href="#taccuino-esplorazioni"' +
      (active === 'exploration' ? ' aria-current="page"' : '') +
      '>' +
      icon('exploration') +
      'Esplorazioni</a></nav>'
    );
  }
  root.GeoPaths = Object.freeze({ moduleInfo, forPlanet, links, badge, prerequisites, legend, tabs });
})(globalThis);
