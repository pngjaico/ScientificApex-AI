# Graph-First Operating Policy

Use the graph before broad manual exploration when any of these are true:

- The user asks where something is.
- The user asks which project, skill, module, or document to use.
- The task is about architecture, relationships, dependencies, routing, cleanup,
  staging, or handoff.
- The path is unknown or the workspace feels ambiguous.
- A new conversation starts inside `D:\Usuario-pc\Projetos\Doutorado`.

## Commands

```powershell
python scripts\generate_workspace_graph.py
python -m graphify query "Como um agente deve navegar esta tarefa?" --budget 1200
python -m graphify query "Qual projeto ativo e quais skills cobrem este pedido?" --budget 1200
python -m graphify query "Quais areas sao risco para staging ou reorganizacao?" --budget 1200
```

## Boundaries
- The root graph is operational, not a scientific evidence graph.
- Project-specific evidence graphs should be run inside `projects/<project_id>/`
  when needed.
- If the graph contradicts current files, current files win and the graph must be
  regenerated.
