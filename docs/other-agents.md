<!--
Copyright (c) 2026 JG Systems Consulting Ltd.
MIT License (see LICENSE).
-->

# Using the kit with other agents

The three skills are pure prompt-engineering workflows: no MCP server, no external
runtime, no Claude-specific API. They ship in Claude Code's `SKILL.md` format, which
**several agents read natively** and others can consume after a small format transform.
`install.py` handles both: pick a target with `--agent`.

```bash
python install.py --list-agents          # show every target and where it installs
python install.py --agent <name>          # install for one agent
python install.py --agent all             # all user-global agents (not cursor)
python install.py --agent <name> --dry-run --force --uninstall   # the usual flags
```

## Supported targets

| Agent | `--agent` | Install path | Format | Invoke as |
|---|---|---|---|---|
| Claude Code | `claude` *(default)* | `~/.claude/skills/jgs-goal-spec/<skill>/SKILL.md` | SKILL.md (copied) | `/goal-formatter` |
| OpenClaw | `openclaw` | `~/.openclaw/skills/jgs-goal-spec/<skill>/SKILL.md` | SKILL.md (copied) | `/goal-formatter` |
| GitHub Copilot CLI | `copilot` | `~/.copilot/skills/jgs-goal-spec/<skill>/SKILL.md` | SKILL.md (copied) | reference `/goal-formatter` in a prompt; `/skills reload` |
| OpenAI Codex CLI | `codex` | `~/.codex/prompts/<skill>.md` | Markdown + `description` frontmatter | `/prompts:goal-formatter` |
| Gemini CLI | `gemini` | `~/.gemini/commands/jgs-goal-spec/<skill>.toml` | TOML (`prompt = """…"""`) | `/jgs-goal-spec:goal-formatter` (run `/commands reload`) |
| Cursor | `cursor` | `./.cursor/rules/<skill>.mdc` **(project-local)** | `.mdc` rule + frontmatter | `@goal-formatter`, or auto-applied by rule description |

### Native SKILL.md agents: `claude`, `openclaw`, `copilot`
These read the `SKILL.md` format directly, so the installer copies each skill folder
unchanged, references and all. This is the richest experience; the multi-file skill
(`goal-spec`, which carries a spec template under `references/`) works in full.

### Transform agents: `codex`, `gemini`, `cursor`
These use prompt/rule conventions rather than skills, so the installer converts each
`SKILL.md` into the agent's format. To keep the result self-contained, any
`references/` files are **inlined into the prompt as an appendix** (so `goal-spec`'s
spec template travels with it instead of relying on a sibling file).

## Notes & limitations

- **Cursor is project-local.** Cursor has no programmatically-writable user-global rules
  directory (global rules are typed into Settings by hand), so the installer writes
  `./.cursor/rules/*.mdc` under the **current directory**. Run it from your project root.
  For that reason `cursor` is *not* included in `--agent all`.
- **Codex prompts vs. skills.** Codex's custom-prompts directory is the stable, widely
  supported target today; that's what the installer writes. (Codex's newer `skills/`
  mechanism may become the preferred home over time.)
- **Restart / reload.** After installing, restart the agent or run its reload command
  (`/skills reload` for Copilot, `/commands reload` for Gemini) so it picks up the files.
- **`--target`** overrides the install directory for a single agent (it cannot be combined
  with `--agent all`).

## What stays the same everywhere

Regardless of agent, the workflow is identical: `goal-formatter` → `goal-spec` →
`spec-review`, ending in a hardened spec you hand to an executor. See
[skill-usage.md](skill-usage.md) for the chain and how to execute the result.
