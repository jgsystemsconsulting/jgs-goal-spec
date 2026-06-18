---
name: goal-spec
description: Turn a goal (or a goal + draft spec) into a complete, detailed engineering specification by defining all eight spec sections and asking gap-filling clarifying questions grounded in the user's stated goal. Use when you say "spec this goal", "write a spec for X", "define the specification", "flesh out the spec", or have a goal that needs to become an implementable design. Pairs with goal-formatter (upstream) and spec-review (downstream). Model-agnostic.
compatibility: Git, repo read access, AskUserQuestion (for clarifying questions)
---
<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->


# Goal Spec

Convert a **goal** into a **complete engineering specification**. The goal-formatter answers
*"what does done look like?"*; this skill answers *"what exactly are we building, and how?"* — by
defining every section of the spec and **asking the user gap-filling questions** wherever the goal
leaves a section under-determined.

This is the **middle skill** in a three-skill chain:

```
goal-formatter  →  goal-spec  →  spec-review
 (goal + draft     (THIS: full     (autonomous
  spec, optional)   defined spec    multi-discipline
                    via Q&A)        hardening loop)
```

Each skill is independently invocable. The handoff works because all three use the **same
8-section engineering spec template** (defined below — this skill owns it).

## When to use

**Trigger phrases:**
- "Spec this goal" / "Write a spec for X"
- "Define the specification" / "Flesh out the spec"
- "Turn this goal into a spec"
- "I have a goal, now I need the detailed design"

**Best for:**
- A goal that's clear on *done* but vague on *how* / *what exactly*
- Work where requirements, constraints, and design approach need to be pinned down before coding
- Producing an artifact you'll then harden with `spec-review`

## Inputs this skill accepts

