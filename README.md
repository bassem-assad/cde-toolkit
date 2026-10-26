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
4. Open <http://localhost:3000>. Stop the server with `Ctrl+C`.

No `npm install` is needed: the server has no dependencies.

## One-off Autodesk setup

1. At <https://aps.autodesk.com> > **My Apps**, create an app of type
   **Desktop, Mobile, Single-Page App** (a public app that uses PKCE, with no client secret).
2. Callback URL: `http://localhost:3000/` (the home page shows the exact value with a Copy button).
3. Enable the **Data Management**, **Model Derivative**, **Viewer** and **Autodesk Construction Cloud / BIM 360** APIs.
4. Ask your ACC account admin to add the Client ID under
   **Account Admin > Custom Integrations**.
5. Paste the Client ID on the CDE Toolkit home page and click **Sign in with Autodesk**.

Autodesk renames portal menus from time to time, so the labels above may differ slightly.

### SharePoint source (optional, CDE Sync only)

Register an app in Microsoft Entra ID with a **Single-page application** redirect URI of
`http://localhost:3000/modules/migrate.html` and delegated Microsoft Graph permissions
`Files.Read.All` and `Sites.Read.All`. Enter its Client ID in CDE Sync > Settings.

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
public/index.html       home page, Autodesk sign-in and callback
public/assets/auth.js   shared Autodesk sign-in (OAuth 2 with PKCE)
public/assets/nav.js    shared top bar
public/assets/app.css   shared styles (home and Rename)
public/modules/         one page per module
```

© 2026 Bassem Assad. All rights reserved.
