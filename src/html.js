/* One escaping rule for every view that builds markup from strings, and the Trusted Types default policy. */
(function (root) {
  'use strict';
  const entities = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
  const escape = value => String(value ?? '').replace(/[&<>"']/g, c => entities[c]);
  const RAW = Symbol('GeoHTML.raw');
  // Marks markup that was already built and escaped elsewhere.
  const raw = value => ({ [RAW]: String(value ?? '') });
  // Tagged template: every interpolated value is escaped unless wrapped with raw().
  const html = (strings, ...values) =>
    strings.reduce((out, part, i) => {
      if (i >= values.length) return out + part;
      const v = values[i];
      return out + part + (v && typeof v === 'object' && RAW in v ? v[RAW] : escape(v));
    }, '');
  // With `require-trusted-types-for 'script'` in the CSP every HTML and script-URL sink passes through
  // this policy. Escaped text cannot form tags, so only real markup can trip these checks.
  const scriptTag = /<script\b/i,
    handler = /<[a-z][^>]*\son[a-z]+\s*=/i,
    scriptUrl = /\b(?:href|src|action|formaction)\s*=\s*["']?\s*javascript:/i;
  function checkedHTML(markup) {
    const text = String(markup);
    if (scriptTag.test(text) || handler.test(text) || scriptUrl.test(text))
      throw new TypeError('GeoHTML: markup with executable content rejected');
    return text;
  }
  function checkedScriptURL(value) {
    const url = new URL(String(value), root.location?.href);
    if (url.protocol !== 'blob:' && url.origin !== root.location?.origin)
      throw new TypeError('GeoHTML: script URL outside the site rejected');
    return String(value);
  }
  let policy = null;
  try {
    if (root.trustedTypes?.createPolicy && !root.trustedTypes.defaultPolicy)
      policy = root.trustedTypes.createPolicy('default', {
        createHTML: checkedHTML,
        createScriptURL: checkedScriptURL,
        createScript: () => {
          throw new TypeError('GeoHTML: dynamic code is not allowed');
        },
      });
  } catch (err) {
    root.console?.warn('GeoHTML: Trusted Types policy unavailable.', err);
  }
  root.GeoHTML = Object.freeze({ escape, html, raw, checkedHTML, checkedScriptURL, trusted: () => Boolean(policy) });
})(globalThis);
