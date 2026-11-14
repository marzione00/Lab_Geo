// Lossless build-only compaction. Editable SVG sources remain untouched.
// Repeated presentation colours become local classes; all numeric values stay exact.
export function compactCourseSVG(source) {
  if (/<style\b|\b(?:class|style)=/.test(source)) return source;
  const colours = new Map();
  for (const match of source.matchAll(/\bfill="(rgb\([^"<>]*\))"/g))
    colours.set(match[1], (colours.get(match[1]) || 0) + 1);
  let output = source;
  const rules = [];
  for (const [value, count] of colours) {
    const name = 'c' + rules.length,
      original = 'fill="' + value + '"';
    const replacement = 'class="' + name + '"',
      rule = '.' + name + '{fill:' + value + '}';
    if (count * (original.length - replacement.length) <= rule.length) continue;
    output = output.replaceAll(original, replacement);
    rules.push(rule);
  }
  if (rules.length) output = output.replace(/(<svg\b[^>]*>)/, '$1<style>' + rules.join('') + '</style>');
  // SVG 2 href has the same local-fragment target as the legacy xlink spelling.
  output = output.replaceAll('xlink:href=', 'href=').replace(' xmlns:xlink="http://www.w3.org/1999/xlink"', '');
  // A final move immediately after a closed path draws no geometry.
  output = output.replace(/\bd="([^"]*)"/g, (attribute, data) => {
    const compact = data.replace(/([zZ])M[-+0-9.eE, ]+$/, '$1');
    return 'd="' + compact + '"';
  });
  return output;
}
