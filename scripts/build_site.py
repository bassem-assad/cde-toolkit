#!/usr/bin/env python3
"""Rebuild the CDE Toolkit marketing pages from scripts/site_data.py.

    python3 scripts/build_site.py

Generates: public/index.html (landing), public/tools/*.html (one per tool) and
public/admin-guide.html. It also refreshes the shared header and footer inside the
hand-written pages (about.html, contact.html). Needs Python 3 and Pillow (pip install pillow)
only to read screenshot sizes.
"""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_data import FAQ, GROUPS, SCOPES, TOOLS  # noqa: E402

try:
    from PIL import Image
except ImportError:  # sizes are optional
    Image = None

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
E = html.escape

NAV = [("tools", "Tools", "/#tools"), ("how", "How it works", "/#how"), ("admin", "Admin guide", "/admin-guide.html"),
       ("faq", "FAQ", "/#faq"), ("about", "About", "/about.html"), ("contact", "Contact", "/contact.html")]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">')


def header(current):
    links = "".join(f'<a href="{href}"{" aria-current=\"page\"" if key == current else ""}>{label}</a>' for key, label, href in NAV)
    return ('<!--site-header-->\n<header class="deep">\n  <div class="wrap">\n    <a class="logo" href="/">CDE<span>·</span>Toolkit</a>\n'
            f'    <nav aria-label="Main">{links}</nav>\n    <a class="btn pri" href="/app/">Open the app</a>\n  </div>\n</header>\n<!--/site-header-->')


def footer():
    return ('<!--site-footer-->\n<footer>\n  <div class="wrap">\n    <nav aria-label="Footer"><a href="/app/">Open the app</a><a href="/#tools">Tools</a>'
            '<a href="/admin-guide.html">Admin guide</a><a href="/#requirements">Requirements</a><a href="/#security">Security</a>'
            '<a href="/about.html">About</a><a href="/contact.html">Contact</a><a href="/terms.html">Terms of Use</a><a href="/privacy.html">Privacy</a></nav>\n'
            '    <p>© 2026 Bassem Assad. All rights reserved.</p>\n'
            '    <p>Autodesk, Autodesk Construction Cloud, Forma and Revit are registered trademarks or trademarks of Autodesk, Inc. ProjectWise is a trademark of Bentley Systems. '
            'SharePoint is a trademark of Microsoft. InEight is a trademark of InEight Inc. CDE Toolkit is an independent product and is not affiliated with or endorsed by them.</p>\n'
            '  </div>\n</footer>\n<!--/site-footer-->')


def page(title, desc, body, current, extra_head="", extra_body=""):
    return (f'<!doctype html>\n<html lang="en-AU">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            f'<title>{E(title)}</title>\n<meta name="description" content="{E(desc)}">\n'
            f'<meta property="og:title" content="{E(title)}">\n<meta property="og:description" content="{E(desc)}">\n<meta property="og:type" content="website">\n'
            f'<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n{FONTS}\n<link rel="stylesheet" href="/assets/site.css">\n{extra_head}</head>\n<body>\n'
            f'{header(current)}\n{body}\n{footer()}\n{extra_body}</body>\n</html>\n')


def img(name, alt, lazy=True, cls=""):
    path = PUB / "assets" / "shots" / f"{name}.jpg"
    size = ""
    if Image and path.exists():
        w, h = Image.open(path).size
        size = f' width="{w}" height="{h}"'
    return f'<img src="/assets/shots/{name}.jpg" alt="{E(alt)}"{size}{" loading=\"lazy\" decoding=\"async\"" if lazy else ""}{f" class=\"{cls}\"" if cls else ""}>'


def ul(items, cls):
    return f'<ul class="{cls}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


# ----------------------------------------------------------------- landing
OUTCOMES = [
    ("A cleaner CDE from the start", "Check names and attributes before files go in, and correct them on the way in. CDE Sync and the File validator work from your own naming standard."),
    ("Less manual coordination", "Build a Model Coordination view for each location, and see on a map which locations are missing a discipline."),
    ("Controlled change", "Book drawings out through your review workflow, with files that are already booked out caught before they cause a conflict."),
    ("Evidence, not opinions", "Download failure reports to send to suppliers, and see which review step, reviewer or company is running late."),
    ("Lower risk", "Preview before anything changes, act only with the signed-in person's own permissions, and try every tool on sample data first."),
    ("Nothing to install or host", "It's a website. There's no server or add-in to roll out, and an update reaches everyone at once."),
]
ROLES = ["BIM managers", "Information managers", "Document controllers", "BIM coordinators", "Project directors", "Consultants", "Contractors"]


