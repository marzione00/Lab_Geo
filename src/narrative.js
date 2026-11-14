/* Narrative and evidence refer to the model actually executed by R. */
(function (root) {
  'use strict';
  const D = root.GEO_NARRATIVE,
    key = 'geostat-fieldbook-v1';
  const esc = root.GeoHTML.escape;
  const fmt = (x, d = 3) => Number(x).toLocaleString('it-IT', { maximumFractionDigits: d });
  const paragraphs = xs => xs.map(p => '<p>' + esc(p) + '</p>').join('');
  const activity = id => root.GEO_LABS.activities.find(a => a.id === id);
  const has = id => Object.hasOwn(D.activities, id);
  function home() {
    return `<div class="narrative-opening"><div class="narrative-prose">${paragraphs(D.home.paragraphs)}</div><aside class="narrative-departure"><p class="eyebrow">INDAGINE GUIDATA / PELAGO</p><h2>Quanto racconta un campione?</h2><p>Segui nove indagini sulla conoscenza di un ambiente osservato soltanto in parte.</p><a class="button" href="#sistema-M05">Raggiungi Pelago ↗</a><a href="#sistema-T00">Comincia dai fondamenti →</a><a href="#taccuino">Apri il taccuino scientifico →</a></aside></div>`;
  }
  function chapter(id) {
    return D.chapters[id] || null;
  }
  function system(s) {
    const c = chapter(s.id);
    return `<div class="narrative-system"><p class="eyebrow">${esc(c.title)}</p><p>${esc(s.id === 'M05' ? D.sampling.arrival : c.text)}</p><p class="narrative-question">${esc(c.question)}</p></div>`;
  }
  function destination(id) {
    const c = chapter(id);
    return `<div class="narrative-destination"><small>LA DOMANDA DELLA SPEDIZIONE</small><p>${esc(c.question)}</p></div>`;
  }
  function planet(s, p) {
    if (!p.isTarget) return '';
    const c = chapter(s.id);
    return `<div class="narrative-planet"><h3>${esc(c.title)}</h3><p>${esc(s.id === 'M05' ? D.sampling.planet : c.text)}</p></div>`;
  }
  function moduleIntro(id) {
    const c = chapter(id);
    return c
      ? `<div class="narrative-module"><p class="eyebrow">${esc(c.title)}</p><p>${esc(c.text)}</p>${id === 'M05' ? '<p class="narrative-prerequisites">' + esc(D.sampling.prerequisites) + '</p>' : ''}<a href="#sistema-${id}">Rivedi il sistema stellare →</a> · <a href="#taccuino">Taccuino scientifico →</a></div>`
      : '';
  }
  function scene(a) {
    const x = D.activities[a.id];
    return x
      ? `<section id="narrative-scene" class="narrative-scene"><div><p class="eyebrow">RICOGNIZIONE DI PELAGO / ${esc(x.title)}</p><p>${esc(x.scene)}</p></div><div class="narrative-enquiry"><span>Domanda d’indagine</span><p>${esc(x.question)}</p><small>Scenario didattico · dati simulati</small></div></section>`
      : '';
  }
  function prediction(a) {
    return D.activities[a.id]?.prediction || a.action;
  }
  function bridge(a) {
    const x = D.activities[a.id];
    return x
      ? `<section class="narrative-bridge"><p class="eyebrow">LA TAPPA SUCCESSIVA</p><p>${esc(x.bridge)}</p>${a.id === 'm05-precisione' ? '<a class="button secondary" href="#sistema-M06">Prosegui verso Gemina →</a>' : ''}</section>`
      : '';
  }
  function metricMap(r) {
    const out = Object.create(null);
    if (!Array.isArray(r?.metrics) || r.metrics.length > 30) return null;
    for (const m of r.metrics) {
      if (
        !m ||
        typeof m.grandezza !== 'string' ||
        Object.hasOwn(out, m.grandezza) ||
        !['string', 'number'].includes(typeof m.valore)
      )
        return null;
      const s = String(m.valore).trim();
      if (!/^[+-]?(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?$/i.test(s) || !Number.isFinite(Number(s))) return null;
      out[m.grandezza] = Number(s);
    }
    return out;
  }
  function reading(id, p, r, standard = true) {
    if (!has(id)) return null;
    if (!standard)
      return 'Hai eseguito una versione modificata del codice. Il commento automatico previsto per il modello originale è sospeso: verifica il significato delle nuove grandezze prima di formulare una conclusione.';
    const m = metricMap(r);
    if (!m)
      return 'Le grandezze disponibili non consentono di ricostruire il commento della configurazione. Consulta la tabella e il codice prima di interpretare il risultato.';
    const v = name => {
      if (!Object.hasOwn(m, name)) throw Error('Missing metric');
      return fmt(m[name], 4);
    };
    try {
      if (id === 'm05-intervalli') {
        v('Copertura osservata');
        v('Livello nominale');
        v('Repliche');
      }
      switch (id) {
        case 'm05-estimandi':
          return `Con ${fmt(p.nHigh, 0)} misure nella stazione C, la media che attribuisce lo stesso peso a ogni misura è ${v('Media misure')}, mentre quella che attribuisce lo stesso peso alle tre stazioni è ${v('Media stazioni')}. ${Number(p.nHigh) === 10 ? 'Poiché ogni stazione contribuisce con dieci misure, i pesi coincidono e le due medie sono uguali per costruzione. Questa coincidenza dipende dall’allocazione delle misure.' : 'Le due quantità rispondono a bersagli distinti; la loro differenza va interpretata alla luce dei pesi, prima di giudicare quale sia pertinente alla domanda.'}`;
        case 'm05-selezione':
          return `Il modello impone alla distribuzione selezionata uno scostamento di ${v('Bias teorico selezionato')} rispetto al valore 10. Con n = ${fmt(p.n, 0)}, la deviazione standard teorica delle medie è ${v('SD teorica')}; sulle ${fmt(p.B, 0)} repliche, l’errore quadratico medio osservato è ${v('MSE selezionato')}. ${Number(p.bias) === 0 ? 'In questa configurazione lo spostamento sistematico è nullo; le differenze fra istogrammi derivano dalla simulazione.' : 'Aumentando n si riduce la dispersione teorica, mentre lo spostamento imposto resta invariato finché conservi lo stesso parametro di selezione.'}`;
        case 'm05-distribuzioni':
          return `Le ${fmt(p.B, 0)} medie, ciascuna calcolata su ${fmt(p.n, 0)} osservazioni ${p.population === 'normal' ? 'normali' : 'esponenziali'} indipendenti, hanno media complessiva ${v('Media delle medie')} e deviazione standard empirica ${v('SD empirica')}. Il riferimento teorico è ${v('SE teorico')}, poiché entrambe le popolazioni hanno varianza unitaria. La differenza fra dispersione empirica e teorica risente del numero finito delle repliche; ogni valore dell’istogramma rappresenta una media campionaria.`;
        case 'm05-dipendenza':
          return `L’ipotesi di indipendenza darebbe un errore standard di ${v('SE assumendo indipendenza')}; con correlazione ${fmt(p.rho)}, il modello fornisce ${v('SE corretto teorico')}. La dispersione osservata fra le repliche è ${v('SD delle repliche')}. Le ${fmt(p.n, 0)} misure corrispondono a una numerosità effettiva di circa ${v('n effettivo')}, definita qui attraverso l’equivalenza della varianza della media.`;
        case 'm05-intervalli':
          return `La copertura osservata sulle ${fmt(p.B, 0)} repliche è ${fmt(m['Copertura osservata'] * 100, 2)}%, rispetto al livello nominale del ${fmt(p.level * 100, 2)}%; l’errore standard Monte Carlo stimato per la copertura è ${v('MC SE copertura')}. ${Number(p.rho) > 0 ? 'Le misure simulate sono correlate, mentre la formula dell’intervallo continua ad assumere indipendenza: il confronto esamina le conseguenze di questa discordanza.' : 'Le misure simulate sono indipendenti; lo scarto dal livello nominale va letto insieme alla variabilità Monte Carlo.'} Il grafico mostra al massimo ottanta intervalli. La copertura riguarda la procedura ripetuta, mentre il parametro resta fisso a 10.`;
        case 'm05-bootstrap': {
          const lo = Object.keys(m).find(k => k.startsWith('Percentile 2,5%')),
            hi = Object.keys(m).find(k => k.startsWith('Percentile 97,5%'));
          return `Dal campione di ${fmt(p.n, 0)} osservazioni, la cui media è ${v('Media osservata')}, il ricampionamento produce un errore standard di ${v('SE bootstrap')} e limiti percentili pari a ${v(lo)} e ${v(hi)}. Le ${fmt(p.B, 0)} repliche riutilizzano il campione: aumentandole puoi stabilizzare il calcolo dei percentili, mentre la verifica della copertura richiederebbe nuove raccolte indipendenti.`;
        }
        case 'm05-ricampionamento':
          return `Ricampionando singole misure ottieni un errore standard di ${v('SE singole misure')}; ricampionando stazioni intere ottieni ${v('SE stazioni')}. Il campione comprende ${v('Unità indipendenti')} stazioni, ciascuna con sei misure, e una componente comune di ampiezza τ = ${fmt(p.tau)}. Il secondo procedimento conserva i gruppi; il confronto osservato riguarda questa realizzazione e risente anche del numero dei ricampionamenti.`;
        case 'm05-blocchi':
          return `Sulla stessa serie di ${v('Osservazioni originali')} osservazioni, il bootstrap individuale restituisce un errore standard di ${v('SE osservazioni')}, mentre i blocchi di lunghezza ${v('Lunghezza del blocco')} restituiscono ${v('SE blocchi')}. I blocchi conservano sequenze contigue, con prosecuzione circolare oltre il termine della serie. Il risultato documenta la scelta corrente della lunghezza, la cui sensibilità va esaminata attraverso altri confronti.`;
        case 'm05-precisione':
          return `Le trenta ripetizioni del calcolo, ciascuna con ${v('Repliche per calcolo')} ricampionamenti, producono limiti superiori con deviazione standard ${v('SD dei limiti superiori')}. Il campione originario conserva ${v('Campione fisso: n')} osservazioni. Questa dispersione misura l’instabilità numerica del limite stimato: per valutare l’incertezza fra campioni occorrerebbe ripetere anche la raccolta originaria.`;
      }
    } catch {
      return 'Una delle grandezze necessarie al commento non è disponibile. Verifica la tabella e il codice prima di interpretare la configurazione.';
    }
    return null;
  }
  function comparison(a, entries) {
    if (!has(a.id) || entries.length !== 2) return '';
    const [x, y] = entries,
      changed = a.controls.filter(c => x.params[c.key] !== y.params[c.key]).map(c => c.label.toLowerCase());
    if (!x.standard || !y.standard)
      return 'Il confronto include codice personalizzato. L’interpretazione richiede di verificare che i due calcoli definiscano le medesime quantità.';
    if (!changed.length)
      return 'I due scenari conservano gli stessi parametri e lo stesso seme. Costituiscono una ripetizione del calcolo; per studiare la sensibilità, modifica una condizione dichiarata.';
    let text = 'Fra gli scenari A e B hai modificato: ' + changed.join(', ') + '. ';
    if (a.id === 'm05-distribuzioni' && changed.length === 1 && x.params.n !== y.params.n)
      text += `Con popolazione, numero di repliche e seme invariati, il rapporto teorico SE(B)/SE(A) è √(${fmt(x.params.n, 0)}/${fmt(y.params.n, 0)}) ≈ ${fmt(Math.sqrt(x.params.n / y.params.n))}. Confrontalo con le dispersioni empiriche riportate, che includono la variabilità Monte Carlo.`;
    else if (changed.length === 1 && a.id === 'm05-estimandi' && x.params.nHigh !== y.params.nHigh)
      text += `Il peso della stazione C nella media delle misure passa da ${fmt(x.params.nHigh / (20 + x.params.nHigh))} a ${fmt(y.params.nHigh / (20 + y.params.nHigh))}; nella media delle stazioni rimane pari a un terzo. Anche la media campionaria di C può cambiare, poiché varia il numero delle osservazioni generate.`;
    else if (changed.length === 1 && x.params.seed !== y.params.seed)
      text +=
        'Le condizioni del modello restano invariate; il nuovo seme consente di esaminare un’altra realizzazione della simulazione.';
    else if (changed.length === 1)
      text +=
        'Gli altri parametri rimangono invariati. Le grandezze osservate documentano il confronto per queste realizzazioni; la variabilità della simulazione va distinta dalle proprietà teoriche del modello.';
    else
      text +=
        'Leggi le grandezze dei due scenari insieme alle condizioni modificate; quando variano più parametri, il confronto non isola il contributo di ciascuno.';
    return text;
  }
  function cleanRecord(raw) {
    try {
      if (!raw || !has(raw.id) || typeof raw.date !== 'string' || !Number.isFinite(Date.parse(raw.date))) return null;
      const a = activity(raw.id),
        params = root.GeoSecurity.parameters(a, raw.params),
        result = { metrics: raw.metrics };
      if (!metricMap(result)) return null;
      return {
        id: a.id,
        date: raw.date,
        params,
        metrics: raw.metrics.map(m => ({ grandezza: m.grandezza.slice(0, 90), valore: String(m.valore).slice(0, 80) })),
        notes: typeof raw.notes === 'string' ? raw.notes.slice(0, 20000) : '',
        scenarios: Array.isArray(raw.scenarios)
          ? raw.scenarios
              .slice(0, 2)
              .map(x => ({ params: root.GeoSecurity.parameters(a, x.params), metrics: x.metrics }))
              .filter(x => metricMap(x))
          : [],
      };
    } catch {
      return null;
    }
  }
  function records() {
    try {
      const raw = localStorage.getItem(key);
      if (!raw || raw.length > 600000) return [];
      const data = JSON.parse(raw);
      if (data.version !== 1 || !Array.isArray(data.entries)) return [];
      const map = new Map();
      for (const raw of data.entries.slice(0, 20)) {
        const r = cleanRecord(raw);
        if (r) map.set(r.id, r);
      }
      return [...map.values()];
    } catch {
      return [];
    }
  }
  function save(a, p, r, notes, scenarios) {
    const entry = cleanRecord({
      id: a.id,
      date: new Date().toISOString(),
      params: p,
      metrics: r.metrics,
      notes,
      scenarios: scenarios.filter(x => x.standard).map(x => ({ params: x.params, metrics: x.result.metrics })),
    });
    if (!entry) return false;
    try {
      const entries = records().filter(x => x.id !== a.id);
      entries.push(entry);
      localStorage.setItem(key, JSON.stringify({ version: 1, entries }));
      return true;
    } catch {
      return false;
    }
  }
  function journal(main) {
    const entries = records().sort((a, b) => activity(a.id).page - activity(b.id).page);
    main.innerHTML = `<div class="wrap narrative-journal">${root.GeoPaths?.tabs('course') || ''}<p class="eyebrow">CORSO / PELAGO / TACCUINO SCIENTIFICO</p><h1>Le tracce dell’indagine.</h1><p class="lead">Ritrova le configurazioni che hai scelto di conservare dopo il calcolo in R, insieme alle osservazioni annotate e agli eventuali scenari di confronto. Una registrazione documenta il lavoro svolto; la sua interpretazione rimane da argomentare.</p><p class="narrative-prerequisites">Conservato in questo browser. L’esportazione permette di custodirne una copia; la visita di una pagina non aggiunge registrazioni.</p><div class="actions"><a class="button" href="#modulo-M05">Riprendi l’indagine su Pelago →</a><button class="button secondary" id="journal-export" ${entries.length ? '' : 'disabled'}>Esporta il taccuino</button></div><p role="status">${entries.length} ${entries.length === 1 ? 'attività documentata' : 'attività documentate'} su 9.</p><div class="journal-entries">${
      entries.length
        ? entries
            .map(e => {
              const a = activity(e.id),
                query = encodeURIComponent(JSON.stringify(e.params));
              return `<article class="journal-entry"><p class="eyebrow">${esc(a.sectionTitle)} · ${esc(new Date(e.date).toLocaleDateString('it-IT'))}</p><h2>${esc(a.title)}</h2><p>${esc(reading(e.id, e.params, { metrics: e.metrics }))}</p><dl class="journal-params">${a.controls.map(c => `<div><dt>${esc(c.label)}</dt><dd>${esc(e.params[c.key])}</dd></div>`).join('')}</dl>${e.scenarios.length ? '<details><summary>' + e.scenarios.length + ' scenari conservati</summary>' + e.scenarios.map((s, i) => '<div class="journal-scenario"><h3>Scenario ' + String.fromCharCode(65 + i) + '</h3><p>' + esc(reading(e.id, s.params, { metrics: s.metrics })) + '</p><p>' + esc(a.controls.map(c => c.label + ': ' + s.params[c.key]).join(' · ')) + '</p></div>').join('') + '</details>' : ''}${e.notes ? '<h3>Le tue osservazioni</h3><p class="journal-notes">' + esc(e.notes) + '</p>' : '<p class="lab-footer-note">Nessuna osservazione personale registrata.</p>'}<a href="#laboratorio/${e.id}?c=${esc(query)}">Ricalcola questa configurazione →</a></article>`;
            })
            .join('')
        : '<div class="journal-empty"><h2>Il taccuino attende la prima osservazione.</h2><p>Apri un esperimento di Pelago, esegui il calcolo e annota ciò che osservi. Il pulsante «Conserva nel taccuino» registra la configurazione corrente e gli scenari che hai confrontato.</p></div>'
    }</div></div>`;
    main.querySelector('#journal-export').addEventListener('click', () => {
      const blob = new Blob([JSON.stringify({ application: 'GeoStatLab', version: 1, entries }, null, 2)], {
          type: 'application/json',
        }),
        url = URL.createObjectURL(blob),
        a = document.createElement('a');
      a.href = url;
      a.download = 'GeoStatLab_taccuino_Pelago.json';
      a.click();
      setTimeout(() => URL.revokeObjectURL(url), 1500);
    });
  }
  root.GeoNarrative = Object.freeze({
    data: D,
    has,
    home,
    chapter,
    system,
    destination,
    planet,
    moduleIntro,
    scene,
    prediction,
    bridge,
    reading,
    comparison,
    records,
    save,
    journal,
  });
})(globalThis);
