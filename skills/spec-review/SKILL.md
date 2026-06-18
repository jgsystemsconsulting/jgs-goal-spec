---
name: spec-review
description: Autonomously harden an engineering specification through a roundtable of independent engineering-discipline reviewers (architecture, security, test/QA, operations, product). Each reviewer is a real subagent thinking independently; the orchestrator collects findings, revises the spec itself, and loops until convergence (no CRITICAL or MAJOR findings) with NO user checkpoints. Use when you say "review this spec", "harden this spec", "spec review", "run the roundtable on this spec", or want a spec battle-tested before implementation. Self-contained — no dependency on any other skill.
compatibility: Agent tool (spawns reviewer subagents), file read/write for the spec + triage log
---
<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->


# Spec Review — Autonomous Multi-Discipline Hardening

Drive an engineering specification to convergence through repeated rounds of **independent
multi-discipline review**. Each round spawns several reviewer subagents — one per engineering
discipline — that critique the spec from their own expertise, **in parallel, thinking
independently**. The orchestrator (you) collects their findings, revises the spec to fix the
genuine ones, and **loops automatically until no CRITICAL or MAJOR findings remain**.

This runs **fully autonomously**: no user checkpoints between rounds. The user sees the converged
spec (and a round-by-round summary) at the end.

This is the **final skill** in a three-skill chain, but is fully usable standalone:

```
goal-formatter  →  goal-spec  →  spec-review
                                 (THIS: autonomous
                                  roundtable hardening
                                  to convergence)
```

> **Heritage & independence.** The roundtable mechanic — real independent subagents, each a
> distinct expert voice, spawned in parallel — is inspired by multi-agent group-discussion
> patterns. This skill is a **clean-room fork with NO dependency on any other skill, external
> config file, or agent manifest.** Its personas are defined inline below. It can be shared and
> run entirely on its own. The convergence discipline (severity classes, no-CRITICAL/MAJOR stop,
> triage log) follows a standard iterative adversarial-hardening pattern but invokes no other
> skill to do it.

## When to use

**Trigger phrases:**
- "Review this spec" / "Harden this spec" / "Spec review"
- "Run the roundtable on this spec"
- "Battle-test this specification"
- "Get multiple engineering perspectives on this spec"

**Input:** a specification — ideally one using the 8-section engineering template
(Problem & Context, Scope, Requirements, Constraints, Design Approach, Success Criteria,
Risks & Mitigations, Open Questions). It works on any spec/design doc, but the disciplines map
most cleanly onto that structure. If the input isn't a spec, say so and suggest `goal-spec` first.

---

## The reviewer personas (defined inline — no external manifest)

Each round spawns a subset of these as **independent subagents**. They are the "engineering
disciplines" whose concerns must be addressed — a fixed, spec-focused, self-contained roundtable.

| Persona | Icon | Lens — what they attack |
|---------|------|--------------------------|
| **Architect** | 🏛️ | Structural soundness: component boundaries, coupling, data flow, scalability, whether the Design Approach actually satisfies every requirement, missing interfaces, hidden complexity. |
| **Security Reviewer** | 🔒 | Threat surface: auth/authz, input validation, data exposure, secrets, trust boundaries, abuse cases, compliance gaps. Assumes the system will be attacked. |
| **Test/QA Engineer** | 🧪 | Verifiability: is each requirement testable? Are success criteria measurable & binary? Edge cases, failure modes, untestable claims, missing acceptance criteria. |
| **Operations / SRE** | ⚙️ | Run-time reality: deployability, observability, failure recovery, rollback, performance budgets, maintenance burden, on-call impact, capacity. |
| **Product / Scope Owner** | 🎯 | Intent & boundaries: does the spec solve the stated problem? Scope creep, gold-plating, missing user need, unstated assumptions, conflicting requirements, vague "Open Questions". |

**Domain-adapt the personas to the spec (do this before Round 1).** The five lenses are
universal, but their *concrete focus* shifts with the artifact. Re-map them to the domain rather
than reviewing a non-software spec through a software lens:
- **Software/service:** Security = threat surface/auth/data; Ops = deploy/observability/SRE.
- **Physical product (e.g. hardware, a device):** Security = product *safety* + data/privacy
  (electrical, thermal, battery, biocompatibility, RF); Ops = *manufacturability* (DFM), supply
  chain, line QA, field reliability/RMA, EOL.
