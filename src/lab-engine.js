/* Same R programs for browser execution and standalone reproduction. */
(function (root) {
  'use strict';
  let runtime = null,
    opening = null,
    queue = Promise.resolve(),
    generation = 0,
    latest = 0,
    customRuntime = false;
  const S = root.GeoSecurity;
  const listeners = new Set();
  let state = { phase: 'idle', text: 'Il motore R si avvia al primo calcolo.' };
  const notify = (phase, text) => {
    state = { phase, text };
    listeners.forEach(fn => fn(state));
  };
  function subscribe(fn) {
    listeners.add(fn);
    fn(state);
    return () => listeners.delete(fn);
  }
  function reset() {
    generation++;
    latest++;
    customRuntime = false;
    if (runtime)
      try {
        runtime.close();
      } catch {
        /* the runtime may already be closed */
      }
    runtime = null;
    opening = null;
    queue = Promise.resolve();
    notify('idle', 'Calcolo interrotto. Puoi riavviare R.');
  }
  function deadline(promise, ms, message) {
    let timer;
    return Promise.race([
      promise,
      new Promise((_, reject) => {
        timer = setTimeout(() => {
          reset();
          notify('error', message);
          reject(Error(message));
        }, ms);
      }),
    ]).finally(() => clearTimeout(timer));
  }
  // Installed packages must match the pinned lock; build-only dependencies (cpp11) are simply absent.
  function packageDrift(lock, listing, required = ['ggplot2', 'jsonlite', 'svglite']) {
    const installed = Object.fromEntries(
      String(listing)
        .split(';')
        .filter(Boolean)
        .map(x => x.split('=')),
    );
    const pinned = Object.fromEntries(lock.map(p => [p.package, p.version]));
    return Object.keys(pinned)
      .filter(n => n in installed && installed[n] !== pinned[n])
      .map(n => n + ' ' + installed[n] + ' ≠ ' + pinned[n])
      .concat(required.filter(n => !(n in installed)).map(n => n + ' assente'));
  }
  async function init() {
    if (opening) return opening;
    const gen = generation;
    opening = deadline(
      (async () => {
        notify('loading', 'Avvio di R sul dispositivo…');
        const { WebR, ChannelType } = await import('../vendor/webr/webr.mjs');
        const r = new WebR({
          baseUrl: new URL(
            '../vendor/webr/',
            document.currentScript?.src || new URL('assets/lab-engine.js', location.href),
          ).href,
          channelType: ChannelType.PostMessage,
        });
        runtime = r;
        await r.init();
        if (gen !== generation) throw Error('Avvio interrotto');
        // All binary packages are pinned and hosted with the site. No student data leaves this page.
        const lock = root.GEO_LABS.packages;
        notify('loading', 'Caricamento dei pacchetti R e del sistema grafico…');
        await r.evalRVoid(
          'options(repos=c(GeoStat=' + JSON.stringify(new URL('vendor/r-repo/', location.href).href) + '))',
        );
        await r.installPackages(['ggplot2', 'jsonlite', 'svglite'], {
          repos: new URL('vendor/r-repo/', location.href).href,
          quiet: true,
          mount: false,
        });
        if (gen !== generation) throw Error('Avvio interrotto');
        // Only the pinned packages are queried: installed.packages() would also read the lazily mounted
        // base library (parallel, tcltk, translations) and download 3.4 MB that no laboratory uses.
        const names = lock.map(p => p.package).filter(n => /^[A-Za-z][A-Za-z0-9.]*$/.test(n));
        const drift = packageDrift(
          lock,
          await r.evalRString(
            'p<-c(' +
              names.map(n => JSON.stringify(n)).join(',') +
              ');v<-vapply(p,function(x){d<-suppressWarnings(utils::packageDescription(x,fields="Version"));' +
              'if(is.na(d))"" else d},"");paste(paste0(p,"=",v)[nzchar(v)],collapse=";")',
          ),
        );
        if (drift.length) throw Error('Pacchetti R diversi dalla versione fissata: ' + drift.join(', '));
        await r.evalRVoid(root.GEO_LABS.common);
        notify('ready', 'R pronto · calcolo locale sul dispositivo');
        return r;
      })(),
      180000,
      'Avvio di R scaduto dopo 3 minuti. Puoi riprovare.',
    ).catch(err => {
      if (gen === generation) {
        opening = null;
        if (runtime) {
          try {
            runtime.close();
          } catch {
            /* the runtime may already be closed */
          }
        }
        runtime = null;
        notify('error', 'Avvio di R non riuscito. Riprova oppure scarica lo script per RStudio.');
      }
      throw err;
    });
    return opening;
  }
  const rvalue = v =>
    typeof v === 'string' ? JSON.stringify(v) : Number.isFinite(Number(v)) ? String(Number(v)) : 'NULL';
  function paramsCode(p) {
    return (
      'p <- list(' +
      Object.entries(p)
        .map(([k, v]) => {
          if (!/^[a-z][a-z0-9_]*$/i.test(k) || ['__proto__', 'constructor', 'prototype'].includes(k))
            throw Error('Parametro R non valido.');
          return k + '=' + rvalue(v);
        })
        .join(', ') +
      ')'
    );
  }
  function script(a, p, body = a.code) {
    return (
      '# GeoStat Lab · ' +
      a.title +
      '\n# ' +
      a.goal +
      '\n# Dati sintetici; ambiente e pacchetti documentati nel manifesto.\n# Se necessario: install.packages(c("ggplot2", "jsonlite", "svglite"))\n\n' +
      root.GEO_LABS.common +
      '\n' +
      (root.GeoCodeGuide ? root.GeoCodeGuide.parameterScript(a, p) : paramsCode(p) + '\nset.seed(p$seed)') +
      '\n\n' +
      (root.GeoCodeGuide ? root.GeoCodeGuide.annotated(a, body) : body) +
      '\n\nprint(metrics, row.names=FALSE)\nif (!interactive()) grDevices::cairo_pdf("figure_esperimento.pdf", width=9, height=5.5)\nfor (g in plots) print(g)\nif (!interactive()) grDevices::dev.off()\n# write.csv(data, "dati_esperimento.csv", row.names=FALSE)\n# ggsave("figura.svg", plots[[1]], width=9, height=5.5)\n'
    );
  }
  async function run(a, p, body = a.code, datasetCSV = null, { partial = false } = {}) {
    p = S.parameters(a, p);
    body = S.code(body);
    if (
      datasetCSV !== null &&
      (typeof datasetCSV !== 'string' || datasetCSV.length > 2000000 || datasetCSV.includes('\0'))
    )
      throw Error('Campione CSV non valido.');
    const inputCode =
      datasetCSV === null
        ? ''
        : 'observations <- read.csv(text=' +
          JSON.stringify(datasetCSV) +
          ',stringsAsFactors=FALSE,check.names=FALSE)\n';
    if (customRuntime || body !== a.code) {
      reset();
      customRuntime = body !== a.code;
    }
    const gen = generation,
      jobId = ++latest;
    const job = async () => {
      if (jobId !== latest || gen !== generation) throw Error('Calcolo superato da una nuova configurazione.');
      const r = await init();
      if (gen !== generation) throw Error('Calcolo interrotto');
      notify('running', 'R sta calcolando risultati e figure…');
      const expression = `local({
    e <- new.env(parent=globalenv())
    eval(parse(text=${JSON.stringify(paramsCode(p) + '\nset.seed(p$seed)\n' + inputCode + body)}),envir=e)
    stopifnot(is.data.frame(e$data),is.data.frame(e$metrics),length(e$plots)>=${partial ? 0 : 1}, length(e$plots)<=6, nrow(e$data)<=100000, ncol(e$data)<=80, nrow(e$metrics)<=80)
    figures <- lapply(seq_along(e$plots), function(j) {
      path <- paste0('/tmp/geostat-plot-',j,'.svg')
      ggplot2::ggsave(path, e$plots[[j]], device=svglite::svglite, width=9, height=5.5, bg='#F5F6F3')
      paste(readLines(path,warn=FALSE),collapse='\\n')
    })
    csv <- paste(capture.output(write.csv(e$data,row.names=FALSE)),collapse='\\n')
    jsonlite::toJSON(list(metrics=e$metrics,data=head(e$data,80),rows=nrow(e$data),figures=figures,csv=csv,
      R=R.version.string,ggplot2=as.character(packageVersion('ggplot2')),svglite=as.character(packageVersion('svglite'))),auto_unbox=TRUE,na='null',digits=12)
   })`;
      try {
        const value = await deadline(
          r.evalRString(expression),
          60000,
          'Calcolo interrotto dopo 60 secondi. Riduci il carico o scarica lo script R.',
        );
        if (gen !== generation) throw Error('Calcolo interrotto');
        notify('ready', 'R pronto · risultati ricalcolati');
        return S.result(S.parseJSON(value, S.limits.result), { allowEmptyFigures: partial });
      } catch (err) {
        if (gen === generation) notify('ready', 'R pronto · controlla il messaggio del calcolo');
        throw err;
      }
    };
    const promise = queue.then(job, job);
    queue = promise.catch(() => {});
    return promise;
  }
  root.GeoREngine = Object.freeze({
    packageDrift,
    init,
    run,
    reset,
    script,
    paramsCode,
    subscribe,
    getState: () => ({ ...state }),
  });
})(window);
