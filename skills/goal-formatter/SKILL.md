---
name: goal-formatter
description: Convert verbal task descriptions into structured, testable goals. Use when you say "write me a goal", "create a goal for X", or want to frame work as a measurable objective. Analyzes repo state (git history, technical debt, memory, code) to synthesize clear goals with success criteria, verification methods, and test coverage outlines, then SELF-REVIEWS the draft against a quality rubric and revises before presenting. Optionally also emits a draft engineering specification alongside the goal (spec mode) for handoff to the goal-spec and spec-review skills. Model-agnostic — works with any LLM or agent framework.
compatibility: Git, Python, repo read access, memory files
---
<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->


# Goal Formatter

## When to use

Invoke this skill whenever you want to **convert a verbal description into a structured, testable goal** that any model or agent can execute without your context.

**Trigger phrases:**
- "Write me a goal"
- "Create a goal for X"
- "Generate a goal"
- "Frame this as a goal"
- "Set a goal for [task]"

**Best for:**
- Multi-step tasks with unclear scope
- Work that needs both execution clarity and test coverage planning
- Decisions about what "done" means before starting

## What the skill does

### 1. Analyze repo state
- Read git history (recent commits, branches, tags)
- Parse memory files (MEMORY.md, project memory)
- Check current code state (test pass rate, build status)
- Surface technical debt and blockers from context

### 2. Synthesize a testable goal
The skill generates a **draft** goal in this structure (it is not presented yet — step 3 reviews it first):

```
## Goal
[Clear, measurable end state]

## Success Criteria
- Test coverage: [high-level percentage paths]
- Build status: [specific condition]
- Artifact validation: [what must be true]
- Constraints: [what must NOT change]

## Verification Method
[How the executing agent will prove it's done — measurable, observable]

## Reference Points
[Known-good examples, related prior work, baseline state]
```

### 3. Self-review the draft (MANDATORY — do not skip)

**Before presenting the goal, review your own draft against the rubric below and revise.** A goal is an instruction set another agent (or model) will execute without your context — a vague or untestable goal silently fails downstream. This gate catches that.

This is a **rigid** step: always run it, even when the draft "looks fine."

1. Hold the drafted goal as `draft`.
2. Score it against every item in the **Self-Review Rubric** (below). For each FAIL, note the specific defect.
3. If any rubric item FAILs → **revise `draft` to fix it**, then re-score. Max **2 revision rounds**.
4. After 2 rounds, if an item still can't pass, **present the goal anyway but flag the residual gap explicitly** to the user (e.g. "⚠️ Verification for criterion X is manual-only — no automated check exists"). Never silently ship a known-weak goal.
5. Only present the goal once it passes the rubric (or carries explicit flagged residuals).

Do this review **in the same turn**, inline — it does not require a subagent. For a large or high-stakes goal, you MAY dispatch a separate `critic`/`verifier` subagent for an independent pass, but the inline rubric check is always required.

### 4. Apply model-agnostic framing principles
The goal is written so **any** model or agent can execute it without your context. Apply these universal prompting principles to the goal text:

- **Front-load the critical constraint.** State the single most important "do this / don't do that" at the very top, before the detail.
- **Use imperative, unambiguous language.** MUST / MUST NOT / ONLY — not "should" or "try to."
- **Decompose multi-step work into ordered, independent sub-steps** with explicit handoffs and dependencies. Name what can run in parallel vs. what is strictly sequential.
- **State the reasoning shape when it matters.** For analysis-heavy work, say "analyze X and report findings before changing anything"; for mechanical work, keep it terse.
- **Make every instruction self-contained.** Assume zero conversation history — spell out file paths, IDs, and baselines inline.

These principles are model-independent: they make a goal robust whether it's executed by a frontier model, a smaller local model, or an autonomous agent loop. If you ever need to tune for a *specific* model's quirks, do that as a thin layer on top — but the core goal stays portable.

---

## Spec mode (OPTIONAL — additive; default behavior is unchanged)

By default this skill emits **only the goal**. In **spec mode**, it *additionally* emits a
**draft engineering specification** alongside the goal, as the first step of a longer
spec-authoring chain:

```
goal-formatter (spec mode)  →  goal-spec  →  spec-review
 (goal + DRAFT spec)           (full spec     (autonomous
                                via Q&A)        hardening)
```

**When to enter spec mode:**
- The user explicitly asks for a spec: "write me a goal *and a spec*", "goal plus spec",
  "spec this out", "I need the detailed design too".
- The request is clearly a build/design effort (new feature, system, component) where a goal
  alone won't be enough downstream.