- **Data/ML:** Security = privacy/PII/model-abuse; Ops = pipeline reliability, drift, retraining.
- **Process/org spec:** Security = compliance/risk; Ops = rollout, training, sustainment.
State the mapping you're using in one line at the start so the reviewers attack the right things.
*(Lesson from live runs: a user shouldn't have to hand-map personas in the invocation — infer the
domain from the spec and adapt automatically.)*

**Persona selection per round:**
- **Default:** spawn all five for Round 1 (full coverage of a fresh spec).
- **Later rounds:** spawn only the disciplines whose findings were unresolved last round, plus
  any whose area the latest revision touched. (Don't re-run a clean discipline every round —
  that inflates findings and cost.)
- **Small/narrow spec:** 3 personas may suffice — always include Architect + Test/QA, then the
  most relevant third.

---

## Severity classification (shared across all personas)

Every finding is one of:

- **CRITICAL** — a contradiction, impossibility, or gap that makes the spec un-implementable as
  written, OR a security/data-loss flaw that would ship broken or unsafe. The spec cannot
  converge while any CRITICAL stands.
- **MAJOR** — a missing definition, untestable requirement, undefined interface, or gap that
  would cause a competent implementer to **build the wrong thing or ship broken behaviour**.
  Ask: "Would a competent implementer get this wrong?" If yes → MAJOR.
- **ADVISORY** — clarity, minor inconsistency, nice-to-have, or a concern about a hypothetical
  future case. Advisory-only rounds **count as converged**.

**Cross-persona promotion:** if 2+ personas independently raise the same finding, promote it one
level (ADVISORY → MAJOR, MAJOR → CRITICAL). Tag it with the personas that raised it.

**Do not mandate findings.** A persona that finds nothing genuine reports nothing — manufacturing
issues to look thorough is a failure, not a virtue.

---

## The autonomous loop

Run this without stopping for the user. The user gets the result at the end.

### Phase 0 — Setup (once)

1. **Read the spec fully.** Hold the file path; you will edit this file in place each round.
2. **Pre-loop sanity check** — fix these yourself before Round 1 (they're authoring defects, not
   review findings):
   - Every section of the template has real content (no empty headings).
   - No placeholder artifacts (`TODO`, `[GAP]`, `MISSING`, truncated blocks).
   - Every term used in a requirement is defined somewhere.
   If any fail, patch the spec, then proceed.
3. **Create a triage log** next to the spec: `<spec-name>-spec-review-log.md` with header:
   ```
   | Round | Persona | Severity | Finding | Verdict | Action |
   |-------|---------|----------|---------|---------|--------|
   ```
   Update it after every round — it survives context compaction; in-context tables don't.
4. Set `round = 1`, `max_rounds = 6` (hard cap — see Stop conditions).

### Phase 1 — Review (each round)

Spawn the selected personas as **independent subagents in parallel** (all Agent tool calls in a
single message so they run concurrently). Give each subagent this prompt, filled in:

```
You are the {Persona} ({icon}) on an engineering spec-review roundtable. You think
independently — do NOT defer to the other reviewers; bring your own discipline's concerns.

## Your lens
{the persona's "what they attack" row, verbatim}

## The specification under review
{full spec text, or — if >400 lines — the normative sections verbatim + compressed prose}

## What changed since last round (omit in Round 1)
{one-line summary of the revisions made after the previous round}

## Your task
Review the spec ONLY through your discipline's lens. Find genuine problems that would cause this
spec to fail in your area. For each, classify severity:
- CRITICAL: makes the spec un-implementable as written, or unsafe/data-losing.
- MAJOR: would make a competent implementer build the wrong thing or ship broken behaviour.
- ADVISORY: clarity / minor / hypothetical-future only.
Do NOT manufacture findings. If your area is clean, say so and return an empty findings list.

## Output — return EXACTLY this JSON, nothing before it:
{
  "persona": "{Persona}",
  "critical": [{"loc": "section/line", "what": "<=30 words", "fix": "<=20 words"}],
  "major":    [{"loc": "...", "what": "...", "fix": "..."}],
  "advisory": [{"loc": "...", "what": "...", "fix": "..."}],
  "verdict": "ISSUES_FOUND" | "CLEAN"
}
Use verdict "ISSUES_FOUND" if you have any CRITICAL or MAJOR; otherwise "CLEAN".
Do NOT use any tools. Just return the JSON.
```

