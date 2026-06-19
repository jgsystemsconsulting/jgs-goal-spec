# Copyright (c) 2026 JG Systems Consulting Ltd. — MIT License (see LICENSE).
#
# This file is part of the jgs-goal-spec kit, open-source software of
# JG Systems Consulting Ltd., released under the MIT License. See LICENSE.
#
# SPDX-License-Identifier: MIT
"""Installer for the JGS Goal-to-Spec Kit — multi-agent.

The kit ships three skills as Claude Code `SKILL.md` files. That format is read
natively by several agents and can be transformed into the prompt/rule
conventions of others. This installer targets both kinds:

  Native SKILL.md agents (folder is copied unchanged):
    claude    ~/.claude/skills/jgs-goal-spec/<skill>/SKILL.md   (default)
    openclaw  ~/.openclaw/skills/jgs-goal-spec/<skill>/SKILL.md
    copilot   ~/.copilot/skills/jgs-goal-spec/<skill>/SKILL.md   (GitHub Copilot CLI)

  Transform agents (each SKILL.md is converted to that agent's format;
  any references/ files are inlined as an appendix so the result is standalone):
    codex     ~/.codex/prompts/<skill>.md                       (OpenAI Codex CLI)
    gemini    ~/.gemini/commands/jgs-goal-spec/<skill>.toml      (Gemini CLI)
    cursor    ./.cursor/rules/<skill>.mdc                        (Cursor — PROJECT-local)

Usage:
    python install.py                       # install for Claude Code (default)
    python install.py --agent openclaw      # install for a specific agent
    python install.py --agent all           # all user-global agents (not cursor)
    python install.py --list-agents         # show supported agents and paths
    python install.py --dry-run             # show what would be written; no changes
    python install.py --force               # overwrite existing kit files
    python install.py --target PATH         # override the install directory
    python install.py --uninstall           # remove a previously-installed kit

Notes:
  * Multi-file skills (with a references/ folder) are richest on native SKILL.md
    agents. On transform agents the references are inlined into the prompt.
  * `cursor` writes PROJECT-local rules under the current directory, so it is not
    included in `--agent all`; request it explicitly from your project root.
  * `--target` overrides the final install directory for native agents, or the
    base directory for transform agents.
"""
from __future__ import annotations

import argparse
import os
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
SKILLS_SRC = HERE / "skills"

# These skills do not share a common prefix, so the kit ships an explicit list.
KIT_SKILLS = ["goal-formatter", "goal-spec", "spec-review"]

VENDOR_NAMESPACE = "jgs-goal-spec"


# --------------------------------------------------------------------------- #
# Base-directory resolvers (one per agent)
# --------------------------------------------------------------------------- #
def _home() -> pathlib.Path:
    return pathlib.Path.home()


def claude_base() -> pathlib.Path:
    env = os.environ.get("CLAUDE_CONFIG_DIR")
    root = pathlib.Path(env) if env else _home() / ".claude"
    return root / "skills" / VENDOR_NAMESPACE


def openclaw_base() -> pathlib.Path:
    return _home() / ".openclaw" / "skills" / VENDOR_NAMESPACE


def copilot_base() -> pathlib.Path:
    return _home() / ".copilot" / "skills" / VENDOR_NAMESPACE


def codex_base() -> pathlib.Path:
    # Codex discovers prompts only at the top level of this folder.
    return _home() / ".codex" / "prompts"


def gemini_base() -> pathlib.Path:
    # Gemini namespaces commands by subdirectory -> /jgs-goal-spec:<skill>.
    return _home() / ".gemini" / "commands" / VENDOR_NAMESPACE


def cursor_base() -> pathlib.Path:
    # Cursor rules are project-local; there is no writable user-global rules dir.
    return pathlib.Path.cwd() / ".cursor" / "rules"


# kind: "native" copies the SKILL.md folder; otherwise a transform key.
# global_: included in --agent all (cursor is project-local, so excluded).
AGENTS: dict[str, dict] = {
    "claude":   {"label": "Claude Code",     "kind": "native",   "base": claude_base,   "global_": True,
                 "invoke": "/goal-formatter  (or /jgs-goal-spec:goal-formatter via the plugin marketplace)"},
    "openclaw": {"label": "OpenClaw",         "kind": "native",   "base": openclaw_base, "global_": True,
                 "invoke": "/goal-formatter"},
    "copilot":  {"label": "GitHub Copilot CLI", "kind": "native", "base": copilot_base,  "global_": True,
                 "invoke": "reference the /goal-formatter skill in a prompt; run /skills reload"},
    "codex":    {"label": "OpenAI Codex CLI", "kind": "codex",    "base": codex_base,    "global_": True,
                 "invoke": "/prompts:goal-formatter"},
    "gemini":   {"label": "Gemini CLI",       "kind": "gemini",   "base": gemini_base,   "global_": True,
                 "invoke": "/jgs-goal-spec:goal-formatter  (run /commands reload first)"},
    "cursor":   {"label": "Cursor (project-local)", "kind": "cursor", "base": cursor_base, "global_": False,
                 "invoke": "@goal-formatter, or let the agent auto-apply by rule description"},
}


