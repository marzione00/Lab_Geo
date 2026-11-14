/* Narrative human hospitality is a teaching metaphor, never an exoplanet habitability score. */
(function (root) {
  'use strict';
  const levels = ['', 'Introduttivo', 'Fondamentale', 'Intermedio', 'Avanzato', 'Ricerca'];
  const rows = [
    ['gaia', 'Gaia', 1, 'terrestrial', 'M01', 1, 0.3, 1, 'Continenti verdi, oceani e una base di ricerca attrezzata.'],
    [
      'temperate',
      'Terrestre temperato',
      1,
      'terrestrial',
      'M01',
      1,
      0.28,
      1.04,
      'Terre emerse, fasce climatiche e approdi protetti.',
    ],
    ['ocean', 'Oceanico', 2, 'terrestrial', 'M05', 1.1, 0.26, 1.02, 'Arcipelaghi radi e piattaforme oceanografiche.'],
    [
      'forest',
      'Forestale',
      2,
      'terrestrial',
      'M06',
      1,
      0.24,
      1.06,
      'Copertura vegetale immaginaria, rilievi e bacini.',
    ],
    ['plains', 'Pianure', 2, 'terrestrial', 'M02', 0.96, 0.25, 1.08, 'Vaste pianure, catene montuose e mari interni.'],
    [
      'swamp',
      'Paludoso',
      3,
      'terrestrial',
      'M06',
      1,
      0.22,
      0.95,
      'Bacini bassi e zone umide rendono il terreno discontinuo.',
    ],
    ['desert', 'Desertico', 3, 'desert', 'M11', 0.85, 0.3, 1.17, 'Dune, altipiani e forti contrasti fra superfici.'],
    ['arctic', 'Artico', 3, 'ice', 'M09', 1.1, 0.55, 1.55, 'Calotte estese, fratture e mari marginali.'],
    ['rocky', 'Roccioso', 4, 'rock', 'T00', 0.6, 0.16, 0.5, 'Crateri, pareti scoscese e affioramenti minerali.'],
    ['barren', 'Arido sterile', 4, 'rock', 'M12', 0.7, 0.2, 0.7, 'Regolite esposta e bacini segnati dagli impatti.'],
    [
      'volcanic',
      'Vulcanico',
      4,
      'lava',
      'M14',
      0.92,
      0.13,
      0.28,
      'Fessure incandescenti attraversano la crosta scura.',
    ],
    [
      'acid',
      'Atmosfera corrosiva',
      5,
      'terrestrial',
      'M03',
      1.1,
      0.62,
      0.67,
      'Coltri atmosferiche opache richiedono osservazioni indirette.',
    ],
    [
      'gas',
      'Gigante gassoso',
      5,
      'gas',
      'M04',
      9.2,
      0.4,
      3.5,
      'Bande, vortici e nubi profonde si osservano dall’orbita.',
    ],
  ];
  const families = rows.map(([id, name, level, category, template, radius, albedo, axis, description]) => ({
    id,
    name,
    level,
    category,
    template,
    radius,
    albedo,
    axis,
    description,
  }));
  const byId = Object.fromEntries(families.map(f => [f.id, f]));
  const pilots = { 'M01-b': 'gaia', 'M03-b': 'ocean', 'M09-e': 'arctic', 'M14-c': 'volcanic', 'M16-e': 'gas' };
  function forWorld(systemIndex, slot, worldId) {
    return byId[pilots[worldId]] || families[(systemIndex * 5 + slot) % families.length];
  }
  const hospitality = [
    '',
    'Base abitabile',
    'Ambiente favorevole',
    'Ambiente impegnativo',
    'Ambiente ostile',
    'Esplorazione estrema',
  ];
  const criteria = [
    '',
    'Dati pronti, lettura guidata e statistiche descrittive.',
    'Selezione dei dati e confronto fra variabili.',
    'Struttura temporale e verifica delle ipotesi.',
    'Qualità delle misure, sensibilità e diagnosi dei modelli.',
    'Scelte metodologiche autonome, incertezza e validazione.',
  ];
  const note =
    'L’ospitalità descrive uno scenario immaginario per l’esploratore umano e rappresenta la difficoltà del progetto. Non misura l’abitabilità astronomica; oceani e vegetazione delle texture sono elementi narrativi.';
  function texture(p, detail = false) {
    if (p.familyId && byId[p.familyId]) return 'assets/space/families/' + p.familyId + (detail ? '-4k' : '') + '.webp';
    return 'assets/space/' + ((p.textureId || p.id) === 'M01' ? 'day' : 'p-' + (p.textureId || p.id)) + '.webp';
  }
  root.GeoFamilies = Object.freeze({ families, byId, levels, hospitality, criteria, forWorld, note, texture });
})(globalThis);
