# Entry Filters (jurisdiction / capital / regulation / offtake)

These filters are applied on top of the price radar. They are heuristics, not decisions.

## Purpose
Turn a price signal into the question: "Can I enter this with limited capital, and where?"

## Current heuristics (see mashina/filters.py)
- Low capital + light regulation: software, data, pure trading, arbitrage.
- High capital + heavy regulation: refining, plants, mining, defense, pharma, energy infrastructure.
- Strong offtake: public tenders, green mandates, long-term offtake agreements.

## Preferred jurisdictions for testing
- NL: fast setup, commodity/logistics hub.
- DK: living base + EU access.
- CH / SG / AE: lower tax trading and holding structures.

## How to use
1. Run the radar (`python -m mashina.radar`).
2. Take the top lasting price rises.
3. Run `score_entry()` from `mashina.filters` on each title.
4. Manually verify offtake and permits before treating any signal as actionable.

This layer does not replace the physical-constraint check. It only adds the "can I enter" question.