# --------------------------------------------------------------------------- #
# SKILL.md parsing + format transforms
# --------------------------------------------------------------------------- #
def parse_skill(skill_md: pathlib.Path) -> tuple[str, str, str]:
    """Return (name, description, body) from a SKILL.md file.

    Frontmatter is a minimal `key: value` block delimited by `---` lines. We only
    need `name` and `description`; everything after the closing `---` is the body.
    """
    text = skill_md.read_text(encoding="utf-8")
    name = skill_md.parent.name
    description = ""
    body = text

    lines = text.splitlines(keepends=True)
    if lines and lines[0].strip() == "---":
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
        if end is not None:
            for ln in lines[1:end]:
                key, sep, val = ln.partition(":")
                if not sep:
                    continue
                key, val = key.strip(), val.strip()
                if key == "name" and val:
                    name = val
                elif key == "description" and val:
                    description = val
            body = "".join(lines[end + 1:]).lstrip("\n")
    return name, description, body


def references_appendix(skill_dir: pathlib.Path) -> str:
    """Inline any references/ files so transform targets stay self-contained."""
    refs = skill_dir / "references"
    if not refs.is_dir():
        return ""
    parts: list[str] = []
    for f in sorted(p for p in refs.rglob("*") if p.is_file()):
        rel = f.relative_to(skill_dir).as_posix()
        parts.append(f"\n\n---\n\n## Appendix — {rel}\n\n{f.read_text(encoding='utf-8')}")
    return "".join(parts)


def _toml_basic(s: str) -> str:
    """Escape a string for a TOML basic (double-quoted) value."""
    return s.replace("\\", "\\\\").replace('"', '\\"')


def render_transform(kind: str, name: str, description: str, body: str) -> tuple[str, str]:
    """Return (relative_path, file_contents) for a transform agent."""
    if kind == "codex":
        front = f"---\ndescription: {description}\n---\n" if description else ""
        return f"{name}.md", f"{front}{body}"

    if kind == "gemini":
        esc = body.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
        contents = f'description = "{_toml_basic(description)}"\nprompt = """\n{esc}\n"""\n'
        return f"{name}.toml", contents

    if kind == "cursor":
        front = (
            "---\n"
            f"description: {description}\n"
            "globs:\n"
            "alwaysApply: false\n"
            "---\n"
        )
        return f"{name}.mdc", f"{front}{body}"

    raise ValueError(f"unknown transform kind: {kind}")


# --------------------------------------------------------------------------- #
# Source discovery
# --------------------------------------------------------------------------- #
def list_source_skills() -> list[pathlib.Path]:
    if not SKILLS_SRC.is_dir():
        return []
    return sorted(
        SKILLS_SRC / name for name in KIT_SKILLS if (SKILLS_SRC / name).is_dir()
    )


# --------------------------------------------------------------------------- #
# Install / uninstall
# --------------------------------------------------------------------------- #
def install_native(target: pathlib.Path, skills: list[pathlib.Path],
                   force: bool, dry_run: bool) -> tuple[int, int, int]:
    target.mkdir(parents=True, exist_ok=True) if not dry_run else None
    installed = skipped = overwritten = 0
    for src in skills:
        dst = target / src.name
        if dst.exists():
            if not force:
                print(f"  SKIP  {src.name} (exists — use --force)")
                skipped += 1
                continue
            if not dry_run:
                shutil.rmtree(dst)
            overwritten += 1
        if dry_run:
            print(f"  +     {src.name}/")
        else:
            shutil.copytree(src, dst)
            print(f"  OK    {src.name}/")
        installed += 1
    return installed, skipped, overwritten