**Model:** default the reviewer subagents to a capable model (Sonnet is sufficient for
typical specs; use Opus for dense/safety-critical specs). The value is the multi-lens
independence, not raw model size.

### Phase 2 — Triage & revise (each round, you do this — NOT a subagent)

1. Collect all persona JSON payloads.
2. Apply **cross-persona promotion** (same finding from 2+ personas → promote one level).
3. **Triage each finding:** is it genuine?
   - **Genuine CRITICAL/MAJOR** → fix it: edit the spec file in place. Keep fixes minimal and
     targeted to the finding; don't rewrite wholesale.
   - **Not genuine / wrong** (reviewer misread, out-of-scope, already handled) → record verdict
     "rejected" + one-line rationale; do not edit.
   - **Genuine ADVISORY** → apply if cheap and safe; otherwise log as deferred.
4. **Log every finding** in the triage file with its verdict and the action taken.
4a. **Consistency sweep after revising (DO NOT SKIP).** Any fix that changes a *value* (a number,
   a chosen part, a renamed term) almost always appears in more than one section — the requirement,
   the design, the success criteria, the risks, an interface table. After editing, **re-scan the
   whole spec for the OLD value and for sections that depend on the changed one**, and update every
   occurrence. Stale duplicates left behind by an edit are the single most common defect this loop
   catches in later rounds (and the easiest to prevent here). Treat the spec as having ONE source of
   truth per fact.
5. **Resolve Open Questions:** since this is autonomous, you MUST decide undecided items yourself
   using the spec's own context and sensible engineering defaults, then record the decision in
   the spec (move it from "Open Question" to the relevant section with a stated assumption).
   Only leave an item open if deciding it would change external commitments the spec can't
   assume — and flag those explicitly in the final summary.

### Phase 3 — Convergence test (each round)

- **Converged** when, in a round, **no persona returns any CRITICAL or MAJOR** (all `CLEAN`, or
  advisory-only). → go to Exit.
- **Not converged** → `round += 1`; if `round <= max_rounds`, go to Phase 1 (re-select personas
  per the selection rule). If `round > max_rounds`, go to Exit with a **non-converged** flag.

**Anti-inflation safeguard:** if a round produces only ADVISORY findings that are reworded
versions of previously-rejected ones, treat the round as converged — don't loop forever chasing
taste-level churn.

### Exit

When the loop ends, present to the user (this is the only mandatory user-facing output):

1. **Final spec** (the hardened file) — note its path.
2. **Convergence status:** "Converged in N rounds" OR "Hit max rounds (6) with M residual
   findings" (list them).
3. **Round-by-round summary:** per round — personas run, CRITICAL/MAJOR found, what was fixed.
   Source it from the triage log.
4. **Decisions made autonomously** on former Open Questions, with the assumption behind each.
5. **Residual / deferred items** the user should know about.
6. **The ready-to-run `/goal` prompt** (see "MANDATORY exit artifact" below) — a copy-pasteable
   command that hands the goal + hardened spec to an executor, including model-selection and
   parallelisation guidance. This is the final thing the user sees so they can act immediately.

---

## Stop conditions (so it never runs away)

- **Convergence:** no CRITICAL/MAJOR in a round → stop (success).
- **Max rounds:** hard cap of **6 rounds** → stop and report residuals (don't loop indefinitely).
- **No-progress:** if two consecutive rounds fix nothing genuine (only rejected/advisory churn)
  → stop and report (treat as converged-with-advisories).

---

## Why fully autonomous (and when that's wrong)

The user chose hands-off hardening: agents debate, you respond to feedback automatically, revise,
and loop until convergence with no human in the loop. This is right for **hardening a spec the
user already broadly agrees with** — it removes the round-by-round babysitting.

It is the WRONG mode if the spec's *direction* is still unsettled (the personas will keep
flagging the same foundational disagreement and you'll auto-decide things the user wanted a say
in). In that case, tell the user up front: "this spec has an unresolved directional question (X);
autonomous hardening will pick a default — confirm the direction first, or I'll assume Y." Then
proceed with the stated assumption rather than silently choosing.

---

## Worked example (compressed)

**Input:** a spec for an API rate limiter (8-section template).

