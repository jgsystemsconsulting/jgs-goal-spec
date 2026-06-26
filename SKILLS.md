<!--
Copyright (c) 2026 JG Systems Consulting Ltd.
MIT License (see LICENSE).
-->

# JGS Goal-to-Spec Kit: Skill Index

Auto-generated at release time from each skill's frontmatter. 3 skills in this release.

Run them in order (goal-formatter, goal-spec, spec-review), then execute the hardened spec.

| Skill | Description |
|-------|-------------|
| [`goal-formatter`](skills/goal-formatter/SKILL.md) | Convert verbal task descriptions into structured, testable goals. Use when you say "write me a goal", "create a goal for X", or want to frame work as a measurable objective. Analyzes repo state (git history, technical debt, memory, code) to synthesize clear goals with success criteria, verification methods, and test coverage outlines, then SELF-REVIEWS the draft against a quality rubric and revises before presenting. Optionally also emits a draft engineering specification alongside the goal (spec mode) for handoff to the goal-spec and spec-review skills. Model-agnostic: works with any LLM or agent framework. |
| [`goal-spec`](skills/goal-spec/SKILL.md) | Turn a goal (or a goal + draft spec) into a complete, detailed engineering specification by defining all eight spec sections and asking gap-filling clarifying questions grounded in the user's stated goal. Use when you say "spec this goal", "write a spec for X", "define the specification", "flesh out the spec", or have a goal that needs to become an implementable design. Pairs with goal-formatter (upstream) and spec-review (downstream). Model-agnostic. |
| [`spec-review`](skills/spec-review/SKILL.md) | Autonomously harden an engineering specification through a roundtable of independent engineering-discipline reviewers (architecture, security, test/QA, operations, product). Each reviewer is a real subagent thinking independently; the orchestrator collects findings, revises the spec itself, and loops until convergence (no CRITICAL or MAJOR findings) with NO user checkpoints. Use when you say "review this spec", "harden this spec", "spec review", "run the roundtable on this spec", or want a spec battle-tested before implementation. Self-contained, with no dependency on any other skill. |
