#!/usr/bin/env node
// Build-time MathJax: self-contained SVG paths, no browser scripts or math fonts.
const {mathjax} = require('mathjax-full/js/mathjax.js');
const {MathML} = require('mathjax-full/js/input/mathml.js');
const {SVG} = require('mathjax-full/js/output/svg.js');
const {liteAdaptor} = require('mathjax-full/js/adaptors/liteAdaptor.js');
const {RegisterHTMLHandler} = require('mathjax-full/js/handlers/html.js');
const fs = require('fs');
const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
const doc = mathjax.document('', {
  InputJax: new MathML(), OutputJax: new SVG({fontCache: 'none'})
});
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const result = input.map(({mathml, display}) => {
  const node = doc.convert(mathml, {display, em: 17, ex: 8.5});
  const svg = adaptor.firstChild(node);
  const source = adaptor.outerHTML(svg);
  if (/data-mml-node="merror"/.test(source)) throw new Error('Invalid MathML');
  return {svg: source, widthEx: parseFloat(adaptor.getAttribute(svg, 'width'))};
});
process.stdout.write(JSON.stringify(result));