1. **A goal** (e.g. the output of goal-formatter) — most common.
2. **A goal + draft spec** (goal-formatter's spec mode output) — this skill *completes and
   refines* the draft rather than starting blank.
3. **A raw description** — if no goal exists yet, suggest running goal-formatter first, but you
   MAY proceed by inferring an implicit goal from the description.

---

## The canonical engineering spec template (8 sections)

This is the **shared contract** across goal-formatter (draft-spec mode), goal-spec, and
spec-review. All three MUST use these exact section names so handoffs line up with no
orphaned or renamed sections.

```
# Specification: <title>

## 1. Problem & Context
What problem this solves, why now, and the background a reader needs. Tie back to the
originating goal: one line stating the goal this spec satisfies.

## 2. Scope
- **In scope:** explicit list of what this spec covers.
- **Out of scope:** explicit list of what it deliberately excludes (prevents scope creep).

## 3. Requirements
- **Functional (FR1, FR2, …):** what the system MUST do, numbered for traceability.
- **Non-functional (NFR1, NFR2, …):** performance, security, reliability, usability,
  maintainability targets — each measurable where possible.

## 4. Constraints
Hard limits the design must respect: tech stack, platforms, compatibility, regulatory,
budget, timeline, "must not change" baselines. Distinct from requirements — these bound
the solution space rather than describe behaviour.

## 5. Design Approach
The proposed solution shape: components, data flow, key interfaces, major decisions and
their rationale. Note alternatives considered and why rejected, where it matters.

## 6. Success Criteria
Observable, binary done/not-done conditions. Each criterion maps to a requirement and to a
verification step. (Inherits the goal's success criteria; refines them to spec granularity.)

## 7. Risks & Mitigations
What could go wrong (technical, integration, dependency, adoption) and the planned
mitigation or contingency for each.

## 8. Open Questions
Anything still undecided. Every item here is either (a) resolved via a clarifying question
to the user, or (b) explicitly flagged as deferred with an owner/trigger for resolution.
```

A copy-pasteable version of this template lives at
`references/spec-template.md` in this skill's directory.

---

## What the skill does

### 1. Read the goal and any draft spec
- Parse the supplied goal (success criteria, constraints, scope, verification).
- If a draft spec was provided, map its content onto the 8 sections.
- Read relevant repo state (git history, memory, code) the way goal-formatter does, so the
  spec is grounded in reality, not invented.

### 2. Draft all 8 sections
Fill every section from the goal + repo context. Where the goal supplies an answer, use it.
Where it doesn't, mark the section with an explicit **`[GAP: …]`** placeholder describing what's
missing — do NOT silently invent. Collect every `[GAP: …]` into the Open Questions section.

### 3. Ask gap-filling clarifying questions (the core of this skill)

For each `[GAP]`, decide: can I resolve it from the goal/repo, or must I ask the user?

**Ask the user via `AskUserQuestion`** when the gap is a genuine decision only they can make
(scope boundary, priority, target numbers, tech choice, acceptable trade-off). Rules:
- Group related gaps; ask in **batches of up to 4 questions** per `AskUserQuestion` call.
- **Ground every question in the user's stated goal** — reference what they said they wanted, so
  the question reads as "to satisfy *your goal of X*, which of these…?" not a generic survey.
- Offer concrete options with trade-offs; recommend one (mark it "(Recommended)") when there's a
  sensible default.
- Only ask what changes the spec. If a gap has an obvious default, fill it and note the
  assumption in the spec rather than asking.

**Resolve yourself** (no question) when the goal or repo already implies the answer, or a
conventional default clearly applies — record it as a stated assumption in the relevant section.

### 4. Integrate answers and finalize
- Fold every answer back into the right section.
- Clear resolved items from Open Questions; leave only genuinely-deferred ones (each flagged
  with why it's deferred and what would resolve it).
- Re-check section consistency: Requirements ↔ Success Criteria ↔ Design Approach must describe
  the same system.

### 5. Self-review before presenting (MANDATORY)

Run the **Spec Self-Review Rubric** (below) against the draft. Fix any FAIL (max 2 rounds), then
present. This mirrors goal-formatter's step-3 gate — a spec that ships with hidden gaps fails
downstream in spec-review or in implementation.

### 6. Offer the handoff
After presenting the spec, tell the user they can run **`spec-review`** to harden it through an
autonomous multi-discipline review loop. Don't auto-invoke it — let the user choose.

---

## Apply model-agnostic framing principles

The spec is written so **any** model or agent can implement from it without your context:
- **Number requirements** (FR1, NFR1…) so they're individually addressable and traceable.
- **Imperative, unambiguous language** — MUST / MUST NOT / ONLY, not "should" / "try to".
- **Self-contained** — spell out file paths, IDs, versions, baselines inline; assume zero
  conversation history.
- **Decompose** the Design Approach into independent components with stated dependencies; name
  what can be built in parallel vs. what is strictly sequential.
- **State measurable targets** in NFRs ("p95 < 200ms", not "fast").
- **Mark execution parallelism** — in the Design Approach, explicitly say which components are
  INDEPENDENT (can be built concurrently by parallel subagents) vs. strictly sequential. The
  downstream executor uses this to parallelise; an undecomposed blob forces slow serial work.

---

## Spec Self-Review Rubric

Run against every drafted spec in step 5 before presenting. Each row PASS/FAIL. **Any FAIL →
revise (max 2 rounds), then present with explicit flags for anything still failing.**

| # | Check | PASS looks like | FAIL looks like |
|---|-------|-----------------|-----------------|
| 1 | **All 8 sections present** | Every template section has real content | A section missing or left as a heading |
| 2 | **Requirements numbered & testable** | Each FR/NFR is atomic, numbered, and verifiable | Vague blobs, unnumbered, untestable |
| 3 | **Scope both ways** | In-scope AND out-of-scope explicitly listed | Only in-scope, or open-ended |
| 4 | **Constraints distinct from requirements** | Constraints bound the solution; requirements describe behaviour | The two conflated or constraints absent |
| 5 | **Design maps to requirements** | Every FR is satisfied by something in Design Approach | Requirements with no design, or design for nothing |
| 6 | **Success criteria measurable & mapped** | Each criterion is binary, has a NUMERIC threshold (or an objective observation), AND names the verification method + sample size where physical | "Works well", adjectives, or a criterion with no stated test method |
| 7 | **Grounded in repo reality** | Paths, versions, counts verified, not guessed | Invented specifics |
| 8 | **No silent gaps** | Every gap is either resolved or listed in Open Questions | A `[GAP]` left buried in a section |
| 9 | **Risks have mitigations** | Each named risk has a mitigation/contingency | Risks listed with no response |
| 10 | **Self-consistent** | Sections 1, 3, 5, 6 describe the same system; a value (number/part/term) appears identically everywhere it is referenced | Sections contradict each other; the same fact stated two different ways |
| 11 | **Every NFR/safety target is testable** | Each performance, safety, or regulatory target is a number/range a test can pass/fail | A safety or perf target stated as an adjective, or with no acceptance test |
| 12 | **No unstated assumptions** | Any value the skill filled by default (not user-given) is explicitly labelled as an assumption | A specific value asserted as fact when it was actually a guess |

**Revision discipline:** fix the *specific* failing row; re-score only after editing. If two
rounds can't clear a row, present the spec with that row flagged as a residual risk.

---

## Example flow

**You say:**
> "Spec this goal" — and paste a goal-formatter goal about adding a rate limiter to the public API.

**The skill:**
1. Maps the goal's success criteria/constraints onto the 8 sections; reads the API code.
2. Drafts all 8; finds gaps: *which* limiting algorithm? per-key or per-IP? what limit values?
   what happens on breach (429 vs queue)? Marks each `[GAP]`.
3. Asks via `AskUserQuestion`, grounded in the goal: *"To satisfy your goal of protecting the
   public API without harming legit users, which limiting strategy?"* → token-bucket (Recommended)
   / fixed-window / sliding-log, with trade-offs.
4. Folds answers in; clears Open Questions; checks consistency.
5. Self-reviews against the rubric; revises.
6. Presents the full spec and offers: *"Run `spec-review` to harden this autonomously?"*

---

## What you do after

1. Review the spec; adjust anything the Q&A didn't catch.
2. **Run `spec-review`** to drive it through autonomous multi-discipline hardening to convergence.
3. Implement from the hardened spec (any model/agent), or feed it into your planning workflow.

---

## Relationship to the other skills

- **Upstream — `goal-formatter`:** produces the goal (and optionally a draft spec) this skill
  completes. If the user only has a rough idea, point them there first.
- **Downstream — `spec-review`:** takes the spec this skill produces and hardens it through an
  autonomous roundtable of engineering-discipline reviewers until it converges (no
  CRITICAL/MAJOR findings). Self-contained — no dependency on any other skill.
