---
title: Networking
---

How a web page gets from a name to a screen: DNS, TCP, TLS, HTTP, caching, and the browser rules (origin and CORS) that decide what a page may read. Each page builds on the one before it, so read them in order.

## Reading order

1. **[[networking/http-message|HTTP message]]**: the shape of an HTTP request and response: the start line, headers, and body.
2. **[[networking/request-lifecycle|Request lifecycle]]**: what happens, step by step, from typing a URL to the first byte of the page.
3. **[[networking/dns|DNS]]**: turning a name like `example.com` into an IP address.
4. **[[networking/tcp|TCP]]**: the reliable, ordered byte stream and its three-way handshake.
5. **[[networking/tls|TLS]]**: encryption, integrity, and server identity on top of TCP.
6. **[[networking/http-caching|HTTP caching]]**: how browsers and CDNs skip or revalidate requests with `Cache-Control` and `ETag`.
7. **[[networking/origin|Origin]]**: scheme, host, and port, and why they decide what a page may read.
8. **[[networking/cors|CORS]]**: how a server opts in to let other origins' pages read its responses.
9. **[[networking/cors-credentials|CORS and credentials]]**: cookies and logins across origins, `credentials: 'include'`, and why `*` is not allowed with them.
10. **[[networking/cors-expose-headers|CORS exposed headers]]**: which response headers a page can read, and how to expose more.
11. **[[networking/cors-lab|CORS lab]]**: a local lab that runs the CORS rules with two servers, step by step.