def landing():
    tools_html = ""
    for title, slugs in GROUPS:
        tools_html += f'      <h3 class="grp">{E(title)}</h3>\n'
        for s in slugs:
            t = TOOLS[s]
            tools_html += (f'      <article class="tool"><h3><a href="/tools/{s}.html">{E(t["name"])}</a></h3>'
                           f'<div><p>{t["summary"]}</p><div class="meta"><span class="tag {t["tagkind"]}">{E(t["tag"])}</span>'
                           f'<a class="more" href="/tools/{s}.html">Who it\'s for and what it needs</a></div></div>'
                           f'<a class="thumb" href="/tools/{s}.html" tabindex="-1" aria-hidden="true">{img(t["images"][0][0], t["images"][0][1])}</a></article>\n')
    outcomes = "".join(f"<li><b>{E(a)}</b><p>{E(b)}</p></li>" for a, b in OUTCOMES)
    roles = "".join(f"<li>{E(r)}</li>" for r in ROLES)
    faq = "".join(f"<details><summary>{E(q)}</summary><p>{a}</p></details>" for q, a in FAQ)
    body = f'''
<section class="deep hero" style="padding:0">
  <div class="wrap">
    <div>
      <p class="eyebrow" style="color:var(--ondeep2)">For BIM, digital engineering and information managers</p>
      <h1 style="margin-top:14px">Keep your Autodesk Forma project files in order.</h1>
      <p class="lead">CDE Toolkit moves, checks, books out and renames files in Autodesk Construction Cloud, and builds federated model views, from one browser tab. Your files go straight between your systems and ACC.</p>
      <div class="cta">
        <a class="btn pri" href="/app/?demo=1">Try the demo</a>
        <a class="btn sec" href="#tools">See the tools</a>
      </div>
      <p class="note">The demo uses sample data. No sign-in, nothing is sent to Autodesk.</p>
    </div>
    <div class="anat" aria-label="Example of a file name checked against a naming standard">
      <span class="eyebrow">Illustration: a file name against a naming standard</span>
      <div class="fname" role="img" aria-label="DPI-ARC-STN-A-MOD-0001-C02.rvt">
        <span class="seg"><b>DPI</b><i>Project</i></span><span class="sep">-</span>
        <span class="seg"><b>ARC</b><i>Originator</i></span><span class="sep">-</span>
        <span class="seg"><b>STN-A</b><i>Zone</i></span><span class="sep">-</span>
        <span class="seg"><b>MOD</b><i>Type</i></span><span class="sep">-</span>
        <span class="seg"><b>0001</b><i>Number</i></span><span class="sep">-</span>
        <span class="seg"><b>C02</b><i>Revision</i></span><span class="ext">.rvt</span>
      </div>
      <ul class="checks">
        <li><span class="mark ok">✓</span><span><code>DPI-ARC-STN-A-MOD-0001-C02.rvt</code><small>Matches the standard, ready to transfer</small></span></li>
        <li><span class="mark no">✕</span><span><code>DPI-ARC-MOD-0001.rvt</code><small>3 name parts, standard has 6. Skipped with the reason shown</small></span></li>
        <li><span class="mark mv">→</span><span><code>Model.rvt → Model_20260915.rvt</code><small>Upload date added to the name, previewed before it changes</small></span></li>
      </ul>
    </div>
  </div>
</section>

<section id="why">
  <div class="wrap">
    <span class="eyebrow">What it gives your team</span>
    <h2>Less rework in your CDE, and a clearer view of where it stands.</h2>
    <ul class="outcomes">{outcomes}</ul>
    <ul class="pills" aria-label="Who it is for">{roles}</ul>
  </div>
</section>

<section id="tools">
  <div class="wrap">
    <span class="eyebrow">Seven tools, one sign-in</span>
    <h2>Everything you do over and over in ACC, in one place.</h2>
    <p class="sub">Each tool works on its own. Sign in once with your Autodesk account and move between them from the top bar. Open any tool to see who it's for, what it does and what it needs.</p>
    <div class="tools">
{tools_html}    </div>
  </div>
</section>

<section id="how">
  <div class="wrap">
    <span class="eyebrow">How it works</span>
    <h2>One setup step for the ACC admin, then nothing to install.</h2>
    <ol class="steps">
      <li><b>Admin adds the app</b><p>Your ACC hub admin adds the CDE Toolkit Client ID under Hub Admin, Custom Integrations. It's a one-off step, and it's also your organisation's approval. The <a href="/admin-guide.html">admin guide</a> has the steps.</p></li>
      <li><b>People sign in as themselves</b><p>Each person signs in with their own Autodesk account. The toolkit can only do what that person's ACC permissions already allow.</p></li>
      <li><b>Work in the browser</b><p>Files go directly between the source system and ACC. Nothing is uploaded to or stored on our servers.</p></li>
    </ol>
  </div>
</section>

<section id="requirements">
  <div class="wrap">
    <span class="eyebrow">Requirements</span>
    <h2>Check these before you pilot it.</h2>
    <div class="two">
      <div>
        <h3>You need</h3>
        <ul>
          <li>An ACC (Autodesk Forma) hub on a full subscription such as Forma Data Management, Forma Build or Forma Design Collaboration.</li>
          <li>A hub admin who can add a Custom Integration.</li>
          <li>Model Coordination, for Federated views.</li>
          <li>A current version of Chrome or Edge.</li>
        </ul>
      </div>
      <div>
        <h3>Optional sources for CDE Sync</h3>
        <ul>
          <li>ProjectWise and InEight servers must allow the toolkit's web address (CORS).</li>
          <li>SharePoint needs a one-off Microsoft Entra app registration.</li>
          <li>Local folders and CSV attribute exports need nothing extra.</li>
        </ul>
      </div>
    </div>
    <div class="callout"><b>Trial and Essentials hubs can't use it</b>Autodesk Support notes that the Custom Integrations tab is hidden for trial hubs and for hubs on Essentials subscriptions. Those hubs can't add CDE Toolkit. Ask your admin whether the tab is visible before you plan a pilot.</div>
  </div>
</section>

<section id="security">
  <div class="wrap">
    <span class="eyebrow">Security and data</span>
    <h2>Built so your files don't pass through us.</h2>
    <div class="two">
      <ul>
        <li>The toolkit runs in your browser. Files travel between your source system and Autodesk, not through our servers.</li>
        <li>Sign-in uses Autodesk's OAuth 2.0 with PKCE. There's no client secret and no password is stored.</li>
        <li>The sign-in token stays in your browser tab and is cleared when you sign out or close the tab.</li>
      </ul>
      <ul>
        <li>There are no advertising or analytics scripts on this site or in the app.</li>
        <li>Tools that change data (CDE Sync, Rename, File Book Out, Federated views) show what will happen before they do it. Test on non-critical projects first and keep your own backups.</li>
        <li>See the <a href="/admin-guide.html">admin guide</a> for the permissions requested and a data-flow summary, and the <a href="/terms.html">Terms of Use</a> and <a href="/privacy.html">Privacy</a> pages.</li>
      </ul>
    </div>
  </div>
</section>

<section id="faq">
  <div class="wrap">
    <span class="eyebrow">Questions</span>
    <h2>What teams and IT ask first.</h2>
    <div class="faq">{faq}</div>
    <p class="sub">Something else? <a href="/contact.html">Send a message</a>.</p>
  </div>
</section>

<section class="band" id="pilot">
  <div class="wrap">
    <div>
      <h2 style="color:#fff">Want to pilot it?</h2>
      <p>Pricing is being finalised. If you'd like to try CDE Toolkit on a non-critical project, send a message. Meanwhile the demo shows every tool on sample data.</p>
    </div>
    <div class="cta">
      <a class="btn pri" href="/contact.html">Request a pilot</a>
      <a class="btn sec" href="/app/?demo=1">Try the demo</a>
    </div>
  </div>
</section>'''
    head_js = ('<script>\n/* Autodesk sends the browser back to this address after sign-in. The app finishes the sign-in. */\n'
               "if (/[?&]state=aps(&|$)/.test(location.search)) location.replace('/app/' + location.search);\n</script>\n")
    return page("CDE Toolkit | Tools for Autodesk Construction Cloud",
                "Move, check, book out and rename files in Autodesk Construction Cloud, and build federated model views, from one browser tab. Your files go straight between your systems and ACC.",
                body, "", extra_head=head_js)


