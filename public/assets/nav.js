/* CDE Toolkit: shared top bar. Rendered in a shadow root so module styles and
   the bar's styles never affect each other. Include right after <body>:
   <script src="/assets/nav.js" data-page="migrate"></script> */
(function () {
  const me = document.currentScript, page = me && me.dataset.page;
  const LINKS = [
    ['home', '/', 'Home'],
    ['migrate', '/modules/migrate.html', 'CDE Sync'],
    ['validate', '/modules/validate.html', 'Validate'],
    ['book-out', '/modules/book-out.html', 'Book out'],
    ['rename', '/modules/rename.html', 'Rename'],
    ['turnaround', '/modules/turnaround.html', 'Review turnaround'],
    ['geofed', '/modules/geofed.html', 'GeoFed'],
    ['federate', '/modules/federate.html', 'Federated views']
  ];
  let signed = false, demo = false;
  try { signed = !!sessionStorage.getItem('cdetk.tok'); demo = sessionStorage.getItem('cdetk.demo') === '1' || new URLSearchParams(location.search).has('demo'); } catch (e) { }

  const host = document.createElement('div');
  host.id = 'cdetk-nav';
  me.parentNode.insertBefore(host, me);
  const root = host.attachShadow({ mode: 'open' });
  root.innerHTML = `<style>
    :host{display:block;all:initial}
    nav{display:flex;flex-wrap:wrap;align-items:center;gap:4px 14px;background:#0c2725;color:#e5ecea;
      font:500 14px/1.3 "Instrument Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
      padding:8px max(16px,env(safe-area-inset-right,0px)) 8px max(16px,env(safe-area-inset-left,0px));border-bottom:2px solid #3fc2ae}
    .brand{font-weight:700;color:#fff;text-decoration:none;margin-right:8px;letter-spacing:-.01em}
    .links{display:flex;flex-wrap:wrap;gap:2px;flex:1;min-width:0}
    a.l{color:#b9cbc6;text-decoration:none;padding:5px 9px;border-radius:5px}
    a.l:hover{color:#fff;background:rgba(255,255,255,.08)}
    a.l[aria-current=page]{color:#0c2725;background:#3fc2ae;font-weight:600}
    a:focus-visible{outline:2px solid #3fc2ae;outline-offset:2px}
    .st{font-size:12px;color:#b9cbc6;display:inline-flex;align-items:center;gap:6px;text-decoration:none}
    .dot{width:8px;height:8px;border-radius:50%;background:${demo ? '#f0c25a' : signed ? '#5fd39b' : '#e38b7a'}}
  </style>
  <nav aria-label="CDE Toolkit">
    <a class="brand" href="/">CDE Toolkit</a>
    <div class="links">${LINKS.slice(1).map(([id, href, label]) =>
      `<a class="l" href="${href}"${id === page ? ' aria-current="page"' : ''}>${label}</a>`).join('')}</div>
    <a class="st" href="/" title="${demo ? 'Demo mode: sample data. Exit on the home page.' : 'Autodesk connection'}"><span class="dot"></span>${demo ? 'Demo mode' : signed ? 'Autodesk connected' : 'Not signed in'}</a>
  </nav>`;
})();
