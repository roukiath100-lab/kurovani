// Exporte chaque dessin de tools/studio.html en PNG (fond transparent pour les pièces).
// Usage : node tools/render.js [dossier de sortie]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const out = process.argv[2] || path.join(__dirname, '..', 'img');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1000, height: 1300 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(__dirname, 'studio.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(800);
  for (const id of await p.$$eval('svg.art', els => els.map(e => e.id))) {
    await p.locator('#' + id).screenshot({ path: path.join(out, id + '.png'), omitBackground: !id.startsWith('poster') });
    console.log('ok', id);
  }
  await b.close();
})();