# ------------------------------------------------------------- tool pages
def tool_page(slug):
    t = TOOLS[slug]
    group = next(g for g, s in GROUPS if slug in s)
    figs = "".join(f'<figure class="fig">{img(n, alt, lazy=(i > 0))}<figcaption>{E(cap)} <em>Sample data.</em></figcaption></figure>'
                   for i, ((n, alt), cap) in enumerate(zip(t["images"], t["captions"])))
    steps = ""
    if t.get("steps"):
        steps = ('<h3 style="margin-bottom:10px;font-size:16px">The steps</h3>'
                 + '<ol class="stepstrip">' + "".join(f"<li>{E(s)}</li>" for s in t["steps"]) + "</ol>"
                 + f'<p class="sub" style="margin-bottom:22px">{E(t["stepnote"])}</p>')
    benefits = '<ul class="benefit">' + "".join(f"<li><b>{E(a)}</b><span>{E(b)}</span></li>" for a, b in t["benefits"]) + "</ul>"
    related = "".join(f'<a href="/tools/{r}.html"><b>{E(TOOLS[r]["name"])}</b><span>{E(TOOLS[r]["kicker"])}</span></a>' for r in t["related"])
    body = f'''
<section class="deep thero" style="padding:0">
  <div class="wrap">
    <p class="crumb"><a href="/#tools">Tools</a> › {E(group)}</p>
    <h1>{E(t["name"])}</h1>
    <p class="lead">{E(t["kicker"])}</p>
    <div class="cta">
      <a class="btn pri" href="/modules/{t["module"]}.html?demo=1">Try the demo</a>
      <a class="btn sec" href="/contact.html">Request a pilot</a>
      <span class="tag">{E(t["tag"])}</span>
    </div>
  </div>
</section>

<div class="wrap figs{" two-up" if len(t["images"]) > 1 else ""}">{figs}</div>

<section class="tsec">
  <div class="wrap cols">
    <div><h2>Who it's for</h2>{ul(t["who"], "tick")}</div>
    <div><h2>Why it helps your company</h2>{benefits}</div>
  </div>
</section>

<section class="tsec">
  <div class="wrap">
    <h2>What it does</h2>
    {steps}
    {ul(t["does"], "tick")}
    <div class="scenario"><span class="eyebrow">Example scenario</span><p>{E(t["scenario"])}</p></div>
  </div>
</section>

<section class="tsec">
  <div class="wrap cols">
    <div><h2>What you need</h2>{ul(t["needs"], "tick")}
      <p class="sub" style="margin-top:14px">See the <a href="/#requirements">requirements</a> for hub plans, and the <a href="/admin-guide.html">admin guide</a> for the one-off setup.</p></div>
    <div><h2>Good to know</h2>{ul(t["limits"], "dash")}</div>
  </div>
</section>

<section class="tsec">
  <div class="wrap">
    <h2>Related tools</h2>
    <div class="related">{related}</div>
  </div>
</section>

<section class="band" id="pilot">
  <div class="wrap">
    <div>
      <h2 style="color:#fff">See {E(t["name"])} on sample data.</h2>
      <p>The demo needs no sign-in and sends nothing to Autodesk. When you're ready, ask for a pilot on a non-critical project.</p>
    </div>
    <div class="cta">
      <a class="btn pri" href="/modules/{t["module"]}.html?demo=1">Try the demo</a>
      <a class="btn sec" href="/contact.html">Request a pilot</a>
    </div>
  </div>
</section>'''
    return page(f'{t["name"]} | CDE Toolkit', t["kicker"], body, "tools")


