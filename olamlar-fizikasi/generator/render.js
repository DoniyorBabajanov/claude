// SVG -> 300 dpi PNG (Chromium orqali). Foydalanish: node render.js [rasm_2-1 ...]
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const SVG_DIR = path.join(__dirname, '..', 'svg');
const PNG_DIR = path.join(__dirname, '..', 'png');
const DPI = 300;

(async () => {
  const only = process.argv.slice(2);
  const files = fs.readdirSync(SVG_DIR).filter(f => f.endsWith('.svg'))
    .filter(f => !only.length || only.includes(f.replace('.svg', '')));
  fs.mkdirSync(PNG_DIR, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const f of files.sort()) {
    const svg = fs.readFileSync(path.join(SVG_DIR, f), 'utf8');
    const wmm = parseFloat(svg.match(/width="([\d.]+)mm"/)[1]);
    const hmm = parseFloat(svg.match(/height="([\d.]+)mm"/)[1]);
    const w = Math.ceil(wmm / 25.4 * DPI), h = Math.ceil(hmm / 25.4 * DPI);
    const body = svg.replace(/^<\?xml[^>]*>\s*/, '')
      .replace(/width="[\d.]+mm" height="[\d.]+mm"/, `width="${w}" height="${h}"`);
    await page.setViewportSize({ width: w, height: h });
    await page.setContent(`<html><body style="margin:0;background:#fff">${body}</body></html>`);
    await page.waitForTimeout(50);
    await page.screenshot({ path: path.join(PNG_DIR, f.replace('.svg', '.png')),
      clip: { x: 0, y: 0, width: w, height: h } });
    console.log('png', f, w + 'x' + h);
  }
  await browser.close();
})();
