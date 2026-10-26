# CDE Toolkit

Browser-based tools for Autodesk Construction Cloud (ACC), behind one Autodesk sign-in.

| Module | What it does | Needs |
|---|---|---|
| CDE Sync | Move files into ACC from ProjectWise, SharePoint, InEight, another ACC project or your computer. Maps attributes and applies the folder's naming standard. | Autodesk sign-in |
| File validator | Check an ACC Docs file-list export against a naming convention and required attributes. | Excel or CSV export |
| Rename | Add the upload date to a model's name, e.g. `Model_20260915.rvt`. | Autodesk sign-in |
| File Book Out | Find drawings by attribute and book them out through an ACC review. | Autodesk sign-in |
| Review turnaround | See where reviews slow down by step, reviewer and company. | CSV or JSON export |
| GeoFed | Federate ACC models on a map, with 3D/2D views, snapshots and markup. | Autodesk sign-in |
| Federated views | Create a Model Coordination view of every published model with a chosen location code. Folder and attribute names are set in Settings. | Autodesk sign-in |

Everything runs in the browser. Files go directly between the source system and ACC; the
local server only serves the pages.

## Run it on your laptop

1. Install **Node.js LTS** from <https://nodejs.org>. Check it in PowerShell: `node -v`.
2. Download this repository (green **Code** button > **Download ZIP**) and unzip it, e.g. to `C:\cde-toolkit`.
3. In PowerShell:
   ```powershell
   cd C:\cde-toolkit
   npm start
   ```
4. Open <http://localhost:3000> for the product website, or <http://localhost:3000/app/> for the tools. Stop the server with `Ctrl+C`.

No `npm install` is needed: the server has no dependencies.

## Try it without Autodesk (demo mode)

On the app home page (`/app/`) click **Try demo mode**, or use the **Try the demo** button on the website. Every module then runs on built-in sample data (a
sample ACC hub, projects, Revit models, a model set, a file list and review data), nothing is
sent to Autodesk, and nothing in ACC is changed. Use it to see how each tool works, take
screenshots or show it to someone. Demo mode lasts for the browser tab; **Exit demo mode**
(home page, or inside a module) switches it off. Adding `?demo=1` to any module's address
also turns it on.

## One-off Autodesk setup

1. At <https://aps.autodesk.com> > **My Apps**, create an app of type
   **Desktop, Mobile, Single-Page App** (a public app that uses PKCE, with no client secret).
2. Callback URL: `http://localhost:3000/` (the app home page at `/app/` shows the exact value with a Copy button). Autodesk returns to the site root, which forwards the sign-in to the app.
3. Enable the **Data Management**, **Model Derivative**, **Viewer** and **Autodesk Construction Cloud / BIM 360** APIs.
4. Ask your ACC account admin to add the Client ID under
   **Account Admin > Custom Integrations**.
5. Open `/app/`, paste the Client ID and click **Sign in with Autodesk**.

Autodesk renames portal menus from time to time, so the labels above may differ slightly.

### SharePoint source (optional, CDE Sync only)

Register an app in Microsoft Entra ID with a **Single-page application** redirect URI of
`http://localhost:3000/modules/migrate.html` and delegated Microsoft Graph permissions
`Files.Read.All` and `Sites.Read.All`. Enter its Client ID in CDE Sync > Settings.

## Put it online for other people (Cloudflare Pages, free)

Hosting gives everyone one web address, with nothing to install. The app is a static site, so
the free Cloudflare Pages plan is enough. Menu names below may differ slightly as Cloudflare
updates its dashboard.

1. Create a free account at <https://dash.cloudflare.com/sign-up>.
2. Go to **Workers & Pages > Create > Pages > Connect to Git**, sign in to GitHub and give
   Cloudflare access to the `cde-toolkit` repository only.
3. Build settings: **Framework preset** `None`, **Build command** empty,
   **Build output directory** `public`. Click **Save and Deploy**.
4. Note your address, e.g. `https://cde-toolkit.pages.dev`.
5. At <https://aps.autodesk.com>, create a **production** APS app
   (Desktop, Mobile, Single-Page App) with callback URL `https://cde-toolkit.pages.dev/`
   (your exact address, with the trailing `/`). Enable the same APIs as above.
6. In GitHub, edit `public/config.js` and paste that app's Client ID into `clientId`. Set
   `contactEmail` to a business address you are happy to publish; it shows a **Request a pilot**
   button on the website (leave it empty to hide the button).
   Commit the change: Cloudflare redeploys automatically in about a minute. The Client ID is
   not a secret (sign-in uses PKCE), so it is safe in this file.
7. Each company that uses it: their ACC account admin adds your production Client ID under
   **Account Admin > Custom Integrations**.

Every push to `main` now updates the live site. Optional: add your own domain under the Pages
project's **Custom domains** (the only cost is the domain registration).

### Turn on the Contact form (free, 5 minutes)

The website's Contact page needs somewhere to send messages. Web3Forms does this without
publishing your email address (free plan: 250 messages a month at the time of writing; check
<https://web3forms.com> for current limits).

1. Go to <https://web3forms.com>, enter the email address that should receive messages, and
   get your **Access Key** (it is emailed to you).
2. In GitHub, edit `public/config.js` and set:
   ```js
   contactEndpoint: 'https://api.web3forms.com/submit',
   contactAccessKey: 'paste-your-access-key-here',
   ```
   The access key is safe to publish. Optionally set `contactEmail` (shown as an alternative
   on the Contact page) and `linkedinUrl` (adds a LinkedIn button on the About page).
3. Commit. The site updates in about a minute. Send yourself a test message.
4. Complete the contact-form paragraph on `public/privacy.html`.

Until step 2 is done the form shows "This form isn't connected yet" and cannot be submitted.
Another form service works too: set `contactEndpoint` to its URL and leave the key empty.

`public/_headers` adds security headers on Cloudflare. `public/terms.html` and
`public/privacy.html` are draft templates: have them reviewed before charging anyone.

## Notes

- The Autodesk session is kept in the browser tab (`sessionStorage`). Opening the toolkit in a
  new tab means signing in again; closing the tab signs you out.
- ProjectWise and InEight sources are reached straight from the browser, so those servers must
  allow `http://localhost:3000` (CORS). Demo mode in CDE Sync shows the full flow without them.
- The Rename module changes the name of the current version. Test it on a copy first and check
  Manage Links in a host model.

## Project layout

```
server.js               local web server (no dependencies)
public/index.html       product website (landing page); forwards the Autodesk sign-in return to /app/
public/app/index.html   app home: Autodesk sign-in, demo mode and the tool list
public/about.html, contact.html   About page and Contact page (form)
public/assets/site.css  styles shared by the website pages
public/terms.html       draft Terms of Use      public/privacy.html   draft Privacy page
public/favicon.svg, robots.txt
public/config.js        built-in APS Client ID for a hosted deployment (optional)
public/_headers         security headers used by Cloudflare Pages
public/assets/auth.js   shared Autodesk sign-in (OAuth 2 with PKCE)
public/assets/nav.js    shared top bar
public/assets/app.css   shared styles (home and Rename)
public/modules/         one page per module
```

© 2026 Bassem Assad. All rights reserved.
