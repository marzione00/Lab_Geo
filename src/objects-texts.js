/* Texts of the notable objects. Every number comes from the models in objects-model.js. */
(function (root) {
  'use strict';
  const O = root.GeoObjects,
    { html } = root.GeoHTML;
  const n = (v, d = 2) => v.toLocaleString('it-IT', { maximumFractionDigits: d, minimumFractionDigits: 0 });
  const sci = (v, d = 2) => {
    const e = Math.floor(Math.log10(Math.abs(v))),
      m = v / 10 ** e;
    const sup = String(e).replace(/[-0-9]/g, c => '⁻⁰¹²³⁴⁵⁶⁷⁸⁹'['-0123456789'.indexOf(c)]);
    return n(Number(m.toFixed(d)), d) + ' × 10' + sup;
  };
  // Scientific notation with a real superscript, for the values of the card.
  const sciHTML = (v, d = 2) => {
    const e = Math.floor(Math.log10(Math.abs(v)));
    return html`${n(Number((v / 10 ** e).toFixed(d)), d)} × 10<sup>${e}</sup>`;
  };
  const eq = (tag, title, formula, text) =>
    html`<article><small>${tag}</small><h3>${title}</h3><p class="equation">${formula}</p><p>${text}</p></article>`;
  const section = (title, ...paragraphs) =>
    html`<section class="object-section"><h3>${title}</h3>${paragraphs.map(p => html`<p>${p}</p>`)}</section>`;
  const course = links =>
    html`<div class="object-course"><h3>Collegamenti con il corso</h3><ul>${links.map(
      ([href, label, text]) => html`<li><a href="${href}">${label}</a><span>${text}</span></li>`,
    )}</ul></div>`;
  const SI = O.SI;

  // ------------------------------------------------------------------ Erebo
  function blackHole(o) {
    const m = o.model,
      AU = SI.AU;
    return {
      lead: 'Un buco nero di Schwarzschild al centro della galassia, circondato da un disco di accrescimento sottile e da due getti relativistici.',
      canvas:
        'Buco nero con disco di accrescimento visto da un osservatore fermo. Trascina o usa le frecce per cambiare punto di vista; più e meno regolano la distanza.',
      instrument: 'OTTICA RELATIVISTICA',
      scale: 'UNITÀ GM/c²',
      caption: 'GEODETICHE NULLE DI SCHWARZSCHILD',
      essential:
        'La scena richiede WebGL2. I valori fisici e la spiegazione restano consultabili nella scheda e nelle sezioni seguenti.',
      signal: 'OSSERVAZIONE RELATIVISTICA',
      abstract:
        'La luce che passa vicino all’orizzonte segue traiettorie curve. Il disco appare così sopra e sotto l’ombra del buco nero, e la sua parte posteriore resta visibile anche quando è nascosta dalla geometria ordinaria.',
      note: 'r_g = GM/c² è il raggio gravitazionale. Le grandezze del disco assumono un accrescimento pari al 10% del limite di Eddington.',
      learningEyebrow: 'LEGGERE LA SCENA',
      learningTitle: 'Che cosa mostra l’immagine di un buco nero.',
      learningIntro: html`<p>Ogni punto luminoso del disco è disegnato nella direzione da cui la sua luce raggiunge l’osservatore. Le direzioni provengono da geodetiche nulle calcolate numericamente, e la stessa particella può comparire due o tre volte: una volta per la luce che arriva per il percorso più breve, poi per la luce che gira attorno al buco nero.</p>`,
      equations: html`${eq('01 / ORIZZONTE', 'Raggio di Schwarzschild', 'r_s = 2GM/c²', 'Per la massa di Erebo il raggio vale ' + sci(m.schwarzschild / 1000, 3) + ' km, cioè ' + n(m.schwarzschild / AU, 4) + ' UA.')}${eq('02 / LUCE', 'Sfera dei fotoni e ombra', 'r_ph = 3GM/c² · b_c = 3√3 GM/c²', 'A 3 r_g la luce può percorrere orbite circolari instabili. I raggi con parametro d’impatto minore di b_c ≈ 5,196 r_g cadono nell’orizzonte e formano l’ombra.')}${eq('03 / DISCO', 'Orbita circolare stabile più interna', 'r_isco = 6GM/c²', 'Il disco termina a ' + n(m.isco / AU, 3) + ' UA dal centro. A quel raggio un’orbita dura ' + n(m.iscoPeriod / 60, 1) + ' minuti.')}`,
      sections: html`${section(
        'Le immagini multiple del disco',
        'Un raggio di luce che parte dal disco dietro il buco nero può passare sopra l’ombra e raggiungere l’osservatore: la parte posteriore del disco appare come un arco che sovrasta l’ombra. La luce che la stessa zona emette verso il basso passa sotto il buco nero e forma un secondo arco sotto l’ombra.',
        'La luce che compie un giro completo attorno al buco nero forma immagini sempre più sottili, addensate in un anello attorno all’ombra: l’anello dei fotoni, vicino alla curva critica dove il parametro d’impatto vale b_c. Il pulsante «Immagini secondarie» lascia nella scena la sola immagine primaria e rende visibile quanta parte dell’aspetto del disco dipende dalla luce deviata più a lungo.',
      )}${section(
        'Colori, Doppler e spostamento gravitazionale',
        'Il gas del disco ruota a velocità relativistiche: la parte che si avvicina all’osservatore appare più brillante e più blu, quella che si allontana più debole e più rossa. A questo spostamento Doppler si somma lo spostamento gravitazionale verso il rosso della luce che risale dal pozzo di potenziale.',
        'Il fattore di frequenza di una particella in orbita circolare è g = √(1 − 3r_g/r) / [√(1 − 2r_g/r_c)(1 − Ωλ)], dove λ è il momento angolare del fotone attorno all’asse del disco e r_c la distanza dell’osservatore. La luminosità di ogni immagine cresce come g⁴. Il pulsante dedicato disattiva questo effetto: nelle immagini del film Interstellar lo spostamento Doppler fu omesso per rendere il disco più comprensibile al pubblico.',
        'La temperatura locale segue il profilo relativistico di Page e Thorne, con il massimo a ' +
          n(m.peakRadius, 2) +
          ' r_g. Con i parametri di Erebo la temperatura massima vale ' +
          n(Math.round(m.peakTemperature / 1000) * 1000, 0) +
          ' K e l’emissione cade nell’ultravioletto. I colori della scena moltiplicano le temperature per ' +
          n(m.displayFactor, 3) +
          ', in modo che il massimo corrisponda a ' +
          n(m.displayPeak, 0) +
          ' K e i rapporti fra le temperature restino quelli calcolati.',
      )}${section(
        'Getti e corona',
        'Lungo l’asse di rotazione due getti di plasma escono a una velocità pari al 92% di quella della luce. La radiazione del getto che si avvicina è amplificata dal fattore Doppler relativistico, quella del getto opposto è attenuata. Attorno alle regioni interne del disco una corona di gas caldo aggiunge una luminosità diffusa.',
      )}`,
      method: html`<p>Un worker integra con il metodo di Runge-Kutta del quarto ordine l’equazione dell’orbita della luce, d²u/dφ² = −u + 3u² con u = r_g/r, per alcune migliaia di raggi che partono dall’osservatore. Le tabelle che ne derivano associano a ogni raggio di emissione e a ogni angolo percorso la direzione d’arrivo; sono calcolate per dodici distanze dell’osservatore fra 42 e 260 r_g e interpolate durante lo zoom.</p><p>Il disco, la corona e i getti sono particelle generate nella scheda grafica a partire dal loro indice: il disco usa fino a ${n(3.2, 1)} milioni di particelle, ciascuna disegnata nell’immagine primaria e in quella secondaria, e una su quattro anche nella terziaria. Il cielo di sfondo è la stessa volta stellare dell’atlante, deviata pixel per pixel lungo le geodetiche. Il buco nero non ruota: un buco nero di Kerr avrebbe un’ombra asimmetrica e un disco interno più vicino all’orizzonte.</p>`,
      course: course([
        [
          '#modulo-T00',
          'Basalto · Calcolo scientifico',
          'integrazione numerica di equazioni differenziali e controllo dell’errore di passo',
        ],
        ['#modulo-M03', 'Iride · Visualizzazione', 'scelta delle scale di colore e della dinamica di luminosità'],
      ]),
      sources: [
        { href: 'https://science.nasa.gov/universe/black-holes/', label: 'NASA · Black holes' },
        {
          href: 'https://arxiv.org/abs/1502.03808',
          label:
            'James et al. (2015) · Gravitational lensing by spinning black holes in astrophysics, and in the movie Interstellar',
        },
        {
          href: 'https://ui.adsabs.harvard.edu/abs/1974ApJ...191..499P',
          label: 'Page e Thorne (1974) · Disk-accretion onto a black hole',
        },
        {
          href: 'https://ui.adsabs.harvard.edu/abs/1979A%26A....75..228L',
          label: 'Luminet (1979) · Image of a spherical black hole with thin accretion disk',
        },
      ],
      modelNote: 'Oggetto immaginario · massa, accrescimento e distanze scelti a fini didattici.',
    };
  }
  function blackHoleFacts(o) {
    const m = o.model;
    return [
      ['Massa', sciHTML(m.mass, 1), 'M☉'],
      ['Raggio di Schwarzschild', n(m.schwarzschild / SI.AU, 4), 'UA'],
      ['Orbita stabile più interna', n(m.isco / SI.AU, 3), 'UA'],
      ['Periodo all’ISCO', n(m.iscoPeriod / 60, 1), 'min'],
      ['Efficienza radiativa', n(m.efficiency * 100, 1), '%'],
      ['Accrescimento', n(m.mdotSolarPerYear, 4), 'M☉/anno'],
      ['Temperatura massima', sciHTML(m.peakTemperature, 2), 'K'],
    ];
  }

  // ------------------------------------------------------------------ Lapis
  // Density of semimajor axes with the resonances of the giant, as an SVG figure.
  function beltFigure(model) {
    const W = 320,
      H = 150,
      lo = 1.9,
      hi = 5.4,
      x = a => 28 + ((a - lo) / (hi - lo)) * (W - 38);
    const values = [];
    let top = 0;
    for (let a = lo; a < hi - 1e-9; a += 0.02) {
      let v = O.beltDensity(a + 0.01, model);
      v += 0.18 * Math.exp(-(((a + 0.01 - model.giant) / 0.05) ** 2));
      values.push([a, v]);
      top = Math.max(top, v);
    }
    const bars = values.map(([a, v]) => {
      const h = (v / top) * (H - 40);
      return html`<rect class="bar" x="${x(a).toFixed(1)}" y="${(H - 22 - h).toFixed(1)}" width="${(x(a + 0.02) - x(a) - 0.4).toFixed(2)}" height="${h.toFixed(1)}"/>`;
    });
    const marks = model.resonances
      .filter(r => r.label !== '4:1')
      .map(
        r =>
          html`<line class="mark" x1="${x(r.a).toFixed(1)}" x2="${x(r.a).toFixed(1)}" y1="14" y2="${H - 22}"/><text x="${x(r.a).toFixed(1)}" y="11" text-anchor="middle">${r.label}</text>`,
      );
    const ticks = [2, 3, 4, 5].map(a => html`<text x="${x(a)}" y="${H - 6}" text-anchor="middle">${a}</text>`);
    return html`<figure class="object-figure"><h3>DISTRIBUZIONE DEI SEMIASSI</h3><p>Numero relativo di asteroidi per intervallo di semiasse maggiore, con le risonanze di moto medio rispetto al gigante.</p><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Densità dei semiassi maggiori: lacune alle risonanze 3:1, 5:2, 7:3 e 2:1, gruppo di Hilda a 3:2 e Troiani a 1:1"><line class="axis" x1="28" x2="${W - 10}" y1="${H - 22}" y2="${H - 22}"/>${bars}${marks}${ticks}<text x="${W - 10}" y="${H - 6}" text-anchor="end">UA</text></svg></figure>`;
  }
  function belt(o) {
    const m = o.model,
      res = l => m.resonances.find(r => r.label === l);
    return {
      lead: 'Una stella simile al Sole, un pianeta gigante e una fascia di asteroidi scolpita dalle risonanze orbitali.',
      canvas:
        'Fascia di asteroidi attorno alla stella Lapis, con il pianeta gigante. Trascina o usa le frecce per ruotare; più e meno regolano la distanza.',
      instrument: 'DINAMICA ORBITALE',
      scale: 'UNITÀ ASTRONOMICHE',
      caption: 'ORBITE KEPLERIANE · RAGGI DI STELLA E GIGANTE INGRANDITI',
      essential:
        'La scena richiede WebGL2. La distribuzione dei semiassi e la spiegazione restano consultabili qui accanto e nelle sezioni seguenti.',
      signal: 'OSSERVAZIONE DINAMICA',
      abstract:
        'Gli asteroidi seguono orbite di Keplero attorno a Lapis. Dove il periodo di un asteroide è una frazione semplice di quello del gigante, le perturbazioni si sommano a ogni passaggio e svuotano intervalli precisi di semiasse.',
      note: 'UA: unità astronomica. I periodi seguono la terza legge di Keplero per una stella di una massa solare.',
      figure: beltFigure(m),
      learningEyebrow: 'LEGGERE LA SCENA',
      learningTitle: 'Le lacune di Kirkwood e i gruppi risonanti.',
      learningIntro: html`<p>Nel 1866 Daniel Kirkwood osservò che i semiassi maggiori degli asteroidi conosciuti evitavano alcuni valori. Quei valori corrispondono a periodi pari a 1/3, 2/5, 3/7 e 1/2 del periodo di Giove. Nella scena il gigante svolge lo stesso ruolo: ogni lacuna si trova dove la terza legge di Keplero assegna un periodo commensurabile con il suo.</p>`,
      equations: html`${eq('01 / KEPLERO', 'Periodo e semiasse', 'P/anno = (a/UA)^(3/2)', 'Il gigante orbita a ' + n(m.giant, 1) + ' UA con un periodo di ' + n(m.giantPeriod, 2) + ' anni.')}${eq('02 / RISONANZA', 'Semiasse risonante p:q', 'a = a_G (q/p)^(2/3)', 'La risonanza 3:1 cade a ' + n(res('3:1').a, 3) + ' UA, la 5:2 a ' + n(res('5:2').a, 3) + ' UA, la 2:1 a ' + n(res('2:1').a, 3) + ' UA.')}${eq('03 / GRUPPI', 'Hilda e Troiani', 'a_3:2 = ' + n(res('3:2').a, 3) + ' UA', 'Gli asteroidi di Hilda compiono tre orbite ogni due del gigante; i Troiani ne condividono il periodo restando 60° avanti o indietro.')}`,
      sections: html`${section(
        'Perché le lacune non si vedono in una fotografia',
        'Le lacune riguardano il semiasse maggiore, cioè una proprietà dell’orbita. La distanza istantanea di un asteroide dalla stella oscilla fra a(1 − e) e a(1 + e): con eccentricità di circa 0,1 la posizione di un corpo della fascia esterna varia di alcuni decimi di unità astronomica e riempie gli intervalli vuoti. Per questo la fascia appare continua.',
        'Il pulsante «Semiasse maggiore» disegna ogni asteroide su un’orbita circolare con lo stesso semiasse. In questa rappresentazione le lacune alle risonanze 3:1, 5:2, 7:3 e 2:1 diventano anelli scuri, come nell’istogramma della scheda.',
      )}${section(
        'Hilda e Troiani',
        'In risonanza 3:2 la longitudine del perielio di un asteroide di Hilda resta legata alla posizione del gigante: gli afeli cadono lontano dal pianeta e l’insieme del gruppo, visto ruotare con il gigante, forma un triangolo. I Troiani occupano le regioni dei punti lagrangiani L4 e L5, dove la combinazione della gravità della stella e del gigante con la rotazione dell’orbita li mantiene in librazione attorno a una posizione stabile.',
      )}${section(
        'L’asteroide osservato da vicino',
        'La vista «Asteroide» mostra un corpo irregolare di circa 60 chilometri, con un piccolo satellite. La superficie conta ' +
          n(327680, 0) +
          ' triangoli nella risoluzione maggiore: crateri con orlo e coltre di materiale espulso, rilievi a più scale e una regolite descritta da una texture di 4096 × 4096 pixel. La luce della stella proietta ombre calcolate con una mappa di profondità.',
        'Anche da vicino la fascia resta un ambiente quasi vuoto: la distanza media fra asteroidi di dimensioni confrontabili supera di molto il milione di chilometri, e gli altri corpi compaiono nel cielo come punti.',
      )}`,
      method: html`<p>Ogni asteroide è una particella con elementi orbitali estratti da un generatore pseudocasuale nella scheda grafica: semiasse dalla distribuzione dell’istogramma, eccentricità, inclinazione, nodo, perielio e anomalia media. A ogni fotogramma la posizione si ottiene risolvendo l’equazione di Keplero E − e sin E = M con il metodo di Newton. La luminosità dipende dall’albedo, dalle dimensioni, dalla distanza dalla stella e dall’angolo di fase.</p><p>Le texture della regolite sono generate da <code>scripts/bake-objects.py</code> per sintesi spettrale periodica: la superficie si ripete senza giunture e viene proiettata sul modello lungo i tre assi. Il canale alfa contiene un campo di quota usato per il rilievo della luce.</p>`,
      course: course([
        [
          '#modulo-M03',
          'Iride · Visualizzazione',
          'istogrammi e scelta degli intervalli per una distribuzione con lacune strette',
        ],
        [
          '#esplorazione/M03-b',
          'Missione L2 · Dimensione e riflettività degli asteroidi',
          'diametri e albedo di asteroidi reali dal database del JPL',
        ],
      ]),
      sources: [
        { href: 'https://ssd.jpl.nasa.gov/', label: 'NASA JPL · Solar System Dynamics' },
        { href: 'https://science.nasa.gov/solar-system/asteroids/', label: 'NASA · Asteroids' },
        {
          href: 'https://ui.adsabs.harvard.edu/abs/1867PAPhS..10..392K',
          label: 'Kirkwood (1867) · On the theory of meteors',
        },
      ],
      modelNote: 'Sistema immaginario · raggi della stella e del gigante ingranditi; orbite e periodi in scala.',
    };
  }
  function beltFacts(o) {
    const m = o.model,
      res = l => m.resonances.find(r => r.label === l);
    return [
      ['Semiasse del gigante', n(m.giant, 1), 'UA'],
      ['Periodo del gigante', n(m.giantPeriod, 2), 'anni'],
      ['Lacuna 3:1', n(res('3:1').a, 3), 'UA'],
      ['Lacuna 5:2', n(res('5:2').a, 3), 'UA'],
      ['Lacuna 2:1', n(res('2:1').a, 3), 'UA'],
      ['Gruppo di Hilda', n(res('3:2').a, 3), 'UA'],
    ];
  }

  // ------------------------------------------------------------------ Faro
  const PULSE = { W: 320, H: 130 };
  function pulsePath(chi, zeta) {
    const v = O.pulseProfile(chi, zeta, 0.4, 180),
      { W, H } = PULSE;
    return v
      .map(
        (y, i) =>
          (i ? 'L' : 'M') +
          (24 + (i / 179) * (W - 34)).toFixed(1) +
          ',' +
          (H - 22 - Math.min(1.2, y) * (H - 40)).toFixed(1),
      )
      .join('');
  }
  function pulsarFigure(o) {
    const chi = (o.model.inclination * Math.PI) / 180,
      { W, H } = PULSE;
    return html`<figure class="object-figure" data-figure="pulse"><h3>PROFILO DEGLI IMPULSI</h3><p>Intensità ricevuta durante un giro, per la direzione da cui la camera osserva la pulsar: angolo fra asse di rotazione e linea di vista <b data-zeta>…</b>.</p><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Profilo degli impulsi in funzione della fase di rotazione"><line class="axis" x1="24" x2="${W - 10}" y1="${H - 22}" y2="${H - 22}"/><path class="curve" d="${pulsePath(chi, 1.2)}"/><line class="mark" data-phase x1="24" x2="24" y1="10" y2="${H - 22}"/><text x="24" y="${H - 6}">0</text><text x="${(W + 14) / 2}" y="${H - 6}" text-anchor="middle">0,5</text><text x="${W - 10}" y="${H - 6}" text-anchor="end">1 giro</text></svg></figure>`;
  }
  function pulsarUpdate(main, o, data) {
    const fig = main.querySelector('[data-figure="pulse"]');
    if (!fig) return;
    const key = Math.round(data.zeta * 200);
    if (fig.dataset.key !== String(key)) {
      fig.dataset.key = String(key);
      fig.querySelector('.curve').setAttribute('d', pulsePath(data.chi, data.zeta));
      fig.querySelector('[data-zeta]').textContent = n((data.zeta * 180) / Math.PI, 0) + '°';
    }
    const x = (24 + data.phase * (PULSE.W - 34)).toFixed(1);
    const mark = fig.querySelector('[data-phase]');
    mark.setAttribute('x1', x);
    mark.setAttribute('x2', x);
  }
  function pulsar(o) {
    const m = o.model;
    return {
      lead: 'Una stella di neutroni che ruota venticinque volte al secondo e invia due fasci di radiazione dai poli magnetici.',
      canvas:
        'Pulsar con le linee del campo magnetico, i fasci dai poli e il vento oltre il cilindro di luce. Trascina o usa le frecce per ruotare; più e meno regolano la distanza.',
      instrument: 'MAGNETOSFERA',
      scale: 'UNITÀ: RAGGIO DELLA STELLA (12 KM)',
      caption: 'ROTAZIONE MOSTRATA ' + n(2.5 / m.period, 1) + ' VOLTE PIÙ LENTA',
      essential:
        'La scena richiede WebGL2. Il profilo degli impulsi e la spiegazione restano consultabili nella scheda e nelle sezioni seguenti.',
      signal: 'OSSERVAZIONE RADIO',
      abstract:
        'L’asse magnetico è inclinato di ' +
        n(m.inclination, 0) +
        '° rispetto all’asse di rotazione. Ogni fascio descrive un cono nel cielo, e un osservatore riceve un impulso quando il cono attraversa la sua linea di vista.',
      note: 'Il campo magnetico è la stima del dipolo nel vuoto, B ≈ 3,2 × 10¹⁹ (P Ṗ)^(1/2) gauss; l’età caratteristica assume un frenamento magnetico dall’inizio.',
      figure: pulsarFigure(o),
      learningEyebrow: 'LEGGERE LA SCENA',
      learningTitle: 'Un faro magnetico e il suo segnale periodico.',
      learningIntro: html`<p>Una stella di neutroni concentra circa una massa e mezza solare in una sfera di dodici chilometri di raggio. La rotazione e il campo magnetico intenso trasformano l’energia di rotazione in radiazione e in un vento di particelle: il periodo cresce lentamente, e da P e dalla sua derivata Ṗ si stimano il campo, l’età e la potenza emessa.</p>`,
      equations: html`${eq('01 / ROTAZIONE', 'Cilindro di luce', 'R_L = cP/2π', 'A ' + n(m.lightCylinder / 1000, 0) + ' km dall’asse la corotazione raggiungerebbe la velocità della luce: le linee di campo che lo attraversano restano aperte.')}${eq('02 / FRENAMENTO', 'Potenza persa dalla rotazione', 'Ė = 4π² I Ṗ / P³', 'Con un momento d’inerzia di 10³⁸ kg m² la pulsar perde ' + sci(m.spinDown, 1) + ' W, ' + n(m.spinDown / 3.828e26, 0) + ' volte la luminosità del Sole.')}${eq('03 / ETÀ', 'Età caratteristica', 'τ = P / (2Ṗ)', 'Il valore è ' + n(m.age / O.SI.year, 0) + ' anni: una stima che presuppone un periodo iniziale molto più breve di quello attuale.')}`,
      sections: html`${section(
        'Perché il segnale è periodico',
        'Il fascio radio parte dal polo magnetico come un cono cavo. Durante la rotazione l’asse magnetico descrive a sua volta un cono attorno all’asse di rotazione, e la linea di vista dell’osservatore attraversa il fascio una volta per giro, oppure due volte se è abbastanza vicina all’equatore da incontrare entrambi i poli. Il grafico della scheda calcola il profilo per la direzione della camera: ruotando la scena si passa da due impulsi a uno solo, fino all’assenza di segnale.',
        'Il periodo è stabile al punto che le pulsar servono da orologi astronomici. Le variazioni dei tempi di arrivo degli impulsi, analizzate come serie temporale, rivelano il frenamento, eventuali compagni in orbita e le perturbazioni del mezzo interstellare.',
      )}${section(
        'Magnetosfera e cilindro di luce',
        'Il plasma che riempie la magnetosfera ruota insieme alla stella lungo le linee di campo chiuse. A distanza R_L dall’asse una corotazione rigida richiederebbe la velocità della luce: le linee che raggiungono il cilindro di luce restano aperte e trasportano verso l’esterno particelle e flusso magnetico. Le loro basi formano le calotte polari, di raggio circa R(R/R_L)^(1/2), pari a ' +
          n(m.polarCap, 0) +
          ' m.',
        'Oltre il cilindro il vento magnetizzato porta con sé un foglio di corrente che separa campi di verso opposto. Con l’asse magnetico inclinato il foglio oscilla in latitudine con ampiezza pari all’inclinazione e si avvolge in una spirale che si allontana alla velocità della luce.',
      )}${section(
        'Materia estrema',
        'La densità media della stella vale ' +
          sci(m.density, 1) +
          ' kg/m³, confrontabile con quella dei nuclei atomici. La gravità superficiale è ' +
          sci(m.gravity, 1) +
          ' m/s² e la velocità di fuga raggiunge il ' +
          n((m.escape / O.SI.c) * 100, 0) +
          '% di quella della luce. Un punto dell’equatore si muove a ' +
          n(m.equatorSpeed / 1000, 0) +
          ' km/s.',
      )}`,
      method: html`<p>Le particelle sono generate nella scheda grafica dal loro indice. Il plasma segue linee di dipolo r = L sin²θ nel riferimento magnetico, ruotato dell’inclinazione e poi della fase di rotazione; i fasci sono coni cavi attorno ai poli; il foglio di corrente segue la latitudine arctan[tan χ sin(φ − Ω(t − r/c))] del modello a monopolo diviso inclinato. Il profilo degli impulsi usa la geometria del vettore rotante: l’angolo fra la linea di vista e il polo vale cos θ = cos χ cos ζ + sin χ sin ζ cos φ, e ogni polo contribuisce con un fascio gaussiano.</p><p>La rotazione è rallentata di ${n(2.5 / m.period, 1)} volte. Le dimensioni sono in scala: il cilindro di luce ha un raggio di ${n(m.lightCylinder / m.radius, 0)} raggi stellari.</p>`,
      course: course([
        ['#modulo-M09', 'Borealis · Serie temporali', 'segnali periodici, stazionarietà e analisi dei residui'],
        ['#modulo-M10', 'Futura · Previsione', 'previsione dei tempi di arrivo a partire da un modello di frenamento'],
      ]),
      sources: [
        { href: 'https://www.atnf.csiro.au/research/pulsar/psrcat/', label: 'ATNF Pulsar Catalogue' },
        {
          href: 'https://ui.adsabs.harvard.edu/abs/1969ApJ...157..869G',
          label: 'Goldreich e Julian (1969) · Pulsar electrodynamics',
        },
        {
          href: 'https://ui.adsabs.harvard.edu/abs/1999ApJ...516..409B',
          label: 'Bogovalov (1999) · On the physics of cold MHD winds from oblique rotators',
        },
        { href: 'https://science.nasa.gov/universe/stars/', label: 'NASA · Stars' },
      ],
      modelNote: 'Pulsar immaginaria · parametri tipici di una pulsar giovane; rotazione rallentata per la visione.',
    };
  }
  function pulsarFacts(o) {
    const m = o.model;
    return [
      ['Periodo', n(m.period * 1000, 0), 'ms'],
      ['Derivata del periodo', sciHTML(m.pdot, 1), 's/s'],
      ['Campo al polo', sciHTML(m.field, 1), 'G'],
      ['Età caratteristica', n(m.age / O.SI.year, 0), 'anni'],
      ['Potenza di frenamento', sciHTML(m.spinDown, 1), 'W'],
      ['Cilindro di luce', n(m.lightCylinder / 1000, 0), 'km'],
    ];
  }

  // ------------------------------------------------------------------ Clio
  function comet(o) {
    const m = o.model;
    return {
      lead: 'Una cometa su un’orbita molto allungata: vicino alla stella il nucleo si attiva e libera una coda di polvere e una di ioni.',
      canvas:
        'Cometa con le code di polvere e di ioni lungo l’orbita attorno alla stella. Trascina o usa le frecce per ruotare; più e meno regolano la distanza.',
      instrument: 'DINAMICA DEI GRANI',
      scale: 'UNITÀ ASTRONOMICHE',
      caption: 'PASSAGGIO AL PERIELIO RIPETUTO OGNI 48 S',
      essential:
        'La scena richiede WebGL2. I parametri dell’orbita e la spiegazione restano consultabili nella scheda e nelle sezioni seguenti.',
      signal: 'OSSERVAZIONE DI UNA COMETA',
      abstract:
        'Clio impiega ' +
        n(m.period, 0) +
        ' anni per un’orbita e trascorre circa ' +
        n(m.activeYears, 1) +
        ' anni entro 3 UA dalla stella, la distanza alla quale il ghiaccio d’acqua comincia a sublimare in modo efficace.',
      note: 'Orbita kepleriana attorno a una stella di una massa solare; le perturbazioni planetarie e le forze non gravitazionali sono trascurate.',
      learningEyebrow: 'LEGGERE LA SCENA',
      learningTitle: 'Perché una cometa ha due code.',
      learningIntro: html`<p>Il nucleo è un corpo di pochi chilometri fatto di ghiacci e polveri. Vicino alla stella i ghiacci sublimano, il gas trascina i grani di polvere e forma la chioma. Da quel momento polvere e gas seguono leggi di moto diverse, e le due code puntano in direzioni diverse.</p>`,
      equations: html`${eq('01 / ORBITA', 'Semiasse e periodo', 'a = q/(1 − e) · P = a^(3/2)', 'Con perielio a ' + n(m.perihelion, 1) + ' UA ed eccentricità ' + n(m.eccentricity, 2) + ' il semiasse vale ' + n(m.a, 1) + ' UA e l’afelio ' + n(m.aphelion, 1) + ' UA.')}${eq('02 / VELOCITÀ', 'Vis viva', 'v² = GM (2/r − 1/a)', 'Al perielio la velocità raggiunge ' + n(m.perihelionSpeed / 1000, 1) + ' km/s; all’afelio scende a ' + n(m.aphelionSpeed / 1000, 2) + ' km/s.')}${eq('03 / POLVERE', 'Pressione di radiazione', 'g_eff = (1 − β) GM/r²', 'Un grano con rapporto β fra pressione di radiazione e gravità si muove come se la stella avesse massa ridotta di un fattore 1 − β.')}`,
      sections: html`${section(
        'La coda di polvere',
        'Ogni grano lasciato dal nucleo prosegue su un’orbita propria. La radiazione della stella esercita una forza che decresce con il quadrato della distanza come la gravità, e il loro rapporto β dipende dalle dimensioni del grano: i grani più piccoli hanno β più grande. Un grano emesso giorni prima si trova così più lontano dalla stella e più indietro lungo l’orbita, e la coda si incurva.',
        'Nella scena ogni grano parte dal nucleo nel momento in cui è stato emesso, con la velocità del nucleo più una piccola velocità di espulsione, e il suo moto sotto la gravità ridotta è integrato con il metodo di Runge-Kutta. È il modello di Finson e Probstein, usato per interpretare le code osservate.',
      )}${section(
        'La coda di ioni',
        'Le molecole del gas vengono ionizzate dalla radiazione ultravioletta e raccolte dal vento stellare, che le trascina a circa 400 km/s. La coda di ioni punta quindi quasi esattamente nella direzione opposta alla stella, con una piccola inclinazione dovuta alla velocità della cometa; il colore blu è l’emissione degli ioni CO⁺.',
      )}${section(
        'Il nucleo',
        'La vista «Nucleo» mostra un corpo a due lobi lungo circa sei chilometri, con superficie scura e chiazze di ghiaccio. I getti partono da regioni attive fisse sulla superficie: durante la rotazione si accendono quando entrano nel lato illuminato. La pressione della radiazione spinge i grani della chioma in direzione opposta alla stella.',
      )}`,
      method: html`<p>La posizione del nucleo deriva dall’equazione di Keplero risolta con il metodo di Newton. Le particelle della coda di polvere sono fino a ${n(1.4, 1)} milioni; per ciascuna la scheda grafica integra il moto dal momento dell’emissione con dieci passi di Runge-Kutta del quarto ordine. L’attività cresce come 1/r² entro 3 UA e si spegne oltre. Il tempo della scena ripete il passaggio da ${n(WINDOW_YEARS, 1)} anni prima a ${n(WINDOW_YEARS, 1)} anni dopo il perielio.</p><p>La texture del nucleo è generata da <code>scripts/bake-objects.py</code>: crosta scura con fosse di sublimazione, terrazze, fratture e ghiaccio esposto.</p>`,
      course: course([
        [
          '#modulo-T00',
          'Basalto · Calcolo scientifico',
          'metodo di Newton per l’equazione di Keplero e integrazione numerica del moto',
        ],
        [
          '#modulo-M07',
          'Annula · Relazioni e regressione',
          'leggi di potenza e rette in scala logaritmica, come l’attività in funzione della distanza',
        ],
      ]),
      sources: [
        { href: 'https://science.nasa.gov/solar-system/comets/', label: 'NASA · Comets' },
        {
          href: 'https://ui.adsabs.harvard.edu/abs/1968ApJ...154..327F',
          label: 'Finson e Probstein (1968) · A theory of dust comets',
        },
        { href: 'https://ssd.jpl.nasa.gov/', label: 'NASA JPL · Solar System Dynamics' },
      ],
      modelNote:
        'Cometa immaginaria · orbita in scala; dimensioni del nucleo e della chioma non rappresentabili alla scala dell’orbita.',
    };
  }
  const WINDOW_YEARS = 1.4;
  function cometFacts(o) {
    const m = o.model;
    return [
      ['Perielio', n(m.perihelion, 2), 'UA'],
      ['Afelio', n(m.aphelion, 1), 'UA'],
      ['Eccentricità', n(m.eccentricity, 2), ''],
      ['Periodo', n(m.period, 1), 'anni'],
      ['Velocità al perielio', n(m.perihelionSpeed / 1000, 1), 'km/s'],
      ['Tempo entro 3 UA', n(m.activeYears, 2), 'anni'],
    ];
  }

  // ------------------------------------------------------------------ Diade
  const LIGHT = { W: 320, H: 130 };
  function lightPath(curve) {
    const { W, H } = LIGHT,
      k = curve.length;
    return curve
      .map(
        (y, i) =>
          (i ? 'L' : 'M') + (24 + (i / (k - 1)) * (W - 34)).toFixed(1) + ',' + (H - 22 - y * (H - 40)).toFixed(1),
      )
      .join('');
  }
  function binaryFigure(o) {
    const { W, H } = LIGHT,
      curve = O.eclipseCurve(o.model, (o.model.inclination * Math.PI) / 180, { samples: 160 });
    return html`<figure class="object-figure" data-figure="eclipse"><h3>CURVA DI LUCE</h3><p>Luce di disco, punto caldo e nana bianca durante un’orbita, per l’inclinazione della camera <b data-inclination>…</b>. Fase 0: la nana rossa passa davanti alla nana bianca.</p><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Curva di luce in funzione della fase orbitale, con l’eclisse"><line class="axis" x1="24" x2="${W - 10}" y1="${H - 22}" y2="${H - 22}"/><path class="curve" d="${lightPath(curve)}"/><line class="mark" data-phase x1="24" x2="24" y1="10" y2="${H - 22}"/><text x="24" y="${H - 6}">0</text><text x="${(W + 14) / 2}" y="${H - 6}" text-anchor="middle">0,5</text><text x="${W - 10}" y="${H - 6}" text-anchor="end">1 orbita</text></svg></figure>`;
  }
  function binaryUpdate(main, o, data) {
    const fig = main.querySelector('[data-figure="eclipse"]');
    if (!fig) return;
    const key = String(Math.round(data.inclination * 100));
    if (fig.dataset.key !== key) {
      fig.dataset.key = key;
      fig
        .querySelector('.curve')
        .setAttribute('d', lightPath(O.eclipseCurve(o.model, data.inclination, { samples: 160 })));
      fig.querySelector('[data-inclination]').textContent = n((data.inclination * 180) / Math.PI, 0) + '°';
    }
    const x = (24 + data.phase * (LIGHT.W - 34)).toFixed(1),
      mark = fig.querySelector('[data-phase]');
    mark.setAttribute('x1', x);
    mark.setAttribute('x2', x);
  }
  function binary(o) {
    const m = o.model,
      Rsun = O.SI.Rsun,
      normal = O.hotSpot(m).normal,
      spotAngle = (Math.atan2(normal[1], normal[0]) * 180) / Math.PI,
      spotPhase = (((-spotAngle / 360) % 1) + 1) % 1;
    return {
      lead: 'Una nana bianca e una nana rossa così vicine che la seconda riempie il proprio lobo di Roche e cede gas alla compagna.',
      canvas:
        'Binaria cataclismica con il lobo di Roche della nana rossa, il flusso di gas e il disco di accrescimento. Trascina o usa le frecce per ruotare; più e meno regolano la distanza.',
      instrument: 'POTENZIALE DI ROCHE',
      scale: 'SEPARAZIONE ' + n(m.a / Rsun, 2) + ' R☉',
      caption: 'UN’ORBITA OGNI 40 S · ' + n(m.period / 40, 0) + ' VOLTE PIÙ LENTA',
      essential:
        'La scena richiede WebGL2. La curva di luce e la spiegazione restano consultabili nella scheda e nelle sezioni seguenti.',
      signal: 'OSSERVAZIONE FOTOMETRICA',
      abstract:
        'Le due stelle compiono un’orbita in ' +
        n(m.hours, 1) +
        ' ore a una distanza di ' +
        n(m.a / 1000, 0) +
        ' km. Il gas attraversa il punto di Lagrange L1, cade verso la nana bianca e forma un disco caldo; il punto in cui il flusso colpisce il bordo del disco brilla più del resto.',
      note:
        'Lobi di Roche secondo Eggleton (1983); raggio di circolarizzazione secondo Warner (1995). Le velocità orbitali sono proiettate per l’inclinazione di ' +
        n(m.inclination, 0) +
        '°.',
      figure: binaryFigure(o),
      learningEyebrow: 'LEGGERE LA SCENA',
      learningTitle: 'Quando una stella cede materia alla compagna.',
      learningIntro: html`<p>Nel riferimento che ruota con la binaria, ogni elemento di gas risente della gravità delle due stelle e della forza centrifuga. Le superfici di uguale potenziale si chiudono attorno a ciascuna stella fino a toccarsi nel punto L1: quella superficie critica è il lobo di Roche. Una stella che lo riempie perde gas attraverso L1.</p>`,
      equations: html`${eq('01 / ORBITA', 'Terza legge di Keplero', 'a³ = G(M₁ + M₂) P² / 4π²', 'Con ' + n(m.primary, 2) + ' e ' + n(m.donor, 2) + ' masse solari e un periodo di ' + n(m.hours, 1) + ' ore la separazione vale ' + n(m.a / Rsun, 3) + ' raggi solari.')}${eq('02 / LOBO', 'Raggio del lobo di Roche', 'r_L/a = 0,49 q^(2/3) / [0,6 q^(2/3) + ln(1 + q^(1/3))]', 'Per la nana rossa, con q = ' + n(m.q, 3) + ', il lobo ha un raggio di ' + n((m.donorLobe * m.a) / Rsun, 3) + ' R☉.')}${eq('03 / DENSITÀ', 'Periodo e densità del donatore', 'ρ = 3π μ / (G P² f³)', 'Una stella che riempie il lobo ha densità media fissata dal periodo: ' + n(m.donorDensity / 1000, 1) + ' g/cm³, il valore di una nana rossa di sequenza principale.')}`,
      sections: html`${section(
        'Il lobo di Roche e la forma della nana rossa',
        'La superficie della nana rossa coincide con l’equipotenziale critica: verso la nana bianca si allunga in una punta che termina in L1, a ' +
          n(m.l1, 3) +
          ' volte la separazione dalla nana bianca. Il modello della scena è calcolato direzione per direzione, cercando con il metodo di bisezione il raggio al quale il potenziale di Roche raggiunge il valore di L1.',
        'La parte della stella vicina a L1 ha gravità efficace minore e appare più scura; la faccia rivolta verso la nana bianca e il disco è riscaldata dalla loro radiazione.',
      )}${section(
        'Flusso, disco e punto caldo',
        'Il gas che attraversa L1 conserva il momento angolare dell’orbita: per questo non può cadere direttamente sulla nana bianca. La traiettoria del flusso nella scena è integrata nel riferimento rotante, con le forze di Coriolis e centrifuga; il gas forma un anello attorno al raggio di circolarizzazione, ' +
          n(m.circularisation, 3) +
          ' volte la separazione, e la viscosità lo trasforma in un disco che trasporta materia verso l’interno e momento angolare verso l’esterno.',
        'Nel disco le maree della nana rossa producono due bracci a spirale, fermi nel riferimento che ruota con la binaria. Dove il flusso urta il bordo si forma il punto caldo, responsabile di una gobba nella curva di luce prima dell’eclisse.',
      )}${section(
        'Eclissi e curva di luce',
        'Per inclinazioni superiori a circa 75° la nana rossa nasconde a ogni orbita la nana bianca e le regioni interne del disco. La curva della scheda è calcolata per la direzione della camera: abbassando il punto di vista sul piano dell’orbita l’eclisse diventa profonda, mentre vista dall’alto la binaria non mostra eclissi.',
        'Il punto caldo irraggia soprattutto verso la direzione da cui arriva il gas, opposta alla velocità del flusso rispetto al bordo del disco. Per Diade quella direzione forma un angolo di ' +
          n(spotAngle, 0) +
          '° con la congiungente delle due stelle, e la gobba culmina alla fase ' +
          n(spotPhase, 2) +
          ', poco prima dell’eclisse.',
      )}`,
      method: html`<p>La nana rossa è un modello di ${n(163842, 0)} vertici costruito sull’equipotenziale critica. Il disco usa fino a ${n(1.5, 1)} milioni di particelle su orbite kepleriane attorno alla nana bianca, con temperatura proporzionale a r^(−3/4); il flusso è descritto da particelle che percorrono la traiettoria balistica calcolata nel worker. La curva di luce approssima la nana rossa con la sfera di raggio pari al suo lobo; il punto caldo sta dove il flusso raggiunge il bordo del disco, a ${n(m.diskRadius, 3)} volte la separazione dalla nana bianca.</p>`,
      course: course([
        ['#modulo-M09', 'Borealis · Serie temporali', 'curve di luce periodiche, fase e ripiegamento dei dati'],
        ['#modulo-T00', 'Basalto · Calcolo scientifico', 'metodo di bisezione e integrazione di equazioni del moto'],
      ]),
      sources: [
        {
          href: 'https://ui.adsabs.harvard.edu/abs/1983ApJ...268..368E',
          label: 'Eggleton (1983) · Approximations to the radii of Roche lobes',
        },
        {
          href: 'https://www.cambridge.org/core/books/cataclysmic-variable-stars/',
          label: 'Warner (1995) · Cataclysmic Variable Stars',
        },
        { href: 'https://science.nasa.gov/universe/stars/', label: 'NASA · Stars' },
      ],
      modelNote: 'Binaria immaginaria · dimensioni e distanze in scala; nana bianca di raggio 0,0102 R☉.',
    };
  }
  function binaryFacts(o) {
    const m = o.model,
      Rsun = O.SI.Rsun;
    return [
      ['Periodo orbitale', n(m.hours, 1), 'ore'],
      ['Separazione', n(m.a / Rsun, 3), 'R☉'],
      ['Rapporto di massa', n(m.q, 3), ''],
      ['Lobo della nana rossa', n((m.donorLobe * m.a) / Rsun, 3), 'R☉'],
      ['L1 dalla nana bianca', n(m.l1, 3), 'a'],
      ['Velocità della nana bianca', n(m.K1 / 1000, 0), 'km/s'],
    ];
  }

  const pages = { 'buco-nero': blackHole, asteroidi: belt, pulsar, cometa: comet, binaria: binary };
  const facts = {
    'buco-nero': blackHoleFacts,
    asteroidi: beltFacts,
    pulsar: pulsarFacts,
    cometa: cometFacts,
    binaria: binaryFacts,
  };
  const updates = { pulsar: pulsarUpdate, binaria: binaryUpdate };
  const controls = {
    'buco-nero': [
      { key: 'doppler', label: 'Doppler e spostamento gravitazionale', on: true },
      { key: 'images', label: 'Immagini secondarie', on: true },
      { key: 'jets', label: 'Getti relativistici', on: true },
      { key: 'photons', label: 'Traiettorie della luce', on: false },
    ],
    asteroidi: [
      { key: 'axes', label: 'Semiasse maggiore', on: false },
      { key: 'groups', label: 'Hilda e Troiani', on: true },
      { key: 'resonances', label: 'Risonanze', on: true },
      { key: 'giant', label: 'Gigante e orbita', on: true },
    ],
    pulsar: [
      { key: 'field', label: 'Linee di campo', on: true },
      { key: 'beams', label: 'Fasci radio', on: true },
      { key: 'wind', label: 'Vento oltre il cilindro', on: true },
      { key: 'cylinder', label: 'Cilindro di luce', on: true },
    ],
    cometa: [
      { key: 'dust', label: 'Coda di polvere', on: true },
      { key: 'ions', label: 'Coda di ioni', on: true },
      { key: 'orbit', label: 'Orbita e limite di attività', on: true },
    ],
    binaria: [
      { key: 'disk', label: 'Disco di accrescimento', on: true },
      { key: 'stream', label: 'Flusso da L1', on: true },
      { key: 'lobes', label: 'Lobi di Roche', on: true },
    ],
  };
  const views = {
    asteroidi: [
      { key: 'belt', label: 'Fascia' },
      { key: 'asteroid', label: 'Asteroide' },
    ],
    pulsar: [
      { key: 'magnetosphere', label: 'Magnetosfera' },
      { key: 'surface', label: 'Superficie' },
    ],
    cometa: [
      { key: 'orbit', label: 'Orbita' },
      { key: 'tail', label: 'Code' },
      { key: 'nucleus', label: 'Nucleo' },
    ],
  };
  const summaries = {
    'buco-nero': 'Disco di accrescimento e getti visti attraverso la lente gravitazionale.',
    pulsar: 'Fasci radio, linee di campo e vento oltre il cilindro di luce.',
    asteroidi: 'Lacune di Kirkwood, Hilda, Troiani e un asteroide craterizzato da vicino.',
    cometa: 'Code di polvere e di ioni calcolate grano per grano lungo l’orbita.',
    binaria: 'Lobo di Roche, flusso da L1, disco di accrescimento ed eclissi.',
  };
  root.GeoObjectTexts = Object.freeze({
    summary: id => summaries[id],
    page: o => pages[o.id](o),
    facts: o => facts[o.id](o),
    controls: id => controls[id] || [],
    views: id => views[id] || [],
    updateFigure: (main, o, data) => updates[o.id]?.(main, o, data),
  });
})(globalThis);