def install_transform(kind: str, base: pathlib.Path, skills: list[pathlib.Path],
                      force: bool, dry_run: bool) -> tuple[int, int, int]:
    installed = skipped = overwritten = 0
    for src in skills:
        name, description, body = parse_skill(src / "SKILL.md")
        body = body + references_appendix(src)
        rel, contents = render_transform(kind, name, description, body)
        dst = base / rel
        if dst.exists():
            if not force:
                print(f"  SKIP  {rel} (exists — use --force)")
                skipped += 1
                continue
            overwritten += 1
        if dry_run:
            print(f"  +     {rel}")
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(contents, encoding="utf-8")
            print(f"  OK    {rel}")
        installed += 1
    return installed, skipped, overwritten


def install_for_agent(agent: str, override: pathlib.Path | None,
                      force: bool, dry_run: bool) -> int:
    cfg = AGENTS[agent]
    skills = list_source_skills()
    if not skills:
        print(f"ERROR: no skills found in {SKILLS_SRC}")
        return 1

    base = override if override is not None else cfg["base"]()
    print(f"\n== {cfg['label']} ({agent}) ==")
    print(f"Target: {base}")
    if dry_run:
        print("(dry run — no files written)")

    if cfg["kind"] == "native":
        installed, skipped, overwritten = install_native(base, skills, force, dry_run)
    else:
        installed, skipped, overwritten = install_transform(cfg["kind"], base, skills, force, dry_run)

    if dry_run:
        print(f"Would install {installed}; would skip {skipped}.")
    else:
        print(f"Installed {installed}. Overwrote {overwritten}. Skipped {skipped}.")
        print(f"Invoke: {cfg['invoke']}")
    return 0


def uninstall_for_agent(agent: str, override: pathlib.Path | None, dry_run: bool) -> int:
    cfg = AGENTS[agent]
    base = override if override is not None else cfg["base"]()
    print(f"\n== {cfg['label']} ({agent}) ==")
    print(f"Target: {base}")
    if dry_run:
        print("(dry run — no files removed)")

    removed = 0
    if cfg["kind"] == "native":
        for name in KIT_SKILLS:
            p = base / name
            if p.is_dir():
                print(f"  {'-' if dry_run else 'RM'}    {name}/")
                if not dry_run:
                    shutil.rmtree(p)
                removed += 1
    elif cfg["kind"] == "gemini":
        # Whole namespaced command folder belongs to the kit.
        if base.is_dir():
            for f in sorted(base.glob("*.toml")):
                print(f"  {'-' if dry_run else 'RM'}    {f.name}")
                if not dry_run:
                    f.unlink()
                removed += 1
            if not dry_run and not any(base.iterdir()):
                base.rmdir()
    else:
        ext = {"codex": ".md", "cursor": ".mdc"}[cfg["kind"]]
        for name in KIT_SKILLS:
            p = base / f"{name}{ext}"
            if p.is_file():
                print(f"  {'-' if dry_run else 'RM'}    {p.name}")
                if not dry_run:
                    p.unlink()
                removed += 1

    print(f"{'Would remove' if dry_run else 'Removed'} {removed} item(s).")
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def resolve_agents(choice: str) -> list[str]:
    if choice == "all":
        return [a for a, c in AGENTS.items() if c["global_"]]
    return [choice]


def print_agents() -> int:
    print("Supported agents:\n")
    for key, cfg in AGENTS.items():
        scope = "user-global" if cfg["global_"] else "PROJECT-local"
        print(f"  {key:9} {cfg['label']:24} [{cfg['kind']:7}] {scope}")
        print(f"            -> {cfg['base']()}")
    print("\n'all' targets every user-global agent (cursor is project-local; request it explicitly).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--agent", default="claude",
                        choices=list(AGENTS) + ["all"],
                        help="Target agent (default: claude)")
    parser.add_argument("--target", type=pathlib.Path, default=None,
                        help="Override the install/base directory")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite existing kit files")
    parser.add_argument("--dry-run", action="store_true",
                        help="List changes without making them")
    parser.add_argument("--uninstall", action="store_true",
                        help="Remove previously-installed kit files")
    parser.add_argument("--list-agents", action="store_true",
                        help="Show supported agents and their install paths")
    args = parser.parse_args()

    if args.list_agents:
        return print_agents()

    agents = resolve_agents(args.agent)
    if args.target is not None and len(agents) > 1:
        print("ERROR: --target cannot be combined with --agent all.")
        return 2

    rc = 0
    for agent in agents:
        if args.uninstall:
            rc |= uninstall_for_agent(agent, args.target, args.dry_run)
        else:
            rc |= install_for_agent(agent, args.target, args.force, args.dry_run)
    return rc


if __name__ == "__main__":
    sys.exit(main())
