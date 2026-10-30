// node render.js in.html out.pdf [footerText]
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const [, , inp, out, foot] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + require('path').resolve(inp), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({
    path: out, preferCSSPageSize: true, printBackground: true, displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: `<div style="width:100%;font:7px 'JetBrains Mono',monospace;color:#6c5f74;padding:0 12mm;display:flex;justify-content:space-between">
      <span>${foot || 'PIXEL VERSE · Мультстудия в кармане'}</span><span class="pageNumber"></span></div>`,
  });
  await b.close();
})();
