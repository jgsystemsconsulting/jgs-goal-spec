# Graph Report - .  (2026-09-11)

## Corpus Check
- 2 files · ~16,535 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 25 nodes · 39 edges · 6 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]

## God Nodes (most connected - your core abstractions)
1. `_home()` - 6 edges
2. `install_transform()` - 5 edges
3. `install_for_agent()` - 5 edges
4. `main()` - 5 edges
5. `render_transform()` - 4 edges
6. `parse_skill()` - 3 edges
7. `references_appendix()` - 3 edges
8. `_toml_basic()` - 3 edges
9. `claude_base()` - 2 edges
10. `openclaw_base()` - 2 edges

## Surprising Connections (you probably didn't know these)
- `install_transform()` --calls--> `render_transform()`  [EXTRACTED]
  install.py → install.py  _Bridges community 2 → community 1_
- `install_for_agent()` --calls--> `install_transform()`  [EXTRACTED]
  install.py → install.py  _Bridges community 1 → community 4_
- `main()` --calls--> `install_for_agent()`  [EXTRACTED]
  install.py → install.py  _Bridges community 4 → community 3_

## Communities

### Community 0 - "Community 0"
Cohesion: 0.43
Nodes (6): claude_base(), codex_base(), copilot_base(), gemini_base(), _home(), openclaw_base()

### Community 1 - "Community 1"
Cohesion: 0.4
Nodes (5): install_transform(), parse_skill(), Return (name, description, body) from a SKILL.md file.      Frontmatter is a min, Inline any references/ files so transform targets stay self-contained., references_appendix()

### Community 2 - "Community 2"
Cohesion: 0.5
Nodes (4): Escape a string for a TOML basic (double-quoted) value., Return (relative_path, file_contents) for a transform agent., render_transform(), _toml_basic()

### Community 3 - "Community 3"
Cohesion: 0.5
Nodes (4): main(), print_agents(), resolve_agents(), uninstall_for_agent()

### Community 4 - "Community 4"
Cohesion: 0.67
Nodes (3): install_for_agent(), install_native(), list_source_skills()

### Community 5 - "Community 5"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **4 isolated node(s):** `Return (name, description, body) from a SKILL.md file.      Frontmatter is a min`, `Inline any references/ files so transform targets stay self-contained.`, `Escape a string for a TOML basic (double-quoted) value.`, `Return (relative_path, file_contents) for a transform agent.`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 5`** (1 nodes): `install.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `render_transform()` connect `Community 2` to `Community 0`, `Community 1`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Why does `parse_skill()` connect `Community 1` to `Community 0`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Why does `references_appendix()` connect `Community 1` to `Community 0`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **What connects `Return (name, description, body) from a SKILL.md file.      Frontmatter is a min`, `Inline any references/ files so transform targets stay self-contained.`, `Escape a string for a TOML basic (double-quoted) value.` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._