# ------------------------------------------------------------- admin guide
def admin_page():
    scopes = "".join(f"<tr><td><code>{E(a)}</code></td><td>{E(b)}</td></tr>" for a, b in SCOPES)
    body = f'''
<section class="deep thero" style="padding:0">
  <div class="wrap">
    <p class="crumb"><a href="/">CDE Toolkit</a> › Admin guide</p>
    <h1>Add CDE Toolkit to your ACC hub.</h1>
    <p class="lead">A one-off setup for your hub admin, about five minutes. This guide covers the steps, the permissions requested and where your data goes, so your IT team can review it.</p>
    <div class="cta">
      <a class="btn pri" href="/contact.html">Request a pilot</a>
      <a class="btn sec" href="/app/?demo=1">Try the demo first</a>
    </div>
  </div>
</section>

<section class="tsec">
  <div class="wrap">
    <h2>Before you start</h2>
    <ul class="tick">
      <li>You are an admin of the ACC (Autodesk Forma) hub.</li>
      <li>Hub Admin shows a <b>Custom Integrations</b> tab. Autodesk Support notes that this tab is hidden for trial hubs and for hubs on Essentials subscriptions. If you can't see it, the hub can't add integrations.</li>
      <li>You have the CDE Toolkit Client ID (shown below).</li>
      <li>You have picked a non-critical project and a few test users for the pilot.</li>
    </ul>
  </div>
</section>

<section class="tsec">
  <div class="wrap">
    <h2>Add the integration</h2>
    <ol class="adm-steps">
      <li><b>Open Hub Admin</b><span>Sign in to ACC at acc.autodesk.com with your admin account and open Hub Admin.</span></li>
      <li><b>Open Custom Integrations</b><span>Select the Custom Integrations tab, then Add custom integration.</span></li>
      <li><b>Enter the details</b><span>Paste the Client ID below and name the integration, for example CDE Toolkit. Complete any other fields Autodesk shows. Autodesk renames screens from time to time, so labels may differ slightly.</span></li>
      <li><b>Save</b><span>The integration now appears in the list. Remove it there at any time to cut off access.</span></li>
      <li><b>Tell your users where to go</b><span>Send people to <code id="appUrl">/app/</code>. Each person signs in with their own Autodesk account.</span></li>
    </ol>
    <p class="sub" style="margin-top:22px">CDE Toolkit Client ID</p>
    <div class="clientid"><code id="cid">Your contact will provide the Client ID.</code><button class="btn line" id="copyCid" type="button" hidden>Copy</button></div>
  </div>
</section>

<section class="tsec">
  <div class="wrap">
    <h2>What permissions does it ask for?</h2>
    <p class="sub" style="margin:0 0 16px">The toolkit asks for one set of permissions at sign-in, shared by all tools.</p>
    <div class="tablewrap"><table class="scopes"><thead><tr><th>Permission</th><th>Used for</th></tr></thead><tbody>{scopes}</tbody></table></div>
    <ul class="tick" style="margin-top:20px">
      <li>The toolkit acts as the signed-in person. It can only see and change what that person can already see and change in ACC.</li>
      <li>For a project to appear in the hub list, the person needs access to the project's Docs files.</li>
      <li>Tools that change data (CDE Sync, Rename, File Book Out, Federated views) show what will happen before they do it.</li>
    </ul>
  </div>
</section>

<section class="tsec">
  <div class="wrap">
    <h2>Where does the data go?</h2>
    <div class="flow" role="img" aria-label="CDE Toolkit's website delivers web pages to your browser. Your browser talks directly to Autodesk, and optionally to ProjectWise, SharePoint or InEight.">
      <div class="fbox"><b>CDE Toolkit website</b><span>Delivers the web pages and scripts. Receives no ACC data.</span></div>
      <div class="farrow"><i>→</i>web pages only</div>
      <div class="fbox mid"><b>Your browser</b><span>The tools run here, signed in as the user.</span></div>
      <div class="farrow"><i>⇄</i>files, attributes, reviews, sign-in</div>
      <div class="fstack">
        <div class="fbox"><b>Autodesk (ACC)</b><span>Where your project data lives.</span></div>
        <div class="fbox"><b>Optional sources</b><span>ProjectWise, SharePoint or InEight, for CDE Sync only.</span></div>
      </div>
    </div>
    <ul class="tick" style="margin-top:22px">
      <li>Sign-in uses OAuth 2.0 with PKCE. There is no client secret. The sign-in token lives in the browser tab's session storage and is cleared when the tab closes or the user signs out.</li>
      <li>There are no advertising or analytics scripts. The only message we receive is one a person chooses to send through the Contact page, handled by a form service (see <a href="/privacy.html">Privacy</a>).</li>
      <li>Your browser also fetches some third-party resources: Google Fonts, library files from cdnjs, and in GeoFed, map tiles from OpenStreetMap and Esri.</li>
    </ul>
  </div>
</section>

<section class="tsec">
  <div class="wrap cols">
    <div>
      <h2>Optional sources for CDE Sync</h2>
      <ul class="dash" style="color:var(--ink)">
        <li><b>ProjectWise.</b> Your server must allow the toolkit's web address (CORS), and users need a Web API address and login.</li>
        <li><b>SharePoint.</b> A Microsoft Entra app registration with read permission for files and sites. Your Microsoft 365 admin may need to approve it.</li>
        <li><b>InEight Document.</b> An API base URL and a key or token. API paths aren't published openly, so they can be edited in the tool.</li>
      </ul>
    </div>
    <div>
      <h2>Rolling it out</h2>
      <ul class="dash" style="color:var(--ink)">
        <li>Start with a non-critical project and a few people. Use demo mode for training.</li>
        <li>Test tools that change data on copies first, and keep your own backups.</li>
        <li>To end a pilot, remove the integration from Custom Integrations.</li>
      </ul>
    </div>
  </div>
</section>

<section class="tsec">
  <div class="wrap">
    <h2>Troubleshooting</h2>
    <ul class="benefit">
      <li><b>The hub or project doesn't appear after sign-in.</b><span>Check the integration was added in this hub, and that the person has access to the project's Docs files. Autodesk lists a project only when the user can see at least one file in it.</span></li>
      <li><b>There's no Custom Integrations tab.</b><span>See Before you start. Trial and Essentials hubs hide it. Ask Autodesk or your reseller about moving the hub to a full subscription.</span></li>
      <li><b>Federated views can't find a model set.</b><span>It needs Model Coordination in your hub and a model set based on your Published folder. The tool can create the model set if you have permission.</span></li>
      <li><b>Autodesk shows a sign-in error page.</b><span>The web address the tool runs at must match the one registered in the APS app. Contact us and we'll check it.</span></li>
    </ul>
    <p class="sub" style="margin-top:20px">Still stuck? <a href="/contact.html">Send a message</a>.</p>
  </div>
</section>'''
    js = '''<script src="/config.js"></script>
<script>
(function () {
  var cfg = window.CDETK_CONFIG || {}, id = String(cfg.clientId || '').trim();
  document.getElementById('appUrl').textContent = location.origin + '/app/';
  if (!id) return;
  document.getElementById('cid').textContent = id;
  var b = document.getElementById('copyCid'); b.hidden = false;
  b.onclick = function () {
    (navigator.clipboard ? navigator.clipboard.writeText(id) : Promise.reject()).then(function () { b.textContent = 'Copied'; }, function () {
      var r = document.createRange(); r.selectNodeContents(document.getElementById('cid')); getSelection().removeAllRanges(); getSelection().addRange(r); b.textContent = 'Press Ctrl+C'; });
    setTimeout(function () { b.textContent = 'Copy'; }, 1800);
  };
})();
</script>
'''
    return page("Admin guide | CDE Toolkit", "How an ACC hub admin adds CDE Toolkit as a Custom Integration, the permissions it asks for, and where data goes.", body, "admin", extra_body=js)


