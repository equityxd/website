// Post-build fix for GitHub Pages.
//
// GitHub Pages does NOT serve files/directories that start with an underscore (`_`),
// because underscore-prefixed entries are treated as hidden. Astro bundles its hashed
// assets into a directory literally named `_astro`, so on a GitHub Pages deployment
// those assets (CSS/JS) are never fetched -> "no graphics" / broken styles.
//
// This script:
//   1. Renames the `dist/_astro` directory to `dist/astro` (no leading underscore).
//   2. Rewrites every `/_astro/` reference in the generated HTML to `/astro/`.
//
// Run via `npm run build && npm run postbuild`.

import { readdirSync, statSync, renameSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const DIST = 'dist';
const OLD = '_astro';
const NEW = 'astro';

// 1. Rename the directory if it exists.
const astroDir = join(DIST, OLD);
if (existsSync(astroDir)) {
  renameSync(astroDir, join(DIST, NEW));
  console.log(`Renamed ${OLD}/ -> ${NEW}/`);
} else {
  console.log(`No ${OLD}/ directory to rename`);
}

// 2. Rewrite `/_astro/` -> `/astro/` in all HTML files (recursively).
let fixed = 0;
function walk(dir) {
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    const st = statSync(full);
    if (st.isDirectory()) walk(full);
    else if (name.endsWith('.html')) {
      const html = readFileSync(full, 'utf8');
      const after = html.replace(/\/\_astro\//g, '/astro/');
      if (after !== html) {
        writeFileSync(full, after, 'utf8');
        fixed += 1;
      }
    }
  }
}

walk(DIST);
console.log(`Updated ${fixed} HTML file(s): /_astro/ -> /astro/`);