When the ask is a plain "write me a goal" with no spec signal, **stay in default mode — emit the
goal only.** Do not force a spec on a user who didn't ask for one.

**What spec mode adds:** after producing and self-reviewing the goal as normal, also produce a
**draft** of the 8-section engineering spec (below). It is a *draft* — deliberately incomplete
where the verbal description doesn't determine an answer. Mark every such gap with an explicit
`[GAP: …]` placeholder rather than inventing a value; the downstream `goal-spec` skill resolves
gaps by asking the user.

**The 8-section engineering spec template** (shared verbatim with `goal-spec` and `spec-review`
so the three hand off cleanly — same section names, no renaming):

```
# Specification: <title>

## 1. Problem & Context        — what/why + the goal this spec satisfies
## 2. Scope                    — in scope / out of scope (both explicit)
## 3. Requirements             — Functional (FR1…) + Non-functional (NFR1…)
## 4. Constraints              — hard limits bounding the solution
## 5. Design Approach          — components, data flow, key decisions + rationale
## 6. Success Criteria         — observable, binary, mapped to FRs (inherits the goal's)
## 7. Risks & Mitigations      — what could go wrong + planned response
## 8. Open Questions           — every [GAP] collected here for goal-spec to resolve
```

**Spec-mode rules:**
- The goal still comes first and still passes the step-3 self-review gate unchanged.
- The draft spec's **Success Criteria (§6)** must be consistent with the goal's success
  criteria — they describe the same end state at different granularity.
- Don't over-fill. A good draft spec confidently states what the description determines and
  honestly marks the rest `[GAP]`. Resolving gaps is `goal-spec`'s job, not this skill's.
