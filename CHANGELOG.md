<!--
Copyright (c) 2026 JG Systems Consulting Ltd.
MIT License (see LICENSE).
-->

# Changelog

All notable changes to the JGS Goal-to-Spec Kit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.3.1] - 2026-06-26

Cursor plugin manifest.

### Added
- **`.cursor-plugin/` manifest** (`marketplace.json` + `plugin.json`), so Cursor (2.5+) discovers
  and installs the pack through its plugin system, reading the existing `skills/` tree natively.
  Satisfies the Cursor arm of RR-B-29 (in-host plugin manifest per targeted host).
- README documents the Cursor plugin route alongside the existing `--agent cursor` installer path.

## [1.3.0] - 2026-06-26

Website expansion and release-standard alignment.

### Added
- **Two new site pages.** `docs/skills.html` (a browsable reference for the three skills: what
  each does, when to use it, how to invoke it) and `docs/usage.html` (the step-by-step chain
  walkthrough and execution handoff). Both are self-contained, self-host their fonts, match the
  landing-page design system, and cross-link with `docs/index.html`.
- Landing-page navigation now links the Skills and Usage pages.

### Changed
- **Security reporting is advisory-based, not email.** `SECURITY.md` and the README now point to a
  private GitHub security advisory (or a pull request), removing the published support email.
- **De-slopped the human-facing surface.** Removed every em dash from the README, the docs, the
  CHANGELOG, `SECURITY.md`, `SKILLS.md`, and the community files; rewrote each with a comma, colon,
  or parentheses.
- README "What's in this distribution" corrected: the `COPYRIGHT`/`NOTICE` files (removed in 1.1.0)
  no longer appear; `SECURITY.md` and `docs/other-agents.md` are now listed.

## [1.2.0] - 2026-06-19

Multi-agent install.

### Added
- **Multi-agent installer.** `install.py` now installs into any of Claude Code, Cursor,
  Codex CLI, or Gemini CLI: `--agent <name>`, `--all`, or auto-detect installed agents.
  The same `SKILL.md` folders work unmodified across all of them (agentskills.io format).
- README "Installation & Invocation" documents the per-agent skill directories.

## [1.1.0] - 2026-06-19

Open-sourced under the MIT License.

### Changed
- **License: MIT.** The pack is now open source. `LICENSE` is the MIT License; `plugin.json`
  `license` is `MIT`; all proprietary/EULA language removed from README, SECURITY, and installers.

### Added
- `CONTRIBUTING.md`: how to report issues and submit pull requests.
- `CODE_OF_CONDUCT.md`: Contributor Covenant v2.1.

### Removed
- Proprietary `COPYRIGHT` and `NOTICE` files (superseded by the MIT `LICENSE`).

## [1.0.0] - 2026-06-18

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

## [0.1.1] - 2026-06-18

Improvements from the first full end-to-end run of the chain (lessons-learned pass).

### Added / Changed

- **spec-review** now ends with a **ready-to-run `/goal` execution prompt**, a copy-pasteable
  command that hands the goal + hardened spec to an executor, including guidance to **use the
  best-suited model per task** (fast for lookups, standard for build/test, deep for
  architecture/security) and to **parallelise independent work via concurrent subagents** with a
  writer/verifier split.
- **spec-review** gained a **post-revision consistency sweep** in triage: after any value change,
  re-scan the whole spec for stale duplicates (the most common defect the loop catches late).
- **spec-review** personas are now **domain-adaptive**: Security/Ops auto-remap for physical
  products, data/ML, or process specs, so users no longer hand-map them in the invocation.
- **goal-spec** rubric strengthened: success criteria must be numeric with a named test method;
  added rows for "every NFR/safety target is testable" and "no unstated assumptions". Design
  Approach now marks which components are parallel-safe for the executor.

## [0.1.0] - 2026-06-18

Initial external release of the Goal-to-Spec Kit.

### Added

- Three composable, tool-agnostic Claude Code skills:
  - **goal-formatter**: convert a verbal idea into a structured, testable goal; optional
    spec mode also emits a draft engineering spec.
  - **goal-spec**: turn a goal into a complete 8-section engineering spec, asking gap-filling
    clarifying questions grounded in the stated goal.
  - **spec-review**: harden a spec autonomously through a roundtable of engineering-discipline
    reviewers (architecture, security, test/QA, ops, product), looping to convergence with no
    user checkpoints.
- Shared 8-section engineering spec template (`goal-spec/references/spec-template.md`) used by
  all three skills so handoffs line up with no renamed sections.
- Documented execution handoff: every skill and the README state that the hardened spec is the
  input to a separate execution step, with concrete options for running it.
- Python / bash / PowerShell installer that copies the skills into the user's Claude Code skills
  folder under a vendor namespace.
- `SKILLS.md`: auto-generated skill index with one-line descriptions.
- `docs/skill-usage.md`: how to invoke, chain, and execute the result.

### Notes

- These skills have no external runtime dependencies; they call no MCP server and require no
  licence tier at call time. The pack is released under the MIT License.
