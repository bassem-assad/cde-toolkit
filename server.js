// CDE Toolkit local server: serves the public/ folder at http://localhost:3000.
// No dependencies; run with `npm start` (or `node server.js`).
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = Number(process.env.PORT) || 3000;
const HOST = process.env.HOST || '127.0.0.1';
const ROOT = path.join(__dirname, 'public');
const TYPES = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.ico': 'image/x-icon', '.csv': 'text/csv', '.txt': 'text/plain; charset=utf-8'
};

http.createServer((req, res) => {
  let rel;
  let search = '';
  try { const u = new URL(req.url, 'http://x'); rel = decodeURIComponent(u.pathname); search = u.search; }
  catch (e) { res.writeHead(400); return res.end('Bad request'); }
  if (rel !== '/' && !path.extname(rel) && !rel.endsWith('/')) { res.writeHead(301, { Location: rel + '/' + search }); return res.end(); }
  if (rel.endsWith('/')) rel += 'index.html';
  const file = path.join(ROOT, path.normalize(rel));
  if (!file.startsWith(ROOT + path.sep)) { res.writeHead(403); return res.end('Forbidden'); }
  fs.readFile(file, (err, data) => {
    if (err) { res.writeHead(404, { 'Content-Type': 'text/plain' }); return res.end('Not found'); }
    res.writeHead(200, {
      'Content-Type': TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream',
      'Cache-Control': 'no-cache',
      'X-Content-Type-Options': 'nosniff',
      'Referrer-Policy': 'no-referrer'
    });
    res.end(data);
  });
}).listen(PORT, HOST, () => {
  console.log(`CDE Toolkit is running: http://localhost:${PORT}`);
  console.log(`APS callback URL to register: http://localhost:${PORT}/`);
  console.log('Press Ctrl+C to stop.');
});