- After presenting, point the user at the next step: "Run `goal-spec` to complete this draft into
  a full spec (it'll ask clarifying questions), then `spec-review` to harden it."

---

## Goal Template

The baseline goal works across all models and agents:

```
## Goal
[Clear, measurable end state]

## Success Criteria
- Test coverage: [high-level percentage paths]
- Build/validation status: [specific condition]
- Artifact quality: [what must be true]
- Constraints: [what must NOT change]

## Verification Method
[How the goal is proven complete — measurable, observable, checkable]

## Test Plan
[Rough outline of test coverage needed to validate all paths]

## Reference Points
[Known-good examples, baseline state, related prior work]
```

This template works with any model. The framing principles in step 4 are baked into how the goal is written, so no model-specific rewrite is needed before use.

---

## How to invoke

Say your verbal description naturally:

> "I want to close the v1 gap closure work. We've been focusing on v2 for months but there are still 22 expected-failing tests in v1. I know we have some progress on safety negatives but I'm not sure what the actual blocker is."

The skill will:

1. **Automatically read:**
   - Recent v1/v2 commit history
   - Memory entries on v1 gap closure state
   - Current test status from your repo

2. **Generate a goal like:**
```
## Goal
Achieve 100% v1 safety negative pass rate (57/57 tests green) 
while maintaining v2 test suite at ≥90% pass rate.

## Success Criteria
- v1 test suite: 57/57 safety negatives pass
- v2 contract tests: ≥90% pass rate (baseline protection)
- No regression in v1/v2 bridge coverage
- Git history shows clear atomic commits per fix

## Verification
$ pytest qa/v1/ -k safety_negative  # must exit 0
$ pytest qa/v2/ --tb=short         # must show ≥90% pass

## Execution Notes
MUST front-load: "Fix v1 safety negatives. Do NOT touch v2.
Each fix must be atomic and tested separately."
Two-phase: (1) analyze v1 failures and report root causes
BEFORE changing anything; (2) apply fixes with v2 regression guards.
Context to load: [recent commits, current blockers from memory].

## Reference
- Memory: v1_gap_closure_work_package.md (33 items, 6 spikes)
- Baseline: commit abc1234 (88.5% v1 verified)
- Known blocker: BRIDGE-NNN-013 pending restart
```

---

## Test-based success criteria

Every goal includes **test coverage suggestions** at a high level:

- **Unit path coverage:** "All code paths in X must be covered"
  - Example: "safety_negative.py → 5 assertion paths → each must have a test"
  
- **Integration coverage:** "End-to-end flows must validate"
  - Example: "v1 bridge accept_action → groovy execution → test assertion"

- **Constraint validation:** "No regression in [baseline area]"
  - Example: "v2 contract tests must stay ≥90%"

The goal describes the **coverage shape**, not individual test names. You then write tests to fill that shape.

---

## Self-Review Rubric

Run this against every drafted goal in step 3 before presenting it. Each row is PASS/FAIL. **Any FAIL → revise (max 2 rounds), then present with explicit flags for anything still failing.**

| # | Check | PASS looks like | FAIL looks like |
|---|-------|-----------------|-----------------|
| 1 | **Measurable end state** | The Goal states an observable, binary done/not-done condition | "Improve X", "make better", "clean up" with no threshold |
| 2 | **Verifiable criteria** | Every Success Criterion maps to a command, file check, or observation in Verification | A criterion no one can check (e.g. "code is clean") |
| 3 | **Verification is runnable** | Verification has concrete commands/steps an agent can execute and read the result of | "Confirm it works" with no how |
| 4 | **Constraints / must-NOT-change named** | Explicit list of what must not regress or change (slugs, schemas, baselines, scope) | No guardrails — agent free to refactor anything |
| 5 | **Scope boundary explicit** | In-scope and out-of-scope both stated; ambiguous items resolved or flagged | Open-ended; "and anything related" |
| 6 | **Grounded in repo reality** | Counts, paths, file names, baselines verified against the actual repo (not guessed) | Invented file paths, made-up test counts, stale assumptions |
| 7 | **Right size / decomposed** | Multi-step work is broken into independent groups with dependencies stated | One monolithic blob with hidden ordering |
| 8 | **Test/coverage shape present** | A Test Plan describes the coverage shape (unit/integration/constraint), even if rough | No mention of how completion is tested |
| 9 | **No fabricated specifics** | Every concrete claim (version, command, ID) is either verified or marked as "verify before use" | Confident-but-unchecked specifics that may be stale |
| 10 | **Self-consistent** | Goal ↔ Success Criteria ↔ Verification all describe the same end state | Criteria test things the Goal never asked for, or vice versa |

**Revision discipline:** fix the *specific* failing row — don't rewrite wholesale. Re-score only after editing. If two rounds don't clear a row (commonly #2/#3 when no automated check exists, or #6 when the repo can't confirm a fact), present the goal with that row called out as a residual risk so the user decides.

### Worked self-review (compressed)

**Draft criterion:** "Success: the diagrams look good."
- Rubric #1 FAIL (not measurable), #2/#3 FAIL (unverifiable).
- **Revision:** "Success: each exported diagram passes the visual self-check defect table (no label truncation, no overlapping symbols) — verified by the agent reading the exported JPEG and reporting a clean verdict, max 2 rounds." → #1 ✅ #2 ✅ #3 ✅.

---

## Example flow

**You say:**
> "Tidy up the main branch. We've merged a lot of feature work but docs are out of sync, old feature branches are cluttering things, and I want a clean state."

**Skill generates:**
```
## Goal
main branch is in "release-ready" state: docs synchronized, 
no stale branches, all PR checks green, CHANGELOG updated.

## Success Criteria
- docs/ARCHITECTURE.md ↔ actual codebase architecture (verified via code tour)
- Stale branches: 0 (anything not touched in 30d is archived)
- CI all green (no skipped checks)
- CHANGELOG.md ↔ recent commits (no gaps, all merges documented)

## Verification
1. Run code-tour tool against docs → zero architectural drift
2. Run: git branch -v | grep 30-days-old → empty
3. CI dashboard: all checks ✓
4. git log --grep="merge" | diff CHANGELOG.md → zero diff

## Execution Notes
MUST sequence in order: docs-sync → branch-cleanup → verify-CI.
Do NOT merge anything new during cleanup.
Phase 1 (compare docs to code) is reasoning-heavy — analyze and
report drift before editing. Phases 2-3 (stale branches, sign-off
summary) are mechanical.
```

---

## What you do after

1. **Copy the goal** into your `/goal` invocation
2. **Write tests** to cover the coverage percentages suggested
3. **Run the goal** in Claude Code (or any model/agent of your choice)
4. **Verify** that the executing agent achieves the criteria you set

The skill gives you a head start on clarity; the **self-review gate (step 3) means the goal you receive has already been checked against the rubric** — but you still own final sign-off and testability.

> **Note on the self-review gate:** the rubric pass in step 3 runs *before* the goal is shown to you. If you see a goal with a "⚠️ residual" flag, that's the gate being honest about a rubric item it couldn't fully satisfy in 2 rounds (usually an unverifiable criterion) — not an oversight. Decide whether that residual is acceptable before running the goal.

---

## Guidance sources

- [Claude Code /goal Documentation](https://code.claude.com/docs/en/goal)
- [Prompt Engineering Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
