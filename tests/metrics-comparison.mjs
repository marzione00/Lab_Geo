/* Shared by Node regressions and the browser harness; no DOM dependencies. */
const numeric = /^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$/;
function scalar(value) {
  if (value === null) return { kind: 'null', value };
  if (typeof value === 'boolean') return { kind: 'boolean', value };
  if (typeof value === 'number') {
    if (!Number.isFinite(value)) throw Error('Metrica numerica non finita');
    return { kind: 'number', value };
  }
  if (typeof value === 'string') {
    const text = value.trim();
    if (text && numeric.test(text)) {
      const number = Number(text);
      if (!Number.isFinite(number)) throw Error('Metrica numerica fuori intervallo');
      return { kind: 'number', value: number };
    }
    return { kind: 'string', value };
  }
  throw Error('Tipo della metrica non valido');
}
function index(rows) {
  if (!Array.isArray(rows) || !rows.length) throw Error('Metriche assenti');
  const result = new Map();
  for (const row of rows) {
    if (!row || typeof row.grandezza !== 'string' || !row.grandezza.trim() || !Object.hasOwn(row, 'valore'))
      throw Error('Metrica incompleta');
    if (result.has(row.grandezza)) throw Error('Nome di metrica duplicato: ' + row.grandezza);
    result.set(row.grandezza, scalar(row.valore));
  }
  return result;
}
export function compareMetrics(actual, expected) {
  const current = index(actual),
    baseline = index(expected),
    differences = [];
  for (const [name, reference] of baseline) {
    if (!current.has(name)) {
      differences.push({ name, reason: 'metrica mancante' });
      continue;
    }
    const value = current.get(name);
    if (value.kind !== reference.kind)
      differences.push({ name, reason: 'tipo diverso', actual: value, expected: reference });
    else if (value.kind === 'number') {
      const tolerance = Math.max(1e-5, 0.025 * Math.max(Math.abs(value.value), Math.abs(reference.value)));
      if (Math.abs(value.value - reference.value) > tolerance)
        differences.push({
          name,
          reason: 'scarto numerico',
          actual: value.value,
          expected: reference.value,
          tolerance,
        });
    } else if (value.value !== reference.value)
      differences.push({ name, reason: 'valore diverso', actual: value.value, expected: reference.value });
  }
  for (const name of current.keys()) if (!baseline.has(name)) differences.push({ name, reason: 'metrica inattesa' });
  return differences;
}