- **Round 1** (all 5 personas, parallel):
  - 🔒 Security (MAJOR): "no spec for limit-bypass via spoofed X-Forwarded-For" → fix: bind
    limits to authenticated key, not client IP.
  - 🧪 Test/QA (MAJOR): "Success criterion 'handles burst traffic' not measurable" → fix:
    "rejects >100 req/s/key with 429; p95 added latency <5ms".
  - 🏛️ Architect (ADVISORY): "token-bucket store could be Redis or in-proc — unspecified" →
    decide: Redis (shared across instances); record assumption.
  - ⚙️ Ops (CLEAN). 🎯 Product (CLEAN).
  - Triage: fix both MAJORs, decide the architect's open question. Round not converged.
- **Round 2** (Security + Test/QA + Architect — the touched disciplines):
  - All return CLEAN. → **Converged in 2 rounds.**
- **Exit:** present hardened spec, "Converged in 2 rounds", the two fixes, and the Redis decision
  as an autonomous call.

---

## After convergence — execute the spec

**This skill produces a hardened spec; it does not implement it.** Authoring ends here;
execution is the next, separate phase — performed by whatever executor you choose, not by
this skill. The whole point of the chain is to reach a spec trustworthy enough to hand off
for implementation with confidence.

Once the spec has converged (no CRITICAL/MAJOR), hand the **goal + hardened spec** to an
execution agent. Good options:

- **Claude Code `/goal`** — paste the goal; point it at the spec file as the detailed design.
- **An autonomous loop** (e.g. an autopilot / ralph-style runner) — feed it the spec as the
  source of truth and let it implement to the spec's Success Criteria.
- **An `executor` subagent** — dispatch with the spec inline; verify its output against the
  spec's Success Criteria (§6) and Verification.

Whatever the executor, the spec's **Success Criteria (§6)** are the acceptance gate: execution
is done when every criterion is observably met. Tell the user this explicitly at exit so the
loop closes on a *built* outcome, not just a *written* one.

### MANDATORY exit artifact — the ready-to-run `/goal` prompt

At the very end of the run, after the convergence report, you MUST print a **copy-pasteable
`/goal` command** the user can paste straight into Claude Code (or hand to any agent) to execute
the spec. Put it in its own fenced block so it's one-click to copy. Use this exact shape, filled
in from the converged spec:

```
/goal "Implement <one-line goal restated>. The authoritative design is the hardened spec at
<relative/path/to/spec.md> — build to it exactly. Acceptance gate: every Success Criterion
(SC1..SCn in §6) must be observably met; do not declare done until each passes its stated
verification.

WORK EFFICIENTLY:
- Use the best-suited model per task: a fast/cheap model (e.g. Haiku) for lookups, file scans,
  and mechanical edits; a standard model (e.g. Sonnet) for implementation, tests, and review;
  a deep model (e.g. Opus) only for architecture, tricky debugging, or security-sensitive work.
- Parallelise aggressively: decompose the spec's Design Approach (§5) into INDEPENDENT
  components, then dispatch them as concurrent subagents in a single batch rather than building
  sequentially. Only serialise where a real data dependency forces it. State the parallel groups
  before starting.
- Keep a writer/verifier split: implement in one pass, then verify against §6 in a SEPARATE pass
  (ideally a different subagent) — never self-approve the same context."
```

Fill the bracketed parts from the actual spec; pull the parallel groups from the Design
Approach's component decomposition (§5) when it already names what can run in parallel. Keep the
efficiency guidance verbatim — it is generic and applies to any executor. If the spec is for a
NON-software artifact (e.g. a physical product), reword "build/tests" to the artifact's
equivalent (e.g. "produce the costed BOM + prototype plan; verification = the SC bench tests"),
but keep the model-selection and parallelisation guidance.

---

## Relationship to the other skills

- **Upstream — `goal-spec`:** produces the 8-section spec this skill hardens. If the user hands
  you a goal rather than a spec, point them to `goal-spec` first.
- **No external-skill dependency:** this skill defines its own personas inline and runs its own
  loop. It shares the *idea* of an independent-subagent roundtable and the *idea* of a
  converge-on-no-CRITICAL/MAJOR loop with other multi-agent and review skills, but invokes none
  of them and needs no config/manifest files. It is safe to share standalone.
