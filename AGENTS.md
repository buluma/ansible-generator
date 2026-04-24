# Repository Guidelines

## Project Overview

An Ansible-based tool that generates documentation and CI files for an Ansible Role. Automates boilerplate creation so developers can focus on core role logic. The main playbook `generate.yml` reads metadata and configuration from a target role, then renders files from Jinja2 templates.

## Project Structure & Module Organization

- `generate.yml` is the core playbook; it reads role metadata and renders files from `templates/*.j2`.
- `defaults/main.yml` and `vars/main.yml` define generator defaults and shared variables.
- `files/` contains static files copied into target roles (for example `.gitignore`, `.yamllint`, and PR templates).
- `workflows/` stores reusable CI workflow templates used by generated repositories.
- `tests/` contains fixture roles (`ansible-role-default`, `ansible-role-minimal`, etc.) used to validate generated output and Molecule behavior.
- Utility scripts: `run_generator.py`, `clone_repos.py`, and `run_command_in_roles.py` automate batch generation tasks.

## Build, Test, and Development Commands

**Running the generator:**

1. Navigate to the directory of the Ansible role you want to process.
2. Run the `generate.yml` playbook from the `ansible-generator` directory.

```bash
cd /path/to/your/ansible-role
/path/to/ansible-generator/generate.yml
```

**Other commands:**

- `python run_generator.py` runs `generate.yml` across repos in `../ansible-roles`.
- `pre-commit run --all-files` runs YAML and Ansible hygiene checks configured in `.pre-commit-config.yaml`.
- `yamllint -c .yamllint .` validates YAML formatting rules for this repo.
- `cd tests/ansible-role-default && tox` runs Molecule tests (same pattern for other `tests/ansible-role-*` fixtures).

## Configuration

Customize behavior by modifying variables in `defaults/main.yml`. Controls which files are generated, Docker images, Galaxy and GitHub namespaces, and author information.

## Coding Style & Naming Conventions

- Use 2-space YAML indentation and valid YAML document headers (`---`) where applicable.
- Keep Jinja template names descriptive and output-oriented (example: `molecule-action.yml.j2`, `SECURITY.md.j2`).
- Prefer snake_case for variable names in YAML/Python (`github_namespace`, `generator_path`).
- Run pre-commit before opening a PR; enforced checks include `yamllint`, trailing whitespace, merge conflicts, and Ansible role hygiene hooks.

## Testing Guidelines

- Primary validation is fixture-based: regenerate files and run Molecule via each fixture's `tox.ini`.
- Add or update fixtures in `tests/` when changing template behavior.
- Name test fixtures by scenario, not implementation detail (example: `ansible-role-preferences`).

## Commit & Pull Request Guidelines

- Recent history favors short, imperative commit subjects (example: `Update main.yml`, `Bump actions`).
- Keep commits focused to one logical change (template update, workflow change, or fixture adjustment).
- PRs should include: purpose, impacted templates/files, test evidence (`pre-commit`, `tox`), and linked issue/PR context.
- If generated output changes, mention which fixture roles were re-validated.
