<!--
Copyright (c) 2026 JG Systems Consulting Ltd.
MIT License — see LICENSE.
-->
# Contributing to jgs-goal-spec

Thanks for your interest in improving this pack. It's a small, focused set of three
Claude Code skills (`goal-formatter` → `goal-spec` → `spec-review`), released under the
[MIT License](LICENSE).

## Ways to contribute

- **Report a bug or rough edge** — open an issue describing what you tried, what you expected,
  and what happened. Skill behaviour is prompt-driven, so a copy of the invocation and the
  result is the most useful thing you can include.
- **Suggest an improvement** — open an issue first to discuss the idea before a large change.
- **Submit a fix** — small, focused pull requests are easiest to review.

## Making a change

1. Fork the repo and create a branch (`git switch -c fix/short-description`).
2. Edit the relevant `skills/<skill>/SKILL.md` (or docs). Keep each skill's `## When to use`
   heading and a clear description — the CI check (`.github/workflows/validate.yml`) enforces
   valid frontmatter (`name` matching the directory, non-empty `description`).
3. Keep changes scoped. A PR that touches one skill is easier to reason about than one that
   rewrites several.
4. Open a pull request with a short description of the problem and your fix.

## What the CI checks

The `validate` workflow runs on every push and pull request. It is read-only and never
executes repository code. It checks:

- No accidental secrets or private-key material in the tree.
- Every `skills/*/SKILL.md` has valid frontmatter (kebab-case `name` matching its folder,
  non-empty `description`).

If CI is red, read the job log — the failing check names the file and the reason.

## Code of conduct

By participating you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Licensing of contributions

By submitting a contribution you agree that it is licensed under the same
[MIT License](LICENSE) as the rest of the project.
