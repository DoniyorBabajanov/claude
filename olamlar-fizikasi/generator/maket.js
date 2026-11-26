// Barcha rasmlarni A5 sahifalarga haqiqiy o'lchamda joylab, PDF maket yaratadi.
// Foydalanish: node maket.js            -> rangli maket
//              node maket.js --oq-qora  -> oq-qora bosma tekshiruvi
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const gray = process.argv.includes('--oq-qora');
const blender = process.argv.includes('--blender');
const BL = path.join(ROOT, 'blender', 'svg');
const caps = JSON.parse(fs.readFileSync(path.join(__dirname, 'izohlar.json'), 'utf8'));
const files = fs.readdirSync(path.join(ROOT, 'svg')).filter(f => f.endsWith('.svg')).sort();

const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
let pages = files.map(f => {
  const num = f.match(/rasm_(\d)-(\d)/).slice(1).join('.');
  const src = blender && fs.existsSync(path.join(BL, f)) ? path.join(BL, f) : path.join(ROOT, 'svg', f);
  let svg = fs.readFileSync(src, 'utf8').replace(/^<\?xml[^>]*>\s*/, '');
  // har bir SVG ichidagi id lar to'qnashmasligi uchun prefiks
  const p = 'r' + num.replace('.', '_') + '_';
  svg = svg.replace(/id="([^"]+)"/g, `id="${p}$1"`)
           .replace(/url\(#([^)]+)\)/g, `url(#${p}$1)`)
           .replace(/href="#([^"]+)"/g, `href="#${p}$1"`);
  return `<section class="page">
  <div class="run">«Olamlar fizikasi» — rasmlar maketi${blender ? ' (Blender varianti)' : ''}</div>
  <figure>${svg}
    <figcaption><b>Rasm ${num}.</b> ${esc(caps[num] || '')}</figcaption>
  </figure>
  <div class="file">${src.includes('blender') ? 'Blender · ' : ''}${f} · ${(svg.match(/width="([\d.]+mm)"/) || [])[1]} × ${(svg.match(/height="([\d.]+mm)"/) || [])[1]}</div>
</section>`;
}).join('\n');

const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@page { size: 148mm 210mm; margin: 0; }
body { margin: 0; font-family: 'Liberation Serif', 'Times New Roman', serif; }
.page { width: 148mm; height: 210mm; box-sizing: border-box; padding: 18mm 18mm 0 18mm;
  page-break-after: always; position: relative; ${gray ? 'filter: grayscale(1);' : ''} }
.run { font: 7pt 'Liberation Sans', Arial, sans-serif; color: #888; border-bottom: 0.3pt solid #bbb;
  padding-bottom: 1.5mm; margin-bottom: 8mm; }
figure { margin: 0; width: 112mm; }
figure svg { display: block; margin: 0 auto; }
figcaption { font-size: 9pt; line-height: 1.35; margin-top: 3.5mm; color: #222; }
.file { position: absolute; bottom: 10mm; left: 18mm; font: 6.5pt 'Liberation Sans', Arial, sans-serif; color: #999; }
</style></head><body>${pages}</body></html>`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'load' });
  const out = path.join(ROOT, (gray ? 'olamlar_fizikasi_rasmlar_oq-qora' : 'olamlar_fizikasi_rasmlar_maket') + (blender ? '_blender' : '') + '.pdf');
  await page.pdf({ path: out, width: '148mm', height: '210mm', printBackground: true,
    margin: { top: 0, bottom: 0, left: 0, right: 0 } });
  await browser.close();
  console.log('pdf', out);
})();
