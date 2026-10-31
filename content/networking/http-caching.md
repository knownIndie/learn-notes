---
title: HTTP caching
tags: [networking, http-caching]
---

<!-- series:start -->
> [!series]- Networking · 6 of 8
> 1. [[networking/http-message|HTTP message]]
> 2. [[networking/request-lifecycle|Request lifecycle]]
> 3. [[networking/dns|DNS]]
> 4. [[networking/tcp|TCP and UDP]]
> 5. [[networking/tls|TLS and HTTPS]]
> 6. **HTTP caching** · you are here
> 7. [[networking/origin|Origin]]
> 8. [[networking/cors|CORS]]
<!-- series:end -->

> [!abstract] What this page is for
> **Intent:** understand how a browser or CDN keeps a copy of a file, when it uses that copy, and when it asks the server first. Answer the common HTTP caching interview questions.
> **You'll learn:** why caching matters · where caches live · `Cache-Control` · fresh vs stale · ETag and `304` · cache busting · what to cache.
> **Time:** about 7 minutes. Every section has a longer version on the [[networking/deep/http-caching|detailed HTTP caching page]].

## Words you need first

- **HTTP (HyperText Transfer Protocol)**: the rules a browser and a server use to ask for files and send them back. A request is a `GET` (give me this URL). A reply has a status like `200 OK`.
- **Cache**: a store of copies. The next request for the same URL can use the copy instead of the network.
- **Browser cache**: the copy store inside one user's browser.
- **CDN (Content Delivery Network)**: servers around the world that hold copies of files close to users. A shared cache.
- **Proxy**: a middle server, often run by a company or ISP, that can keep copies too.
- **Header**: a `name: value` line sent with a request or reply, e.g. `Cache-Control: max-age=3600`.
- **ETag (entity tag)**: a short label for one version of a file, e.g. `"7f3a-9c1"`. A changed file gets a new label.
- **`304 Not Modified`**: a reply that means "your copy is still good". It has no body.

## Why it exists

A page loads `logo.png`, `app.css` and `app.js` on every visit. Without caching, the browser downloads the same bytes every time. On a slow phone network, that costs seconds, and the site pays for the bandwidth.

Example: `shop.com/styles/site.css` is 80 KB. A customer opens shop.com 20 times a week. Without caching, that is 1.6 MB of CSS for a file that never changed.

## The picture

![HTTP caching decision flow: is there a copy, is it fresh, use it or revalidate with the ETag, then 304 or 200](../assets/diagrams/http-caching-decision-phone.svg)

Read it top to bottom. Each yes/no question is one check. A repeat visit usually stops at "Use the copy".

## How it works, with an example

Take `/styles/site.css` on shop.com.

1. The first reply arrives with `Cache-Control: max-age=3600` and `ETag: "7f3a-9c1"`. The browser stores the body and the headers.
2. Ten minutes later, the copy is fresh (10 minutes old, less than the 3600-second `max-age`). The browser uses it. No request leaves the computer.
3. Two hours later, the copy is stale. The browser sends `If-None-Match: "7f3a-9c1"` with the request.
4. The file has not changed, so the server replies `304 Not Modified` with no body.
5. The browser reuses its stored body. No file bytes were downloaded.

If the file had changed, step 4 would give `200 OK` with the new file and a new ETag.

## The most common mistake

> [!warning] `no-cache` does not mean "do not cache"
> `no-cache` means "you may store it, but check with the server before every reuse". To say "never store this", use `no-store`. Mixing them up is the classic trick question. For a bank page with account data, `no-store` is the right choice.

## Fresh or stale

A stored copy is **fresh** when its age is less than its `max-age`. Age is how long the copy has been stored. A fresh copy is used with no request. A **stale** copy must be checked with the server before use.

`Cache-Control` carries these rules. The main directives:

- `max-age=N`: fresh for N seconds.
- `no-cache`: store it, but check with the server before each reuse.
- `no-store`: do not store it at all.
- `private`: only the user's own browser may store it. CDNs must not.
- `public`: any cache may store it, even with cookies or login data.
- `s-maxage=N`: a lifetime for shared caches (CDN, proxy) only. It overrides `max-age` there.
- `immutable`: the file never changes at this URL, so do not check during its lifetime.

