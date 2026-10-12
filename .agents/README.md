# `.agents` Central Layer

This folder is intentionally small. It is not a dump of every skill and should
not become another raw corpus.

## What Belongs Here
- Central agent instructions: `.agents/AGENTS.md`.
- Graph-first policy: `.agents/GRAPH_FIRST.md`.
- Small local skills that help agents enter and navigate this workspace.

## What Stays Ignored
- Broad upstream mirrors such as `.agents/skills/scientific-agent-skills/`.
- Caches, generated files, credentials, and temporary tool state.

## Current Local Skills
- `.agents/skills/workspace-graph-navigator/SKILL.md`
- `.agents/skills/project-entry-navigator/SKILL.md`
- `.agents/skills/content-preservation-guardian/SKILL.md`

The authoritative runtime skill catalog for Article Machine remains
`skills/` plus `article_machine/agent_skills.py`. The `.agents` copies exist so
future coding agents can discover the same navigation policy early.

Codex runtime orchestration is separate and lives in `.codex/`: project-level
subagent limits, read-only role definitions, and MCP declarations belong there.
Do not duplicate model or concurrency policy in this directory.
