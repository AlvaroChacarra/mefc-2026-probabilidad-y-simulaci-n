#!/usr/bin/env node
/* PDF de entrega desde main.html: la narrativa vive únicamente en los notebooks.
 * npm ci --prefix tools && npx --prefix tools playwright install chromium
 * python tools/build_notebooks_procesos.py --pdf
 * CHROMIUM_EXECUTABLE permite usar un Chromium ya instalado.
 */
const fs = require('node:fs/promises');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');

async function main() {
  const output = path.resolve(__dirname, '../entrega-2-procesos-estocasticos/output');
  const browser = await chromium.launch({
    ...(process.env.CHROMIUM_EXECUTABLE ? {executablePath: process.env.CHROMIUM_EXECUTABLE} : {}),
    args: ['--no-sandbox'],
  });
  try {
    const page = await browser.newPage();
    await page.goto(pathToFileURL(path.join(output, 'main.html')).href);
    await page.evaluate(() => document.fonts.ready);
    await page.emulateMedia({media: 'print'});
    await page.setViewportSize({width: 673, height: 1000});
    await page.addStyleTag({content: `
      @page { size: A4; margin: 16mm 16mm 18mm; }
      html, body.notebook-report { width: auto; max-width: none; margin: 0; padding: 0; }
      body.notebook-report, body.notebook-report .jp-RenderedHTMLCommon {
        font-size: 10.5pt; line-height: 1.42; background: white;
      }
      body.notebook-report h1 { font-size: 22pt; }
      body.notebook-report h2 { font-size: 17pt; }
      body.notebook-report h3 { font-size: 12.5pt; margin: 15pt 0 7pt; }
      p, li { orphans: 3; widows: 3; }
      p { margin: 0 0 8pt; }
      h1, h2, h3, h4 { break-after: avoid; }
      section + section { break-before: page; }
      .jp-Notebook { min-height: 0 !important; background: white !important; }
      .jp-Cell, .jp-Cell-inputWrapper, .jp-Cell-outputWrapper,
      .jp-OutputArea, .jp-OutputArea-child, .jp-RenderedHTMLCommon { break-inside: auto; }
      .code-details, nav, .formula-hint, .swipe-hint { display: none !important; }
      .math-scroll, .formula { padding: 4pt 0; margin: 5pt 0 10pt; break-inside: avoid; }
      .math-render.block { font-size: 10.5pt; }
      .math-render > svg { max-width: 100% !important; }
      .math-line { max-width: 100%; }
      .math-line svg { max-width: 100% !important; }
      .table-scroll { overflow: visible; margin: 7pt 0 12pt; }
      table { width: 100%; min-width: 0 !important; table-layout: auto; }
      .table-scroll { break-inside: avoid; }
      body.notebook-report .jp-RenderedHTMLCommon table { font-size: 8pt; }
      th, td { padding: 4pt 4pt; white-space: normal !important; }
      .jp-CodeCell table tbody td { white-space: nowrap !important; }
      #ejercicio-3 .jp-CodeCell:last-child { margin-bottom: 0; }
      #ejercicio-3 img { max-height: 130mm; }
      tr { break-inside: avoid; }
      thead { display: table-header-group; }
      img { display: block; max-width: 100%; max-height: 140mm; width: auto; object-fit: contain; margin: auto; break-inside: avoid; }
      pre { font-size: 8pt; white-space: pre-wrap; overflow-wrap: anywhere; }
    `});
    await page.evaluate(() => {
      // Pandas can enforce a natural table width. Fit the whole table, never clip columns.
      for (const table of document.querySelectorAll('table')) {
        const available = table.parentElement.clientWidth;
        table.style.setProperty('table-layout', 'auto', 'important');
        if (table.closest('.jp-CodeCell')) {
          table.style.setProperty('width', 'max-content', 'important');
          table.style.setProperty('max-width', 'none', 'important');
        }
        const actual = Math.max(table.scrollWidth, table.getBoundingClientRect().width);
        if (actual > available) table.style.zoom = String(available / actual);
      }
    });
    if (await page.locator('merror,[data-mml-node="merror"]').count()) {
      throw new Error('Hay fórmulas con errores de renderizado');
    }
    const visibleSections = await page.locator('h2').filter({hasText: /Apartado 3\.[1-4]/}).evaluateAll(nodes => nodes.filter(n => n.getBoundingClientRect().height > 0).length);
    if (visibleSections !== 4) throw new Error('Faltan apartados visibles del Ejercicio 3');
    const target = path.join(output, 'procesos_estocasticos.pdf');
    await page.pdf({path: target, format: 'A4', preferCSSPageSize: true, printBackground: true,
      displayHeaderFooter: true, headerTemplate: '<span></span>',
      footerTemplate: '<div style="width:100%;text-align:center;font:8px Arial;color:#475569">MEFC 2026 · Procesos estocásticos · <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
    });
    // Alias histórico: ambos nombres contienen la misma memoria canónica completa.
    await fs.copyFile(target, path.join(output, 'memoria_detallada.pdf'));
    console.log('PDF completos regenerados desde main.html (dos nombres compatibles).');
  } finally {
    await browser.close();
  }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
