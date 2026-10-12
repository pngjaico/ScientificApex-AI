# Migration to 0.3.0

Run `uv sync --locked --all-extras --dev` and `npm ci --prefix tools/playwright
--ignore-scripts`. For browser binaries use `article-machine env prepare
<project> --runtime browser`. R-dependent projects declare a project renv.lock.

New projects use contract_version 2. Historical V1 contracts remain readable,
but V1 runners cannot execute. Configure runner, version, package manager,
lockfile, timeout and allowed directories explicitly before execution.

Previously written `.json` files may contain YAML. Loaders retain compatibility,
but all newly written `.json` reports now contain actual JSON. Do not rewrite
scientific source archives to normalize this; rebuild affected reports from
current inputs when required.

Evidence Lock requires registered source ID/hash, observation time, locator,
excerpt, bounded freshness for temporal claims and supported status. Partial
support and stale sources cannot approve final claims. File ingestion assigns
IDs and hashes; DOI/URL registration alone does not establish retrieval.

Use `workflow plan --language en|pt-BR` for complex tasks, and `workflow
audit-language --reference ...` for translation regression. Existing model
comparison profiles are historical. Active defaults use Sol medium and Luna.

Blocked stage/strict export commands now exit nonzero. Task Packets are created
only for the active mode after a current canonical gate; blocked attempts go
under `.machine/attempts/`. Never treat old pass flags as approvals.

The registry inventories broad local skills but only the curated operational
trees are clone requirements. Entries on hold require verification before
promotion. Refresh registry hashes after approved changes and regenerate
the marked catalog sections with `scripts/generate_skill_docs.py --write-workspace`.

Expose the approved twelve skill trees to agent discovery with
`scripts/publish_workspace_skills.py --apply`. This creates local directory links
and preserves any conflicting existing directory. Start a new task to reload
the available-skills catalog; this does not alter the model of an open task.
