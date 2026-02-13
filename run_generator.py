import os
import subprocess

# The directory where the cloned repositories are located.
CLONE_DIR = "../ansible-roles"

# The path to the generate.yml playbook.
PLAYBOOK_PATH = os.path.abspath("generate.yml")

def run_generator():
    """
    Run the generate.yml playbook against each repository in the CLONE_DIR.
    """
    if not os.path.exists(CLONE_DIR):
        print(f"The directory {CLONE_DIR} does not exist. Please run clone_repos.py first.")
        return

    for repo_name in os.listdir(CLONE_DIR):
        repo_path = os.path.join(CLONE_DIR, repo_name)
        if os.path.isdir(repo_path):
            print(f"Running generator on {repo_name}...")
            # The playbook needs to be run from within the role's directory.
            subprocess.run(["ansible-playbook", PLAYBOOK_PATH, "--extra-vars", f"generator_path={os.path.dirname(PLAYBOOK_PATH)}"], cwd=repo_path, check=True)

if __name__ == "__main__":
    run_generator()
    print("Done.")
