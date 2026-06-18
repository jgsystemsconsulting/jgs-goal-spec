<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->

# Changelog

All notable changes to the JGS Goal-to-Spec Kit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2026-06-18

First professional-standard release (conforms to RR-S-08..14).

### Added
- Plugin-marketplace install: `.claude-plugin/marketplace.json` + `plugin.json`
  (`/plugin marketplace add jgsystemsconsulting/jgs-goal-spec`).
- `SECURITY.md` report-only vulnerability policy.
- README badge cluster (license, version, skill count, Claude Code).
- CI quality gate (`.github/workflows/validate.yml`): content-integrity + frontmatter checks.

### Changed
- Promoted to v1.0.0 (production-ready).
- `RELEASE-INFO.txt` no longer embeds the internal source commit SHA.

## [0.1.1] — 2026-06-18

Improvements from the first full end-to-end run of the chain (lessons-learned pass).

### Added / Changed

- **spec-review** now ends with a **ready-to-run `/goal` execution prompt** — a copy-pasteable
  command that hands the goal + hardened spec to an executor, including guidance to **use the
  best-suited model per task** (fast for lookups, standard for build/test, deep for
  architecture/security) and to **parallelise independent work via concurrent subagents** with a
  writer/verifier split.
- **spec-review** gained a **post-revision consistency sweep** in triage — after any value change,
  re-scan the whole spec for stale duplicates (the most common defect the loop catches late).
- **spec-review** personas are now **domain-adaptive** — Security/Ops auto-remap for physical
  products, data/ML, or process specs, so users no longer hand-map them in the invocation.
- **goal-spec** rubric strengthened — success criteria must be numeric with a named test method;
  added rows for "every NFR/safety target is testable" and "no unstated assumptions". Design
  Approach now marks which components are parallel-safe for the executor.

## [0.1.0] — 2026-06-18

Initial external release of the Goal-to-Spec Kit.

### Added

- Three composable, tool-agnostic Claude Code skills:
  - **goal-formatter** — convert a verbal idea into a structured, testable goal; optional
    spec mode also emits a draft engineering spec.
  - **goal-spec** — turn a goal into a complete 8-section engineering spec, asking gap-filling
    clarifying questions grounded in the stated goal.
  - **spec-review** — harden a spec autonomously through a roundtable of engineering-discipline
    reviewers (architecture, security, test/QA, ops, product), looping to convergence with no
    user checkpoints.
- Shared 8-section engineering spec template (`goal-spec/references/spec-template.md`) used by
  all three skills so handoffs line up with no renamed sections.
- Documented execution handoff: every skill and the README state that the hardened spec is the
  input to a separate execution step, with concrete options for running it.
- Python / bash / PowerShell installer that copies the skills into the user's Claude Code skills
  folder under a vendor namespace.
- `SKILLS.md` — auto-generated skill index with one-line descriptions.
- `docs/skill-usage.md` — how to invoke, chain, and execute the result.

### Notes

- These skills have no external runtime dependencies — they call no MCP server and require no
  licence tier at call time. The pack itself is proprietary software under LICENSE.
