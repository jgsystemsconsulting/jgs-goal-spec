# Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
#
# This file is part of the JGS Goal-to-Spec Kit, proprietary software of
# JG Systems Consulting Ltd. Unauthorized copying, modification,
# distribution, reverse engineering, or use of this file, via any medium,
# is strictly prohibited without a valid written licence from JG Systems
# Consulting Ltd. See LICENSE for the full terms.
#
# SPDX-License-Identifier: LicenseRef-JGSystemsConsulting-Proprietary
"""Installer for the JGS Goal-to-Spec Kit (Claude Code skills).

Copies the three skill directories in this release into the user's Claude Code
skills folder, under a vendor-namespaced directory.

Usage:
    python install.py                    # install to default location
    python install.py --dry-run          # list what would be copied; no changes
    python install.py --force            # overwrite existing same-named skills
    python install.py --target PATH      # install into a custom skills folder
    python install.py --uninstall        # remove previously-installed kit skills

Default install target (vendor-namespaced):
    Windows:          %USERPROFILE%\\.claude\\skills\\jgs-goal-spec\\
    macOS / Linux:    ~/.claude/skills/jgs-goal-spec/
    Override:         $CLAUDE_CONFIG_DIR/skills/jgs-goal-spec/ if CLAUDE_CONFIG_DIR is set

The vendor-namespaced layout keeps the kit's skills grouped under a single
directory so they can be updated or removed atomically without touching any
other vendor's skills you may have installed.
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


def default_target() -> pathlib.Path:
    env = os.environ.get("CLAUDE_CONFIG_DIR")
    if env:
        return pathlib.Path(env) / "skills" / VENDOR_NAMESPACE
    return pathlib.Path.home() / ".claude" / "skills" / VENDOR_NAMESPACE


def list_source_skills() -> list[pathlib.Path]:
    if not SKILLS_SRC.is_dir():
        return []
    return sorted(
        SKILLS_SRC / name
        for name in KIT_SKILLS
        if (SKILLS_SRC / name).is_dir()
    )


def install(target: pathlib.Path, force: bool, dry_run: bool) -> int:
    skills = list_source_skills()
    if not skills:
        print(f"ERROR: no skills found in {SKILLS_SRC}")
        return 1

    target.mkdir(parents=True, exist_ok=True)
    print(f"Target: {target}")
    print(f"Source: {SKILLS_SRC} ({len(skills)} skills)")
    if dry_run:
        print("(dry run — no files will be written)\n")

    installed = 0
    skipped = 0
    overwritten = 0

    for src in skills:
        dst = target / src.name
        if dst.exists():
            if not force:
                print(f"  SKIP  {src.name} (already exists — use --force to overwrite)")
                skipped += 1
                continue
            if not dry_run:
                shutil.rmtree(dst)
            overwritten += 1

        if dry_run:
            print(f"  +     {src.name}")
        else:
            shutil.copytree(src, dst)
            print(f"  OK    {src.name}")
        installed += 1

    print()
    if dry_run:
        print(f"Would install {installed} skill(s); {skipped} would be skipped.")
    else:
        print(f"Installed {installed} skill(s). Overwrote {overwritten}. Skipped {skipped}.")
        print("Restart Claude Code to pick up the new skills.")

    return 0


def uninstall(target: pathlib.Path, dry_run: bool) -> int:
    if not target.is_dir():
        print(f"Nothing to uninstall — {target} does not exist.")
        return 0

    to_remove = sorted(
        target / name
        for name in KIT_SKILLS
        if (target / name).is_dir()
    )
    if not to_remove:
        print(f"Nothing to uninstall — no kit skills in {target}.")
        return 0

    print(f"Target: {target}")
    if dry_run:
        print("(dry run — no files will be removed)\n")

    for p in to_remove:
        if dry_run:
            print(f"  -     {p.name}")
        else:
            shutil.rmtree(p)
            print(f"  RM    {p.name}")

    print()
    print(f"{'Would remove' if dry_run else 'Removed'} {len(to_remove)} skill(s).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=pathlib.Path, default=None,
                        help="Custom skills directory (default: platform-standard Claude Code path)")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite existing same-named skills")
    parser.add_argument("--dry-run", action="store_true",
                        help="List changes without making them")
    parser.add_argument("--uninstall", action="store_true",
                        help="Remove previously-installed kit skills")
    args = parser.parse_args()

    target = args.target if args.target is not None else default_target()

    if args.uninstall:
        return uninstall(target, dry_run=args.dry_run)
    return install(target, force=args.force, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
