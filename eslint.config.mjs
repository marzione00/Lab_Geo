// Lint rules for hand-written code; generated, vendored and archived files are excluded.
import js from '@eslint/js';
import globals from 'globals';

export default [
  { ignores: ['dist/**', 'vendor/**', 'node_modules/**', 'assets/**', 'materiali/**', 'qa/**', 'moduli/**', 'content/**'] },
  js.configs.recommended,
  {
    files: ['src/**/*.js'],
    languageOptions: { ecmaVersion: 2024, sourceType: 'script', globals: { ...globals.browser } },
    rules: {
      complexity: ['warn', 15],
      'no-unused-vars': ['error', { argsIgnorePattern: '^_', varsIgnorePattern: '^_', caughtErrors: 'none' }],
      'no-empty': 'error',
      eqeqeq: ['error', 'smart'],
    },
  },
  { files: ['src/cosmos-worker.js'], languageOptions: { globals: { ...globals.worker } } },
  {
    files: ['scripts/**/*.mjs', 'tests/**/*.mjs'],
    languageOptions: { ecmaVersion: 2024, sourceType: 'module', globals: { ...globals.node } },
    rules: { complexity: ['warn', 15], 'no-unused-vars': ['error', { argsIgnorePattern: '^_', varsIgnorePattern: '^_', caughtErrors: 'none' }] },
  },
  {
    files: ['tests/**/*.js'],
    languageOptions: {
      ecmaVersion: 2024,
      sourceType: 'module',
      globals: { ...globals.browser, GeoREngine: 'readonly', GeoSecurity: 'readonly', GEO_LABS: 'readonly', GEO_QA_BASELINES: 'readonly' },
    },
  },
  { files: ['tests/**/*.cjs'], languageOptions: { sourceType: 'commonjs', globals: { ...globals.node } } },
];
