import json
from pathlib import Path
import shutil
import subprocess


SCRIPT_DIR = Path(__file__).resolve().parent
CLONE_DIR = SCRIPT_DIR.parent / "ansible-roles"
PLAYBOOK_PATH = SCRIPT_DIR / "generate.yml"


def run_generator():
    """Generate files for each active role checkout and report failed roles."""
    try:
        roles = sorted(
            role for role in CLONE_DIR.iterdir()
            if role.name.startswith("ansible-role-")
            and role.is_dir() and not role.is_symlink()
            and (role / ".git").exists() and (role / "meta/main.yml").is_file()
        )
    except FileNotFoundError:
        print(f"The directory {CLONE_DIR} does not exist. Please run clone_repos.py first.")
        return 1
    except OSError as error:
        print(f"Could not read {CLONE_DIR}: {error}")
        return 1

    if not roles:
        print(f"No active role checkouts found in {CLONE_DIR}.")
        return 0

    if shutil.which("ansible-playbook") is None:
        print("ansible-playbook was not found on PATH. Install Ansible before running the generator.")
        return 1

    failed = []
    for role in roles:
        print(f"Running generator on {role.name}...", flush=True)
        try:
            subprocess.run(
                [
                    "ansible-playbook", str(PLAYBOOK_PATH), "--extra-vars",
                    json.dumps({"role_path": str(role)}),
                ],
                cwd=role,
                check=True,
                timeout=300,
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError) as error:
            print(f"Generation failed for {role.name}: {error}")
            failed.append(role.name)

    if failed:
        print(f"Failed roles: {', '.join(failed)}")
        return 1

    print(f"Generated files for {len(roles)} roles.")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_generator())