# ------------------------------------------------------------------ write
def refresh_partials(path, current):
    s = path.read_text(encoding="utf8")
    hdr = re.compile(r"(?:<!--site-header-->\s*)?<header class=\"deep\">.*?</header>(?:\s*<!--/site-header-->)?", re.S)
    ftr = re.compile(r"(?:<!--site-footer-->\s*)?<footer>.*?</footer>(?:\s*<!--/site-footer-->)?", re.S)
    s, n1 = hdr.subn(lambda m: header(current), s, count=1)
    s, n2 = ftr.subn(lambda m: footer(), s, count=1)
    if n1 != 1 or n2 != 1:
        sys.exit(f"{path.name}: header/footer not found")
    path.write_text(s, encoding="utf8")


def main():
    (PUB / "tools").mkdir(exist_ok=True)
    (PUB / "index.html").write_text(landing(), encoding="utf8")
    for slug in TOOLS:
        (PUB / "tools" / f"{slug}.html").write_text(tool_page(slug), encoding="utf8")
    (PUB / "admin-guide.html").write_text(admin_page(), encoding="utf8")
    refresh_partials(PUB / "about.html", "about")
    refresh_partials(PUB / "contact.html", "contact")
    print(f"built landing, {len(TOOLS)} tool pages, admin guide; refreshed about and contact")


if __name__ == "__main__":
    main()
