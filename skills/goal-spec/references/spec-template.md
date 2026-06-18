<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->
# Canonical Engineering Spec Template (8 sections)

This is the shared contract across `goal-formatter` (draft-spec mode), `goal-spec`, and
`spec-review`. Use these exact section names so handoffs between the skills line up with no
orphaned or renamed sections. Copy this block to start a new spec.

```
# Specification: <title>

## 1. Problem & Context
<What problem this solves, why now, background a reader needs.
 One line stating the originating goal this spec satisfies.>

## 2. Scope
- **In scope:** <explicit list of what this spec covers>
- **Out of scope:** <explicit list of what it deliberately excludes>

## 3. Requirements
### Functional
- FR1: <what the system MUST do>
- FR2: ...
### Non-functional
- NFR1: <performance / security / reliability / usability / maintainability target, measurable>
- NFR2: ...

## 4. Constraints
- <hard limit: tech stack, platform, compatibility, regulatory, budget, timeline,
  "must not change" baseline>
- ...

## 5. Design Approach
<Solution shape: components, data flow, key interfaces, major decisions + rationale.
 Note alternatives considered and why rejected, where it matters.
 Decompose into independent components with stated dependencies; mark parallel vs. sequential.>

## 6. Success Criteria
- <observable, binary done/not-done condition, mapped to an FR and a verification step>
- ...

## 7. Risks & Mitigations
- Risk: <what could go wrong> → Mitigation: <planned response/contingency>
- ...

## 8. Open Questions
- <undecided item — resolved via clarifying question, OR explicitly deferred with
  owner/trigger for resolution>
- ...
```

## Section intent (quick reference)

| # | Section | Answers | Distinct from |
|---|---------|---------|---------------|
| 1 | Problem & Context | Why build this? | — |
| 2 | Scope | What's in/out? | Requirements (boundary vs. behaviour) |
| 3 | Requirements | What must it do? | Constraints (behaviour vs. limits) |
| 4 | Constraints | What bounds the solution? | Requirements |
| 5 | Design Approach | How is it built? | Requirements (how vs. what) |
| 6 | Success Criteria | When is it done? | Requirements (verification vs. behaviour) |
| 7 | Risks & Mitigations | What could fail? | — |
| 8 | Open Questions | What's undecided? | — |
