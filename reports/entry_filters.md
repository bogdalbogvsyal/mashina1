# Entry Filters (jurisdiction / capital / regulation / offtake / financeability / priority_35)

These filters are applied on top of the price radar. They are heuristics, not decisions.

## Purpose
Turn a price signal into the questions:
- Can I enter this with limited personal capital?
- Can external investors be brought in?
- Does this fit the goal of nearly passive high income by ~35 (ownership over salary)?

## Priority for the age-35 goal
`priority_35` ranks signals by how well they match the target of nearly passive high income by roughly age 35. It prefers cases where:
- Ownership (equity or asset share) is realistic.
- External capital can be brought in relatively early (especially with offtake).
- The project can be started in parallel with studies, not instead of them.

## Current heuristics (see mashina/filters.py)
- Low capital + light regulation + high ownership + high parallel: software, data, pure trading, arbitrage.
- High capital + heavy regulation: refining, plants, mining (ownership possible, but harder to start while studying and harder to finance early).
- Strong offtake: improves financeability and raises priority_35.

## Preferred jurisdictions for testing
- NL: fast setup, commodity/logistics hub.
- DK: living base + EU access.
- CH / SG / AE: lower tax trading and holding structures.

## How to use
1. Run the radar (`python -m mashina.radar`).
2. Take the top lasting price rises.
3. Run `score_entry()` from `mashina.filters` on each title.
4. Prefer signals with `priority_35 = high` when choosing what to investigate next.
5. Manually verify offtake, permits, and real ownership path before treating any signal as actionable.

This layer does not replace the physical-constraint check. It only ranks signals against the specific goal of ownership-based income by ~35.
