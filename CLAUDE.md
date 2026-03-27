# Project: TCO Calculator

## What This Does
A tool for accurately calculating the Total Cost of Ownership (TCO) for various problems and issues, with a focus on IT-related scenarios. Designed to surface hidden costs and provide comprehensive cost analysis beyond simple sticker-price comparisons.

## Key Contacts / Stakeholders
- **Joel** — Owner/Developer

## Project Flags
- Project Tier: Bronze
- Personal project — not a Merakey PMO initiative, but results may feed into Merakey projects

## Scope Boundaries

DO:
- Calculate TCO for recurring IT issues (help desk tickets, process inefficiencies)
- Calculate ROI for proposed improvements and investments
- Calculate implementation TCO including hidden costs (training, productivity dip)
- Calculate downtime costs per event and annualized
- Model opportunity cost using both conservative (loaded cost) and full-impact (revenue-based) methods
- Support Merakey-specific defaults with configurable org settings
- Enable sharing via clipboard export, JSON export, and print-to-PDF

DO NOT:
- Backend server or database — all state is localStorage
- User authentication or multi-user features
- Integration with Asana, Jira, or other PM tools
- Automated data ingestion from ticketing systems
- Financial modeling beyond 5-year horizon

## Key Deliverables
1. `src/calculator.html` — Single-file React web app (portable, no build step)
2. `reference/formula-research.md` — Documented formulas with citations
3. `reference/org-defaults.json` — Merakey default values
4. `tools/validate_formulas.py` — Pytest tests validating all calculations

## Key Decisions
- **Single-file HTML with CDN dependencies** — no build step, maximally portable (email, SharePoint, GitHub Pages)
- **Revenue-per-employee replaces arbitrary role multipliers** — grounded in organizational data or industry defaults
- **Conservative/full-impact dual display** — always shows both so user can choose based on audience
- **Three-row cost breakdown (Direct / Opportunity / Total)** — consistent across all modes, avoids double-counting
- **localStorage for persistence** — zero infrastructure, scenarios survive page reload
- **Value multiplier fallback** when revenue data unavailable — default 2.0x loaded cost for healthcare

## Open Questions
- What is Merakey's annual revenue? (Needed for revenue-based opportunity cost calculation)
- Should the calculator be deployed to GitHub Pages or internal SharePoint?

## Decision Logging
When I make a significant decision during a session (architecture choice, vendor selection, scope change, stakeholder commitment), append it to decisions.md. Only log decisions, not tasks or notes.

---

# Agent Instructions

You're working inside the **WAT framework** (Workflows, Agents, Tools). This architecture separates concerns so that probabilistic AI handles reasoning while deterministic code handles execution. That separation is what makes this system reliable.

**Organizational Context:** Read `C:\Users\joels\Code\.claude\org-context.md` for stakeholder patterns and project context.

## The WAT Architecture

**Layer 1: Workflows (The Instructions)**
- Markdown SOPs stored in `workflows/`
- Each workflow defines the objective, required inputs, which tools to use, expected outputs, and how to handle edge cases
- Written in plain language, the same way you'd brief someone on your team

**Layer 2: Agents (The Decision-Maker)**
- This is your role. You're responsible for intelligent coordination.
- Read the relevant workflow, run tools in the correct sequence, handle failures gracefully, and ask clarifying questions when needed
- You connect intent to execution without trying to do everything yourself
- Example: If you need to pull data from a website, don't attempt it directly. Read the relevant workflow, figure out the required inputs, then execute the appropriate tool script

**Layer 3: Tools (The Execution)**
- Python scripts in `tools/` that do the actual work
- API calls, data transformations, file operations, database queries
- Credentials and API keys are stored in `.env`
- These scripts are consistent, testable, and fast

**Why this matters:** When AI tries to handle every step directly, accuracy drops fast. If each step is 90% accurate, you're down to 59% success after just five steps. By offloading execution to deterministic scripts, you stay focused on orchestration and decision-making where you excel.

## How to Operate

**1. Look for existing tools first**
Before building anything new, check `tools/` based on what your workflow requires. Only create new scripts when nothing exists for that task.

**2. Learn and adapt when things fail**
When you hit an error:
- Read the full error message and trace
- Fix the script and retest (if it uses paid API calls or credits, check with me before running again)
- Document what you learned in the workflow (rate limits, timing quirks, unexpected behavior)

**3. Keep workflows current**
Workflows should evolve as you learn. When you find better methods, discover constraints, or encounter recurring issues, update the workflow. Don't create or overwrite workflows without asking unless I explicitly tell you to.

## The Self-Improvement Loop
1. Identify what broke
2. Fix the tool
3. Verify the fix works
4. Update the workflow with the new approach
5. Move on with a more robust system

## File Structure
- **Deliverables**: Final outputs go to cloud services (Google Sheets, Slides, etc.) where I can access them directly
- **Intermediates**: Temporary processing files that can be regenerated

```
workflows/      # Markdown SOPs defining what to do and how
reference/      # Source documents, meeting notes, policy docs (read-only context)
tools/          # Python scripts for execution
.tmp/           # Temporary files (gitignored)
```

**Core principle:** Local files are just for processing. Anything I need to see or use lives in cloud services.

## Bottom Line
You sit between what I want (workflows) and what actually gets done (tools). Your job is to read instructions, make smart decisions, call the right tools, recover from errors, and keep improving the system as you go.
Stay pragmatic. Stay reliable. Keep learning.
