# Decision Log

## Active Decisions

| Date | Decision | Rationale |
|---|---|---|
| 2026-03-27 | Single-file HTML app (React + Tailwind via CDN) | Max portability — no build step, can be emailed, opened locally, or hosted on SharePoint/GitHub Pages |
| 2026-03-27 | Replace arbitrary role multipliers with revenue-per-employee or configurable value multiplier | Original 0.25x–2.0x multipliers had no empirical basis. New approach uses org revenue data or industry-standard 2.0x loaded cost for healthcare |
| 2026-03-27 | Three-layer cost display (Direct / Opportunity / Total) across all modes | Avoids double-counting risk in Joel's original framing. Direct = paid-for-nothing, Opportunity = value delta, Total = full value per hour |
| 2026-03-27 | Two estimation modes: Conservative (loaded cost) and Full Impact (revenue-based) | Conservative for formal business cases and budget requests; Full Impact for strategic analysis and true organizational cost |
| 2026-03-27 | localStorage for all persistence (org settings, scenarios) | Zero-infrastructure approach appropriate for a personal BA tool with sharing via export |
| 2026-03-27 | Default benefits multiplier 1.4x for healthcare | Based on industry benchmarks (general 1.25-1.4x, IT 1.4-1.6x); 1.4 is appropriate for mixed healthcare workforce |
| 2026-03-27 | Default value multiplier 2.0x loaded cost | Conservative end of 1.5-2.5x range for healthcare/nonprofit when revenue data is unavailable |

## Superseded
<!-- Decisions that were later changed or reversed -->
