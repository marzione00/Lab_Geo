/* Read-only teaching view of the actual R source. No evaluation or code rewriting. */
(function (root) {
  'use strict';
  const glossary = {
    rnorm: 'Estrae valori da una distribuzione normale, con media e deviazione standard specificate negli argomenti.',
    runif: 'Estrae valori uniformi nell’intervallo indicato; senza estremi espliciti usa [0, 1].',
    rexp: 'Estrae valori esponenziali; rate indica il tasso, il cui reciproco è la media.',
    rlnorm: 'Estrae valori lognormali; meanlog e sdlog descrivono il logaritmo della variabile.',
    rbinom: 'Simula conteggi binomiali; con size = 1 produce esiti di Bernoulli.',
    replicate: 'Ripete l’espressione per il numero di repliche indicato e ne raccoglie i risultati.',
    sample: 'Campiona gli elementi del vettore; replace = TRUE consente estrazioni con reinserimento.',
    mean: 'Calcola la media aritmetica degli elementi, salvo gli argomenti che ne modificano il trattamento.',
    sd: 'Calcola la deviazione standard campionaria, con denominatore n − 1.',
    var: 'Calcola la varianza campionaria; su più colonne restituisce la matrice di covarianza.',
    quantile: 'Stima i quantili campionari alle probabilità richieste.',
    median: 'Calcola la mediana del campione.',
    IQR: 'Calcola la differenza fra il terzo e il primo quartile.',
    cor: 'Misura la correlazione fra le variabili secondo il metodo richiesto.',
    weighted_mean: 'Calcola una media nella quale ciascun valore contribuisce secondo il proprio peso.',
    'weighted.mean': 'Calcola la media pesata dei valori, usando il vettore dei pesi.',
    cumsum: 'Restituisce le somme cumulative, conservando l’ordine degli elementi.',
    diff: 'Calcola differenze successive; lag indica la distanza fra gli elementi confrontati.',
    sum: 'Somma gli elementi del vettore; applicata a valori logici conta i TRUE.',
    sqrt: 'Calcola la radice quadrata elemento per elemento.',
    log: 'Calcola il logaritmo naturale, se non viene specificata un’altra base.',
    exp: 'Applica la funzione esponenziale a ciascun elemento.',
    log1p: 'Calcola log(1 + x) conservando precisione anche per valori di x vicini a zero.',
    expm1: 'Calcola exp(x) − 1 conservando precisione anche vicino a zero.',
    abs: 'Restituisce il valore assoluto di ciascun elemento.',
    'data.frame': 'Riunisce vettori in colonne nominate della stessa tabella.',
    'expand.grid': 'Costruisce tutte le combinazioni dei valori forniti, utilizzate qui come griglia.',
    matrix: 'Dispone gli elementi in una matrice; nrow e ncol ne specificano le dimensioni.',
    cbind: 'Affianca vettori o matrici per colonne.',
    rbind: 'Accoda tabelle o matrici per righe.',
    t: 'Traspone la matrice, scambiando righe e colonne.',
    sweep: 'Combina una matrice con statistiche riferite alle sue righe o colonne.',
    scale: 'Centra e, salvo diversa richiesta, standardizza le colonne numeriche.',
    factor: 'Rappresenta una variabile categoriale mediante livelli distinti.',
    aggregate: 'Calcola una sintesi separata per i gruppi specificati.',
    tapply: 'Applica una funzione ai sottogruppi individuati dai fattori.',
    apply: 'Applica una funzione alle righe o alle colonne di una matrice.',
    sapply: 'Applica la funzione a ciascun elemento, tentando di semplificare il risultato.',
    lapply: 'Applica la funzione a ciascun elemento e restituisce una lista.',
    ifelse: 'Seleziona elemento per elemento uno dei due valori secondo una condizione logica.',
    switch: 'Sceglie una delle espressioni alternative in base al valore fornito.',
    seq: 'Costruisce una sequenza regolare con estremi, passo o lunghezza indicati.',
    seq_along: 'Produce gli indici da 1 alla lunghezza dell’oggetto.',
    seq_len: 'Produce una sequenza di indici della lunghezza richiesta.',
    rep: 'Ripete i valori; each e times controllano rispettivamente le ripetizioni degli elementi e del vettore.',
    c: 'Combina gli elementi in un vettore.',
    list: 'Raccoglie oggetti anche di tipo diverso in una lista.',
    length: 'Restituisce il numero di elementi dell’oggetto.',
    nrow: 'Restituisce il numero di righe della tabella o della matrice.',
    'is.na': 'Individua i valori mancanti e restituisce un vettore logico.',
    'is.finite': 'Individua i valori numerici finiti, escludendo NA, NaN e gli infiniti.',
    all: 'Verifica se tutte le condizioni logiche sono vere.',
    any: 'Verifica se almeno una delle condizioni logiche è vera.',
    which: 'Restituisce gli indici degli elementi per cui la condizione è vera.',
    order: 'Restituisce gli indici che ordinano i valori.',
    sort: 'Ordina gli elementi del vettore.',
    rank: 'Assegna a ciascuna osservazione il suo rango.',
    duplicated: 'Individua gli elementi già comparsi nel vettore o nella tabella.',
    merge: 'Unisce le tabelle mediante le colonne chiave indicate.',
    subset: 'Seleziona osservazioni o variabili secondo la condizione indicata.',
    'as.numeric': 'Converte in numeri; le stringhe non interpretabili diventano valori mancanti.',
    'as.matrix': 'Converte la struttura in una matrice.',
    'as.vector': 'Converte l’oggetto in un vettore.',
    'as.integer': 'Converte in interi, troncando la parte decimale dei valori numerici.',
    head: 'Seleziona la parte iniziale dell’oggetto; un argomento negativo esclude gli ultimi elementi.',
    tail: 'Seleziona la parte finale dell’oggetto; un argomento negativo esclude i primi elementi.',
    lm: 'Stima un modello lineare mediante la formula specificata.',
    glm: 'Stima un modello lineare generalizzato; family stabilisce distribuzione e collegamento.',
    predict: 'Calcola le previsioni dal modello stimato, eventualmente su nuovi dati.',
    coef: 'Estrae i coefficienti del modello stimato.',
    resid: 'Estrae i residui del modello.',
    hatvalues: 'Estrae le leve, che descrivono la posizione delle osservazioni nello spazio dei predittori.',
    'cooks.distance': 'Calcola la distanza di Cook per valutare l’influenza delle osservazioni.',
    't.test':
      'Esegue il test t nella configurazione indicata; per due campioni indipendenti usa Welch salvo diversa richiesta.',
    'wilcox.test': 'Esegue il test di Wilcoxon nella configurazione specificata.',
    'chisq.test': 'Calcola il test chi quadrato sulla tabella fornita.',
    'fisher.test': 'Calcola il test esatto di Fisher per la tabella di contingenza.',
    'p.adjust': 'Corregge i p-value secondo il metodo scelto per i confronti multipli.',
    'power.t.test': 'Calcola potenza o numerosità per il test t secondo le ipotesi specificate.',
    anova: 'Costruisce la tabella di analisi della varianza o confronta i modelli indicati.',
    'oneway.test': 'Confronta le medie di più gruppi; senza var.equal = TRUE usa l’approccio di Welch.',
    prcomp: 'Calcola le componenti principali tramite decomposizione ai valori singolari.',
    kmeans: 'Suddivide le osservazioni in gruppi minimizzando la dispersione interna.',
    hclust: 'Costruisce un raggruppamento gerarchico dalla matrice delle dissimilarità.',
    cutree: 'Taglia il dendrogramma per ottenere la partizione richiesta.',
    dist: 'Calcola le dissimilarità fra le righe; per impostazione predefinita usa la distanza euclidea.',
    arima: 'Stima il modello ARIMA specificato negli argomenti.',
    'arima.sim': 'Simula una serie temporale dal modello ARIMA indicato.',
    'Box.test': 'Calcola un test di indipendenza seriale secondo il tipo e il ritardo indicati.',
    approx: 'Interpola i valori; per impostazione predefinita usa segmenti lineari.',
    filter: 'Applica il filtro lineare ai valori della serie.',
    dnorm: 'Valuta la densità normale nei punti indicati.',
    pnorm: 'Valuta la probabilità cumulata della distribuzione normale.',
    qnorm: 'Restituisce i quantili della distribuzione normale.',
    dbinom: 'Calcola le probabilità dei possibili conteggi binomiali.',
    dpois: 'Calcola le probabilità dei possibili conteggi di Poisson.',
    qpois: 'Restituisce i quantili della distribuzione di Poisson.',
    dt: 'Valuta la densità della distribuzione t di Student.',
    pt: 'Valuta la probabilità cumulata della distribuzione t di Student.',
    qt: 'Restituisce i quantili della distribuzione t di Student.',
    plogis: 'Trasforma il predittore con la funzione logistica, ottenendo valori fra 0 e 1.',
    solve: 'Risolve il sistema lineare; senza un termine noto calcola l’inversa della matrice.',
    chol: 'Calcola il fattore triangolare della decomposizione di Cholesky.',
    diag: 'Costruisce una matrice diagonale o estrae la diagonale di una matrice.',
    outer: 'Calcola la funzione per tutte le coppie di elementi dei due vettori.',
    rowSums: 'Somma gli elementi di ciascuna riga.',
    rowMeans: 'Calcola la media di ciascuna riga.',
    colMeans: 'Calcola la media di ciascuna colonna.',
    ggplot: 'Associa i dati alle variabili grafiche e avvia la composizione della figura.',
    aes: 'Definisce la corrispondenza fra variabili e proprietà grafiche, come assi, colore e gruppi.',
    geom_point: 'Aggiunge uno strato di punti.',
    geom_line: 'Aggiunge linee che collegano i valori ordinati sull’asse orizzontale.',
    geom_histogram: 'Raggruppa i valori in intervalli e ne rappresenta le frequenze.',
    geom_density: 'Rappresenta una stima smussata della densità.',
    geom_boxplot: 'Rappresenta mediana, quartili, baffi e osservazioni oltre i baffi.',
    geom_col: 'Disegna colonne la cui altezza è il valore fornito.',
    geom_ribbon: 'Rappresenta la fascia compresa fra due limiti verticali.',
    geom_vline: 'Aggiunge un riferimento verticale.',
    geom_hline: 'Aggiunge un riferimento orizzontale.',
    geom_abline: 'Aggiunge una retta con intercetta e pendenza specificate.',
    geom_segment: 'Disegna segmenti fra le coordinate iniziali e finali.',
    geom_area: 'Evidenzia l’area sotto il profilo.',
    geom_raster: 'Rappresenta le celle regolari mediante il colore.',
    labs: 'Specifica titolo, nomi degli assi e altre etichette.',
    coord_equal: 'Mantiene uguale la scala geometrica sui due assi.',
    coord_cartesian: 'Definisce la finestra di visualizzazione cartesiana.',
    point_plot:
      'La funzione del corso costruisce un grafico di punti con ggplot2; il suo sorgente è nello script completo.',
    line_plot:
      'La funzione del corso costruisce un grafico a linee con ggplot2; il suo sorgente è nello script completo.',
    hist_plot: 'La funzione del corso costruisce un istogramma con ggplot2; il suo sorgente è nello script completo.',
    bar_plot:
      'La funzione del corso costruisce un grafico a colonne con ggplot2; il suo sorgente è nello script completo.',
    map_plot: 'La funzione del corso rappresenta la griglia con ggplot2, mantenendo uguali le scale dei due assi.',
    ar_series: 'La funzione del corso simula un processo autoregressivo di ordine uno con varianza marginale unitaria.',
    acf_data: 'La funzione del corso restituisce le autocorrelazioni campionarie, escludendo il ritardo zero.',
    dist_cross: 'La funzione del corso calcola le distanze euclidee fra i punti delle due matrici di coordinate.',
    idw: 'La funzione del corso interpola pesando le osservazioni con l’inverso della distanza elevato alla potenza indicata.',
    cart_fit:
      'La funzione del corso costruisce un albero di classificazione rispettando profondità e numerosità minima delle foglie.',
    cart_predict: 'La funzione del corso percorre l’albero e restituisce la probabilità della foglia raggiunta.',
    metric: 'La funzione del corso raccoglie nomi e valori delle metriche nella tabella di riepilogo.',
    f: 'La funzione del corso formatta i numeri per la visualizzazione, senza modificare i dati del calcolo.',
    'set.seed': 'Fissa lo stato iniziale del generatore pseudocasuale per rendere ripetibile la sequenza.',
    tempfile: 'Prepara un nome di file temporaneo.',
    'write.csv': 'Scrive la tabella in un file CSV nell’ambiente R locale.',
    'read.csv': 'Legge un file CSV e restituisce una tabella.',
    unlink: 'Rimuove i file temporanei indicati.',
    md5sum: 'Calcola l’impronta MD5 del file per confrontarne il contenuto; non ne certifica l’autenticità.',
    readBin: 'Legge il file come sequenza di valori binari.',
    identical: 'Controlla se i due oggetti sono identici per struttura, tipo e valori.',
    stopifnot: 'Interrompe il calcolo se una delle condizioni richieste non è soddisfatta.',
    suppressWarnings: 'Sopprime la visualizzazione degli avvisi generati dall’espressione interna.',
  };
  const esc = root.GeoHTML.escape;
  function tokens(text) {
    return (
      text.match(
        /#[^\n]*|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`|\b(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?\b|[A-Za-z_.][A-Za-z0-9_.]*|<-|\|>|%[^%]*%|[^]/g,
      ) || []
    );
  }
  function highlight(text) {
    const t = tokens(text);
    return t
      .map((v, i) => {
        const cls =
          v[0] === '#'
            ? 'comment'
            : /^['"`]/.test(v)
              ? 'string'
              : /^\d|^\.\d/.test(v)
                ? 'number'
                : /^(?:if|else|for|function|return|TRUE|FALSE|NA|NULL)$/.test(v)
                  ? 'keyword'
                  : t.slice(i + 1).find(x => !/^\s+$/.test(x)) === '(' && /^[A-Za-z_.]/.test(v)
                    ? 'function'
                    : v === '<-'
                      ? 'operator'
                      : '';
        return cls ? '<span class="r-' + cls + '">' + esc(v) + '</span>' : esc(v);
      })
      .join('');
  }
  function calls(source) {
    const clean = tokens(source)
      .map(t => (/^[#'"`]/.test(t) ? ' ' : t))
      .join('');
    return [...new Set([...clean.matchAll(/\b([A-Za-z_.][A-Za-z0-9_.]*)\s*\(/g)].map(m => m[1]))];
  }
  function explain(source) {
    const line = source.trim(),
      assignment = /^([\w.$[\], ]+)\s*<-/.exec(line),
      target = assignment?.[1].trim(),
      names = calls(line);
    let opening = target ? 'Assegna il risultato a ' + target + '.' : '';
    if (target === 'data') opening = 'Prepara la tabella data, utilizzata per i risultati e per l’esportazione.';
    if (target === 'plots') opening = 'Raccoglie in plots le figure ggplot2 che l’esperimento deve produrre.';
    if (target === 'metrics') opening = 'Prepara le metriche numeriche mostrate nel riepilogo dell’esperimento.';
    if (/^\w+\s*<-\s*function\b/.test(line))
      return (
        'Definisce la funzione ' +
        target +
        ': gli argomenti fra parentesi sono gli ingressi; il corpo verrà valutato quando la funzione sarà chiamata.'
      );
    if (/^for\b/.test(line)) opening = 'Esegue il corpo del ciclo per ciascun valore dell’indice.';
    if (/^if\b/.test(line)) opening = 'Valuta la condizione prima di eseguire il ramo corrispondente.';
    const notes = names.filter(
      n => glossary[n] && n !== 'f' && n !== 'list' && n !== 'c' && n !== 'aes' && n !== 'metric',
    );
    const main = notes
      .slice(0, 3)
      .map(n => n + '(): ' + glossary[n])
      .join(' ');
    if (main) return [opening, main].filter(Boolean).join(' ');
    if (names.includes('c')) return opening + ' c() riunisce i valori in un vettore, nell’ordine scritto.';
    if (line.includes('['))
      return opening + ' Le parentesi quadre selezionano gli elementi o le righe e colonne indicate dagli indici.';
    if (/(?:>=|<=|==|!=|>|<|&|\|)/.test(line.replace('<-', '')))
      return (
        opening +
        ' Il confronto restituisce valori logici, utilizzati per distinguere le osservazioni o scegliere una condizione.'
      );
    if (/\^|\*|\/|\+| - /.test(line))
      return (
        opening +
        ' Gli operatori applicano la trasformazione numerica indicata, rispettando parentesi e precedenza delle operazioni.'
      );
    return opening || 'Esegue l’espressione R riportata in questo passaggio.';
  }
  function blocks(source) {
    let number = 1;
    return source.split(/(\n\s*\n)/).flatMap((part, i) => {
      const start = number;
      number += (part.match(/\n/g) || []).length;
      if (i % 2 || !part.trim()) return [];
      return [{ source: part, start, end: start + part.split('\n').length - 1, comment: explain(part) }];
    });
  }
  function parameterScript(a, p) {
    return (
      'p <- list(\n' +
      a.controls
        .map(
          (c, i) =>
            '  # ' +
            c.label +
            (c.help ? ': ' + c.help : '') +
            '\n  ' +
            c.key +
            ' = ' +
            (typeof p[c.key] === 'string'
              ? JSON.stringify(p[c.key])
              : Number.isFinite(p[c.key])
                ? p[c.key]
                : 'NA_real_') +
            (i < a.controls.length - 1 ? ',' : ''),
        )
        .join('\n') +
      '\n)\n# Rende ripetibile la sequenza pseudocasuale.\nset.seed(p$seed)'
    );
  }
  function annotated(a, body = a.code) {
    if (body !== a.code) return body;
    return blocks(body)
      .map(b => '# ' + b.comment.replace(/\n/g, ' ') + '\n' + b.source)
      .join('\n\n');
  }
  function mount(host, a, params, options = {}) {
    let body = a.code,
      steps = blocks(body),
      selected = 0,
      comments = true,
      focused = false,
      active = true;
    host.classList.add('r-terminal');
    host.setAttribute('aria-label', 'Terminale didattico R');
    host.innerHTML =
      '<header class="r-terminal-head"><span class="r-terminal-mark" aria-hidden="true">R</span><div><h2>Il codice dell’esperimento</h2><p>' +
      esc(a.id) +
      '.R</p></div></header><div class="r-terminal-tools"><button type="button" data-r="comments" aria-pressed="true">Commenti</button><button type="button" data-r="focus" aria-pressed="false">Lettura per passi</button><button type="button" data-r="edit">Modifica</button></div><p class="r-terminal-state" role="status">Modello originale · parametri del pannello</p><details class="r-parameters" open><summary>Parametri della configurazione</summary><pre tabindex="0" role="region" aria-label="Parametri della configurazione"><code></code></pre></details><div class="r-code-scroll" role="region" aria-label="Sorgente R commentato" tabindex="0"><ol class="r-code-blocks"></ol></div><div class="r-step-tools"><button type="button" data-r="previous" aria-label="Passaggio precedente">←</button><span class="r-step-count" aria-live="polite"></span><button type="button" data-r="next" aria-label="Passaggio successivo">→</button></div><p class="r-step-reading" aria-live="polite"></p><footer><button type="button" data-r="download">Scarica R completo</button><span>Lettura guidata del sorgente</span></footer>';
    const $ = s => host.querySelector(s),
      list = $('.r-code-blocks');
    // The solution terminal owns stage navigation and downloads when embedded.
    if (options.embedded)
      for (const selector of [
        '.r-terminal-head',
        '[data-r="focus"]',
        '[data-r="edit"]',
        '.r-step-tools',
        '.r-step-reading',
        'footer',
      ])
        $(selector).hidden = true;
    if (options.local) $('.r-parameters').hidden = true;
    function display() {
      if (!active) return;
      list.innerHTML = steps
        .map(
          (b, i) =>
            '<li class="r-code-block"' +
            (i === selected ? ' data-current="true"' : '') +
            (focused && i !== selected ? ' hidden' : '') +
            '><p class="r-code-comment"' +
            (!comments ? ' hidden' : '') +
            '># ' +
            esc(b.comment) +
            '</p><pre><code>' +
            b.source
              .split('\n')
              .map(
                (line, j) =>
                  '<span class="r-source-line"><span class="r-line-number" aria-hidden="true">' +
                  String(b.start + j).padStart(2, '0') +
                  '</span><span>' +
                  highlight(line) +
                  '</span></span>',
              )
              .join('') +
            '</code></pre></li>',
        )
        .join('');
      $('[data-r="previous"]').disabled = selected === 0;
      $('[data-r="next"]').disabled = selected >= steps.length - 1;
      $('.r-step-count').textContent = steps.length
        ? 'Passaggio ' + (selected + 1) + ' / ' + steps.length
        : 'Codice vuoto';
      $('.r-step-reading').textContent =
        body === a.code
          ? steps[selected]?.comment || ''
          : 'Codice personalizzato: le spiegazioni del modello originale sono sospese.';
    }
    function update(p, nextBody = body) {
      params = p;
      if (nextBody !== body) {
        body = nextBody;
        steps = blocks(body);
        if (body !== a.code)
          steps = steps.map(b => ({
            ...b,
            comment: 'Codice personalizzato: leggi e verifica questa istruzione prima di eseguirla.',
          }));
        selected = 0;
        display();
      }
      $('.r-parameters code').innerHTML = highlight(parameterScript(a, params));
      $('.r-terminal-state').textContent =
        body === a.code
          ? options.local
            ? 'Programma originale del corso · esecuzione locale'
            : 'Modello originale · parametri del pannello'
          : 'Codice personalizzato · esecuzione esplicita richiesta';
    }
    function move(direction) {
      selected = Math.max(0, Math.min(steps.length - 1, selected + direction));
      display();
      if (!focused) {
        const row = list.children[selected],
          area = $('.r-code-scroll');
        if (row) area.scrollTop = row.offsetTop - list.offsetTop;
      }
    }
    $('[data-r="comments"]').addEventListener('click', e => {
      comments = !comments;
      e.currentTarget.setAttribute('aria-pressed', String(comments));
      display();
    });
    $('[data-r="focus"]').addEventListener('click', e => {
      focused = !focused;
      e.currentTarget.setAttribute('aria-pressed', String(focused));
      e.currentTarget.textContent = focused ? 'Codice completo' : 'Lettura per passi';
      display();
      $('.r-code-scroll').scrollTop = 0;
    });
    $('[data-r="previous"]').addEventListener('click', () => move(-1));
    $('[data-r="next"]').addEventListener('click', () => move(1));
    $('[data-r="edit"]').addEventListener('click', () => options.edit?.());
    $('[data-r="download"]').addEventListener('click', () => options.download?.());
    display();
    update(params);
    return {
      update,
      destroy() {
        active = false;
        host.replaceChildren();
      },
    };
  }
  root.GeoCodeGuide = Object.freeze({ blocks, explain, highlight, parameterScript, annotated, mount, glossary });
})(typeof window === 'undefined' ? globalThis : window);
