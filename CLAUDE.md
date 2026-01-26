
See [AGENTS.md](AGENTS.md) for cspec workflow and project context.

## GitHub Branch Rules

- **`main`**: PRs required, no deletions, no force push
- **`develop`**: Direct push allowed, no deletions, no force push
- **Workflow**:
  - Small fixes: push directly to `develop`
  - Big features: feature branch → PR → `develop`
  - Releases: PR `develop` → `main`

## NEXT ACTION

- **Evaluate**: migrate to slash command or plugin, add chkcc init and that installs everything on a project
