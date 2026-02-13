import os
import subprocess

# The directory where the ansible roles are located, relative to this script.
ANSIBLE_ROLES_DIR = "../ansible-roles"
# The command to execute, relative to each role's directory.
COMMAND = ["ansible-playbook", "../../ansible-generator/generate.yml"]

def run_command_in_roles():
    """
    Run a command in each subdirectory of the ANSIBLE_ROLES_DIR.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ansible_roles_path = os.path.abspath(os.path.join(script_dir, ANSIBLE_ROLES_DIR))

    if not os.path.exists(ansible_roles_path):
        print(f"Error: The directory '{ansible_roles_path}' does not exist.")
        return

    print(f"Targeting role directories in: '{ansible_roles_path}'")

    try:
        role_dirs = [d for d in os.listdir(ansible_roles_path) if os.path.isdir(os.path.join(ansible_roles_path, d))]
    except OSError as e:
        print(f"Error reading subdirectories from '{ansible_roles_path}': {e}")
        return

    if not role_dirs:
        print(f"No role directories found in '{ansible_roles_path}'.")
        return

    for role_name in role_dirs:
        role_path = os.path.join(ansible_roles_path, role_name)
        print(f"\n--- Processing role: {role_name} ---")

        try:
            print(f"Executing: {' '.join(COMMAND)} in '{role_path}'")

            process = subprocess.run(
                COMMAND,
                cwd=role_path,
                check=True,
                capture_output=True,
                text=True,
                timeout=300
            )
            print(f"Successfully processed {role_name}.")
            # To avoid flooding the console, only show a summary of the output
            if process.stdout:
                lines = process.stdout.strip().split('\n')
                print("Output summary (last 5 lines):")
                for line in lines[-5:]:
                    print(f"  {line}")

        except FileNotFoundError:
            print(
                f"Error: '{COMMAND[0]}' command not found. Is Ansible installed and in your system's PATH?"
            )
            return
        except subprocess.CalledProcessError as e:
            print(f"Error processing {role_name}. Return code: {e.returncode}")
            # Printing stderr is usually more helpful for playbook failures
            if e.stderr:
                print(f"Error Output:\n{e.stderr}")
            else:
                print(f"Output (no stderr):\n{e.stdout}")
        except subprocess.TimeoutExpired as e:
            print(f"Timeout expired while processing {role_name}.")
            if e.stdout:
                print(f"Stdout:\n{e.stdout}")
            if e.stderr:
                print(f"Stderr:\n{e.stderr}")
        except Exception as e:
            print(f"An unexpected error occurred while processing {role_name}: {e}")

if __name__ == "__main__":
    run_command_in_roles()
    print("\n--- All roles processed. ---")
