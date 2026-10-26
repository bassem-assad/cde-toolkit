/* CDE Toolkit: one Autodesk (APS) sign-in shared by every module.
   3-legged OAuth with PKCE, no client secret. The home page (/) is the only
   callback URL, so the APS app needs just one registered address. */
(function () {
  const APS = 'https://developer.api.autodesk.com';
  const SCOPES = 'data:read data:write data:create data:search account:read bucket:read user-profile:read';
  const K = { tok: 'cdetk.tok', cid: 'cdetk.cid', pkce: 'cdetk.pkce', ret: 'cdetk.return' };
  const store = name => {
    let s = null; try { s = window[name]; } catch (e) { }
    return {
      get: k => { try { return s.getItem(k); } catch (e) { return null; } },
      set: (k, v) => { try { s.setItem(k, v); } catch (e) { } },
      del: k => { try { s.removeItem(k); } catch (e) { } }
    };
  };
  const ls = store('localStorage'), ss = store('sessionStorage');
  const redirect = location.origin + '/';
  const b64u = buf => btoa(String.fromCharCode(...new Uint8Array(buf))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');

  const raw = () => { try { return JSON.parse(ss.get(K.tok) || 'null'); } catch (e) { return null; } };
  const save = t => ss.set(K.tok, JSON.stringify(t));
  /* A Client ID built into config.js (hosted deployments) wins over one typed by the user. */
  const builtIn = () => String((window.CDETK_CONFIG && window.CDETK_CONFIG.clientId) || '').trim();
  const clientId = () => builtIn() || ls.get(K.cid) || '';
  const setClientId = id => { if (!builtIn()) ls.set(K.cid, String(id || '').trim()); };

  async function tokenCall(params) {
    const r = await fetch(APS + '/authentication/v2/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded', Accept: 'application/json' },
      body: new URLSearchParams({ client_id: clientId(), ...params })
    });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error('Sign-in failed: ' + (j.developerMessage || j.error_description || j.error || r.status));
    const prev = raw();
    save({ access: j.access_token, refresh: j.refresh_token || (prev && prev.refresh), exp: Date.now() + (j.expires_in - 90) * 1000 });
  }

  /* Send the browser to Autodesk; afterwards the home page returns the user to `returnTo`. */
  async function login(returnTo) {
    if (!clientId()) throw new Error('Enter your APS Client ID on the home page first.');
    const verifier = b64u(crypto.getRandomValues(new Uint8Array(48)));
    const challenge = b64u(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(verifier)));
    ss.set(K.pkce, verifier);
    ss.set(K.ret, returnTo || location.pathname);   // where to land after signing in
    const u = new URL(APS + '/authentication/v2/authorize');
    u.search = new URLSearchParams({
      response_type: 'code', client_id: clientId(), redirect_uri: redirect, scope: SCOPES,
      state: 'aps', code_challenge: challenge, code_challenge_method: 'S256'
    }).toString();
    location.href = u.toString();
  }

  /* Called by the app home page (/app/). The registered callback address is the site root (/), which
     forwards the sign-in parameters here. Returns the path to go back to, or null when this is not a callback. */
  async function handleCallback() {
    const p = new URLSearchParams(location.search);
    if (p.get('error')) { history.replaceState({}, '', location.pathname); throw new Error('Autodesk sign-in: ' + (p.get('error_description') || p.get('error'))); }
    if (!p.get('code') || p.get('state') !== 'aps') return null;
    history.replaceState({}, '', location.pathname);
    await tokenCall({ grant_type: 'authorization_code', code: p.get('code'), redirect_uri: redirect, code_verifier: ss.get(K.pkce) || '' });
    ss.del(K.pkce);
    const back = ss.get(K.ret); ss.del(K.ret);
    return back && back.startsWith('/') ? back : '/app/';
  }

  /* A valid access token, refreshed when it has expired. Throws when signed out. */
  async function accessToken() {
    let t = raw();
    if (!t) throw new Error('Not signed in to Autodesk. Sign in on the home page.');
    if (Date.now() > t.exp) {
      if (!t.refresh) throw new Error('Your Autodesk session expired. Sign in again.');
      await tokenCall({ grant_type: 'refresh_token', refresh_token: t.refresh, scope: SCOPES });
      t = raw();
    }
    return t.access;
  }
  const tokenSync = () => { const t = raw(); return t && Date.now() < t.exp ? t.access : null; };
  /* Demo mode: every module runs on built-in sample data and nothing is sent to Autodesk.
     It is switched on from the home page (or with ?demo=1) and lasts for this browser tab. */
  const DEMO_KEY = 'cdetk.demo';
  const isDemo = () => {
    try { if (new URLSearchParams(location.search).has('demo')) ss.set(DEMO_KEY, '1'); } catch (e) { }
    return ss.get(DEMO_KEY) === '1';
  };
  const setDemo = on => { if (on) ss.set(DEMO_KEY, '1'); else ss.del(DEMO_KEY); };
  const signedIn = () => !!raw();
  const signOut = () => ss.del(K.tok);

  window.CDETK = { APS, SCOPES, redirect, raw, save, clientId, setClientId, builtIn, login, handleCallback, accessToken, tokenSync, signedIn, signOut, isDemo, setDemo };
})();