Example: `Cache-Control: public, max-age=60, s-maxage=3600` means browsers keep a copy for 1 minute and the CDN keeps it for 1 hour.

## Revalidation and 304

Revalidation happens when a copy is stale. The browser sends a **conditional request**: the same `GET`, plus a validator from the stored copy.

- **ETag** is the stronger validator. The browser sends it back as `If-None-Match`.
- **Last-Modified** is a date. The browser sends it back as `If-Modified-Since`. It is weaker, because it has one-second resolution.

The server answers one of two ways:

- **File unchanged:** `304 Not Modified`, with an empty body. The browser uses its stored body.
- **File changed:** `200 OK`, with the new body and a new ETag.

```http
GET /styles/site.css HTTP/1.1
Host: shop.com
If-None-Match: "7f3a-9c1"
```

```http
HTTP/1.1 304 Not Modified
ETag: "7f3a-9c1"
```

## What to cache

- **Hashed static files** (`app.3f9a.js`, images): cache for a long time, e.g. `Cache-Control: public, max-age=31536000, immutable` (one year).
- **HTML pages**: they link to the hashed files and change at each deploy. Use `no-cache` or a short `max-age`, so a new deploy shows up quickly.
- **API responses**: a public product list can be cached for 30 to 60 seconds. Personal data, such as a cart or bank balance, should use `private, no-store`.

**Cache busting** means changing the URL when the content changes. Build tools put a hash of the file content in the name: `app.3f9a.js`. A new version gets a new URL, so the old copy is never wrong, and a one-year lifetime is safe.

## Say it in an interview

> "HTTP caching lets browsers and CDNs reuse stored copies of responses. The server sets `Cache-Control`. While a copy is fresh, meaning its age is under `max-age`, the cache uses it with no request. When it is stale, the cache revalidates: it sends `If-None-Match` with the stored ETag. If the file is unchanged, the server answers `304 Not Modified` with no body. If it changed, the server answers `200` with the new file. For hashed static files, I use a long `max-age` and `immutable`. For HTML, I use `no-cache`. For personal data, I use `no-store`. `no-cache` means store but always check. `no-store` means never store."

## Questions interviewers ask

Tap a question to see the answer.

> [!question]- Why does HTTP caching matter?
> It removes repeated downloads. A fresh copy costs no network at all, and a `304` is a small request with no body.

> [!question]- Where do caches live?
> In the browser (private to one user), in CDNs (shared, close to users), and in proxies run by companies or ISPs (shared).

> [!question]- What is the difference between `no-cache` and `no-store`?
> `no-cache` allows storing, but the cache must check with the server before every reuse. `no-store` forbids storing at all.

> [!question]- What is the difference between `private` and `public`?
> `private` lets only the user's browser store the response. `public` lets any cache store it, even when the request had cookies.

> [!question]- What makes a copy fresh or stale?
> Fresh means its age is less than `max-age`. After that it is stale, and the cache must check with the server first.

> [!question]- What is an ETag, and how does a `304` work?
> An ETag labels one version of a file. The browser sends it as `If-None-Match`. If it still matches, the server replies `304` with no body.

> [!question]- ETag or Last-Modified: which is better?
> ETag is more precise. It names an exact version, while a date has one-second resolution. Use both when you can.

> [!question]- Why use hashed file names?
> A changed file gets a new URL, so old copies are never served by mistake. That makes a very long lifetime safe.

> [!question]- Should you cache HTML?
> Not for long. HTML points to new asset URLs at each deploy. Use `no-cache` or a short `max-age`.

> [!question]- What does `s-maxage` do?
> It sets the lifetime for shared caches only, such as a CDN. It overrides `max-age` there.

## Mental map

![HTTP caching mental map](../assets/diagrams/http-caching-mental-map.svg)

**Want more?** The [[networking/deep/http-caching|detailed HTTP caching page]] has the raw headers, `Vary`, exact revalidation rules, `stale-while-revalidate`, and more interview questions.

<!-- series-nav:start -->
---

← [[networking/tls|TLS and HTTPS]] · [[networking/origin|Origin]] →
<!-- series-nav:end -->
