---
title: CORS lab
subject: networking
tags: [networking, cors, lab, cookies, browser]
aliases: [CORS demo, CORS walkthrough]
created: 2026-10-30
updated: 2026-10-30
status: draft
sources: ["study session 2026-10-30", "https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS"]
---

<!-- series:start -->
> [!series]- Networking · 11 of 11
> 1. [[networking/http-message|HTTP message]]
> 2. [[networking/request-lifecycle|Request lifecycle]]
> 3. [[networking/dns|DNS]]
> 4. [[networking/tcp|TCP]]
> 5. [[networking/tls|TLS]]
> 6. [[networking/http-caching|HTTP caching]]
> 7. [[networking/origin|Origin]]
> 8. [[networking/cors|CORS]]
> 9. [[networking/cors-credentials|CORS and credentials]]
> 10. [[networking/cors-expose-headers|CORS exposed headers]]
> 11. **CORS lab** · you are here
<!-- series:end -->

> [!tldr] In three lines
> A small local lab with two Python servers: a page on `localhost:8000` and an API on `localhost:9000`. Seven clicks show what the browser sends, what the server answers, and when the browser lets the page read the answer. Run it once and the CORS rules stop being abstract.
>
> [[#Interview questions|→ Self-test: 5 questions]]

## Why it exists

Reading CORS rules is easy. Predicting what the browser does with a real reply is harder, because the browser hides the result from the page and prints the reason somewhere else. This lab makes every step visible: the page code, the raw request, the server code that answered, the raw reply, and the browser's check. Each button tests one rule from [[networking/cors|CORS]], [[networking/cors-credentials|CORS and credentials]], or [[networking/cors-expose-headers|CORS exposed headers]].

### Plain version

The lab is a two-room play. Room A is the page (`localhost:8000`). Room B is the API (`localhost:9000`). Each button in room A asks room B a question. A referee (the browser) carries the question and the answer between the rooms, and decides whether room A may read the answer. Each button is a different rule the referee applies.

## How to run

The lab has three files and one setup:

### The three files

| File | Role | Port |
|---|---|---|
| `index.html` | The page. Buttons call the API with `fetch` and show the result. | Served on `8000` |
| [frontend.py](cors-lab-files/frontend.py) | Serves the folder `cors-lab-files/` as static files, so the page has a real origin, `http://localhost:8000`. | `8000` |
| [api.py](cors-lab-files/api.py) | The API. Each route sends a different combination of CORS headers. | `9000` |

### Terms in the lab

| Term | Definition | Where it's used in the lab |
|---|---|---|
| Page origin | `http://localhost:8000`, from the scheme, host, and port of the page | Sent as `Origin` on every call |
| API origin | `http://localhost:9000` | The target of every `fetch` |
| Route | A path in `api.py` such as `/api/allow` | One per button |
| Browser check | The comparison between `Origin` and `Access-Control-Allow-Origin` (plus credential rules) | Decides whether the page reads the reply |

### Start the servers

Open two terminals. Each server runs in the foreground; stop either with Ctrl+C.

```bash
# Terminal 1: the API on localhost:9000
cd ~/Development/learn-notes/content/networking/cors-lab-files
python3 api.py

# Terminal 2: the page on localhost:8000
cd ~/Development/learn-notes/content/networking/cors-lab-files
python3 frontend.py
```

Then open **http://localhost:8000** in the browser. Use `localhost`, not `127.0.0.1`. The page's origin must match the origin the API allows, which is `http://localhost:8000` exactly. If you open `http://127.0.0.1:8000`, every "allowed" button fails, because that origin is not in the list.

Both servers are standard library only (no install step). Python 3 is enough.

## The widget

<iframe src="/static/widgets/cors-lab-seven-buttons-stepper.html" width="100%" height="760" style="border:0" loading="lazy"></iframe>

*Click each button to see the page code, the raw request, the server code, the raw response, and the browser check.*

## Steps

The lab's page has six buttons. Button 5 is clicked twice in the order below (once before login, once after), so the walkthrough has seven steps. The stepper widget above follows this order.

One important detail first. The page's `run` function reads `res.headers.get('Access-Control-Allow-Origin') ?? 'null'`. The browser hides that header from page script unless the server exposes it (see [[networking/cors-expose-headers|CORS exposed headers]]). So on **every successful call**, the page shows `Access-Control-Allow-Origin: null`, even when the server sent the header. The body is still readable.

| Step | Button | Route and call | Expected page output | Why |
|---|---|---|---|---|
| 1 | Who am I, before login (button 5, first click) | `/api/me`, `fetch(.../api/me, { credentials: 'include' })` | `HTTP 200`, `Access-Control-Allow-Origin: null`, `{"cookie_seen": false, "cookie": null}` | No cookie is stored yet, so the request has no `Cookie` line. The CORS check passes because the server allows this origin with credentials. |
| 2 | Log in (set cookie), the first button | `/api/login`, `fetch(.../api/login, { credentials: 'include' })` | `HTTP 200`, `null`, `{"logged_in": true}` | The reply sets `session=demo123`. The browser stores it because the exact origin and `Allow-Credentials: true` are present. |
| 3 | Who am I, after login (button 5, second click) | `/api/me`, `credentials: 'include'` | `HTTP 200`, `null`, `{"cookie_seen": true, "cookie": "demo123"}` | The browser now sends `Cookie: session=demo123` because the call uses `include`. |
| 4 | 1. open (no CORS headers) | `/api/open`, `fetch(.../api/open)` | `fetch failed: the browser blocked the request or the response...` | No `Access-Control-Allow-Origin` header, so the browser hides the reply. The server still answered and printed a line. |
| 5 | 2. allow (origin only) | `/api/allow`, `fetch(.../api/allow)` | `HTTP 200`, `null`, `{"route": "allow"}` | The exact origin is allowed. Credentials are the default (`same-origin`), so no cookie is sent and none is needed. |
| 6 | 4. wildcard with credentials | `/api/wildcard-creds`, `fetch(.../api/wildcard-creds, { credentials: 'include' })` | `fetch failed: ...` | `Access-Control-Allow-Origin: *` cannot be used with credentials. The browser blocks the reply even though the server answered. |
| 7 | 3. allow with credentials | `/api/allow-creds`, `fetch(.../api/allow-creds, { credentials: 'include' })` | `HTTP 200`, `null`, `{"route": "allow-creds"}` | The exact origin and `Allow-Credentials: true` satisfy the rule for credentialed calls. |

The page shows `null` for the header on success because of the header filter. That is intended: it is a lesson, not a bug.

The order matters. Steps 1 to 3 build the cookie state. Step 4 is the simplest blocked case. Step 5 is the simplest allowed read. Steps 6 and 7 are the same credentialed call, first with a wildcard (blocked) and then with an exact origin (allowed).

### Where to look while you click

- **Terminal 1 ([api.py](cors-lab-files/api.py)).** One line per request, for example `GET /api/allow Origin=http://localhost:8000`. The lines show the server received every call, including the blocked ones.
- **DevTools > Network.** Each call appears. Open a row to see the request `Origin` and `Cookie`, and the response headers. The status may be 200 in a blocked row.
- **DevTools > Console.** The real CORS message for a blocked call (Chrome: "has been blocked by CORS policy"). The page also logs the error with `console.error(err)`.
- **DevTools > Application > Cookies.** After step 2, a `session` cookie for `localhost`, with no port in it.

### Reset the lab

The cookie persists across page reloads and server restarts. To see the "before login" output of step 1 again, delete the `session` cookie for `localhost` in DevTools > Application > Cookies, then click step 1. Restarting the Python servers does not clear it.

## The real thing

Each route is short. Each one shows one rule. The code is from [api.py](cors-lab-files/api.py), trimmed to the relevant route. The six routes are collapsed below; the widget already shows them in order.

> [!info]- api.py routes
> The six routes, one per button. Each sends one combination of CORS headers.
>
> **`/api/login` (step 2).** The cookie is stored only because both CORS headers are present and the page asked for `include`.
>
> ```python
> elif self.path == "/api/login":
>     self.reply(200, {"logged_in": True}, [
>         ("Set-Cookie", "session=demo123; Path=/; SameSite=Lax"),  # the browser stores this cookie
>         ("Access-Control-Allow-Origin", "http://localhost:8000"),  # only this page origin may read the response
>         ("Access-Control-Allow-Credentials", "true"),  # lets the browser keep the cookie from this call
>     ])
> ```
>
> **`/api/me` (steps 1 and 3).** The only difference between steps 1 and 3 is the `Cookie` line the browser adds after login. The server code does not change.
>
> ```python
> elif self.path == "/api/me":
>     jar = SimpleCookie(self.headers.get("Cookie", ""))  # parse the Cookie request header
>     session = jar["session"].value if "session" in jar else None  # the demo cookie, or None
>     self.reply(200, {"cookie_seen": session is not None, "cookie": session}, [
>         ("Access-Control-Allow-Origin", "http://localhost:8000"),
>         ("Access-Control-Allow-Credentials", "true"),  # lets the browser send the cookie and read this
>     ])
> ```
>
> **`/api/open` (step 4).** No `Access-Control-*` headers at all. A call from another origin is blocked on the page side, while the server still does its work.
>
> ```python
> if self.path == "/api/open":
>     self.reply(200, {"route": "open"})  # no CORS headers: the browser hides this response from the page
> ```
>
> **`/api/allow` (step 5).** One header. This is the minimum for a simple cross-origin read with the default credentials mode.
>
> ```python
> elif self.path == "/api/allow":
>     self.reply(200, {"route": "allow"}, [
>         ("Access-Control-Allow-Origin", "http://localhost:8000"),  # only this page origin may read the response
>     ])
> ```
>
> **`/api/wildcard-creds` (step 6).** The comment in the code is the lesson. Step 7 is the fix.
>
> ```python
> elif self.path == "/api/wildcard-creds":
>     # Deliberately wrong: browsers block '*' when credentials are used.
>     self.reply(200, {"route": "wildcard-creds"}, [
>         ("Access-Control-Allow-Origin", "*"),  # any origin may read it, but not with credentials
>         ("Access-Control-Allow-Credentials", "true"),  # asks for credentials, which the '*' breaks
>     ])
> ```
>
> **`/api/allow-creds` (step 7).** The exact origin in place of `*`, plus `Allow-Credentials: true`. This is the correct pattern for a logged-in call to another origin.
>
> ```python
> elif self.path == "/api/allow-creds":
>     self.reply(200, {"route": "allow-creds"}, [
>         ("Access-Control-Allow-Origin", "http://localhost:8000"),  # only this page origin may read the response
>         ("Access-Control-Allow-Credentials", "true"),  # lets the browser send and accept cookies
>     ])
> ```

### The page code

The buttons in `index.html` each call one `fetch`, and `run()` shows the result:

```js
async function run(call) {
  const out = document.getElementById('out');
  out.textContent = '';
  try {
    const res = await call();  // throws when the browser blocks the request or response
    const acao = res.headers.get('Access-Control-Allow-Origin') ?? 'null';
    const body = await res.text();
    out.textContent = `HTTP ${res.status}\nAccess-Control-Allow-Origin: ${acao}\n${body}`;
  } catch (err) {
    console.error(err);  // the real reason is in the console
    out.textContent = 'fetch failed: the browser blocked the request or the response. Check the browser console for the real reason.';
  }
}
```

The `catch` branch is the only place a blocked call appears. The browser's real reason is in the console, not in the page text, which is why the page sends you to DevTools.

### Terminal output

For each request, [api.py](cors-lab-files/api.py) prints one line. A captured run of the same routes (sent with `curl` and the same `Origin`, as a check on the server side) printed:

```text
GET /api/open Origin=http://localhost:8000
GET /api/allow Origin=http://localhost:8000
GET /api/wildcard-creds Origin=http://localhost:8000
GET /api/me Origin=http://localhost:8000
GET /api/login Origin=http://localhost:8000
GET /api/me Origin=http://localhost:8000
GET /api/allow-creds Origin=http://localhost:8000
```

This is the server's view. Every call arrived. The browser decided which replies the page could read.

### Lab vs a real app

| | Lab (this page) | Real app with CORS | `curl` |
|---|---|---|---|
| Browser enforces CORS | Yes | Yes | No |
| Cookie value | `demo123`, no `HttpOnly` | A real session, `HttpOnly` and `Secure` | None unless passed with `-b` |
| Origins | `localhost:8000` and `localhost:9000` | Usually different domains | Not applicable |
| Preflight | Not used (only `GET`) | Common for `PUT`, JSON bodies, and auth headers | Not used |

### Use it for

- Learning and interviews: the seven steps cover the CORS checks most interviewers ask about, in the order they build up (origin, credentials, wildcard, exposed headers).
- Debugging an unfamiliar API: run the same pattern against a real API to see which header is missing.
- Teaching: a small, self-contained demo of the same-origin policy with no framework and no build step.
- Not a production setup. The lab uses plain `HTTP` on `localhost`, a demo cookie with no `HttpOnly` or `Secure`, and no authentication. Real APIs need all three.

## Common misconceptions

- **Wrong:** The lab's error message says what is wrong.
  **Right:** The page only says "fetch failed." The real reason is in DevTools > Console. Read the console first when a button fails.

- **Wrong:** `Access-Control-Allow-Origin: null` on the page means the header is missing.
  **Right:** The header is hidden from page script on every success, because it is not CORS-safelisted. The server did send it. See [[networking/cors-expose-headers|CORS exposed headers]].

- **Wrong:** If step 4 fails, the server is broken.
  **Right:** The server answered 200 and printed its line. The browser blocked the page from reading the reply, because there was no `Access-Control-Allow-Origin` header.

- **Wrong:** Opening the page at `127.0.0.1:8000` works the same as `localhost:8000`.
  **Right:** The origin changes, so the server's exact-origin check fails and every allowed route is blocked. Use `http://localhost:8000`.

## Interview questions

> [!question]- Q1. Why does the lab run two servers on different ports?
> The page and the API need different origins, so the browser treats the calls as cross-origin and applies CORS. Two ports on the same host is enough, because an origin includes the port.

> [!question]- Q2. In step 4, the server answered 200. Why does the page fail?
> The browser checks for an exact `Access-Control-Allow-Origin` header before the page can read the reply. The `/api/open` route sends none, so the browser hides the reply and the page's `fetch` rejects. The server did its job; the browser applied the rule.

> [!question]- Q3. Why does step 6 fail even though the server sends `Allow-Credentials: true`?
> Because the other header, `Access-Control-Allow-Origin`, is `*`. A wildcard is not allowed with credentials. The browser requires an exact origin for credentialed calls. Step 7 changes only that header, and then the call works.

> [!question]- Q4. Why does the page show `Access-Control-Allow-Origin: null` even on success?
> The header is not CORS-safelisted, so the browser hides it from page script unless the server lists it in `Access-Control-Expose-Headers`. The lab does not list it, so `headers.get()` returns `null`. The body is still readable.

> [!question]- Q5. What would you check first if a real app's login call works in `curl` but the page cannot read the response?
> The `Access-Control-Allow-Origin` value (must match the page's origin exactly), `Access-Control-Allow-Credentials: true` (required when the page sends `include`), and whether the page is served from the origin the server expects, such as `localhost` and not `127.0.0.1`.

## Trigger card

> [!example] When a lab button shows "fetch failed" but the terminal printed its route, it means the server received the call and the browser blocked the reply, because the CORS headers do not allow this exact page origin to read it.

> [!info]- Sources
> - Study session, 2026-10-30.
> - Lab files in this folder: [api.py](cors-lab-files/api.py), [frontend.py](cors-lab-files/frontend.py), `index.html`.
> - MDN, [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS).

<!-- series-nav:start -->
---

← [[networking/cors-expose-headers|CORS exposed headers]] · [[networking/index|Back to Networking]] →
<!-- series-nav:end -->
