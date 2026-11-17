---
title: Backend system design
---

How a backend stays fast and protects itself under load: caching with Redis, rate limiting, and the race conditions that break limits and one-time codes when many requests arrive at once. The examples use a small food-delivery app (restaurants, menus, logins, email codes). Short on time? Start with the quick revision page. Otherwise read the quick pages in order; each one links to its detailed version.

## Reading order

1. **[[system-design/revision|Quick revision]]**: caching, rate limiting and race conditions on one page, about 10 minutes.
2. **[[system-design/caching|Caching with Redis]]**: cache-aside vs write-through, TTL and jitter, invalidation, cache stampede. ([[system-design/deep/caching|detailed]])
3. **[[system-design/rate-limiting|Rate limiting]]**: fixed window, sliding window, token bucket, and limiting a login endpoint. ([[system-design/deep/rate-limiting|detailed]])
4. **[[system-design/race-conditions|Race conditions in limits and codes]]**: lost updates, check-then-act, and the fixes (atomic commands, row locks, SET NX). ([[system-design/deep/race-conditions|detailed]])
