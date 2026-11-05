---
title: Databases and SQL
---

How a backend reads and changes data safely: transactions under concurrency, then the SQL you write every day (joins, GROUP BY, window functions). The joins, GROUP BY and window pages use the same small food-delivery database (customers, restaurants, orders, menu items), with the SQL and the Drizzle (TypeScript) version side by side and the table shown after each step. The transactions page uses a small shoe shop instead.

## Reading order

1. **[[databases/revision|Quick revision]]**: the whole subject on one page, for the night before an interview.
2. **[[databases/transactions|Transactions and concurrency]]**: lost updates, isolation levels, FOR UPDATE vs SERIALIZABLE and retry. ([[databases/deep/transactions|detailed]])
3. **[[databases/joins|Joins]]**: inner join, left join, and finding rows with no match. ([[databases/deep/joins|detailed]])
4. **[[databases/group-by|Aggregates: GROUP BY and HAVING]]**: piles, count(*) vs count(col), WHERE vs HAVING. ([[databases/deep/group-by|detailed]])
5. **[[databases/window-functions|Window functions]]**: top N per group with rank, running totals, LAG. ([[databases/deep/window-functions|detailed]])
